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
([source](https://fedoraproject.org/wiki/Legal:Licenses/LicenseAgreement).
In addition, the PostgreSQL Development Group (PGDG) was used as a source for
portions of the GEOS, GDAL, and PostGIS `.spec` files and patches.  PGDG uses
the  [PostgreSQL license](./licenses/PostgreSQL-LICENSE)
([source](https://download.postgresql.org/pub/README)).

## CGAL

The [CGAL](https://www.cgal.org) source archives are obtained
directly from its [GitHub releases](https://github.com/CGAL/cgal/releases/) and
is released under the [GNU LGPLv3, GPLv3, and Boost licenses](https://github.com/CGAL/cgal/blob/v4.14.3/Installation/LICENSE).

The [`CGAL.spec`](../SPECS/CGAL.spec) originates from
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

The following packaging files originate from [Fedora's `geos` RPM](https://src.fedoraproject.org/rpms/geos)
and are released under the [Fedora license](./licenses/Fedora-LICENSE):

* [`geos.spec`](../SPECS/geos.spec)
* [`geos_libsuffix.patch`](../SOURCES/geos_libsuffix.patch)

## GDAL

The [GDAL](https://trac.osgeo.org/gdal) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/gdal/) and are mostly
[MIT/X11](https://trac.osgeo.org/gdal/wiki/FAQGeneral#WhatexactlywasthelicensetermsforGDAL)
licensed.

The following packaging files originate from
[Fedora's GDAL RPM](https://src.fedoraproject.org/rpms/gdal/tree/f25)
repository (Fedora 25 release) and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`gdal.spec`](../SPECS/gdal.spec)
* [`gdal-1.9.0-java.patch`](../SOURCES/gdal-1.9.0-java.patch)
* [`gdal-completion.patch`](../SOURCES/gdal-completion.patch)
* [`gdal-installapps.patch`](../SOURCES/gdal-installapps.patch)
* [`gdal-iso8211.patch`](../SOURCES/gdal-iso8211.patch)
* [`gdal-no-diag-disable.patch`](../SOURCES/gdal-no-diag-disable.patch)
* [`gdal-nopdf.patch`](../SOURCES/gdal-nopdf.patch)
* [`gdal-tirpcinc.patch`](../SOURCES/gdal-tirpcinc.patch)
* [`gdalautotest-increase-tolerances.patch`](../SOURCES/gdalautotest-increase-tolerances.patch)

## gpsbabel

The [gpsbabel](https://www.gpsbabel.org/) source archive was obtained directly
from their website.  The [`gpsbabel.spec`](../SPECS/gpsbabel.spec) and all
patches from [`SOURCES`](../SOURCES) starting with `gpsbabel` are from
[Fedora's `gpsbabel` RPM](https://src.fedoraproject.org/rpms/gpsbabel/tree/master)
repository and are [MIT licensed](./licenses/Fedora-LICENSE).

## Google Noto Fonts

The [Google Noto Fonts](https://github.com/googlefonts/noto-source) source
archives are obtained directly from the project's GitHub page and are
released under the Open Font License 1.1.

The [`google-noto-fonts-extra.spec`](../SPECS/lgoogle-noto-fonts-extra.spec) originates from
[Fedora's `google-noto-fonts` RPM](https://src.fedoraproject.org/rpms/google-noto-fonts)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## Hanazono Fonts

The [Hanazono Fonts](http://fonts.jp/hanazono/) source archives are obtained
directly from the project's [OSDN downloads](https://osdn.net/projects/hanazono-font/releases/)
and is released under the Hanazono Font License and the Open Font License 1.1.

The following packaging files originate from
[Fedora's `hanazono-fonts` RPM](https://src.fedoraproject.org/rpms/hanazono-fonts)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`hanazono-fonts.spec`](../SPECS/hanazono-fonts.spec)
* [`hanazono-fonts-fontconfig.conf`](../SOURCES/hanazono-fonts-fontconfig.conf)

## libgeotiff

The [GeoTIFF](https://github.com/OSGeo/libgeotiff) library source archives are
obtained directly from [OSGeo's GitHub](https://github.com/OSGeo/libgeotiff/releases/download)
and is mostly [MIT/X11](https://github.com/OSGeo/libgeotiff/blob/master/libgeotiff/LICENSE)
licensed.

The [`libgeotiff.spec`](../SPECS/libgeotiff.spec) originates from
[Fedora's `libgeotiff` RPM](https://src.fedoraproject.org/rpms/libgeotiff)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## libkml

The [libkml](https://github.com/libkml/libkml) source archives were obtained
directly from [GitHub](https://github.com/libkml/libkml/releases) and are
[BSD](https://github.com/libkml/libkml/blob/master/LICENSE) licensed.

The following packaging files originate from
[Fedora's `libkml` RPM](https://src.fedoraproject.org/rpms/libkml.git)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`libkml.spec`](../SPECS/libkml.spec)
* [`libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch`](../SOURCES/libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch)
* [`libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch`](../SOURCES/libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch)
* [`libkml-0003-Fix-python-tests.patch`](../SOURCES/libkml-0003-Fix-python-tests.patch)
* [`libkml-0004-Correctly-build-and-run-java-test.patch`](../SOURCES/libkml-0004-Correctly-build-and-run-java-test.patch)
* [`libkml-fragile_test.patch`](../SOURCES/libkml-fragile_test.patch)
* [`libkml-dont-bytecompile.patch`](../SOURCES/libkml-dont-bytecompile.patch)

## libosmium

## Mapnik

## openstreetmap-carto

## osm2pgsql

## osmctools

## osmdbt

The `osmdbt` package provides [OpenStreetMap Database Replication Tools](https://github.com/openstreetmap/).

## osmium-tool

## Osmosis

The [Osmosis](https://github.com/openstreetmap/osmosis) source archive is
obtained directly from its [GitHub releases](https://github.com/openstreetmap/osmosis/releases)
project and was released under the
[LGPLv3 and public domain licenses](https://github.com/openstreetmap/osmosis/blob/master/package/copying.txt).

The [`osmosis-fix_launcher.patch`](../SOURCES/osmosis-fix_launcher.patch) file
comes from [Debian's GIS Project](https://salsa.debian.org/debian-gis-team/osmosis/blob/master/debian/patches/01-fix_launcher.patch)
and is licensed under the GPLv3.

## Passenger

## PROJ

The [PROJ](https://github.com/OSGeo/PROJ/releases) source archives are obtained
directly from [its GitHub releases](https://github.com/OSGeo/PROJ/releases);
its source code archives are [MIT licensed](https://github.com/OSGeo/PROJ/blob/master/COPYING),
and its data archives are under [public domain, MIT, BSD, and Creative Commons licenses](https://github.com/OSGeo/PROJ-data#about-the-data-package).

The following packaging files originate from
[Fedora's `proj` RPM](https://src.fedoraproject.org/rpms/proj)
and are [MIT licensed](./licenses/Fedora-LICENSE):
* [`proj.spec`](../SPECS/proj.spec)
* [`proj-pkgconfig.patch`](../SOURCES/proj-pkgconfig.patch)

## protobuf

The following files originate from [Fedora's `protobuf` RPM](https://src.fedoraproject.org/rpms/protobuf)
and are [MIT licensed](./licenses/Fedora-LICENSE):
* [`protobuf.spec`](../SPECS/protobuf.spec)
* [`protobuf-3.14-disable-IoTest.LargeOutput.patch`](../SOURCES/protobuf-3.14-disable-IoTest.LargeOutput.patch)
* [`protobuf-ftdetect-proto.vim`](../SOURCES/protobuf-ftdetect-proto.vim)
* [`protobuf-init.el`](../SOURCES/protobuf-init.el)

## protobuf-c

The [`protobuf-c.spec`](../SPECS/protobuf-c.spec) originates from
[Fedora's `protobuf-c` RPM](https://src.fedoraproject.org/rpms/protobuf-c)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## protozero

The [`protozero.spec`](../SPECS/protozero.spec) originates from
[Fedora's `protozero` RPM](https://src.fedoraproject.org/rpms/protozero)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## PostGIS

The [PostGIS](https://trac.osgeo.org/postgis) source archives are obtained
directly from [OSGeo](https://download.osgeo.org/postgis/) and licensed
under the [GPLv2](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

The following packaging files originate from
PGDG's PostGIS [2.5.5](https://download.postgresql.org/pub/repos/yum/srpms/9.5/redhat/rhel-7-x86_64/)
anad [3.1.1](https://download.postgresql.org/pub/repos/yum/srpms/13/redhat/rhel-7-x86_64/)
source RPMs released under the [PostgreSQL license](./licenses/PostgreSQL-LICENSE).

* [`postgis.spec`](../SPECS/postgis.spec)
* [`postgis-filter-requires-perl-Pg.sh`](../SOURCES/postgis-filter-requires-perl-Pg.sh)
* [`postgis-gdalfpic.patch`](../SOURCES/postgis-gdalfpic.patch)

Any portions of [Fedora's `postgis` RPM](https://src.fedoraproject.org/rpms/postgis/tree/master)
that may appear in these files are [MIT licensed](./licenses/Fedora-LICENSE).

## PyOsmium

## Rack

## Ruby

## SBT

## SFCGAL

## SQLite

## TBB

The `tbb` package provides Intel's Thread Building Blocks library.
