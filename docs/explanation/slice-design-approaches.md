(slice_design_approaches)=

# Slice design approaches

There are two approaches to design slices: **grouping by content** and **grouping by function**. Depending on the package, one of these approaches might be more suitable. It is up to the user to choose a preferred approach.

## Grouping by type of content

 This means putting all the binaries together in one slice, all the libraries together in another slice, and so on.
 A good example is the [`dpkg` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/dpkg.yaml).

  In this case, the best practice is to create:
  - a `bins` slice which contains all the binaries
  - a `libs` slice which contains all the libraries
  - a `config` slice which contains all [configuration files](#create_sdf_inspect_pkg_conffiles)
  - a `scripts` slice which contains ASCII executable scripts, e.g. Python,
    Perl scripts
  - other slices analogously (e.g. `data`, `modules`, `services`, etc)
  
  You may split the above slices into more granular ones, but you should
  reserve the above as a catch-all for their respective types.

## Grouping by function

  This means grouping the contents into slices that deliver a specific
  functionality. For example, the 
  [`python3` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/python3.yaml)
  has a `core` slice providing a very minimal `python3` runtime, but also a
  `standard` slice with the additional libraries on top of `core`.
  
  In this case, the most common is to create:
  - A `minimal` slice that offers a stripped down installation, to the absolute essentials, to make the software 
  work. In most cases, such a minimal installation may only be useful if used as a base for another installation/
  build, where the developer adds their own additional dependencies. Taking the above `python3` example, this slice 
  would only contain the necessary dependencies to run a trivial "Hello World" script, and not much more.
  - A `core` slice that offers a more complete, though still relatively slim installation. Although slightly larger 
  than minimal, core installations are meant to cover the majority of simple use cases, while also being a small and 
  ideal base to be extended for more complex use cases. Using `python3` as an example again, this slice could only 
  contain the topmost referenced modules in the standard library.
  - A `standard` slice that provides a normal installation, supporting the full operation of the application, 
  including all the runtime libs/modules and additional utilities, but possibly still leaving out things like 
  debugging and development utilities.
  - A `dev` slice which is the `standard` slice, plus all the debugging and dev utilities. A close-to full-size 
  installation, designed for development environments, but not production.
  - Other slices which are scoped and named after the functionality they
  provide (e.g. see the 
  [`libpython3.12-stdlib` slices](https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/libpython3.12-stdlib.yaml)).
