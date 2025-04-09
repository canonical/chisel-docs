# Create a slice definition

This guide shows how to create a slice definition and notes the best practices
of doing it.

In this guide, we will create slices for the `openssl` package for the
`ubuntu-24.04` release. Note that while this package does have slices in the
`ubuntu-24.04` release in the {{chisel_releases_repo}}, we will pretend that
it has not been sliced yet.


(create_sdf_pre_req)=

## Pre-requisites

- An Ubuntu machine with `apt`, `dpkg` and `coreutils` packages installed.
- Text editor.


(create_sdf_inspect_pkg)=

## Inspect the package

When writing slice definitions for a package, it is very important to inspect
the package. This helps get a better understanding of which file(s) you need
from the package, the dependencies those files have on other packages and so on.

A Debian package, or a `.deb` file contains few different types of files when
extracted. It has metadata files such as the [`control` file] and [maintainer
scripts] along with the data tarball i.e. the package content. When slicing, we
should take a look at all of these files.


(create_sdf_inspect_pkg_content)=

### Inspect package content

The package data files are the ones who primarily dictate what a particular
slice should contain. To inspect the files a package provides, there are two
popular ways:

1. View the package contents at packages.ubuntu.com.
2. Download the package with `apt` and inspect it locally.

So, to inspect what `openssl` contains, we can take a look
[here](https://packages.ubuntu.com/noble/openssl). Or, we can download the
package with the following command:

```
apt download openssl
```

````{tip}
This command will download the package for the host architecture. To download
the package for another architecture, simply append the package name with the
architecture with colon(:) in between, e.g:

```
apt download openssl:i386
```
````

To view the package data, you can use the following command:

```text
dpkg -c /path/to/package.deb
```

<details>

<summary>Toggle to see the contents of openssl</summary>

```{terminal}
:input: dpkg -c openssl_3.0.13-0ubuntu3.5_amd64.deb

drwxr-xr-x root/root         0 2025-02-05 13:17 ./
drwxr-xr-x root/root         0 2025-02-05 13:17 ./etc/
drwxr-xr-x root/root         0 2025-02-05 13:17 ./etc/ssl/
drwxr-xr-x root/root         0 2025-02-05 13:17 ./etc/ssl/certs/
-rw-r--r-- root/root     12324 2025-02-05 13:17 ./etc/ssl/openssl.cnf
drwx------ root/root         0 2025-02-05 13:17 ./etc/ssl/private/
drwxr-xr-x root/root         0 2025-02-05 13:17 ./usr/
drwxr-xr-x root/root         0 2025-02-05 13:17 ./usr/bin/
-rwxr-xr-x root/root      6841 2025-02-05 13:17 ./usr/bin/c_rehash
-rwxr-xr-x root/root   1005368 2025-02-05 13:17 ./usr/bin/openssl
drwxr-xr-x root/root         0 2025-02-05 13:17 ./usr/lib/
drwxr-xr-x root/root         0 2025-02-05 13:17 ./usr/lib/ssl/
drwxr-xr-x root/root         0 2025-02-05 13:17 ./usr/lib/ssl/misc/
-rwxr-xr-x root/root      8061 2025-02-05 13:17 ./usr/lib/ssl/misc/CA.pl
-rwxr-xr-x root/root      6743 2025-02-05 13:17 ./usr/lib/ssl/misc/tsget.pl
drwxr-xr-x root/root         0 2025-02-05 13:17 ./usr/share/
drwxr-xr-x root/root         0 2025-02-05 13:17 ./usr/share/doc/
drwxr-xr-x root/root         0 2025-02-05 13:17 ./usr/share/doc/openssl/
...
...
lrwxrwxrwx root/root         0 2025-02-05 13:17 ./usr/lib/ssl/cert.pem -> /etc/ssl/certs/ca-certificates.crt
lrwxrwxrwx root/root         0 2025-02-05 13:17 ./usr/lib/ssl/certs -> /etc/ssl/certs
lrwxrwxrwx root/root         0 2025-02-05 13:17 ./usr/lib/ssl/misc/tsget -> tsget.pl
lrwxrwxrwx root/root         0 2025-02-05 13:17 ./usr/lib/ssl/openssl.cnf -> /etc/ssl/openssl.cnf
lrwxrwxrwx root/root         0 2025-02-05 13:17 ./usr/lib/ssl/private -> /etc/ssl/private
lrwxrwxrwx root/root         0 2025-02-05 13:17 ./usr/share/doc/openssl/changelog.Debian.gz -> ../libssl3/changelog.Debian.gz
lrwxrwxrwx root/root         0 2025-02-05 13:17 ./usr/share/doc/openssl/changelog.gz -> ../libssl3/changelog.gz
lrwxrwxrwx root/root         0 2025-02-05 13:17 ./usr/share/doc/openssl/copyright -> ../libssl3/copyright
...
...
```

</details>

And to extract the contents to disk, we can run the following command:

```text
dpkg -x /path/to/package.deb /path/to/dir
```

For `openssl`, we see that there are a few binaries at `/usr/bin`, a few
configuration files, the copyright files, manpages and so on.

Before making up our mind about what we want to include in our slices, let's
also look at the package metadata files.


(create_sdf_inspect_pkg_metadata)=

### Inspect package metadata

The package metadata files include the [`control` file], [maintainer scripts],
and [`conffiles`] file.

To extract these files from the `.deb`, use the following command:

```text
dpkg -e /path/to/package.deb
```

The metadata files are extracted to a `DEBIAN/` directory. Here are the ones for
`openssl`:

```{terminal}
:input: ls DEBIAN/
conffiles  control  md5sums  postinst
```


(create_sdf_inspect_pkg_control)=

#### Inspect package `control` file

The `control` file contains general information about the package including it's
name, description and most importantly for us, dependencies. The `Pre-Depends`
and `Depends` fields of the `control` file indicate which packages a package
depends on. In slicing context, this indicates that the slices of a particular
package may depend on zero or more slices from those packages listed as
dependency.

For `openssl`, the dependency looks like this:

```{terminal}
:input: cat DEBIAN/control | grep Depends
Depends: libc6 (>= 2.34), libssl3t64 (>= 3.0.9)
```


(create_sdf_inspect_pkg_conffiles)=

#### Inspect package `conffiles`

If exists, the [`conffiles`] file lists the configuration files a package
provides. This information comes in handy to create a `config` slice, which
other slices of that package may require.

The `openssl` package lists one such file:

```{terminal}
:input: cat DEBIAN/conffiles
/etc/ssl/openssl.cnf
```


(create_sdf_inspect_pkg_maintainer_scripts)=

#### Inspect package maintainer scripts

A package may have any number of [maintainer scripts]. Primarily, packages may
have `preinst`, `postinst`, `prerm` and `postrm` scripts, each of which run at
different time of the package's installation and removal. Since Chisel never
removes files, we can focus on only the `preinst` and `postinst` scripts.

Our motive to check these scripts to find out what additional things the package
does upon installation. It may install additional files or directories, create
new links, modify existing files and so on. Based on the scripts, slices should
mimic the behavior if needed.

`openssl`'s `postinst` script creates a new symlink, which it's relevant
slice(s) should also do.

```sh
#!/bin/sh -e

if [ ! -e /usr/lib/ssl ]
then
  echo Linking /usr/lib/ssl to /etc/ssl
  ln -sf /etc/ssl /usr/lib/ssl
fi
```


(create_sdf_design_slices)=

## Design the slices

Let's first design the slices, before writing them. There are a few
considerations to be made, such as figuring out what slices we need and the
contents of those slices.


(create_sdf_design_slices_structure)=

### Slice structure

There are two schools of thoughts when creating slices.

1. Group similar files in the same slice. This means, putting all the binaries
   together in a `bins` slice, all the libraries together in a `libs` slice and
   so on. For small to medium packages which does not contain a lot of files and
   for library packages (e.g. `libfoo`), this is _usually_ the preferred
   way.

   One such example is the [`dpkg` slice definition file] where we have the
   `bins`, `locales`, `config` etc slices grouped based on the type of files.

   ```{tip}
   When creating slices in this way, the best practice is to create:

   - a `bins` slice which contains all the binaries.
   - a `libs` slice which contains all the libraries.
   - a `config` slice which contains all configuration files.
   - a `scripts` slice which contains ASCII executable scripts, e.g. Python,
     Perl scripts.

   There may be multiple slices which contains a portion of the binaries (or
   libraries etc). But the `bins` slice (or `libs` etc) should contain all the
   binaries (or libraries etc).
   ```

2. Create size-specific slices where one slice may provide only the core files,
   where another may provide additional files. This approach may come in handy
   for larger packages.

   An example is the [`python3` slice definition file] where the `core` slice
   provides a very minimal `python3` runtime which can run simple commands like
   `print('hello')` and the `standard` slice comes with additional libraries on
   top of the `core` slice. Another example, albeit an extreme one, is the
   [`libpython3.12-stdlib` slice definition file].

   ```{tip}
   When creating slices in this way, the best practice is to create:

   - a `core` slice which contains the very minimal, core set of files
     supporting a minimal yet fundamental operation of the application.
   - a `standard` slice which contains a standard set of files supporting the
     full operation of the application.
   ```

In practice, there have been cases where we have combined both approaches
together as well. It's important to remember that there are no solid rules on
how to create slices, only guidelines.

For `openssl`, after inspecting it's files, it seems more useful to create
slices in the first approach - grouping similar files in the same slice. We
should create:

- a `bins` slice which contains all the binaries.
- a `config` slice for the configuration files.
- a `data` slice for any certificates found in the package.
- a `copyright` slice for the copyright file. Every slice should include this
  one.

Users should install the `openssl_bins` slice and that should install a fully
functioning `openssl` application.


(create_sdf_design_slices_contents_deps)=

### Slice contents and dependencies

The next step is to figure out which file(s) the slices contain. This can be
free-form and is largely dependent on the decisions taken in the last section.


(create_sdf_design_slices_contents_deps_bins)=

#### `bins` slice

In `openssl`, we see that there are two files at `/usr/bin`.

```text
/usr/bin/c_rehash
/usr/bin/openssl
```

But we may not need both these files. Upon closer inspection, the `c_rehash`
file is a Perl executable which scans all files in the directory and adds
symbolic links to their hash values. We do not need this file, for our use case.

We do, however, need the `openssl` binary to run commands. Thus, our `bins`
slice should only contain the `/usr/bin/openssl` file.


(create_sdf_design_slices_contents_deps_bins_deps)=

##### Dependencies

Now that the content is fixed, what are the dependencies of this slice?

Recall the dependencies of `openssl` from the
{ref}`create_sdf_inspect_pkg_control` section. Chances are that the dependencies
of this slice would be a subset of those packages' slices. This provides an idea
of which package slices to look for as dependencies.

Let's closely look at the `/usr/bin/openssl` file. Let's use the `file` command
to determine the type.

```{terminal}
:input: file ./usr/bin/openssl

./usr/bin/openssl: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=83533d9f7c45a684f21f0e24f8a81089484ff272, for GNU/Linux 3.2.0, stripped
```

Since this is a dynamically linked ELF binary, let's use the `ldd` tool to
figure out what libraries it depends on.

```{terminal}
:input: ldd ./usr/bin/openssl
        linux-vdso.so.1 (0x00007ffec45f7000)
        libssl.so.3 => /lib/x86_64-linux-gnu/libssl.so.3 (0x000077e481958000)
        libcrypto.so.3 => /lib/x86_64-linux-gnu/libcrypto.so.3 (0x000077e481445000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x000077e481233000)
        /lib64/ld-linux-x86-64.so.2 (0x000077e481afd000)
```

```{tip}
We can also use the `strings`, `objdump` and `readelf` tools from the `binutils`
package for this type of files to get a better understanding of the
dependencies.
```

We can use the `dpkg -S` command to identify which packages these shared objects
belong to. Doing so points to the `libc6` and `libssl3t64` packages. Those
packages do have slices defined already and we can look at the slices using the
{{info_cmd}}.

```text
chisel info --release ubuntu-24.04 libc6 libssl3t64
```

We see that those shared object files are located at `libc6_libs` and
`libssl3t64_libs` slices. These two must be dependencies of the `bins` slice.

Additionally, the `data` and `config` files should also be included in the
`bins` slice as the binaries may use them. Thus, the
{ref}`create_sdf_design_slices_contents_deps_data` and
{ref}`create_sdf_design_slices_contents_deps_config` should also be listed in
{ref}`slice_definitions_format_slices_essential`.


(create_sdf_design_slices_contents_deps_config)=

#### `config` slice

From the {ref}`create_sdf_inspect_pkg_conffiles` section, we see that `openssl`
provides the `/etc/ssl/openssl.cnf` configuration file. Thus, this should be
part of the `config` slice.

Note also that there is a symbolic link from `/usr/lib/ssl/openssl.cnf` to
`/etc/ssl/openssl.cnf` file. Thus this file should also be part of the `config`
slice.

```text
./usr/lib/ssl/openssl.cnf -> /etc/ssl/openssl.cnf
```

This slice may not have any dependencies because it contains only configuration
files which other slices should make use of.


(create_sdf_design_slices_contents_deps_data)=

#### `data` slice

Notice the `/etc/ssl/certs` and `/etc/ssl/private` directories. These are
locations where certificates are supposed to be stored. Thus, these two
directories and symbolic links pointing to those should be part of the `data`
slice.

There is also a symbolic link from `/usr/lib/ssl/cert.pem` to
`/etc/ssl/certs/ca-certificates.crt` that we need to include in this slice.

```text
./usr/lib/ssl/cert.pem -> /etc/ssl/certs/ca-certificates.crt
```

Note that although the `postinst` maintainer script tries to create a symlink from
`/usr/lib/ssl` to `/etc/ssl` if `/usr/lib/ssl` does not exist, in this slice
`/usr/lib/ssl` does exist and we can safely ignore that script.


(create_sdf_design_slices_contents_deps_copyright)=

#### `copyright` slice

The copyright file should be part of this slice. And this slice should be listed
as an `essential` for all slices, using the top-level
{ref}`slice_definitions_format_essential` field.


(create_sdf_write_slices)=

## Write the slices

Finally, now that we have designed our slices well, let's move to writing.

Clone the {{chisel_releases_repo}}, switch to a new branch and create a file
`openssl.yaml` inside the `slices/` directory. If there is an existing
`slices/openssl.yaml` file, delete it and create the file for this guide.

```text
git clone https://github.com/canonical/chisel-releases.git
cd chisel-releases/
git checkout -b feat/openssl origin/ubuntu-24.04
touch slices/openssl.yaml
```


(create_sdf_write_slices_pkg)=

### Specify `package` name

The first thing to do is properly write the package name in the
{ref}`slice_definitions_format_package` field.

```yaml
package: openssl
```


(create_sdf_write_slices_copyright)=

### Write the `copyright` slice

It's a good idea to write the copyright slice first and pin it as an essential
for every slice.

```yaml
essential:
  - openssl_copyright

slices:
  copyright:
    contents:
      /usr/share/doc/openssl/copyright:
```

```{tip}
Although we are writing the copyright slice first, we typically list the slice
at the bottom of the slice definition file.
```


(create_sdf_write_slices_config)=

### Write the `config` slice

Let's now write the `config` slice based on the decision from the
{ref}`create_sdf_design_slices_contents_deps_config` section.

```yaml
slices:
  config:
    contents:
      /etc/ssl/openssl.cnf:
      /usr/lib/ssl/openssl.cnf:
```

```{important}
Although we can create symbolic links using the
{ref}`slice_definitions_format_slices_contents_symlink` directive, it's good
practice to extract the link directly from the package if it exists.
```


(create_sdf_write_slices_data)=

### Write the `data` slice

Based on the decision from {ref}`create_sdf_design_slices_contents_deps_data`,
let's now write the `data` slice.

```yaml
slices:
  data:
    contents:
      /etc/ssl/certs/:
      /etc/ssl/private/:
      /usr/lib/ssl/cert.pem:
      /usr/lib/ssl/certs:
      /usr/lib/ssl/private:
```

```{note}
When we specify a directory path, Chisel only installs that directory and
nothing else. To also install the files that may be within the directory, use
{ref}`wildcards<slice_definitions_format_slices_contents>`.
```

```{important}
The slice `contents` entries must be sorted in lexicographical order on the keys
i.e. file paths.
```


(create_sdf_write_slices_bins)=

### Write the `bins` slice

Let's now write the `bins` slice based on the analysis at the
{ref}`create_sdf_design_slices_contents_deps_bins` section.

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

```{important}
The slice `essential` entries must be sorted in lexicographical order.
```

(create_sdf_write_slices_complete_sdf)=

### The complete slice definition file

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


(create_sdf_test)=

## Test the slices

Let's now test the slices. Install `openssl_bins` in a root file system.

```
mkdir rootfs/
chisel cut --release ./ --root rootfs/ openssl_bins
```

See if the `openssl` binary prints help information.

```{terminal}
:input: sudo chroot rootfs/ openssl --help
help:

Standard commands
asn1parse         ca                ciphers           cmp
cms               crl               crl2pkcs7         dgst
dhparam           dsa               dsaparam          ec
...
```

Let's now generate a hashed password using `openssl`.

```{terminal}
:input: sudo chroot rootfs/ openssl passwd foo
$1$UNOQEnmV$tX3Bbxnrix6fjTtEA2ZvZ1
```

It works, congratulations!


(create_sdf_best_practices)=

## Best practices

In this section, we will review some best practices we should keep in our minds
when writing slices.


(create_sdf_best_practices_naming)=

### Slice naming and structure

In addition to the details in {ref}`create_sdf_design_slices_structure`, we
should keep the slice names short, but meaningful.


(create_sdf_best_practices_functionality)=

### Slice functionality

Slices must be functional. This means that if we are creating an application
slice such as `openssl_bins`, we must also include necessary files and slices as
dependency to ensure that the application we are installing runs properly. In
this case, `openssl` must run properly.

If a particular necessary dependency has not been sliced already, the author
must also create necessary slices for that and list it as essential for the
original slice. Had `libc6` package not been chiseled, we would have needed to
create the `libc6_libs` slice too. Otherwise, `openssl` would not have worked.


(create_sdf_best_practices_extra_deps)=

### Extra dependencies

Typically package dependencies are reflected in slice dependencies. If a package
depends on A and B, slices typically only depend on those. But there may be
exceptions.

If extra dependencies are need to make slices
{ref}`functional<create_sdf_best_practices_functionality>`, then we should do
so. Such is the case for slices who comes with shell scripts, but the
corresponding package does not depend on any shell interpreters. In that case,
we should include an interpreter as a slice dependency. See the [tar slices] as
an example.

Note that we should always leave comments explaining the reason to add extra
dependencies.


(create_sdf_best_practices_path_attrs)=

### Path attributes

The paths in the contents field should be extracted from the package if
available. This means that if we need to create a `/bin/foo` symlink to
`/bin/bar`, and it actually exists in the package, we should not add the
attribute `symlink: /bin/bar` to the path. Rather, we should extract it from the
package like the following:

```yaml
    contents:
      /bin/foo:
```

The same goes for directories. If there is one in the package, we should extract
that avoiding using `make: true`.

```yaml
    contents:
      /etc/conf.d/:
```

When extracting directories in this way, we should always add a `/` suffix to
the path to indicate that this is a directory.


(create_sdf_best_practices_wildcards)=

### Wildcards

Authors not abuse globs. We should only use globs in the following cases:

* To hide the version number that may change.

  - We should take care not to hide numerals that identify the package. For
    example, in the package `libfoo2to5`, the following usage of glob is OK:
    `/usr/lib/libfoo2-5*.so`, but hiding either the 2 or 5 in is not.

* If two or more files correspond to the same one (via symlinks) and have a
  similar file name, globs can be used. For example, writing
  `/usr/lib/libfoo2-5*.so` is okay to group the following files:

  - `/usr/lib/libfoo2-5.so`   (points to `/usr/lib/libfoo2-5.123.45.so`)
  - `/usr/lib/libfoo2-5.123.so` (points to `/usr/lib/libfoo2-5.123.45.so`)
  - `/usr/lib/libfoo2-5.123.45.so`

  Symbolic links should always be part of the same slice the link target belongs
  to.

* To hide the architecture and the flavour of Linux that may change.

  Example: `/usr/lib/*-linux-*/` for the path `/usr/lib/amd64-linux-gnu/`. Here,
  `amd64` and `gnu` are subject to change.

* To include everything inside a directory.

  Use `**` to include sub-directories too even if it currently does not have
  any. This makes it future-proof. Example: `/usr/share/foo/**`.

* To write a {ref}`generate<slice_definitions_format_slices_contents_generate>`
  path.

  Example: `/var/lib/chisel/**: {generate: manifest}`.


(create_sdf_best_practices_bottom_up)=

### Bottom-up approach

When writing slices, it's best to follow Chisel's bottom-up approach where we
slowly add new files and/or slices as we need. This makes writing slices easier
and helps to produce minimal slices.

We should remember that it is easy to add new content to a slice, but tricky to
remove something as someone may be already using that slice.



<!-- LINKS -->

[`conffiles`]: https://www.debian.org/doc/debian-policy/ap-pkg-conffiles.html
[`control` file]: https://www.debian.org/doc/debian-policy/ch-controlfields.html
[`dpkg` slice definition file]: https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/dpkg.yaml
[`libpython3.12-stdlib` slice definition file]: https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/libpython3.12-stdlib.yaml
[`python3` slice definition file]: https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/python3.yaml
[`tar` slices]: https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/tar.yaml#L13-L20
[maintainer scripts]: https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html
