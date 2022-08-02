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

## Requirements

* Linux host and some basics:
  * Python 3 for `docker-compose` and some of the [scripts](./scripts/).
  * GNU `make` for the [`Makefile`](./Makefile).

* Docker >= 18.09
  * Recent version recommended to take advantage of [BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/).

* Docker Compose >= 1.27
  * Supports compose format 3.7, for its [`init` option](https://docs.docker.com/compose/compose-file/compose-file-v3/#init).
