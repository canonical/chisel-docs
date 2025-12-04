# Chisel

**Chisel** is a developer tool for extracting well-defined portions ({{package_slices}}) of Ubuntu packages.

Chisel extracts specialized slices and only installs the necessary files from Ubuntu packages.

Application creators need to be able to ship container images suited to their specific needs with a reduced attack 
surface and a small storage footprint . With Chisel, users can build a minimal root filesystem for each image by 
selecting only the necessary components from the full Ubuntu package set.

It operates similarly to a package manager, but for package slices, thus being particularly useful for supporting 
developers in the creation of hardened, tailored and fully functional container images.

Read more about [Chisel’s security](https://documentation.ubuntu.com/chisel/en/latest/reference/security/).

---------

## In this documentation

* **Tutorial**: [Hands-on introduction to Chisel in 15 minutes](https://documentation.ubuntu.com/chisel/en/latest/tutorial/getting-started/)
    
* **Using Chisel**: [Installation options](https://documentation.ubuntu.com/chisel/en/latest/how-to/install-chisel/) • 
[Use Chisel in Dockerfile](https://documentation.ubuntu.com/chisel/en/latest/how-to/use-chisel-in-dockerfile/) • 
[CLI reference](https://documentation.ubuntu.com/chisel/en/latest/reference/cmd/) • 
[chisel.yaml](https://documentation.ubuntu.com/chisel/en/latest/reference/chisel-releases/chisel.yaml/) 
    
* **Slices**: [Overview](https://documentation.ubuntu.com/chisel/en/latest/explanation/slices/) • 
[Chisel releases](https://documentation.ubuntu.com/chisel/en/latest/reference/chisel-releases/) • 
[Slice a package](https://documentation.ubuntu.com/chisel/en/latest/how-to/slice-a-package/) • 
[Install Ubuntu Pro package slices](https://documentation.ubuntu.com/chisel/en/latest/how-to/install-pro-package-slices/) • 
[Slice definitions](https://documentation.ubuntu.com/chisel/en/latest/reference/chisel-releases/slice-definitions/)

---------

## How this documentation is organized

This documentation uses the [Diátaxis documentation structure](https://diataxis.fr/).

- The [Tutorial](https://documentation.ubuntu.com/chisel/en/latest/tutorial/getting-started/) takes you step-by-step 
through the creation of your first chiseled Ubuntu root file system, from installation to the slicing of Ubuntu 
packages.
- [How-to guides](https://documentation.ubuntu.com/chisel/en/latest/how-to/) assume you have basic familiarity with 
Chisel. They cover tasks such as installation, slicing and usage of Chisel. 
- [Reference](https://documentation.ubuntu.com/chisel/en/latest/reference/) provides a guide to CLI commands, 
chisel-releases and security details.
- [Explanation](https://documentation.ubuntu.com/chisel/en/latest/explanation/) includes topic overviews, background 
and context and detailed discussion.

---------

## Project and community

Chisel is a member of the Ubuntu family. It’s an open source project that warmly welcomes community contributions, 
suggestions, fixes and constructive feedback.

### Get involved

* <a href="https://matrix.to/#/#chisel:ubuntu.com">Online chat</a>
* [Contribute](https://github.com/canonical/chisel)
    
### Releases

* [Release notes](https://github.com/canonical/chisel/releases)
   
### Governance and policies

* [Code of conduct](https://ubuntu.com/community/docs/ethos/code-of-conduct)  
* [Security policy](https://github.com/canonical/chisel/blob/main/SECURITY.md)
    
### Commercial support

Thinking about using Chisel for your next project? <a href="https://canonical.com/#get-in-touch#">Get in touch!</a>

```{toctree}
:hidden:
:maxdepth: 2

Tutorial <tutorial/getting-started>
how-to/index
reference/index
explanation/index
```
