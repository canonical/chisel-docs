---
myst:
  html_meta:
    description: "Reference for chisel-releases, the versioned directory of slice definitions files and chisel.yaml that Chisel uses to identify and fetch package slices."
---

(chisel-releases_ref)=

# chisel-releases

Chisel uses **slice definitions files** (aka SDFs) to define the slices of packages.
SDFs are YAML files, and there is one per package and per Ubuntu release, named
after the package name.

For a given Ubuntu release, the collection of SDFs plus a configuration file
named `chisel.yaml` form what is called a _chisel-release_.

The {{chisel_releases_repo}} contains a number of branches for various
_chisel-releases_, matching the corresponding Ubuntu releases.
If you find a specific release missing, let the maintainers know by [creating a
new issue] in the {{chisel_releases_repo}}.


A _chisel-release_ is simply a directory with the following structure:

```
├── chisel.yaml
├── slices
│   ├── pkgA.yaml
│   ├── pkgB.yaml
│   └── ...
└── bin-slices
    ├── bin-pkgC.yaml
    └── ...
```

```{note}
The `bin-slices/` directory is only used in format `v3`. It contains slice
definitions for packages fetched from
{ref}`stores<chisel_yaml_format_spec_stores>`. From format `v4` onwards, bin
slice definitions live in `slices/` alongside regular ones, so `bin-slices/`
is not used.
```

The following pages provide more details on:

```{toctree}
:maxdepth: 1

chisel.yaml
slice-definitions
```

[creating a
new issue]: https://github.com/canonical/chisel-releases/issues/new
