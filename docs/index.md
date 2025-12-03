# Chisel

**Chisel** is a developer tool for extracting well-defined portions ({{package_slices}}) of Ubuntu packages to create compact, secure container images.

Chisel extracts specialized slices and only installs the necessary files from Ubuntu packages.

Application creators need to be able to ship container images suited to their specific needs with a reduced attack surface and a small storage footprint . With Chisel, users can build a minimal root filesystem for each image by selecting only the necessary components from the full Ubuntu package set.

It operates similarly to a package manager, but for package slices, thus being particularly useful for supporting developers in the creation of hardened, tailored and fully functional container images.

Read more about [Chisel’s approach to security](https://documentation.ubuntu.com/chisel/en/latest/reference/security/).

---------

## In this documentation

````{grid} 1 1 2 2

```{grid-item-card} [Tutorial](tutorial/getting-started)

**Get started** - become familiar with Chisel by slicing Ubuntu packages to create
a minimal root file system.
```

```{grid-item-card} [How-to guides](how-to/index)

**Step-by-step guides** - learn key operations and common tasks.
```

````

````{grid} 1 1 2 2
:reverse:

```{grid-item-card} [Reference](reference/index)

**Technical information** - understand the CLI commands, slice definitions files
and Chisel manifests.
```

```{grid-item-card} [Explanations](explanation/index)

**Discussion and clarification** - explore Chisel's mode of operation and learn
about fundamental topics such as package slices.
```

````

---------

## Project and community

Chisel is free software and released under {{AGPL3}}.

The Chisel project is sponsored by {{Canonical}}.

- [Code of conduct](https://ubuntu.com/community/ethos/code-of-conduct)
- [Contribute](https://github.com/canonical/chisel)
- [Security policy](https://github.com/canonical/chisel/blob/main/SECURITY.md)


```{toctree}
:hidden:
:maxdepth: 2

Tutorial <tutorial/getting-started>
how-to/index
reference/index
explanation/index
```
