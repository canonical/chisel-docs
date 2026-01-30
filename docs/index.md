# Chisel

**Chisel** is a developer tool for extracting highly customized and specialized ({{package_slices}}) of Ubuntu packages to create 
compact, secure software.

Users need to be able to create software suited to their specific needs with a reduced attack 
surface and a small storage footprint. With Chisel, users build a minimal root filesystem by 
selecting and installing only the necessary slices from the full Ubuntu package set.

---------

## In this documentation

* **Tutorial**: [Hands-on introduction to Chisel in 15 minutes](tutorial/getting-started)
    
* **Common patterns**: [Install Chisel](how-to/install-chisel) • 
[Slice a package](how-to/slice-a-package/) • 
[Use Chisel in a Dockerfile](how-to/use-chisel-in-dockerfile) • 
[Explore the Chisel CLI](reference/cmd/index) 
    
* **Slices**: [Learn more about slices](explanation/slices) • 
[Chisel releases](reference/chisel-releases/index) • 
[chisel.yaml](reference/chisel-releases/chisel.yaml) •
[Slice definitions](reference/chisel-releases/slice-definitions) • [Slice design approaches](explanation/slice-design-approaches.md) • 
[Install Ubuntu Pro package slices](how-to/install-pro-package-slices)

---------

## How this documentation is organized

- The [Tutorial](tutorial/getting-started) takes you step-by-step 
through the creation of your first chiseled Ubuntu root file system, from installation to the slicing of Ubuntu 
packages.
- [How-to guides](how-to/index) assume you have basic familiarity with 
Chisel. They cover tasks such as installation, slicing and usage of Chisel. 
- [Reference](reference/index) provides a guide to CLI commands, 
chisel-releases and security details.
- [Explanation](explanation/index) includes topic overviews, background 
and context and detailed discussion.

---------

## Project and community

Chisel is a member of the Ubuntu family. It’s an open source project that warmly welcomes [community contributions](https://documentation.ubuntu.com/project/contributors/).

### Get involved

* <a href="https://matrix.to/#/#chisel:ubuntu.com">Online chat</a>
* [Contribute](https://github.com/canonical/chisel)
    
### Releases

* [Release notes](https://github.com/canonical/chisel/releases)
* [chisel-releases](https://github.com/canonical/chisel-releases)
   
### Governance and policies

* [Code of conduct](https://ubuntu.com/community/docs/ethos/code-of-conduct)  
* [Security policy](https://github.com/canonical/chisel/blob/main/SECURITY.md)
    
### Commercial support

Thinking about using Chisel for your next project? <a href="https://canonical.com/#get-in-touch#">Get in touch!</a>

---------

This documentation uses the [Diátaxis documentation structure](https://diataxis.fr/).

```{toctree}
:hidden:
:maxdepth: 2

Tutorial <tutorial/getting-started>
how-to/index
reference/index
explanation/index
```
