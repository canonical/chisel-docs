---
myst:
  html_meta:
    description: "Explanation of how Chisel works: read chisel-releases, fetch packages from Ubuntu archives and stores, and extract selected files into a root file system."
---

(chisel_mo_explanation)=

# How Chisel works

The purpose of Chisel is to create a minimal Ubuntu root file system comprising
only the application and its runtime dependencies. Chisel is especially useful
for developers who are looking to create minimal and distroless-like container
images.

Chisel uses the {{cut_cmd}} to _slice_ Ubuntu packages, as depicted in the workflow below:

<table style="width: 100%;">
  <colgroup>
    <col style="width: 45%;">
    <col style="width: 55%;">
  </colgroup>

<!-- MO 1 -->
  <tr>
    <td>

```{image} /_static/MO-1.svg
  :align: center
  :alt: Read and parse chisel-releases
```

</td>
    <td>

Chisel fetches, reads and validates the {ref}`chisel-release<chisel-releases_ref>`.
This includes parsing the {ref}`chisel_yaml_ref` and {ref}`slice 
definitions<slice_definitions_ref>` while validating the release and checking for conflicting paths across packages.
    
</td>
  </tr>


<!-- MO 2 -->
  <tr>
    <td>

```{image} /_static/MO-2.svg
  :align: center
  :alt: Talk to archives and fetch packages
```

</td>
    <td>

Chisel resolves the source of each **requested** package and fetches it.
Packages are typically fetched from {ref}`archives<chisel_yaml_format_spec_archives>`,
which are Debian archives Chisel talks to directly by fetching, validating and
parsing their `InRelease` files. Packages may also be fetched from
{ref}`stores<chisel_yaml_format_spec_stores>`, which serve packages via a store
API rather than from a Debian archive. Stores are used to distribute packages
that are not available in the standard Ubuntu archives, such as `bin` packages.
   
</td>
  </tr>

<!-- MO 3 -->
  <tr>
    <td>

```{image} /_static/MO-3.svg
  :align: center
  :alt: Install package slices
```

</td>
    <td>

Chisel groups and merges all slice definitions per package. Then,
for every package, it extracts the **specified slices' paths** into
the provided root file system. Files ownership (UID:GID) is not 
preserved during this process. The owner of the extracted files 
is the current user.

</td>
  </tr>

<!-- MO 4 -->
  <tr>
    <td>

```{image} /_static/MO-4.svg
  :align: center
  :alt: Run mutation scripts
```

</td>
    <td>

Chisel then runs the {{mutation_scripts}}. Only the
{ref}`mutable<slice_definitions_format_slices_contents_mutable>` files may be
modified at this stage. Finally, the files specified with
{ref}`until:mutate<slice_definitions_format_slices_contents_until>` are
removed from the provided root file system.

    
</td>
  </tr>
</table>
