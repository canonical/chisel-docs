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

## How this documentation is organized

This documentation uses the [Diátaxis documentation structure](https://diataxis.fr/).

- The [Tutorial](https://documentation.ubuntu.com/chisel/en/latest/tutorial/getting-started/) takes you step-by-step through the creation of your first chiseled Ubuntu root file system, from installation to the slicing of Ubuntu packages.
- [How-to guides](https://documentation.ubuntu.com/chisel/en/latest/how-to/) assume you have basic familiarity with Chisel. They cover tasks such as installation, slicing and usage of Chisel. 
- [Reference](https://documentation.ubuntu.com/chisel/en/latest/reference/) provides a guide to CLI commands, chisel-releases and security details.
- [Explanation](https://documentation.ubuntu.com/chisel/en/latest/explanation/) includes topic overviews, background and context and detailed discussion.

---------

## Project and community

Chisel is a member of the Ubuntu family. It’s an open source project that warmly welcomes community contributions, suggestions, fixes and constructive feedback.

### Get involved

* [Support](https://docs.google.com/document/d/1I94nnO1PHx16uKkuFJgDwb-Yl-trd2JhNkE3ELZ0Jvc/edit#)  
* [Online chat](https://matrix.to/#/#chisel:ubuntu.com) 
* [Contribute](https://github.com/canonical/chisel)
    
### Releases

* [Release notes](https://github.com/canonical/chisel/releases)
   
### Governance and policies

* [Code of conduct](https://ubuntu.com/community/docs/ethos/code-of-conduct)  
* [Security policy](https://github.com/canonical/chisel/blob/main/SECURITY.md)
    
### Commercial support

Thinking about using Chisel for your next project? [Get in touch!](https://canonical.com/#get-in-touch#)

```{toctree}
:hidden:
:maxdepth: 2

Tutorial <tutorial/getting-started>
how-to/index
reference/index
explanation/index
```
