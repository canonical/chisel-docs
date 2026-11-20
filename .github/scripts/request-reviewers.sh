#!/usr/bin/env bash
set -euo pipefail

if [[ $# -eq 2 && $1 == --route && $2 =~ ^[1-9][0-9]*$ ]]; then
  mode=route
  pr=$2
elif [[ $# -eq 3 && $1 =~ ^[1-9][0-9]*$ &&
  $2 =~ ^(significant|not-significant)$ && -n $3 ]]; then
  mode=request
  pr=$1
  classification=$2
  reason=$3
else
  echo "Usage: $0 --route <pull-request-number>" >&2
  echo "   or: $0 <pull-request-number> <classification> <reason>" >&2
  exit 2
fi

: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY must be set}"
repo=$GITHUB_REPOSITORY
reason=${reason:-}
reason=${reason//$'\n'/ }
reason=${reason//$'\r'/ }

md=$(gh api --paginate "repos/$repo/pulls/$pr/files" \
  --jq '.[] | select(.filename | endswith(".md")) | [(.filename | @base64), .status, .additions, .deletions] | @tsv')

md_count=0
total_changed_lines=0
has_deterministic_significance=0
file_summary=()
while IFS=$'\t' read -r encoded_filename status additions deletions; do
  [[ -z $encoded_filename ]] && continue
  filename=$(printf '%s' "$encoded_filename" | base64 --decode)
  ((md_count += 1))
  total_changed_lines=$((total_changed_lines + additions + deletions))
  file_summary+=("$(printf '%q' "$filename") ($status, +$additions/-$deletions)")
  if [[ $status != modified ]]; then
    has_deterministic_significance=1
  fi
done <<<"$md"

if ((total_changed_lines >= 20)); then
  has_deterministic_significance=1
fi

if [[ $mode == route ]]; then
  : "${GITHUB_OUTPUT:?GITHUB_OUTPUT must be set in route mode}"
  if ((md_count > 0 && !has_deterministic_significance)); then
    printf 'ai_required=true\n' >>"$GITHUB_OUTPUT"
    exit 0
  fi

  if ((md_count == 0)); then
    classification=not-significant
    reason="No Markdown files changed."
  else
    classification=significant
    reason="A Markdown file is new, renamed, deleted, or the total additions and deletions across changed Markdown files is 20 or more ($total_changed_lines lines)."
  fi
  printf 'ai_required=false\nclassification=%s\nreason=%s\n' \
    "$classification" "$reason" >>"$GITHUB_OUTPUT"
  exit 0
fi

if ((md_count == 0)); then
  classification=not-significant
  reason="No Markdown files changed."
  count=1
elif ((has_deterministic_significance)); then
  classification=significant
  reason="A Markdown file is new, renamed, deleted, or the total additions and deletions across changed Markdown files is 20 or more ($total_changed_lines lines)."
  count=2
else
  count=1
  [[ $classification == significant ]] && count=2
fi

: "${GITHUB_STEP_SUMMARY:?GITHUB_STEP_SUMMARY must be set in request mode}"
author=$(gh api "repos/$repo/pulls/$pr" --jq '.user.login | ascii_downcase')
requested=$(gh api "repos/$repo/pulls/$pr" --jq '.requested_reviewers[].login | ascii_downcase')
reviewed=$(gh api --paginate "repos/$repo/pulls/$pr/reviews" --jq '.[].user.login | ascii_downcase')

contains_line() {
  local needle=$1 line
  while IFS= read -r line; do
    [[ $line == "$needle" ]] && return 0
  done <<<"$2"
  return 1
}

if [[ $author == asanvaq ]]; then
  if [[ $count == 1 ]]; then targets=(cjdcordeiro); else targets=(cjdcordeiro upils); fi
else
  if [[ $count == 1 ]]; then targets=(asanvaq); else targets=(asanvaq cjdcordeiro); fi
fi

new=()
for target in "${targets[@]}"; do
  if ! contains_line "$target" "$requested" && ! contains_line "$target" "$reviewed"; then
    new+=("$target")
  fi
done

if ((${#new[@]})); then
  args=()
  for reviewer in "${new[@]}"; do
    args+=(-f "reviewers[]=$reviewer")
  done
  gh api --method POST "repos/$repo/pulls/$pr/requested_reviewers" "${args[@]}"
fi

{
  echo "## Review requirements for #$pr"
  echo "- Author: $author"
  echo "- Required reviewers: $count"
  echo "- Classification: $classification${reason:+ — $reason}"
  echo "- Changed Markdown files (file, status, +, -):"
  if ((${#file_summary[@]})); then
    printf '  - %s\n' "${file_summary[@]}"
  else
    echo "  - none"
  fi
  echo "- Target reviewers: ${targets[*]}"
  echo "- Already requested: ${requested//$'\n'/, }"
  echo "- Already reviewed: ${reviewed//$'\n'/, }"
  echo "- New requests applied: ${new[*]:-none}"
} >>"$GITHUB_STEP_SUMMARY"
