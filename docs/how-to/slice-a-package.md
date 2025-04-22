# Slice a package

This guide provides instructions on the slicing of an Ubuntu package for
Chisel.

A package slice is represented via a
{ref}`Slice Definitions File<slice_definitions_ref>` (aka SDF), and the creation
of said slice definitions is a result of the **inspection** and **design
process** depicted below.

As an example, this guide will focus on **slicing the `openssl` package from
Ubuntu 24.10**.

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

    You can run `apt depends openssl` or use the [Ubuntu Packages Search] website.

3. [ ] [**Inspect the files the package provides**]{#create_sdf_inspect_pkg_files}

    You can run `apt download openssl` and then `dpkg -c openssl*.deb` to check
    the package data contents. Or check the [`openssl` package contents in the
    Ubuntu Packages Search] website.

    ````{note}
    A package contents and dependencies may change depending on the
    architecture. Make sure to double check any differences and adjust your slices
    accordingly.
    ````

    <details>

    <summary>Snippet of the OpenSSL's contents in Ubuntu 24.10, for amd64</summary>

    ```{terminal}
    :input: dpkg -c openssl_3.3.1-2ubuntu2.1_amd64.deb

    drwxr-xr-x root/root         0 2025-02-05 12:56 ./
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./etc/
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./etc/ssl/
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./etc/ssl/certs/
    -rw-r--r-- root/root     12434 2025-02-05 12:56 ./etc/ssl/openssl.cnf
    drwx------ root/root         0 2025-02-05 12:56 ./etc/ssl/private/
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./usr/
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./usr/bin/
    -rwxr-xr-x root/root      6835 2025-02-05 12:56 ./usr/bin/c_rehash
    -rwxr-xr-x root/root   1075296 2025-02-05 12:56 ./usr/bin/openssl
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./usr/lib/
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./usr/lib/ssl/
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./usr/lib/ssl/misc/
    -rwxr-xr-x root/root      8063 2025-02-05 12:56 ./usr/lib/ssl/misc/CA.pl
    -rwxr-xr-x root/root      6742 2025-02-05 12:56 ./usr/lib/ssl/misc/tsget.pl
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./usr/share/
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./usr/share/doc/
    drwxr-xr-x root/root         0 2025-02-05 12:56 ./usr/share/doc/openssl/
    ...
    ...
    lrwxrwxrwx root/root         0 2025-02-05 12:56 ./usr/lib/ssl/cert.pem -> /etc/ssl/certs/ca-certificates.crt
    lrwxrwxrwx root/root         0 2025-02-05 12:56 ./usr/lib/ssl/certs -> /etc/ssl/certs
    lrwxrwxrwx root/root         0 2025-02-05 12:56 ./usr/lib/ssl/misc/tsget -> tsget.pl
    lrwxrwxrwx root/root         0 2025-02-05 12:56 ./usr/lib/ssl/openssl.cnf -> /etc/ssl/openssl.cnf
    lrwxrwxrwx root/root         0 2025-02-05 12:56 ./usr/lib/ssl/private -> /etc/ssl/private
    lrwxrwxrwx root/root         0 2025-02-05 12:56 ./usr/share/doc/openssl/changelog.Debian.gz -> ../libssl3t64/changelog.Debian.gz
    lrwxrwxrwx root/root         0 2025-02-05 12:56 ./usr/share/doc/openssl/copyright -> ../libssl3t64/copyright
    ...
    ...
    ```

    For `openssl`, we see that there are a few binaries at `/usr/bin/`, a few
    configuration files, the copyright files, manpages and so on.
    </details>

4. [ ] [**Inspect the package metadata**]{#create_sdf_inspect_pkg_control}

    The package metadata files include:
    - the [`control` file] (which you can use
    to double-check the package dependencies you got from above),
    - [maintainer scripts], and
    - [`conffiles`] file.

    Run `dpkg -e openss*.deb` to extract the metadata files into a new
    `DEBIAN/` directory for inspection.

   1. [ ] [**Inspect package [`conffiles`] file**]{#create_sdf_inspect_pkg_conffiles}

      This file lists the configuration files a package provides. This can be
      useful later, when deciding whether to create a `config` slice or not.

      <details>

      <summary>Snippet of the OpenSSL's conffiles</summary>

      ```{terminal}
      :input: cat DEBIAN/conffiles
      /etc/ssl/openssl.cnf
      ```

      </details>

   2. [ ] [**Inspect package [maintainer scripts]**]{#create_sdf_inspect_pkg_maintainer_scripts}

      Since Chisel doesn't remove files, we can focus on only the `preinst` and
      `postinst` scripts. Whatever these scripts do, you should aim to reproduce
      when defining the slices. In Chisel, such scripts are called "mutation
      scripts", and are written in
      [Starlark](https://github.com/canonical/starlark/).

      ```{note}

      <details>

      <summary>Analysing OpenSSL's maintainer scripts</summary>

      From the `postinst` script, we see:

      ```sh

      # !/bin/sh -e

      if [ ! -e /usr/lib/ssl ]
      then
        echo Linking /usr/lib/ssl to /etc/ssl
        ln -sf /etc/ssl /usr/lib/ssl
      fi

      ```

      The `openssl` maintainer scripts create a new symlink, so should its
      slices then.

      </details>

5. [ ] **Repeat the above for all dependencies**

    Slices must also exist for every other package that `openssl` depends on. So
    if these dependencies aren't yet sliced upstream in [chisel-releases], you
    must do the same inspection for them, and create their slices too.

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
  functionality. For example, the [`python3` slice definitions file](https://github.com/canonical/chisel-releases/blob/ubuntu-24.10/slices/python3.yaml)
  has a `core` slice providing a very minimal `python3` runtime, but also a
  `standard` slice with the additional libraries on top of `core`.
    ```{tip}
    In this case, the most common is to create:
    - a `core` slice which contains the very minimal, core set of files
      supporting a minimal yet functional operation of the application,
    - a `standard` slice which contains a standard set of files supporting the
      full operation of the application,
    - and other slices which are scoped and named after the functionality they
      provide (e.g. see the [`libpython3.12-stdlib` slices](https://github.com/canonical/chisel-releases/blob/ubuntu-24.10/slices/libpython3.12-stdlib.yaml)).
    ```
```

```{important}
**Every slice** must install the package's copyright file(s).

It is therefore recommended to create a `copyright` slice for every package, that
other slices can depend on.
```

6. [ ] **Choose the design approach that aligns best with your package**

    Given the {ref}`above package inspection <create_sdf_inspect_pkg>`, the
    `openssl` package can be sliced by *type of content*:
     - a `bins` slice for the `/usr/bin/openssl` binary,
       - note that although `c_rehash` is also under `/usr/bin/`, it is
       actually a Perl script,
     - a `config` slice for the {ref}`configuration files <create_sdf_inspect_pkg_conffiles>`,
     - a `data` slice for the package's certificates files, and
     - a `copyright` slice for the copyright file.

7. [ ] **Prepare to write the slice definitions**

    ```{note}
    There is one Slice Definitions File per package!
    ```

    Slice definitions live in the `slices/` directory of the
    {{chisel_releases_repo}}. Fork and clone this repo, creating a new
    branch for the packages you are slicing.

8. [ ] **Create the YAML Slice Definitions File**

   Create a new file in the `slices/` directory, named after the package you
   are slicing. For example, `openssl.yaml`.

   <details>
   <summary>Snippet of the slices/openssl.yaml file</summary>

   ```yaml
   package: openssl
   slices:
   ```

9. [ ] **Specify `package` name**

   The first thing to do is to write the package name in the
   {ref}`slice_definitions_format_package` field. For example, open
   `slices/openssl.yaml` and write:

   ```yaml
   package: openssl
   ```

10. [ ] **Write the `copyright` slice**

    Write the copyright slice first and pin it as an {ref}`essential for every
    other package slice <slice_definitions_format_essential>`.

    ```yaml
    essential:
      - openssl_copyright

    slices:
      copyright:
        contents:
          # This path is taken from the package contents inspected above.
          /usr/share/doc/openssl/copyright:
          # Notice that this path is in fact a symlink to a copyright file in
          # the libssl3t64 package (which is a dependency of openssl).
          # So we need to add that package's copyright slice as a dependency.
        essential:
          - libssl3t64_copyright
    ```

    ```{tip}
    Although we are writing the copyright slice first, we typically list the
    slice at the bottom of the slice definition file.
    ```

    ```{important}
    Although the above copyright file is a symlink, we **don't need to
    explicitly create it** (using the
    {ref}`slice_definitions_format_slices_contents_symlink` directive) because
    the link is defined in the deb, and Chisel will respect that link during
    the extraction.
    ```

11. [ ] [**Write the `config` slice**]{#create_sdf_design_slices_config_slice}

    Now write the `config` slice, based on the list from the
    {ref}`conffiles <create_sdf_inspect_pkg_conffiles>`.

    ```yaml
    slices:
      config:
        contents:
          /etc/ssl/openssl.cnf:
          /usr/lib/ssl/openssl.cnf:
    ```

    1. [ ] **Are there any other files of the same type?**

        The {ref}`conffiles <create_sdf_inspect_pkg_conffiles>` may not list
        everything that can be considered as a configuration file. These can
        sometimes be different from regular files, live outside `/etc/`, be
        created by a maintainer script, etc.
        So, based on the {ref}`package files <create_sdf_inspect_pkg_files>`,
        you should also identify any other config files.

12. [ ] [**Write the `data` slice**]{#create_sdf_design_slices_data_slice}

    From the {ref}`package files <create_sdf_inspect_pkg_files>`, identify
    anything that can be considered as application data.

    For the OpenSSL package, notice the `/etc/ssl/certs/` and
    `/etc/ssl/private/` directories among its files. These are locations where
    certificates are supposed to be stored. There is also a symbolic link from
    `/usr/lib/ssl/cert.pem` to `/etc/ssl/certs/ca-certificates.crt` that we
    need to include in this slice.

    The `postinst` maintainer script also creates a symlink from
    `/usr/lib/ssl` to `/etc/ssl` if `/usr/lib/ssl` does not exist, in this slice
    `/usr/lib/ssl` **does exist** and we can safely ignore that script.

    ```yaml
    slices:
      data:
        contents:
          /etc/ssl/certs/:
          /etc/ssl/private/:

          # NOTE: this is a symlink to /etc/ssl/certs/ca-certificates.crt.
          # OpenSSL doesn't depend on ca-certificates, but the opposite is true.
          # So ca-certificates may depend on this slice.
          /usr/lib/ssl/cert.pem:
          /usr/lib/ssl/certs:
          /usr/lib/ssl/private:
    ```

13. [ ] **Write the `bins` slice**

    This is a {ref}`function-specific slice <create_sdf_design_slices>`. In
    this case, it will contain just the `/usr/bin/openssl` binary, so we can
    name it after that.

    `/usr/bin/openssl` is this slice's only content. We know it will need the
    internal slices [`openssl_config`](#create_sdf_design_slices_data_slice)
    and [`openssl_data`](#create_sdf_design_slices_config_slice). But given the
    {ref}`above package dependency inspection <create_sdf_inspect_pkg_deps>`,
    we should confirm whether this binary also needs all of those package
    dependencies, or just a subset.

    Let's closely look at the `/usr/bin/openssl` file. Let's use the `file` command to determine the type.

    ```{terminal}
    :input: file /usr/bin/openssl

    /usr/bin/openssl: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=035bc52088d56b575b788c42a7be4fa44f76e6fd, for GNU/Linux 3.2.0, stripped
    ```

    Since this is a dynamically linked ELF binary, let's use a tool (like `ldd`,
    `strings`, `objdump`, `readelf`, etc.) to analyze it and figure out what
    libraries it depends on.

    ```{terminal}
    :input: ldd /usr/bin/openssl
          linux-vdso.so.1 (0x00007ffc1bb1f000)
          libssl.so.3 => /lib/x86_64-linux-gnu/libssl.so.3 (0x000078310b075000)
          libcrypto.so.3 => /lib/x86_64-linux-gnu/libcrypto.so.3 (0x000078310ab19000)
          libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x000078310a907000)
          libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x000078310a8eb000)
          libzstd.so.1 => /lib/x86_64-linux-gnu/libzstd.so.1 (0x000078310a82d000)
          /lib64/ld-linux-x86-64.so.2 (0x000078310b286000)
    ```

    ```{note}
    Note that some times, libraries may be used on a "per need basis" (e.g. only
    when a certain feature is enabled) and thus may not show up when doing a
    basic inspection of your binary.
    ```

    Now, what packages own these objects? Using `dpkg -S`, we can find out:
     - `libc6`
     - `libssl3t64`

    and two additional packages, that are in fact dependencies of `libssl3t64`:
     - `libzstd1`
     - `zlib1g`

    So it matches with what we expected in the {ref}`initial dependency analysis
    <create_sdf_inspect_pkg_deps>`.

    By running `chisel info --release ubuntu-24.10 libc6 libssl3t64` we can
    confirm that these two OpenSSL's package dependencies are already sliced.
    So the final `bins` slice will look like this:

    ```yaml
    slices:
      bins:
        essential:
          - libc6_libs
          - libssl3t64_libs
          - openssl_config
          - openssl_data
        contents:
          /usr/bin/openssl:
    ```

    ```{tip}
    Sometimes, a package (and thus its slices) may have "essential"
    dependencies that are not explicitly listed in the package's
    [`control` file].
    E.g. OpenSSL's `c_rehash` requires Perl to run, but the OpenSSL package
    does not mention it. The same happens frequently for Bash scripts that may
    assume certain packages (like `coreutils`) are installed.
    ```

14. [ ] **Format your slice definitions files**

      Every slice definition file will be checked with linters.

      1. [ ] **Required: sort all slices' contents**

          The slice `contents` entries (i.e. the paths) must be sorted in
          lexicographical order.

      2. [ ] **Recommended: consistent YAML placement**

          Keep the top-level `essential` at the top, and the `copyright` slice at the bottom.

15. [ ] **Review your slice definitions**

    Assemble your slice definitions file, and review it. Make sure you have
    included all the necessary slices, contents, dependencies and mutation
    scripts, and that you have followed the best practices:

     - [ ] keep the slice names meaningful and consistent with existing slices
     - [ ] ensure slices are functional by themselves, or as a dependency of
       other slices
     - [ ] be cautious with broad globs. A good glob simplifies the writing of a
     slice while keeping the resulting paths specific to the package. See
     {ref}`create_sdf_examples`.

    <details>
    <summary>The complete slices/openssl.yaml file</summary>

    ```yaml
    package: openssl

    slices:
      bins:
        essential:
          - libc6_libs
          - libssl3t64_libs
          - openssl_config
          - openssl_data
        contents:
          /usr/bin/openssl:

      config:
        contents:
          /etc/ssl/openssl.cnf:
          /usr/lib/ssl/openssl.cnf:

      data:
        contents:
          /etc/ssl/certs/:
          /etc/ssl/private/:
          /usr/lib/ssl/cert.pem:
          /usr/lib/ssl/certs:
          /usr/lib/ssl/private:

      copyright:
        contents:
          /usr/share/doc/openssl/copyright:
    ```

    </details>

    ```{important}
    If any of your slices' paths are architecture-specific, you must add the
    `arch` field. For
    [example](https://github.com/canonical/chisel-releases/blob/e5db53e97e03c46944a84e7ab5abeb1b7cb53cd9/slices/libc6.yaml#L29):

    >  `/usr/lib/*-linux-*/libmvec.so.*: {arch: [amd64, arm64]}`
    ```

16. [ ] **Repeat for nonexistent package slices**

    If any of the dependencies are not sliced yet, repeat the above design
    process for them too.

(create_sdf_test)=

## Test the slices

A slice definition is only complete when it has been tested.

As a manual test, you can just install your slices into an empty folder, and test your application with `chroot`.

But for upstream contributions, you must also add integration tests in the form
of [Spread tasks](https://github.com/canonical/spread).

17. [ ] **Install the `openssl_bins` locally**

    Create a new rootfs directory, and pointing Chisel to your "chisel-releases"
    clone, cut your packages locally.

    ```bash
    mkdir rootfs/
    # Cut the openssl package, to get the openssl binary only
    chisel cut --release ./ --root rootfs/ openssl_bins
    ```

    Test the `bins` binary:

    ```{terminal}
    :input: sudo chroot rootfs/ openssl passwd foo
    $1$UNOQEnmV$tX3Bbxnrix6fjTtEA2ZvZ1
    ```

18. [ ] **Create the Spread test**

    In your clone of the {{chisel_releases_repo}}, create the new folder
    `tests/spread/integration/openssl`.

    1. [ ] **Create the `task.yaml` file**

        Create a file named `tests/spread/integration/openssl/task.yaml` and
        write your test in the format of a [Spread task](https://github.com/canonical/spread).

        <details>
        <summary>Example of a Spread test for OpenSSL</summary>

        ```yaml
        summary: Integration tests for openssl

        execute: |
          rootfs="$(install-slices openssl_bins)"
 
          chroot "$rootfs" openssl --help
 
          test_sha1="4e1243bd22c66e76c2ba9eddc1f91394e57f9f83"
          chroot "$rootfs" openssl sha1 <<< "test" | grep $test_sha1
        ```

        </details>

    2. [ ] **Run your Spread test**

        Run the test with `spread`:

        ```{terminal}
        :input: spread lxd:tests/spread/integration/openssl

        ...
        2025-04-14 18:29:40 Preparing lxd:ubuntu-oracular:tests/spread/integration/openssl (lxd:ubuntu-oracular)...
        2025-04-14 18:29:40 Executing lxd:ubuntu-oracular:tests/spread/integration/openssl (lxd:ubuntu-oracular) (1/1)...
        2025-04-14 18:29:50 Discarding lxd:ubuntu-oracular...
        2025-04-14 18:29:52 Successful tasks: 1
        2025-04-14 18:29:52 Aborted tasks: 0
        ```

19. [ ] **Contribute!**

    New slice definitions are welcome! Please contribute your new slices to the
    {{chisel_releases_repo}}. See the [contributing guide](https://github.com/canonical/chisel-releases/blob/main/CONTRIBUTING.md).

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
      /usr/lib/python3.12/pydoc_data/_pydoc.css

      # Bad glob, possibly conflicting with other python packages
      /usr/lib/python3.*/tomllib/**:

  ...
```
```
````
`````

<!-- LINKS -->

[Ubuntu Packages Search]: https://packages.ubuntu.com/oracular/openssl
[`openssl` package contents in the Ubuntu Packages Search]: https://packages.ubuntu.com/oracular/amd64/openssl/filelist
[`conffiles`]: https://www.debian.org/doc/debian-policy/ap-pkg-conffiles.html
[maintainer scripts]: https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html
[chisel-releases]: https://github.com/canonical/chisel-releases/blob/ubuntu-24.10/
[`control` file]: https://www.debian.org/doc/debian-policy/ch-controlfields.html
