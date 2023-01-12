# Provenance

The licensing provenance of source files in the repository are explained
in this document.  In particular, this repository is an aggregate work of
existing packaging files that were released under distinct open source licenses.
As this aggregate work was originally based on NGA's
[Hootenanny RPMs](https://github.com/ngageoint/hootenanny-rpms), it is
licensed under the [GPLv3](../LICENSE); there is no intent
to supersede the original licensing of `.spec` files or patches -- and the
provenance of all external code will be explained here.  Unlike Hootenanny's
RPMs, source code archives are not kept in this repository and
downloaded upon RPM creation; licenses for these archives are noted for
convenience.

A majority of `.spec` files and patches in this repository were originally
sourced from Fedora, who uses the [MIT license](./licenses/Fedora-LICENSE)
([source](https://fedoraproject.org/wiki/Legal:Licenses/LicenseAgreement)).
In addition, the PostgreSQL Development Group (PGDG) was used as a source for
portions of the GEOS, GDAL, and PostGIS `.spec` files and patches.  PGDG uses
the  [PostgreSQL license](./licenses/PostgreSQL-LICENSE)
([source](https://download.postgresql.org/pub/README)).

## armadillo

The [armadillo](https://arma.sourceforge.net/) source archives are obtained directly from [Sourceforge](https://sourceforge.net/projects/arma/files/).

The [`armadillo.spec`](../SPECS/el9/armadillo.spec) file originates from [Fedora's `armadillo` RPM](https://src.fedoraproject.org/rpms/armadillo) and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## CGAL

The [CGAL](https://www.cgal.org) source archives are obtained
directly from its [GitHub releases](https://github.com/CGAL/cgal/releases/) and
is released under the [GNU LGPLv3, GPLv3, and Boost licenses](https://github.com/CGAL/cgal/blob/v4.14.3/Installation/LICENSE).

The [`CGAL.spec`](../SPECS/el9/CGAL.spec) originates from
[Fedora's `CGAL` RPM](https://src.fedoraproject.org/rpms/CGAL)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## FileGDBAPI

The File Geodatabase API source archives are obtained from
[ESRI's GitHub repository](https://github.com/Esri/file-geodatabase-api/tree/master/FileGDB_API_1.5.1)
and released under the [Apache 2 license](http://www.apache.org/licenses/LICENSE-2.0).

## GEOS

The [GEOS](https://trac.osgeo.org/geos) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/geos/) and licensed under the
[GNU LGPL v2.1](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html).

The [`geos.spec`](../SPECS/el9/geos.spec) originates from
[Fedora's `geos` RPM](https://src.fedoraproject.org/rpms/geos)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## GDAL

The [GDAL](https://trac.osgeo.org/gdal) source archives are obtained directly from [OSGeo](https://download.osgeo.org/gdal/) and are mostly [MIT/X11](https://trac.osgeo.org/gdal/wiki/FAQGeneral#WhatexactlywasthelicensetermsforGDAL) licensed.

The [`gdal.spec`](../SPECS/el9/gdal.spec) file originates from [Fedora's GDAL RPM](https://src.fedoraproject.org/rpms/gdal/tree/rawhide) repository (`rawhide` branch) and is [MIT licensed](./licenses/Fedora-LICENSE).

## g2clib

The [g2clib](https://github.com/NOAA-EMC/NCEPLIBS-g2c) source archives are obtained directly from its [GitHub releases](https://github.com/NOAA-EMC/NCEPLIBS-g2c/releases).

The [`g2clib.spec`](../SPECS/el9/g2clib.spec) file originates from [Fedora's `g2clib` RPM](https://src.fedoraproject.org/rpms/g2clib) and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## iniparser

The [iniparser](https://github.com/ndevilla/iniparser) source archives are obtained directly from its [GitHub tags](https://github.com/ndevilla/iniparser/tags).

The [`iniparser.spec`](../SPECS/el9/iniparser.spec) file originates from [Fedora's `iniparser` RPM](https://src.fedoraproject.org/rpms/iniparser) and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## libgeotiff

The [GeoTIFF](https://github.com/OSGeo/libgeotiff) library source archives are
obtained directly from [OSGeo's GitHub](https://github.com/OSGeo/libgeotiff/releases/)
and is mostly [MIT/X11](https://github.com/OSGeo/libgeotiff/blob/master/libgeotiff/LICENSE)
licensed.

The [`libgeotiff.spec`](../SPECS/el9/libgeotiff.spec) originates from
[Fedora's `libgeotiff` RPM](https://src.fedoraproject.org/rpms/libgeotiff)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## libosmium

The [libosmium](http://osmcode.org/libosmium/) library source archives are
obtained directly from [GitHub](https://github.com/osmcode/libosmium)
and is [Boost licensed](https://github.com/osmcode/libosmium/blob/master/LICENSE).

The [`libosmium.spec`](../SPECS/el9/libosmium.spec) originates from
[Fedora's `libosmium` RPM](https://src.fedoraproject.org/rpms/libosmium)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## libpqxx

The [libpqxx](https://github.com/jtv/libpqxx) source archives are obtained directly from its [GitHub releases](https://github.com/jtv/libpqxx/releases) and are [BSD licensed](https://github.com/jtv/libpqxx/blob/master/COPYING).

The [`libpqxx.spec`](../SPECS/el9/libpqxx.spec) file originates from [Fedora's `libpqxx` RPM](https://src.fedoraproject.org/rpms/libpqxx) and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## Mapnik

The [Mapnik](http://mapnik.org/) source and test data archives are obtained directly from
[GitHub](https://github.com/mapnik/mapnik/releases) and are
[LGPLv2 licensed](https://github.com/mapnik/mapnik/blob/master/COPYING).

The following packaging files originate from
[Fedora's `mapnik` RPM](https://src.fedoraproject.org/rpms/mapnik)
and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`mapnik.spec`](../SPECS/el9/mapnik.spec)
* [`mapnik-build-json-fix.patch`](../SOURCES/el9/mapnik-build-json-fix.patch)
* [`mapnik-build-viewer.patch`](../SOURCES/el9/mapnik-build-viewer.patch)
* [`mapnik-proj.patch`](../SOURCES/el9/mapnik-proj.patch)
* [`mapnik-rpath.patch`](../SOURCES/el9/mapnik-rpath.patch)
* [`mapnik-system-sparsehash.patch`](../SOURCES/el9/mapnik-system-sparsehash.patch)
* [`mapnik-viewer.desktop`](../SOURCES/el9/mapnik-viewer.desktop)
* [`mapnik-visual-compare.patch`](../SOURCES/el9/mapnik-visual-compare.patch)

## MapServer

The [mapserver](https://github.com/MapServer/MapServer) source archives are obtained directly from its [GitHub releases](https://github.com/MapServer/MapServer/releases).

The [`mapserver.spec`](../SPECS/el9/mapserver.spec) file originates from [Fedora's `mapserver` RPM](https://src.fedoraproject.org/rpms/mapserver) and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## openstreetmap-carto

The [openstreetmap-carto](https://github.com/gravitystorm/openstreetmap-carto)
provides cartographic styles for Mapnik tiles.  Source archives are
obtained directly from GitHub and are
[CC0 1.0 licensed](https://github.com/gravitystorm/openstreetmap-carto/blob/master/LICENSE.txt).

Its data packages contain archives that are public domain and
[ODbL](https://opendatacommons.org/licenses/odbl/) licensed.

Its font packages contain files that are released under the [Hanazono Font
License](http://fonts.jp/hanazono) and the
[Open Font License 1.1](https://scripts.sil.org/OFL).

## osm2pgsql

The [osm2pgsql](https://github.com/openstreetmap/osm2pgsql) source archives are
obtained directly from GitHub and are
[GPLv2 licensed](https://github.com/openstreetmap/osm2pgsql/blob/master/COPYING).

The [`osm2pgsql.spec`](../SPECS/el9/osm2pgsql.spec) originates from
[Fedora's `osm2pgsql` RPM](https://src.fedoraproject.org/rpms/osm2pgsql)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## osmctools

The [osmctools](https://gitlab.com/osm-c-tools/osmctools) source archives
obtained directly from its GitLab and are
released under the [AGPLv3 license](https://gitlab.com/osm-c-tools/osmctools/-/blob/master/COPYING).

## osmdbt

The `osmdbt` package provides [OpenStreetMap Database Replication Tools](https://github.com/openstreetmap/);
source archives are obtained directly from GitHub and are released under the
[GPLv3 license](https://github.com/openstreetmap/osmdbt/blob/master/LICENSE.txt).

## osmium-tool

The [osmium-tool](http://osmcode.org/osmium-tool/) source archives are
obtained directly from [GitHub](https://github.com/osmcode/osmium-tool)
and is [GPLv3 licensed](https://github.com/osmcode/osmium-tool/blob/master/LICENSE.txt).

The [`osmium-tool.spec`](../SPECS/el9/osmium-tool.spec) originates from
[Fedora's `osmium-tool` RPM](https://src.fedoraproject.org/rpms/osmium-tool)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## Osmosis

The [Osmosis](https://github.com/openstreetmap/osmosis) source archive is
obtained directly from its [GitHub releases](https://github.com/openstreetmap/osmosis/releases)
project and was released under the
[LGPLv3 and public domain licenses](https://github.com/openstreetmap/osmosis/blob/master/package/copying.txt).

The [`osmosis-fix_launchers.patch`](../SOURCES/el9/osmosis-fix_launchers.patch) file
comes from [Debian's GIS Project](https://salsa.debian.org/debian-gis-team/osmosis/blob/master/debian/patches/01-fix_launcher.patch)
and is licensed under the GPLv3.

## Passenger

The [Phusion Passenger](https://www.phusionpassenger.com) source archives are obtained
directly from their release S3 bucket and released mostly under Boost/BSD
licenses.

The following packaging files originate from
[Fedora's `passenger` RPM](https://src.fedoraproject.org/rpms/passenger)
and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`passenger.spec`](../SPECS/el9/passenger.spec)
* [`apache-passenger.conf.in`](../SOURCES/el9/apache-passenger.conf.in)
* [`apache-passenger-module.conf`](../SOURCES/el9/apache-passenger-module.conf)
* [`passenger.logrotate`](../SOURCES/el9/passenger.logrotate)
* [`passenger.tmpfiles`](../SOURCES/el9/passenger.tmpfiles)

## PROJ

The [PROJ](https://github.com/OSGeo/PROJ/releases) source archives are obtained
directly from [its GitHub releases](https://github.com/OSGeo/PROJ/releases);
its source code archives are [MIT licensed](https://github.com/OSGeo/PROJ/blob/master/COPYING),
and its data archives are under [public domain, MIT, BSD, and Creative Commons licenses](https://github.com/OSGeo/PROJ-data#about-the-data-package).

The [`proj.spec`](../SPECS/el9/proj.spec) originates from
[Fedora's `proj` RPM](https://src.fedoraproject.org/rpms/proj)
and is [MIT licensed](./licenses/Fedora-LICENSE).

## protobuf

The [`protobuf.spec`](../SPECS/el9/protobuf.spec) originates from
[Fedora's `protobuf` RPM](https://src.fedoraproject.org/rpms/protobuf)
and is [MIT licensed](./licenses/Fedora-LICENSE).

## protozero

The [`protozero.spec`](../SPECS/el9/protozero.spec) originates from
[Fedora's `protozero` RPM](https://src.fedoraproject.org/rpms/protozero)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## PostGIS

The [PostGIS](https://trac.osgeo.org/postgis) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/postgis/) and licensed
under the [GPLv2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

The following packaging files originate from
PGDG's PostGIS [2.5.5](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/)
and [3.1.1](https://download.postgresql.org/pub/repos/yum/srpms/13/redhat/rhel-7-x86_64/)
source RPMs released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE).

* [`postgis.spec`](../SPECS/el9/postgis.spec)
* [`postgis-filter-requires-perl-Pg.sh`](../SOURCES/el9/postgis-filter-requires-perl-Pg.sh)
* [`postgis-3.1-gdalfpic.patch`](../SOURCES/el9/postgis-3.1-gdalfpic.patch)

Any portions of [Fedora's `postgis` RPM](https://src.fedoraproject.org/rpms/postgis/tree/master)
that may appear in these files are [MIT licensed](./licenses/Fedora-LICENSE).

## PyOsmium (`python3-osmium`)

The [PyOsmium](http://osmcode.org/pyosmium/) library source archives are
obtained directly from [GitHub](https://github.com/osmcode/pyosmium)
and is [BSD licensed](https://github.com/osmcode/pyosmium/blob/master/LICENSE.TXT).

The following packaging files originate from
[Fedora's `pyosmium` RPM](https://src.fedoraproject.org/rpms/pyosmium)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`python3-osmium.spec`](../SPECS/el9/python3-osmium.spec)
* [`python3-osmium-no-strip.patch`](../SOURCES/el9/python3-osmium-no-strip.patch)
* [`python3-osmium-no-shapely.patch`](../SOURCES/el9/python3-osmium-no-shapely.patch)

## rubygem-libxml-ruby

The [libxml-ruby](https://github.com/xml4r/libxml-ruby) source is obtained directly from [RubyGems](https://rubygems.org) and are [MIT licensed](https://github.com/xml4r/libxml-ruby/blob/master/LICENSE).

## SBT

The [SBT](http://www.scala-sbt.org) source archives are obtained
directly from [GitHub](https://github.com/sbt/sbt) and are Apache licensed.

## SFCGAL

The [SFCGAL](https://www.sfcgal.org) source archives are obtained
directly from [GitLab](https://gitlab.com/Oslandia/SFCGAL) and
is released under the [LGPLv2 license](https://gitlab.com/Oslandia/SFCGAL/-/blob/master/LICENSE)

## spawn-fcgi

The [spawn-fcgi](https://redmine.lighttpd.net/projects/spawn-fcgi/) source archives are obtained directly from the [Lighttpd website](https://github.com/ndevilla/iniparser/tags) and are BSD licensed.

The [`spawn-fcgi.spec`](../SPECS/el9/spawn-fcgi.spec) file originates from [Fedora's `spawn-fcgi` RPM](https://src.fedoraproject.org/rpms/spawn-fcgi) and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## sqlite-pcre

The `sqlite-pcre` package is derived from
[Ubuntu's `sqlite3-pcre`](https://launchpad.net/ubuntu/+source/sqlite3-pcre/0~git20070120091816+4229ecc-2);
its source code and spec file are considered public domain.

## Smallstep CA / CLI (`step-ca` / `step-cli`)

The [Smallstep CLI](https://github.com/smallstep/cli) and [Smallstep CA](https://github.com/smallstep/certificates) source archives are obtained directly from their GitHub releases. Both are released under the Apache License 2.0: [certificates](https://github.com/smallstep/certificates/blob/master/LICENSE), [cli](https://github.com/smallstep/cli/blob/master/LICENSE).

## wal-g

The [wal-g](https://github.com/wal-g/wal-g) source archives are obtained directly from its [GitHub releases](https://github.com/wal-g/wal-g/releases) and are released under the [ASL 2.0 license](https://github.com/wal-g/wal-g/blob/master/LICENSE.md).
