# Create a chiselled Docker image

Since Chisel can produce a minimal root file system, using it in Docker images
has lots of value. This guide shows how to create a chiselled Docker image.

A _chiselled_ image is one which only contains files installed by the slices and
does not contain any base images such as the ubuntu image.


## Design the image

It's a good idea to think first about what our chiselled image should be able to
do. Let's consider a Python 3 image, which contains a Python 3 interpreter and
is able to run Python 3 scripts and commands.

Goals:
- The [image entrypoint] must be `python3`.
- The image must be chiselled i.e. there must not be anything else.
- The image must be able to run Python 3 scripts.
- The image must be minimal.

To build this image, we will use [multi-stage docker builds].

In earlier stage(s),
1. We will install Chisel and other dependencies that we may
need.
2. We will install the slices using Chisel and prepare a root file system.

Finally, we will copy the root file system to the `/` directory in the final
stage. The final stage base image will be [`scratch`], i.e. nothing. Thus, the
image only contains the root file system installed by Chisel and nothing else.


## Install Chisel and dependencies

To make building easier and configurable, let's first define some variables that
we can re-use.

```docker
ARG UBUNTU_RELEASE=24.04
ARG USER=app UID=101 GROUP=app GID=101
ARG CHISEL_VERSION=1.1.0
```

Let's now initialize a new build stage where we install Chisel and dependencies
and prepare the root file system.

```docker
FROM ubuntu:$UBUNTU_RELEASE AS builder
ARG USER UID GROUP GID TARGETARCH UBUNTU_RELEASE CHISEL_VERSION
SHELL ["/bin/bash", "-oeux", "pipefail", "-c"]
```

We will need the `ca-certificates` package to fetch files. Let's install that.

```docker
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
```

We can now install Chisel. Make sure to install the latest version. Visit the
{{latest_release_page}} to determine the latest version and override
`CHISEL_VERSION` appropriately.

```docker
ADD "https://github.com/canonical/chisel/releases/download/v${CHISEL_VERSION}/chisel_v${CHISEL_VERSION}_linux_${TARGETARCH}.tar.gz" \
    chisel.tar.gz
RUN tar -xvf chisel.tar.gz -C /usr/bin/
```


## Prepare chiselled root file system

Now that we have Chisel installed in the `builder` stage, we can install the
appropriate slices and prepare the root file system.

The [`python3_standard` slice] provides `python3`. We will install this slice,
along with a few others:

- `base-files_base` for file structure.
- `base-files_release-info` for release info.
- `base-files_chisel` for the chisel manifest.
- `ca-certificates_data` for network support.

```docker
RUN mkdir /rootfs \
    && chisel cut --release "ubuntu-$UBUNTU_RELEASE" --root /rootfs \
        base-files_base \
        base-files_release-info \
        base-files_chisel \
        ca-certificates_data \
        python3_standard
```

We will also install two users in the root file system - `USER` and `root`.

```docker
RUN install -d -m 0755 -o "$UID" -g "$GID" "/rootfs/home/$USER" \
    && echo -e "root:x:0:\n$GROUP:x:$GID:" >/rootfs/etc/group \
    && echo -e "root:x:0:0:root:/root:/noshell\n$USER:x:$UID:$GID::/home/$USER:/noshell" >/rootfs/etc/passwd
```


## Copy the root file system to the final image

Finally, we will initialize a new stage where we will copy the prepared root
file system (`/rootfs`) from the previous stage.

```docker
FROM scratch
ARG USER UID GROUP GID

COPY --from=builder /rootfs /
# Workaround for https://github.com/moby/moby/issues/38710
COPY --from=builder --chown="$UID:$GID" "/rootfs/home/$USER" "/home/$USER"
```


## Set the entrypoint

All the remains is to set the entrypoint to `python3`.

```docker
ENTRYPOINT ["/usr/bin/python3"]
```


## Build and test the image

Let's copy all the code-blocks above and save it to `Dockerfile`. Run the
following command to build the image.

```sh
docker build -t python:3-chiselled .
```

Once it's built, run the following command to check if the interpreter works.

```{terminal}
:input: docker run -it python:3-chiselled

Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print('Hello world!')
Hello world!
>>> exit()
```

We can further test the image by writing a custom script and checking if the
script successfully runs. Consider the following `./src/app.py` file.

```py
# ./src/app.py
import datetime

x = datetime.datetime.now()
print(x)
```

Run the following command to run the script in our container image.

```{terminal}
:input: docker run -v $PWD/src:/src:ro python:3-chiselled /src/app.py

2025-03-11 06:36:50.717280
```

It should print out the current date and time.


<!-- LINKS -->

[python3 package on Noble]: https://packages.ubuntu.com/noble/python3
[image entrypoint]: https://github.com/opencontainers/image-spec/blob/main/config.md
[multi-stage docker builds]: https://docs.docker.com/build/building/multi-stage/
[`scratch`]: https://hub.docker.com/_/scratch
[`python3_standard` slice]: https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/python3.yaml#L13
