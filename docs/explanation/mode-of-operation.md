(chisel_mo_explanation)=

# How Chisel works

Chisel uses the {{cut_cmd}} to _slice_ Ubuntu packages, as depicted in the workflow below:

```{list-table}
:widths: 45 55
:header-rows: 0
:class: align-middle

* - ```mermaid
    graph TD
        step1{{1. Read and parse chisel-releases}}
        style step1 fill:#a81c1c,stroke:#333,stroke-width:1px,color:white
    ```
  - Chisel fetches, reads and validates the {ref}`chisel-release<chisel-releases_ref>`.
    This includes parsing the {ref}`chisel_yaml_ref` and {ref}`slice 
    definitions<slice_definitions_ref>` while validating the release and checking for conflicting paths across packages.

* - ```mermaid
    graph TD
        step2{{2. Talk to Ubuntu archives<br>and fetch packages}}
        style step2 fill:#a81c1c,stroke:#333,stroke-width:1px,color:white
    ```
  - Chisel talks to the {ref}`chisel_yaml_format_spec_archives` directly.
    It fetches, validates and parses their `InRelease` files.
    It then resolves which archive holds the **requested** packages and fetches
    the corresponding package tarballs.

* - ```mermaid
    graph TD
        step3{{3. Install only the specified<br>files from packages}}
        style step3 fill:#a81c1c,stroke:#333,stroke-width:1px,color:white
    ```
  - Chisel groups and merges all slice definitions per package. Then,
    for every package, it extracts the **specified slices' paths** into
    the provided root file system.

* - ```mermaid
    graph TD
        step4{{4. Run mutation scripts and<br>remove temporary files}}
        style step4 fill:#a81c1c,stroke:#333,stroke-width:1px,color:white
    ```
  - Chisel then runs the {{mutation_scripts}}. Only the
    {ref}`mutable<slice_definitions_format_slices_contents_mutable>` files may be
    modified at this stage. Finally, the files specified with
    {ref}`until:mutate<slice_definitions_format_slices_contents_until>` are
    removed from the provided root file system.