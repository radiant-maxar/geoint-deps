# FoundationGEOINT Dependencies

## Quickstart

Just type `make $RPM_NAME`, for example start small:

```
export DOCKER_BUILDKIT=1
make FileGDBAPI
```

Or go big and create RPMs for PostGIS and friends with:

```
export DOCKER_BUILDKIT=1
make postgis
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
