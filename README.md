# Foundation Geoint Dependencies

## Quickstart

Just type `make $RPM_NAME`, for example:

```
export DOCKER_BUILDKIT=1
make geos
```

## Requirements

* Linux host and some basics:
  * Python 3
  * GNU `make`
  * GNU Awk (`gawk` package on Ubuntu)

* Docker >= 18.09
  * Recent version recommended to take advantage of [BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/).

* Docker Compose >= 1.27
  * Supports compose format 3.7, for its [`init` option](https://docs.docker.com/compose/compose-file/compose-file-v3/#init).
