# Slice a package

This guide provides instructions on the slicing of an Ubuntu package for
Chisel.

A package slice is represented via a
{ref}`Slice Definitions File<slice_definitions_ref>` (aka SDF), and the creation
of said slice definitions is a result of the **inspection** and **design
process** depicted below.

As an example, this guide will focus on **slicing the `vim-tiny` package from
Ubuntu 24.04**.

(create_sdf_inspect_pkg)=

## Inspect the package

Your first task is to **understand the package** to be sliced.

Packages are primarily composed of files for installation and may reference
additional packages as dependencies such as libraries or other resources.

During the slicing process, we identify subsets of files in a package which can
be installed alone to accomplish one or more tasks. Consequently, the
dependencies required for this slice may be a subset of the dependencies
indicated by the package.

1. [ ] **Is it an Ubuntu package?**

    Chisel only supports packages from the Ubuntu (and Ubuntu Pro) archives.

2. [ ] [**Get the package dependencies**]{#create_sdf_inspect_pkg_deps}

    You can run `apt depends vim-tiny` or use the [Ubuntu Packages Search] website.

    <details>

    <summary>Example: vim-tiny pkg dependencies</summary>

    ```{terminal}
    apt depends vim-tiny

    vim-tiny
      Depends: vim-common (= 2:9.1.0016-1ubuntu7.8)
      Depends: libacl1 (>= 2.2.23)
      Depends: libc6 (>= 2.34)
      Depends: libselinux1 (>= 3.1~)
      Depends: libtinfo6 (>= 6)
      Suggests: indent
    ```

    </details>

3. [ ] [**Inspect the files the package provides**]{#create_sdf_inspect_pkg_files}

    You can run `apt download vim-tiny` and then `dpkg -c vim-tiny*.deb` to
    check the package data contents. Or check the
    [`vim-tiny` package contents in the Ubuntu Packages Search] website.

    ````{note}
    A package's contents and dependencies may change depending on the
    architecture. Make sure to double check any differences and adjust your slices accordingly.
    ````

    <details>

    <summary>Example: vim-tiny contents in Ubuntu 24.04, for amd64</summary>

    ```{terminal}
    dpkg -c vim-tiny_2%3a9.1.0016-1ubuntu7.8_amd64.deb

    drwxr-xr-x root/root         0 2025-04-01 20:12 ./
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./etc/
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./etc/vim/
    -rw-r--r-- root/root       662 2025-04-01 20:12 ./etc/vim/vimrc.tiny
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/bin/
    -rwxr-xr-x root/root   1736392 2025-04-01 20:12 ./usr/bin/vim.tiny
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/bug/
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/bug/vim-tiny/
    -rw-r--r-- root/root       302 2024-08-27 04:05 ./usr/share/bug/vim-tiny/presubj
    -rwxr-xr-x root/root       204 2024-08-27 04:05 ./usr/share/bug/vim-tiny/script
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/doc/
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/doc/vim-tiny/
    -rw-r--r-- root/root     14394 2025-04-01 20:12 ./usr/share/doc/vim-tiny/changelog.Debian.gz
    -rw-r--r-- root/root     28068 2024-08-27 04:05 ./usr/share/doc/vim-tiny/copyright
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/lintian/
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/lintian/overrides/
    -rw-r--r-- root/root       119 2024-08-27 04:05 ./usr/share/lintian/overrides/vim-tiny
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/vim/
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/vim/vim91/
    drwxr-xr-x root/root         0 2025-04-01 20:12 ./usr/share/vim/vim91/doc/
    -rw-r--r-- root/root       324 2024-08-27 04:05 ./usr/share/vim/vim91/doc/README.Debian
    -rw-r--r-- root/root      1350 2024-08-27 04:05 ./usr/share/vim/vim91/doc/help.txt
    -rw-r--r-- root/root      1935 2025-04-01 20:12 ./usr/share/vim/vim91/doc/tags
    ```

    For `vim-tiny`, we see that there are a few binaries at `/usr/bin/`, a few
    configuration files, the copyright files, manpages and so on.
    </details>

4. [ ] [**Inspect the package metadata**]{#create_sdf_inspect_pkg_control}

    The package metadata files include:
    - the [`control` file] (which you can use
    to double-check the package dependencies you got from above),
    - [maintainer scripts], and
    - [`conffiles`] file.

    Run `dpkg -e vim-tiny*.deb` to extract the metadata files into a new
    `DEBIAN/` directory for inspection.

   1. [ ] [**Inspect package [`conffiles`] file**]{#create_sdf_inspect_pkg_conffiles}

      This file lists the configuration files a package provides. This can be
      useful later, when deciding whether to create a `config` slice or not.

      <details>

      <summary>Example: vim-tiny conffiles</summary>

      ```{terminal}
      cat DEBIAN/conffiles

      /etc/vim/vimrc.tiny
      ```

      </details>

   2. [ ] [**Inspect package [maintainer scripts]**]{#create_sdf_inspect_pkg_maintainer_scripts}

      Since Chisel doesn't remove files (except when [`until: mutate` is used](#slice_definitions_format_slices_contents_until)),
      we can focus only on the `preinst` and
      `postinst` scripts. Whatever these scripts do, you should aim to reproduce
      when defining the slices. For the simplest cases where the maintainer
      scripts are creating new contents (e.g. new symlinks), one should simply
      declare said paths as contents of the slice. Otherwise, if logic is
      involved, such scripts should be declared as "mutation scripts",
      which are written in
      [Starlark](https://github.com/google/starlark-go).

      <details>

      <summary>Example: vim-tiny maintainer scripts</summary>

      From the `postinst` script, we see:

      ```sh

      #!/bin/sh

      set -e

      # Automatically added by dh_installalternatives/13.14.1ubuntu5

      if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ] || [ "$1" = "abort-deconfigure" ] || [ "$1" = "abort-remove" ]; then
              update-alternatives --install /usr/bin/editor editor /usr/bin/vim.tiny 15 \
                  --slave /usr/share/man/man1/editor.1.gz editor.1.gz /usr/share/man/man1/vim.1.gz \
                  --slave /usr/share/man/da/man1/editor.1.gz editor.da.1.gz /usr/share/man/da/man1/vim.1.gz \
                  --slave /usr/share/man/de/man1/editor.1.gz editor.de.1.gz /usr/share/man/de/man1/vim.1.gz \
                  --slave /usr/share/man/fr/man1/editor.1.gz editor.fr.1.gz /usr/share/man/fr/man1/vim.1.gz \
                  --slave /usr/share/man/it/man1/editor.1.gz editor.it.1.gz /usr/share/man/it/man1/vim.1.gz \
                  --slave /usr/share/man/ja/man1/editor.1.gz editor.ja.1.gz /usr/share/man/ja/man1/vim.1.gz \
                  --slave /usr/share/man/pl/man1/editor.1.gz editor.pl.1.gz /usr/share/man/pl/man1/vim.1.gz \
                  --slave /usr/share/man/ru/man1/editor.1.gz editor.ru.1.gz /usr/share/man/ru/man1/vim.1.gz \
                  --slave /usr/share/man/tr/man1/editor.1.gz editor.tr.1.gz /usr/share/man/tr/man1/vim.1.gz
      fi

      # End automatically added section

      # Automatically added by dh_installalternatives/13.14.1ubuntu5

      if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ] || [ "$1" = "abort-deconfigure" ] || [ "$1" = "abort-remove" ]; then
              update-alternatives --install /usr/bin/ex ex /usr/bin/vim.tiny 15 \
                  --slave /usr/share/man/man1/ex.1.gz ex.1.gz /usr/share/man/man1/vim.1.gz \
                  --slave /usr/share/man/da/man1/ex.1.gz ex.da.1.gz /usr/share/man/da/man1/vim.1.gz \
                  --slave /usr/share/man/de/man1/ex.1.gz ex.de.1.gz /usr/share/man/de/man1/vim.1.gz \
                  --slave /usr/share/man/fr/man1/ex.1.gz ex.fr.1.gz /usr/share/man/fr/man1/vim.1.gz \
                  --slave /usr/share/man/it/man1/ex.1.gz ex.it.1.gz /usr/share/man/it/man1/vim.1.gz \
                  --slave /usr/share/man/ja/man1/ex.1.gz ex.ja.1.gz /usr/share/man/ja/man1/vim.1.gz \
                  --slave /usr/share/man/pl/man1/ex.1.gz ex.pl.1.gz /usr/share/man/pl/man1/vim.1.gz \
                  --slave /usr/share/man/ru/man1/ex.1.gz ex.ru.1.gz /usr/share/man/ru/man1/vim.1.gz \
                  --slave /usr/share/man/tr/man1/ex.1.gz ex.tr.1.gz /usr/share/man/tr/man1/vim.1.gz
      fi

      # End automatically added section

      # Automatically added by dh_installalternatives/13.14.1ubuntu5

      if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ] || [ "$1" = "abort-deconfigure" ] || [ "$1" = "abort-remove" ]; then
              update-alternatives --install /usr/bin/rview rview /usr/bin/vim.tiny 15
      fi

      # End automatically added section

      # Automatically added by dh_installalternatives/13.14.1ubuntu5

      if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ] || [ "$1" = "abort-deconfigure" ] || [ "$1" = "abort-remove" ]; then
              update-alternatives --install /usr/bin/vi vi /usr/bin/vim.tiny 15 \
                  --slave /usr/share/man/man1/vi.1.gz vi.1.gz /usr/share/man/man1/vim.1.gz \
                  --slave /usr/share/man/da/man1/vi.1.gz vi.da.1.gz /usr/share/man/da/man1/vim.1.gz \
                  --slave /usr/share/man/de/man1/vi.1.gz vi.de.1.gz /usr/share/man/de/man1/vim.1.gz \
                  --slave /usr/share/man/fr/man1/vi.1.gz vi.fr.1.gz /usr/share/man/fr/man1/vim.1.gz \
                  --slave /usr/share/man/it/man1/vi.1.gz vi.it.1.gz /usr/share/man/it/man1/vim.1.gz \
                  --slave /usr/share/man/ja/man1/vi.1.gz vi.ja.1.gz /usr/share/man/ja/man1/vim.1.gz \
                  --slave /usr/share/man/pl/man1/vi.1.gz vi.pl.1.gz /usr/share/man/pl/man1/vim.1.gz \
                  --slave /usr/share/man/ru/man1/vi.1.gz vi.ru.1.gz /usr/share/man/ru/man1/vim.1.gz \
                  --slave /usr/share/man/tr/man1/vi.1.gz vi.tr.1.gz /usr/share/man/tr/man1/vim.1.gz
      fi

      # End automatically added section

      # Automatically added by dh_installalternatives/13.14.1ubuntu5

      if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ] || [ "$1" = "abort-deconfigure" ] || [ "$1" = "abort-remove" ]; then
              update-alternatives --install /usr/bin/view view /usr/bin/vim.tiny 15 \
                  --slave /usr/share/man/man1/view.1.gz view.1.gz /usr/share/man/man1/vim.1.gz \
                  --slave /usr/share/man/da/man1/view.1.gz view.da.1.gz /usr/share/man/da/man1/vim.1.gz \
                  --slave /usr/share/man/de/man1/view.1.gz view.de.1.gz /usr/share/man/de/man1/vim.1.gz \
                  --slave /usr/share/man/fr/man1/view.1.gz view.fr.1.gz /usr/share/man/fr/man1/vim.1.gz \
                  --slave /usr/share/man/it/man1/view.1.gz view.it.1.gz /usr/share/man/it/man1/vim.1.gz \
                  --slave /usr/share/man/ja/man1/view.1.gz view.ja.1.gz /usr/share/man/ja/man1/vim.1.gz \
                  --slave /usr/share/man/pl/man1/view.1.gz view.pl.1.gz /usr/share/man/pl/man1/vim.1.gz \
                  --slave /usr/share/man/ru/man1/view.1.gz view.ru.1.gz /usr/share/man/ru/man1/vim.1.gz \
                  --slave /usr/share/man/tr/man1/view.1.gz view.tr.1.gz /usr/share/man/tr/man1/vim.1.gz
      fi

      # End automatically added section

      ```

      The `vim-tiny` maintainer scripts register `/usr/bin/vim.tiny` as an
      alternative implementation for various standard editor commands like `vi`,
      `view`, `editor`, etc. This is done by the `update-alternatives` command,
      and if necessary, we can reproduce this in our slice definitions.

      </details>

5. [ ] **Repeat the above for all dependencies**

    Slices must also exist for every\* other package that `vim-tiny` depends on.
    So if these dependencies aren't yet sliced upstream in [chisel-releases],
    you must do the same inspection for them, and create their slices too.

    \* *Note that you may sometimes find dependencies that are only needed for
    specific parts of the package (like maintainer scripts) that you may not
    need or that you're going to fulfil through other means (e.g. with mutation
    scripts). In such cases, you may not need to slice said dependencies in
    order to create a functional slice.*

(create_sdf_design_slices)=

## Design the slices

Your second task is to **design the slices**. There are a few
considerations to be made, such as figuring out what slices we need and the
contents of those slices.

There are **two schools of thought** when designing slices:

```{list-table}
:header-rows: 1
:widths: 1 1

* - Group by type
  - Group by function
* - This means putting all the binaries together in one slice, all the
  libraries together in another slice, and so on.
  A good example is the [`dpkg` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/dpkg.yaml).
    ```{tip}
    In this case, the best practice is to create:
    - a `bins` slice which contains all the binaries,
    - a `libs` slice which contains all the libraries,
    - a `config` slice which contains all [configuration files](#create_sdf_inspect_pkg_conffiles),
    - a `scripts` slice which contains ASCII executable scripts, e.g. Python,
      Perl scripts,
    - and others analogously (e.g. `data`, `modules`, `services`, etc).
    
    You may split the above slices into more granular ones, but you should
    reserve the above as a catch-all for their respective types.
    ```
  - This means grouping the contents into slices that deliver a specific
  functionality. For example, the [`python3` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/python3.yaml)
  has a `core` slice providing a very minimal `python3` runtime, but also a
  `standard` slice with the additional libraries on top of `core`.
    ```{tip}
    In this case, the most common is to create:
    - a `minimal` slice that offers a stripped down installation, to the absolute essentials, to make the software work. In most cases, such a minimal installation may only be useful if used as a base for another installation/build, where the developer adds their own additional dependencies. Taking the above `python3` example, this slice would only contain the necessary dependencies to run a trivial "Hello World" script, and not much more,
    - a `core` slice that offers a more complete, though still relatively slim installation. Although slightly larger than minimal, core installations are meant to cover the majority of simple use cases, while also being a small and ideal base to be extended for more complex use cases. Using `python3` as an example again, this slice could only contain the topmost referenced modules in the standard library,
    - a `standard` slice that provides a normal installation, supporting the full operation of the application, including all the runtime libs/modules and additional utilities, but possibly still leaving out things like debugging and development utilities,
    - a `dev` slice which is the `standard` slice, plus all the debugging and dev utilities. A close-to full-size installation, designed for development environments, but not production,
    - and other slices which are scoped and named after the functionality they
      provide (e.g. see the [`libpython3.12-stdlib` slices](https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/libpython3.12-stdlib.yaml)).
    ```
```

6. [ ] **Choose the design approach that aligns best with your package**

    Given the {ref}`above package inspection <create_sdf_inspect_pkg>`, the
    `vim-tiny` package can be sliced by *type of content*:
     - a `bins` slice for the `/usr/bin/vim.tiny` binary,
     - a `config` slice for the {ref}`configuration files <create_sdf_inspect_pkg_conffiles>`, and
     - a `copyright` slice for the copyright file.

    ```{important}
    **Every slice** must install the package's copyright file(s).

    It is therefore recommended to create a `copyright` slice for every package, that other slices can depend on.
    ```

7. [ ] **Prepare to write the slice definitions**

    ```{note}
    There is one Slice Definitions File per package!
    ```

    Slice definitions live in the `slices/` directory of the
    {{chisel_releases_repo}}. Fork and clone this repo, creating a new
    branch for the packages you are slicing.

8. [ ] **Create the YAML Slice Definitions File**

   Create a new file in the `slices/` directory, named after the package you
   are slicing. For example, `vim-tiny.yaml`.

9. [ ] **Specify `package` name**

   The first thing to do is to write the package name in the
   {ref}`slice_definitions_format_package` field. For example, open
   `slices/vim-tiny.yaml` and write:

   ```yaml
   package: vim-tiny
   ```

10. [ ] **Write the `copyright` slice**

    Write the copyright slice first and pin it as an {ref}`essential for every
    other package slice <slice_definitions_format_essential>`.

    ```yaml
    essential:
      - vim-tiny_copyright

    slices:
      copyright:
        contents:
          # This path is taken from the package contents inspected above.
          /usr/share/doc/vim-tiny/copyright:
    ```

    Although we are writing the copyright slice first, we typically list the
    slice at the bottom of the slice definition file.

11. [ ] [**Write the `config` slice**]{#create_sdf_design_slices_config_slice}

    Now write the `config` slice, based on the list from the
    {ref}`conffiles <create_sdf_inspect_pkg_conffiles>`.

    ```yaml
    slices:
      config:
        contents:
          /etc/vim/vimrc.tiny:
    ```

    1. [ ] **Are there any other files of the same type?**

        The {ref}`conffiles <create_sdf_inspect_pkg_conffiles>` may not list
        everything that can be considered as a configuration file. These can
        sometimes be different from regular files, live outside `/etc/`, be
        created by a maintainer script, etc.
        So, based on the {ref}`package files <create_sdf_inspect_pkg_files>`,
        you should also identify any other config files.

12. [ ] **Write the `bins` slice**

    `/usr/bin/vim.tiny` is this slice's only content. We know it will need the
    internal slices [`vim-tiny_config`](#create_sdf_design_slices_config_slice). But given the
    {ref}`above package dependency inspection <create_sdf_inspect_pkg_deps>`,
    we should confirm whether this binary also needs all of those package
    dependencies, or just a subset.

    Let's closely look at the `/usr/bin/vim.tiny` file. Let's use the `file` command to determine the type.

    ```{terminal}
    file /usr/bin/vim.tiny

    /usr/bin/vim.tiny: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=244c06f7943459e771bbf3279ef507ad64f477b5, for GNU/Linux 3.2.0, stripped
    ```

    Since this is a dynamically linked ELF binary, let's use a tool (like `ldd`,
    `strings`, `objdump`, `readelf`, etc.) to analyze it and figure out what
    libraries it depends on.

    ```{terminal}
    ldd /usr/bin/vim.tiny

          linux-vdso.so.1 (0x00007ffcdfecd000)
          libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x0000744edc6ac000)
          libtinfo.so.6 => /lib/x86_64-linux-gnu/libtinfo.so.6 (0x0000744edc678000)
          libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1 (0x0000744edc64b000)
          libacl.so.1 => /lib/x86_64-linux-gnu/libacl.so.1 (0x0000744edc641000)
          libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x0000744edc42f000)
          /lib64/ld-linux-x86-64.so.2 (0x0000744edc948000)
          libpcre2-8.so.0 => /lib/x86_64-linux-gnu/libpcre2-8.so.0 (0x0000744edc393000)
    ```

    ```{note}
    Note that some times, libraries may be used on a "per need basis" (e.g. only
    when a certain feature is enabled) and thus may not show up when doing a
    basic inspection of your binary.
    ```

    Now, what packages own these objects? Using `dpkg -S`, we can find out:
     - `libc6`
     - `libtinfo6`
     - `libselinux1`
     - `libacl1`
     - `libpcre2-8-0`

    Note that `libpcre2-8-0` is not listed as a dependency of `vim-tiny`, but if
    we recursively check `vim-tiny`'s dependencies
    (via `apt-rdepends vim-tiny`), we can see that it is a dependency of
    `libselinux1`, which is an original dependency of `vim-tiny`.

    So it matches with what we expected in the {ref}`initial dependency analysis
    <create_sdf_inspect_pkg_deps>`.

    By running `chisel info --release ubuntu-24.04 libc6 libtinfo6 libselinux1
    libacl1 vim-common` we can
    confirm that all the `vim-tiny`'s package dependencies are already sliced.
    So the final `bins` slice will look like this:

    ```yaml
    slices:
      bins:
        essential:
          - libacl1_libs
          - libc6_libs
          - libselinux1_libs
          - libtinfo6_libs
          - vim-common_addons
          - vim-common_config
          - vim-tiny_config
        contents:
          /usr/bin/vim.tiny:
    ```

    ```{tip}
    Sometimes, a package (and thus its slices) may have "essential"
    dependencies that are not explicitly listed in the package's
    [`control` file].
    E.g. OpenSSL's `c_rehash` requires Perl to run, but the OpenSSL package
    does not mention it. The same happens frequently for Bash scripts that may
    assume certain packages (like `coreutils`) are installed.
    ```

13. [ ] **Format your slice definitions files**

      Every slice definition file will be checked with linters.

      1. [ ] **Required: sort all slices' contents**

          The slice `contents` entries (i.e. the paths) must be sorted in
          lexicographical order.

      2. [ ] **Recommended: consistent YAML placement**

          Keep the top-level `essential` at the top, and the `copyright` slice at the bottom.

14. [ ] **Review your slice definitions**

    Assemble your slice definitions file, and review it. Make sure you have
    included all the necessary slices, contents, dependencies and mutation
    scripts, and that you have followed the best practices:

     - [ ] keep the slice names meaningful and consistent with existing slices
     - [ ] ensure slices are functional by themselves, or as a dependency of
       other slices
     - [ ] be cautious with broad globs. A good glob simplifies the writing of a
     slice while keeping the resulting paths specific to the package. See
     {ref}`create_sdf_examples`.

    The complete `slices/vim-tiny.yaml` file should look something like this:

    ```yaml
    package: vim-tiny

    essential:
      - vim-tiny_copyright

    slices:
      bins:
        essential:
          - libacl1_libs
          - libc6_libs
          - libselinux1_libs
          - libtinfo6_libs
          - vim-common_addons
          - vim-common_config
          - vim-tiny_config
        contents:
          /usr/bin/vim.tiny:

      config:
        contents:
          /etc/vim/vimrc.tiny:

      copyright:
        contents:
          /usr/share/doc/vim-tiny/copyright:
    ```

    ```{important}
    If any of your slices' paths are architecture-specific, you must add the
    `arch` field. For
    [example](https://github.com/canonical/chisel-releases/blob/e5db53e97e03c46944a84e7ab5abeb1b7cb53cd9/slices/libc6.yaml#L29):

    >  `/usr/lib/*-linux-*/libmvec.so.*: {arch: [amd64, arm64]}`
    ```

15. [ ] **Repeat for nonexistent package slices**

    If any of the dependencies are not sliced yet, repeat the above design
    process for them too.

(create_sdf_test)=

## Test the slices

A slice definition is only complete when it has been tested.

As a manual test, you can just install your slices into an empty folder, and test your application with `chroot`.

But for upstream contributions, you must also add integration tests in the form
of [Spread tasks](https://github.com/canonical/spread).

```{important}
**All slices that deliver *"functionality"*** must be tested!

While it might be redundant to test that a specific path has been properly
installed by Chisel, it is **paramount** to test slices that should offer a
specific function. Examples:
 - if you define a [`coreutils` slice that contains only printing functionality](https://github.com/canonical/chisel-releases/blob/63b2311e16308bb1380af32a5a64ff924a493248/slices/coreutils.yaml#L225),
 you must test that when you `cut` that slice alone, its contents
 will be functional;
 - if you slice all the [`python3` modules by function](https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/libpython3.12-stdlib.yaml),
 then you must ensure that each group of modules is functional by itself,
 without other undeclared dependencies.
```

16. [ ] **Install the `vim-tiny_bins` locally**

    Create a new rootfs directory, and pointing Chisel to your "chisel-releases"
    clone, cut your packages locally.

    ```bash
    mkdir rootfs/
    # Cut the vim-tiny package, to get the vim.tiny binary only
    chisel cut --release ./ --root rootfs/ vim-tiny_bins
    ```

    Test the `bins` binary:

    ```{terminal}
    sudo chroot rootfs/ vim.tiny --version

    VIM - Vi IMproved 9.1 (2024 Jan 02, compiled Apr 01 2025 15:29:41)
    Included patches: 1-16, 647-648, 678, 697, 689, 17-496, 707
    Modified by <team+vim@tracker.debian.org>
    Compiled by <team+vim@tracker.debian.org>
    Tiny version without GUI.  Features included (+) or not (-):
    ...
    ```

17. [ ] **Create the Spread test**

    In your clone of the {{chisel_releases_repo}}, create the new folder
    `tests/spread/integration/vim-tiny`.

    1. [ ] **Create the `task.yaml` file**

        Create a file named `tests/spread/integration/vim-tiny/task.yaml` and
        write your test in the format of a [Spread task](https://github.com/canonical/spread).

        <details>
        <summary>Example: Spread test for vim-tiny</summary>

        ```yaml
        summary: Integration tests for vim-tiny

        execute: |
          rootfs="$(install-slices vim-tiny_bins)"
          chroot "${rootfs}/" vim.tiny --version
          echo "hello world" > "$rootfs/test"
          chroot "$rootfs" vim.tiny -c ":s/hello/bye/" -c ":wq" test
          test "$(cat "$rootfs/test")" = "bye world"
        ```

        </details>

    2. [ ] **Run your Spread test**

        Run the test with `spread`:

        ```{terminal}
        spread lxd:tests/spread/integration/vim-tiny

        ...
        2025-04-14 18:29:40 Preparing lxd:ubuntu-noble:tests/spread/integration/vim-tiny (lxd:ubuntu-noble)...
        2025-04-14 18:29:40 Executing lxd:ubuntu-noble:tests/spread/integration/vim-tiny (lxd:ubuntu-noble) (1/1)...
        2025-04-14 18:29:50 Discarding lxd:ubuntu-noble...
        2025-04-14 18:29:52 Successful tasks: 1
        2025-04-14 18:29:52 Aborted tasks: 0
        ```

19. [ ] **Contribute!**

    New slice definitions are welcome! Please contribute your new slices to the
    {{chisel_releases_repo}}. See the [contributing guide](https://github.com/canonical/chisel-releases/blob/main/CONTRIBUTING.md).

    If proposing changes to multiple slice definitions files, only group them
    into the same PR if they are related to the same scope (e.g. *you're slicing
    an application and all its dependencies, in the same PR*).

    ```{important}
    Reminder: all PRs must be forward ported! E.g. if opening a PR against
    `ubuntu-24.04`, you must also forward port it to `ubuntu-24.10`, `ubuntu-25.04`, and so on, for all supported releases at the time of opening the PR.
    ```

(create_sdf_examples)=

## Example: good vs bad slice definitions

`````{tab-set}
````{tab-item} Good
:class-label: sd-text-info

```yaml
package: libpython3.12-stdlib

essential:
  - libpython3.12-stdlib_copyright

slices:
  # File Formats
  # https://docs.python.org/3.12/library/fileformats.html
  file-formats:
    essential:
      - libpython3.12-stdlib_core
      - libpython3.12-stdlib_frameworks
      - libpython3.12-stdlib_markup-tools
    contents:
      /usr/lib/python3.12/netrc.py:
      /usr/lib/python3.12/plistlib.py:
      /usr/lib/python3.12/tomllib/**:
      /usr/lib/python3.12/xdrlib.py:

  ...
```

````

````{tab-item} Bad
:class-label: sd-text-danger

```yaml
package: libpython3.12-stdlib

# Missing a global "essential" dependency on the "copyright" slice, thus
# forcing it to be an "essential" in every slice below, making the file
# less readable and more prone to missing that dependency.

slices:
  # Controversial grouping by type. Makes more sense to group Python by function.
  modules:
    # Possibly missing the dependencies on ".so" files and other contents.

    # No sorting of contents
    contents:
      # No need to define this symlink. It is already defined in the deb
      /usr/share/doc/libpython3.12-stdlib: {symlink: /usr/share/doc/libpython3.12-minimal}

      # Chose to group by type, but still mixing types within the same slice
      /usr/lib/python3.12/netrc.py:
      /usr/lib/python3.12/pydoc_data/_pydoc.css:

      # Bad glob, possibly conflicting with other python packages
      /usr/lib/python3.*/tomllib/**:

  ...
```
````

`````

<!-- LINKS -->

[Ubuntu Packages Search]: https://packages.ubuntu.com/noble/vim-tiny
[`vim-tiny` package contents in the Ubuntu Packages Search]: https://packages.ubuntu.com/noble/amd64/vim-tiny/filelist
[`conffiles`]: https://www.debian.org/doc/debian-policy/ap-pkg-conffiles.html
[maintainer scripts]: https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html
[chisel-releases]: https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/
[`control` file]: https://www.debian.org/doc/debian-policy/ch-controlfields.html
