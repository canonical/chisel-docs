# Known issues

This page lists some known limitations, issues and frequently asked questions.


(faq_arbitrary_package_names)=

## Is it possible to use arbitrary package names?

No, package names must be the same as the package names in the archive, so that
there's a single namespace to remember and respect.


(faq_available_ubuntu_versions)=

## Which Ubuntu versions have package slices?

The slice definitions are located at the {{chisel_releases_repo}}. The
`ubuntu-XX.YY` branches in that repository contains the slice definitions for
the corresponding Ubuntu releases.

If you find a specific release missing, let the maintainers know by [creating a
new issue] in the {{chisel_releases_repo}}.


(faq_non-ubuntu_archives)=

## Is it possible to use non-Ubuntu archives?

Not yet. The supported archives are described at
{ref}`chisel_yaml_format_spec_archives`.


(faq_ppa)=

## Is it possible to use PPAs?

Not yet.


(faq_file_ownership_preserved)=

## Is file ownership preserved?

No, Chisel does not yet preserve the owner UID:GID of files extracted from
packages.


(faq_per-arch_dependency)=

## Does Chisel support per-architecture slice dependency?

Although a package may require additional packages based on the architecture,
Chisel currently does not support listing per-architecture slices in
{ref}`slice_definitions_format_slices_essential`.

See [Issue 93].


(faq_reproducible_output)=

## Does Chisel support reproducible output?

Chisel always fetches the latest version of a package from the archives. Thus,
the root file systems Chisel produces in subsequent executions may not be
identical if a package has changed in the meantime.

Chisel also does not support pinning package versions, nor does it support the
[snapshot service].

See [Issue 154].


(faq_refer_same_path)=

## Can multiple slices refer to the same path?

Multiple slices may _refer_ to the same path, but they cannot install the same path.
For example, multiple slices may install different paths copied from the same
source like the following:

```yaml
package: pkg1
slices:
  slice1:
    contents:
      /new-path-1: {copy: /path}
---
package: pkg2
slices:
  slice2:
    contents:
      /new-path-2: {copy: /path}
```

But they cannot install to the same path. The following is not supported:

```yaml
package: pkg1
slices:
  slice1:
    contents:
      /path:
---
package: pkg2
slices:
  slice2:
    contents:
      /path:
```

These are called _path conflicts_ in Chisel. See {ref}`faq_install_same_path` to
learn more.


(faq_install_same_path)=

## Can multiple slices install the same path?

Not yet. Multiple slices installing the same path raises a conflict in Chisel.
While it is not currently supported, there have been ongoing work to support
this soon.

See [Issue 50].

### Exceptions

#### Slices from the same package

There is a slight exception to slices from the same package when it comes to
path conflicts. If two slices from the same package list the same package path,
they will be able to install the path.

```yaml
package: pkg1
slices:
  slice1:
    contents:
      /file:
  slice2:
    contents:
      /file:
  slice3:
    contents:
      /*file:
```

In the above example, `/file`, `/file` and `/*file` entries from `slice1`,
`slice2` and `slice3` respectively will install the same path `/file`. This will
not raise an error since the slices are from the same package.

#### Identical paths that Chisel creates

If there are identical entries listed across different package slices which are
not _package paths_, that will not raise an error as well. Here, _package path_
refers to a path that is directly extracted from the package tarball and not
created by Chisel.

```yaml
package: pkg1
slices:
  slice1:
    contents:
      /dir/: {make: true}
      /text-file: {text: "foo"}
      /symlink: {symlink: "foo"}
---
package: pkg2
slices:
  slice2:
    contents:
      /dir/: {make: true}
      /text-file: {text: "foo"}
      /symlink: {symlink: "foo"}
```

In the above example, the slices are from different packages but they list the
same paths with identical attributes. These are not paths that will be extracted
from the package, but will be created by Chisel itself. These paths will not
conflict.



<!-- LINKS -->

[creating a new issue]: https://github.com/canonical/chisel-releases/issues/new
[snapshot service]: https://snapshot.ubuntu.com/
[Issue 50]: https://github.com/canonical/chisel/issues/50
[Issue 93]: https://github.com/canonical/chisel/issues/93
[Issue 154]: https://github.com/canonical/chisel/issues/154
