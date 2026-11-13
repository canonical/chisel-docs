---
myst:
  html_meta:
    description: "Reference for the Chisel command-line interface, covering the cut, find, info, version, and help subcommands with their options and usage."
---

(command_reference)=

# CLI Commands

Chisel uses subcommands, and is invoked using `chisel <command>`.

Subcommands are keywords that invoke a new set of options and features, and each
Chisel subcommand has its own set of flags.

Here’s the list of all Chisel subcommands:

- {ref}`cut_command_reference`
- {ref}`find_command_reference`
- {ref}`info_command_reference`
- {ref}`version_command_reference`
- {ref}`help_command_reference`

(cut_command_reference)=

## cut

The **cut** command uses the provided selection of package slices to create a
new file system tree in the root location.

By default it fetches the slices for the same Ubuntu version as the
current host, unless the `--release` option is used.

### Options

<!-- Start: cut command options -->

- `--release` is a {{chisel_releases_repo}} branch or local directory (e.g. ubuntu-22.04).
- `--root` is the path for the resulting root file system.
- `--arch` is used to specify the desired package architecture.
- `--ignore` is used to allow Chisel to work with "unstable" or "unmaintained"
  releases (see {ref}`here<chisel_yaml_format_spec_maintenance>`). The valid
  values are "unstable" or "unmaintained", respectively.

<!-- End: cut command options -->

### Example

To install the `hello_bins` slice from Ubuntu 24.04 for `amd64` architecture,
we can run the following:

<!-- Start: hello_bins installation -->

```{terminal}
chisel cut --release ubuntu-24.04 --root rootfs/ hello_bins

2024/11/26 12:21:35 Consulting release repository...
2024/11/26 12:21:37 Cached ubuntu-24.04 release is still up-to-date.
2024/11/26 12:21:37 Processing ubuntu-24.04 release...
2024/11/26 12:22:12 Selecting slices...
2024/11/26 12:22:12 Fetching ubuntu 24.04 noble suite details...
2024/11/26 12:22:15 Release date: Thu, 25 Apr 2024 15:10:33 UTC
2024/11/26 12:22:15 Fetching index for ubuntu 24.04 noble main component...
2024/11/26 12:22:15 Fetching index for ubuntu 24.04 noble universe component...
2024/11/26 12:22:16 Fetching ubuntu 24.04 noble-security suite details...
2024/11/26 12:22:16 Release date: Tue, 26 Nov 2024  3:33:31 UTC
2024/11/26 12:22:16 Fetching index for ubuntu 24.04 noble-security main component...
2024/11/26 12:22:16 Fetching index for ubuntu 24.04 noble-security universe component...
2024/11/26 12:22:16 Fetching ubuntu 24.04 noble-updates suite details...
2024/11/26 12:22:17 Release date: Tue, 26 Nov 2024  5:53:50 UTC
2024/11/26 12:22:17 Fetching index for ubuntu 24.04 noble-updates main component...
2024/11/26 12:22:18 Fetching index for ubuntu 24.04 noble-updates universe component...
2024/11/26 12:22:19 Fetching pool/main/b/base-files/base-files_13ubuntu10.1_amd64.deb...
2024/11/26 12:22:19 Fetching pool/main/h/hello/hello_2.10-3build1_amd64.deb...
2024/11/26 12:22:19 Fetching pool/main/g/glibc/libc6_2.39-0ubuntu8.3_amd64.deb...
2024/11/26 12:22:19 Extracting files from package "base-files"...
2024/11/26 12:22:19 Extracting files from package "hello"...
2024/11/26 12:22:19 Extracting files from package "libc6"...
```

<!-- End: hello_bins installation -->

(find_command_reference)=

## find

The **find** command queries {{chisel_releases_repo}} for matching slices.

Globs (`*` and `?`) are allowed in the query.

By default it fetches the slices for the same Ubuntu version as the
current host, unless the `--release` option is used.

### Options

- `--release` is a {{chisel_releases_repo}} branch or local directory (e.g. ubuntu-22.04).

### Example

Run the following command to search python3.10 slices in `ubuntu-22.04` release:

```{terminal}
chisel find --release ubuntu-22.04 python3.10

2024/11/26 13:11:08 Consulting release repository...
2024/11/26 13:11:10 Fetching current ubuntu-22.04 release...
2024/11/26 13:11:10 Processing ubuntu-22.04 release...
Slice                 Summary
python3.10_copyright  -
python3.10_core       -
python3.10_standard   -
python3.10_utils      -
python3.11_copyright  -
python3.11_core       -
python3.11_standard   -
python3.11_utils      -
```

```{note}
Notice that there are some python3.11 slices in the output as well. This is
because the find command finds partially-matched slices.
```

The first three lines are logs, which you can ignore with:

```{terminal}
chisel find --release ubuntu-22.04 python3.10 2>/dev/null

Slice                 Summary
python3.10_copyright  -
python3.10_core       -
python3.10_standard   -
python3.10_utils      -
python3.11_copyright  -
python3.11_core       -
python3.11_standard   -
python3.11_utils      -
```

(info_command_reference)=

## info 

The **info** command shows detailed information about package slices.

It complements the {{find_cmd}}. Whereas the `find` command searches for existing
slices, the `info` command takes in slice or package name(s) and displays the
slice definition(s).

It accepts a whitespace-separated list of strings. The list can be
composed of package names, slice names, or a combination of both. The
default output format is YAML. When multiple arguments are provided,
the output is a list of YAML documents separated by a `---` line.

Slice definitions are shown according to their definition in
the selected release. For example, globs are not expanded.

### Options

- `--release` is a {{chisel_releases_repo}} branch or local directory (e.g. ubuntu-22.04).

### Example

The following illustrates using the `info` command to inspect multiple slices:

```{terminal}
chisel info hello libgcc-s1_libs 2>logs

package: hello
archive: ubuntu
slices:
    bins:
        essential:
            - hello_copyright
            - libc6_libs
        contents:
            /usr/bin/hello: {}
    copyright:
        contents:
            /usr/share/doc/hello/copyright: {}
---
package: libgcc-s1
archive: ubuntu
slices:
    libs:
        essential:
            - libgcc-s1_copyright
            - libc6_libs
        contents:
            /usr/lib/*-linux-*/libgcc_s.so.*: {}
```

(version_command_reference)=

## version

The **version** command displays the Chisel version and exits.

### Example

```{terminal}
chisel version

v1.0.0
```

(help_command_reference)=

## help

The **help** command displays information about commands.

### Example

```{terminal}
:scroll:

chisel help --all

Chisel can slice a Linux distribution using a release database
and construct a new filesystem using the finely defined parts.

Usage: chisel <command> [<options>...]

Commands can be classified as follows:

  Basic (general operations):
    find     Find existing slices
    info     Show information about package slices
    help     Show help about a command
    version  Show version details

  Action (make things happen):
    cut      Cut a tree with selected slices

For more information about a command, run 'chisel help <command>'.
```
