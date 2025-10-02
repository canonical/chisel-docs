(chisel_security_ref)=

# Chisel Cryptographic Documentation

Chisel downloads Debian packages from
[archive.ubuntu.com](https://archive.ubuntu.com/), and extracts only selected
few files from each package.  The slice definition files in
[chisel-releases](https://github.com/canonical/chisel-releases) specify the
files to extract.

Chisel is written in Go.

## Detailed Process

1. Chisel downloads and parses the YAMLs from
[chisel-releases](https://github.com/canonical/chisel-releases) repo[^1]. The
Go package [net/http](https://pkg.go.dev/net/http) is used and a tarball is
downloaded over HTTPS. Checksum of the tarball is not checked after downloading.

    Chisel maintains a cache of these files[^2]. When making new requests to
    download a release, Chisel reads the Etag from cache and checks whether the
    cache is still valid. If it is valid, the cached release YAMLs are used.

1. Chisel downloads a few *InRelease* files from the [Ubuntu Archive
but](http://archive.ubuntu.com) these files are never cached. The InRelease
files are signed by GPG, and Chisel verifies[^3] the integrity using the [Ubuntu
Archive Automatic Signing
Key](https://keyserver.ubuntu.com/pks/lookup?search=f6ecb3762474eda9d21b7022871920d1991bc93c&fingerprint=on&op=index).[^4]
The key is specified in the [chisel.yaml in
chisel-releases](https://github.com/canonical/chisel-releases/blob/a442b2e7208128df6366f859b7a858c0d3fce925/chisel.yaml#L47).
The Go package [golang.org/x/crypto/openpgp](http://golang.org/x/crypto/openpgp)
is used for these purposes.

1. After parsing the *InRelease* files, Chisel downloads *Packages.gz* and
subsequently *Packages* from the archive. Downloads are performed over HTTP and
later the digests are cross-checked[^5]. The Go package
[hash](https://pkg.go.dev/hash) is used. Chisel maintains a cache of these
downloaded files. Each file is stored in the cache with their digest as the
filename.

1. The specified files in the slice definition files are extracted from the
downloaded Debian packages.

## (Relevant) Packages used by Chisel

Following lists the relevant packages used by Chisel to support its
cryptographic needs:

* [golang.org/x/crypto/openpgp](http://golang.org/x/crypto/openpgp)	(Go package)

Additionally these Go standard library packages are used:

* [net/http](https://pkg.go.dev/net/http)
* [hash](https://pkg.go.dev/hash)

## Cryptographic technology being exposed to the user

Chisel needs a GPG public key specified in the [chisel.yaml in
chisel-releases](https://github.com/canonical/chisel-releases/blob/a442b2e7208128df6366f859b7a858c0d3fce925/chisel.yaml#L47)
to verify the signed InRelease files it downloads from the Ubuntu Archive. This
file (chisel.yaml) is exposed to the user and Users can very much specify a
different key on their forks. 

The default public key in the official repository is the RSA/4096-bit [Ubuntu
Archive Automatic Signing Key
(2018)](https://keyserver.ubuntu.com/pks/lookup?search=f6ecb3762474eda9d21b7022871920d1991bc93c&fingerprint=on&op=index)
with ID 871920D1991BC93C.

```
pub (4)rsa4096/f6ecb3762474eda9d21b7022871920d1991bc93c 2018-09-17T15:01:46Z
uid Ubuntu Archive Automatic Signing Key (2018) <ftpmaster@ubuntu.com>
```


[^1]: [https://github.com/canonical/chisel/blob/v1.2.0/internal/setup/fetch.go#L32](https://github.com/canonical/chisel/blob/v1.2.0/internal/setup/fetch.go#L32) 

[^2]: [https://github.com/canonical/chisel/blob/v1.2.0/internal/cache/cache.go](https://github.com/canonical/chisel/blob/v1.2.0/internal/cache/cache.go) 

[^3]: The chain of trust here is that we fully trust GitHub so when we download the chisel-release from it we are also "downloading" the public keys. So, because the public keys are trusted, the downloads from the Ubuntu archives can also be trusted.

[^4]: [https://github.com/canonical/chisel/blob/v1.2.0/internal/archive/archive.go#L285](https://github.com/canonical/chisel/blob/v1.2.0/internal/archive/archive.go#L285)

[^5]: [https://github.com/canonical/chisel/blob/v1.2.0/internal/cache/cache.go#L72-L78](https://github.com/canonical/chisel/blob/v1.2.0/internal/cache/cache.go#L72-L78) 
