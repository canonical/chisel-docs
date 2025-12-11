(chisel_mo_explanation)=

# How Chisel works

Chisel uses the {{cut_cmd}} to _slice_ Ubuntu packages, as described in the workflow below:

1. **Read and parse chisel-releases**

   Chisel fetches, reads and validates the {ref}`chisel-release<chisel-releases_ref>`.
   This includes parsing the {ref}`chisel_yaml_ref` and {ref}`slice 
   definitions<slice_definitions_ref>` while validating the release and checking for conflicting paths across packages.

2. **Talk to Ubuntu archives and fetch packages**

   Chisel talks to the {ref}`chisel_yaml_format_spec_archives` directly.
   It fetches, validates and parses their `InRelease` files.
   It then resolves which archive holds the **requested** packages and fetches
   the corresponding package tarballs.

3. **Install only the specified files from the packages**

   Chisel groups and merges all slice definitions per package. Then,
   for every package, it extracts the **specified slices' paths** into
   the provided root file system.

4. **Run mutation scripts and remove temporary files**

   Chisel then runs the {{mutation_scripts}}. Only the
   {ref}`mutable<slice_definitions_format_slices_contents_mutable>` files may be
   modified at this stage. Finally, the files specified with
   {ref}`until:mutate<slice_definitions_format_slices_contents_until>` are
   removed from the provided root file system.
