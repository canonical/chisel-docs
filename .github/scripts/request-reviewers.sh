#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 4 || ! $1 =~ ^[12]$ || ! $2 =~ ^[1-9][0-9]*$ ||
  ! $3 =~ ^(significant|not-significant)$ || -z $4 ]]; then
  echo "Usage: $0 <reviewer-count: 1|2> <pull-request-number> <classification> <reason>" >&2
  exit 2
fi
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY must be set}"
: "${GITHUB_STEP_SUMMARY:?GITHUB_STEP_SUMMARY must be set}"

count=$1
pr=$2
classification=$3
reason=${4//$'\n'/ }
reason=${reason//$'\r'/ }
repo=$GITHUB_REPOSITORY
author=$(gh api "repos/$repo/pulls/$pr" --jq '.user.login | ascii_downcase')
md=$(gh api --paginate "repos/$repo/pulls/$pr/files" \
  --jq '.[] | select(.filename | endswith(".md")) | [.filename, .status, .additions, .deletions] | @tsv')
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
  reviewers_json=$(printf '"%s",' "${new[@]}")
  reviewers_json=${reviewers_json%,}
  safeoutputs add_reviewer "{\"pull_request_number\":$pr,\"reviewers\":[$reviewers_json]}"
fi

{
  echo "## Review requirements for #$pr"
  echo "- Author: $author"
  echo "- Required reviewers: $count"
  echo "- Classification: $classification — $reason"
  echo "- Changed Markdown files (file, status, +, -):"
  if [[ -n $md ]]; then
    while IFS= read -r line; do echo "  - $line"; done <<<"$md"
  else
    echo "  - none"
  fi
  echo "- Target reviewers: ${targets[*]}"
  echo "- Already requested: ${requested//$'\n'/, }"
  echo "- Already reviewed: ${reviewed//$'\n'/, }"
  echo "- New requests emitted: ${new[*]:-none}"
} >>"$GITHUB_STEP_SUMMARY"
