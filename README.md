# FoundationGEOINT Dependencies

[![CI](https://github.com/radiant-maxar/geoint-deps/actions/workflows/ci.el7.yml/badge.svg)](https://github.com/radiant-maxar/geoint-deps/actions/workflows/ci.el7.yml) [![CI](https://github.com/radiant-maxar/geoint-deps/actions/workflows/ci.el9.yml/badge.svg)](https://github.com/radiant-maxar/geoint-deps/actions/workflows/ci.el9.yml)

This repository provides a Docker-based build system for creating RPMs of the latest geospatial libraries on CentOS/RHEL 9 (*as well as CentOS/RHEL 7 until the platform fades into obsolesence*).

**Priorities:**

* Support common geospatial libraries and applications, e.g., those from OSGeo and OSM.
* Build RPMs in isolated environments, using only what's required, as a non-privileged user.
* Embrace the RPM toolchain to support compilation hardening flags.

## Quickstart
***Substitute `Makefile.el9` with `Makefile.el7` in order to target `EL7`***

Just type `make $RPM_NAME`, for example start small:

```
export DOCKER_BUILDKIT=1
make --makefile=Makefile.el9 FileGDBAPI
```

Or go big and create RPMs for all applications with:

```
export DOCKER_BUILDKIT=1
make --makefile=Makefile.el9 all-rpms
```

This will consume a lot of CPU and I/O!

## Pushing up stable RPMs

You will need to have `~/.gnupg-geoint` populated using the `.gpg` file and provided instructions as well as the decrypted passphrase from an email originally sent on `2021.03.05` (ask Justin or David if you require these).

#### EL7

1. Download the RPMS artifact from the [most recent EL7 GitHub Actions workflow run](https://github.com/radiant-maxar/geoint-deps/actions/workflows/ci.el7.yml?query=branch%3Astable).

1. Export variables for `AWS_PROFILE` & `EL_VERSION`
    ```shell
    export AWS_PROFILE=geoint-deps
    export EL_VERSION=el7
    ```

1. Run the [`push_stable_rpms_from_zip.sh`](./scripts/push_stable_rpms_from_zip.sh) script with the RPMS artifact zip file path as the first argument
    ```shell
    scripts/push_stable_rpms_from_zip.sh  ~/Downloads/RPMS.zip
    ```

1. Execute the provided command if everything appears to be correct

#### EL9

1. Download the RPMS artifact from the [most recent EL9 GitHub Actions workflow run](https://github.com/radiant-maxar/geoint-deps/actions/workflows/ci.el9.yml?query=branch%3Astable).

1. Export variables for `AWS_PROFILE` & `EL_VERSION`
    ```shell
    export AWS_PROFILE=geoint-deps
    export EL_VERSION=el9
    ```

1. Run the [`push_stable_rpms_from_zip.sh`](./scripts/push_stable_rpms_from_zip.sh) script with the RPMS artifact zip file path as the first argument
    ```shell
    scripts/push_stable_rpms_from_zip.sh  ~/Downloads/RPMS.zip
    ```

1. Execute the provided command if everything appears to be correct


## Requirements

* Linux host and some basics:
  * Python 3 for `docker-compose` and some of the [scripts](./scripts/).
  * GNU `make` for [`Makefile.el7`](./Makefile.el7)/[`Makefile.el9`](./Makefile.el9).

* Docker >= 18.09
  * Recent version recommended to take advantage of [BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/).

* Docker Compose >= 1.27
  * Supports compose format 3.7, for its [`init` option](https://docs.docker.com/compose/compose-file/compose-file-v3/#init).
