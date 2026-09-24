---
myst:
  html_meta:
    description: "Explanation of the three slice design approaches in Chisel: grouping by content type (bins, libs), by function (crypto, dbus-services) or by tier (minimal, core, standard, dev)."
---

(slice_design_approaches)=

# Slice design approaches

There are three approaches to design slices: **grouping by content**,
**grouping by function** and **grouping by tier**. Depending on the package,
one of these approaches might be more suitable. It is up to the user to choose
a preferred approach.

The approaches are not mutually exclusive, and a single slice definitions file
can mix them. For example, the
[`systemd` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-26.04/slices/systemd.yaml)
has tier slices (`standard`, `dev`), function slices such as `journal`,
`login` and `dbus-services`, and a `config` slice grouping contents by type.

## Grouping by type of content

This means putting all the binaries together in one slice, all the libraries
together in another slice, and so on. A good example is the
[`dpkg` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-26.04/slices/dpkg.yaml).

In this case, the best practice is to create:

- a `bins` slice which contains all the binaries
- a `libs` slice which contains all the libraries
- a `config` slice which contains all [configuration files](#create_sdf_inspect_pkg_conffiles)
- a `scripts` slice which contains ASCII executable scripts, e.g. Python,
  Perl scripts
- other slices analogously (e.g. `data`, `modules`, `services`, etc)

You may split the above slices into more granular ones, but you should
reserve the above as a catch-all for their respective types.

(slice_design_approaches_function)=

## Grouping by function

This means grouping the contents into slices that deliver a specific
functionality, and naming each slice after the functionality it provides. For
example, the
[`libpython3.14-stdlib` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-26.04/slices/libpython3.14-stdlib.yaml)
splits the Python standard library into slices such as `crypto`,
`concurrency` and `internet`, and the `systemd` slice definitions file has a
`dbus-services` slice with the D-Bus service files.

Such slices are best kept small and single-purpose, so that users can install
just the functionality they need on top of a base installation (see
[grouping by tier](#slice_design_approaches_tier)).

(slice_design_approaches_tier)=

## Grouping by tier

This means grouping the contents into slices of increasing completeness, where
each tier is a superset of the previous one. For example, the
[`python3` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-26.04/slices/python3.yaml)
has a `core` slice providing a very minimal `python3` runtime, but also a
`standard` slice with the additional libraries on top of `core`.

In this case, the most common is to create:

- A `minimal` slice that offers a stripped down installation, with the
  absolute bare minimum which still retains the identity of the package. In
  most cases, such a minimal installation may only be useful if used as a base
  for another installation/build, where the developer adds their own
  additional dependencies. Taking the above `python3` example, this slice would
  only contain a runtime with no standard library, able to run a trivial "Hello
  World" script, and not much more.
- A `core` slice that offers what is needed for basic functionality, and
  nothing more. Although slightly larger than `minimal`, `core` installations
  are meant to cover the majority of simple use cases, while also being a small
  and ideal base to be extended for more complex use cases. Using `python3` as
  an example again, this slice could only contain the topmost referenced
  modules in the standard library.
- A `standard` slice that provides what most users would expect from a normal
  installation, supporting the full operation of the application, including all
  the runtime libs/modules and additional utilities. It still does not include
  everything, leaving out things like manual pages, examples, and debugging and
  development utilities.
- A `dev` slice which is the `standard` slice, plus all the debugging and dev
  utilities. A close-to full-size installation, designed for development
  environments, but not production. For example, the `systemd_dev` slice
  adds tools such as `busctl` and `systemd-cgls` on top of `systemd_standard`.

Not all four tiers have to be present, so only define the ones that are
meaningful for the package. However, since each tier is a superset of the
previous one, a higher tier must list the lower one in its `essential`
dependencies.

`standard` is the convenient choice when the package should behave like a
regular installation. Applications that only need part of a package should
instead install the `core` slice plus the
[function slices](#slice_design_approaches_function) they use, which keeps the
root file system smaller. For example, an application that only needs
Python's cryptographic modules can install `python3_core` and
`libpython3.14-stdlib_crypto` instead of `python3_standard`.
