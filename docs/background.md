# Background

## RPMs and Yum

[RPM](http://rpm.org) (RPM Package Manager) is a package distribution system for
Enterprise Linux platforms.  RPM packages comprise metadata and a payload of files
as a GNU gzip-compressed [`cpio`](https://en.wikipedia.org/wiki/Cpio) archive.

RPMs are created from instructions housed in a `.spec` file, typically kept
in a [`SPECS`](../SPECS) folder.  The spec file has instructions on how to
compile and patch the program from a source archive, typically in the
[`SOURCES`](../SOURCES) folder.  The `rpmbuild` program will extract the
source archive and compile the program in a chroot-like environment and
assemble the output into `.rpm` files placed in a `RPMS` folder.

[Yum](http://yum.baseurl.org/) (Yellowdog Updater Modified) manages RPMs of
a system from a network-based repository.  It handles RPM distribution,
updates, and dependency resolution for a Enterprise Linux system.  Yum
repositories are created and updated with the
[`createrepo`](http://createrepo.baseurl.org/) command.  A Yum repository
consists of RPMs and metadata files (as XML and SQLite).  Once updated,
a repository is distributed to a network distribution point like a
web server or S3 bucket.

## Versioning

This repository tries to reconcile [Fedora's package versioning guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Versioning/)
along with each dependency's versioning scheme.

## Repository Dependencies

Building GEOINT dependencies requires use of the following external Enterprise
Linux repositories:

* EPEL
* PGDG (PostgreSQL)

### EPEL

[EPEL](https://fedoraproject.org/wiki/EPEL) (Extra Packages for Enterprise Linux),
is necessary for libraries not included in Enterprise Linux base distributions.
Both PGDG and GEOINT packages have dependencies in the EPEL repository.

### PGDG

[PGDG](https://yum.postgresql.org/) (PostgreSQL Global Development Group) is
for stable PostgreSQL releases with newer versions than what's in the
Enterprise Linux base.  Please note that the PGDG *common* repository is
not used -- it includes versioned spatial dependencies that are not
compatible here (e.g., PGDG's GDAL doesn't support ESRI FileGDBAPI).
