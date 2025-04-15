# FAQ

This page lists some known limitations and frequently asked questions.


(faq_arbitrary_package_names)=

## Is it possible to use arbitrary package names?

No, package names must be the same as the package names in the archive, so that
there's a single namespace to remember and respect.


(faq_available_ubuntu_versions)=

## Which Ubuntu versions have package slices?

The slice definitions are located at the {{chisel_releases_repo}}. The
`ubuntu-XX.YY` branches in that repository contain the slice definitions for
the corresponding Ubuntu releases.

If you find a specific release missing, let the maintainers know by [creating a
new issue] in the {{chisel_releases_repo}}.


(faq_non-ubuntu_archives)=

## Is it possible to use non-Ubuntu archives?

No. The supported archives are described at
{ref}`chisel_yaml_format_spec_archives`.


(faq_ppa)=

## Is it possible to use PPAs?

Not at the moment.


(faq_file_ownership_preserved)=

## Is file ownership preserved?

No, Chisel does not yet preserve the owner UID:GID of files extracted from
packages. The owner of the extracted files is the current user.


(faq_reproducible_output)=

## Does Chisel support reproducible rootfs outputs?

Chisel always fetches the latest version of a package from the archives. Thus,
the root file systems Chisel produces in subsequent executions may not be
identical if a package has changed in the meantime.

Chisel also does not support pinning package versions.

Related: [Issue 154].


<!-- LINKS -->

[creating a new issue]: https://github.com/canonical/chisel-releases/issues/new
[Issue 154]: https://github.com/canonical/chisel/issues/154
