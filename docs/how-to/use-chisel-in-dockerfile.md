# Use Chisel in a Dockerfile

Chiseled file systems are ideal for creating minimal and distroless-like
container images. This guide shows how to use Chisel in a Dockerfile to create a
chiseled Docker image.


## Design the image

Let's set some goals for our chiseled image. Consider a Python 3 image, which
contains a Python 3 interpreter and is able to run Python 3 scripts and
commands.

- The [image entrypoint] must be `python3`.
- The image must be able to run Python 3 scripts.
- The image must be minimal.

To build this image, we will use [multi-stage docker builds].

In earlier stage(s), we will

1. install Chisel and other dependencies that we may need, and
2. install the slices, using Chisel, into a staging area.

Finally, we will copy the staging area's root file system to the `/` directory
in the final stage. The final stage's base image will be [`scratch`]. Thus, the
image only contains the root file system installed by Chisel and nothing else.


## Write the Dockerfile

Create a `Dockerfile` and open it with your favorite text editor.


## Install Chisel and dependencies

To make building easier and configurable, let's first define some variables that
we can re-use. Visit the {{latest_release_page}} to determine the latest version
of Chisel and assign the latest version to `CHISEL_VERSION`.

```docker
ARG UBUNTU_RELEASE=24.04
ARG CHISEL_VERSION=v1.1.0
```

Let's now initialize a new build stage where we install Chisel and dependencies
and prepare the final chiseled root file system.

```docker
FROM ubuntu:$UBUNTU_RELEASE AS builder
ARG TARGETARCH UBUNTU_RELEASE CHISEL_VERSION
SHELL ["/bin/bash", "-oeux", "pipefail", "-c"]
```

Chisel needs the `ca-certificates` package in order to fetch files from the
archives. Let's install that.

```docker
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
```

Install Chisel.

```docker
ADD "https://github.com/canonical/chisel/releases/download/${CHISEL_VERSION}/chisel_${CHISEL_VERSION}_linux_${TARGETARCH}.tar.gz" \
    chisel.tar.gz
RUN tar -xvf chisel.tar.gz -C /usr/bin/
```


## Prepare the chiseled root file system

Now that we have Chisel installed in the `builder` stage, we can install the
appropriate slices and prepare the root file system.

The [`python3_standard` slice] provides `python3`. We will install this slice,
along with a few others:

- `base-files_base` for file structure.
- `base-files_release-info` for release info.
- `base-files_chisel` for the chisel manifest.
- `ca-certificates_data` for network support.

```docker
RUN mkdir /staging-rootfs \
    && chisel cut --release "ubuntu-$UBUNTU_RELEASE" --root /staging-rootfs \
        base-files_base \
        base-files_release-info \
        base-files_chisel \
        ca-certificates_data \
        python3_standard
```

Next, let's copy the `/etc/passwd` and `/etc/group` files to the installed root
file system to use the existing `ubuntu` user. We will also create a working
directory for the user, per the `/etc/passwd` file.

```docker
RUN cp /etc/passwd /etc/group /staging-rootfs/etc \
    && install -o ubuntu -g ubuntu -d /staging-rootfs/home/ubuntu
```


### Copy the root file system to the final image

Finally, we will initialize a new stage where we will copy the prepared root
file system (`/staging-rootfs`) from the previous stage.

```docker
FROM scratch

COPY --from=builder /staging-rootfs /
```


### Set user and working directory

Now we will set the `USER` to `ubuntu` and the `WORKDIR` to `/home/ubuntu`.

```docker
USER ubuntu
WORKDIR /home/ubuntu
```


### Set the entrypoint

All that remains is to set the entrypoint to `python3`.

```docker
ENTRYPOINT ["python3"]
```


## Build and test the image

Let's copy all the code-blocks above and save it to `Dockerfile`.

```docker
ARG UBUNTU_RELEASE=24.04
ARG CHISEL_VERSION=v1.1.0

FROM ubuntu:$UBUNTU_RELEASE AS builder
ARG TARGETARCH UBUNTU_RELEASE CHISEL_VERSION
SHELL ["/bin/bash", "-oeux", "pipefail", "-c"]

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ADD "https://github.com/canonical/chisel/releases/download/${CHISEL_VERSION}/chisel_${CHISEL_VERSION}_linux_${TARGETARCH}.tar.gz" \
    chisel.tar.gz

RUN tar -xvf chisel.tar.gz -C /usr/bin/

RUN mkdir /staging-rootfs \
    && chisel cut --release "ubuntu-$UBUNTU_RELEASE" --root /staging-rootfs \
        base-files_base \
        base-files_release-info \
        base-files_chisel \
        ca-certificates_data \
        python3_standard

RUN cp /etc/passwd /etc/group /staging-rootfs/etc \
    && install -o ubuntu -g ubuntu -d /staging-rootfs/home/ubuntu


FROM scratch

COPY --from=builder /staging-rootfs /

USER ubuntu
WORKDIR /home/ubuntu

ENTRYPOINT ["python3"]
```

Run the following command to build the image.

```sh
docker build -t python:3-chiseled .
```

Once it's built, run the following command to check if the interpreter works.

```{terminal}
:input: docker run -it python:3-chiseled

Python 3.12.3 (main, Feb  4 2025, 14:48:35) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print('Hello world!')
Hello world!
>>> import os
>>> os.getuid()
1000
>>> os.getcwd()
'/home/ubuntu'
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
:input: docker run -v $PWD/src:/src:ro python:3-chiseled /src/app.py

2025-03-11 06:36:50.717280
```

It should print out the current date and time.


<!-- LINKS -->

[python3 package on Noble]: https://packages.ubuntu.com/noble/python3
[image entrypoint]: https://github.com/opencontainers/image-spec/blob/main/config.md
[multi-stage docker builds]: https://docs.docker.com/build/building/multi-stage/
[`scratch`]: https://hub.docker.com/_/scratch
[`python3_standard` slice]: https://github.com/canonical/chisel-releases/blob/ubuntu-24.04/slices/python3.yaml#L13
