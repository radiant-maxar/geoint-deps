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

## arpack

The [arpack](https://github.com/opencollab/arpack-ng) source archives are obtained directly from its [GitHub tags](https://github.com/opencollab/arpack-ng/tags).

The [`arpack.spec`](../SPECS/el9/arpack.spec) file originates from [Fedora's `arpack` RPM](https://src.fedoraproject.org/rpms/arpack) and is released under the [Fedora license](./licenses/Fedora-LICENSE).

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

The following packaging files originate from [Fedora's `geos` RPM](https://src.fedoraproject.org/rpms/geos)
and are released under the [Fedora license](./licenses/Fedora-LICENSE):

* [`geos.spec`](../SPECS/el9/geos.spec)
* [`geos_libsuffix.patch`](../SOURCES/el9/geos_libsuffix.patch)

## GDAL

The [GDAL](https://trac.osgeo.org/gdal) source archives are obtained directly from [OSGeo](https://download.osgeo.org/gdal/) and are mostly [MIT/X11](https://trac.osgeo.org/gdal/wiki/FAQGeneral#WhatexactlywasthelicensetermsforGDAL) licensed.

The [`gdal.spec`](../SPECS/el9/gdal.spec) file originates from [Fedora's GDAL RPM](https://src.fedoraproject.org/rpms/gdal/tree/rawhide) repository (`rawhide` branch) and is [MIT licensed](./licenses/Fedora-LICENSE).

## gpsbabel

The [gpsbabel](https://www.gpsbabel.org/) source archive was obtained directly
from their website.  The [`gpsbabel.spec`](../SPECS/el9/gpsbabel.spec) and all
patches from [`SOURCES`](../SOURCES) starting with `gpsbabel` are from
[Fedora's `gpsbabel` RPM](https://src.fedoraproject.org/rpms/gpsbabel/tree/master)
repository and are [MIT licensed](./licenses/Fedora-LICENSE).

## Google Noto Fonts

The [Google Noto Fonts](https://github.com/googlefonts/noto-source) source
archives are obtained directly from the project's GitHub page and are
released under the Open Font License 1.1.

The [`google-noto-fonts-extra.spec`](../SPECS/el9/lgoogle-noto-fonts-extra.spec) originates from
[Fedora's `google-noto-fonts` RPM](https://src.fedoraproject.org/rpms/google-noto-fonts)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## g2clib

## Hanazono Fonts

The [Hanazono Fonts](http://fonts.jp/hanazono/) source archives are obtained
directly from the project's [OSDN downloads](https://osdn.net/projects/hanazono-font/releases/)
and is released under the Hanazono Font License and the Open Font License 1.1.

The following packaging files originate from
[Fedora's `hanazono-fonts` RPM](https://src.fedoraproject.org/rpms/hanazono-fonts)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`hanazono-fonts.spec`](../SPECS/el9/hanazono-fonts.spec)
* [`hanazono-fonts-fontconfig.conf`](../SOURCES/el9/hanazono-fonts-fontconfig.conf)

## iniparser

## libgeotiff

The [GeoTIFF](https://github.com/OSGeo/libgeotiff) library source archives are
obtained directly from [OSGeo's GitHub](https://github.com/OSGeo/libgeotiff/releases/download)
and is mostly [MIT/X11](https://github.com/OSGeo/libgeotiff/blob/master/libgeotiff/LICENSE)
licensed.

The [`libgeotiff.spec`](../SPECS/el9/libgeotiff.spec) originates from
[Fedora's `libgeotiff` RPM](https://src.fedoraproject.org/rpms/libgeotiff)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## libgta

The [Generic Tagged Arrays (GTA)](https://marlam.de/gta/) library code archives are obtained directly from [the project's website](https://github.com/OSGeo/libgeotiff/releases/download) and are [LGPLv2+](https://github.com/marlam/gta-mirror/blob/master/libgta/COPYING) licensed.

The [`libgta.spec`](../SPECS/el9/libgta.spec) originates from [Fedora's `libgta` RPM](https://src.fedoraproject.org/rpms/libgta) and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## libkml

The [libkml](https://github.com/libkml/libkml) source archives were obtained
directly from [GitHub](https://github.com/libkml/libkml/releases) and are
[BSD](https://github.com/libkml/libkml/blob/master/LICENSE) licensed.

The following packaging files originate from
[Fedora's `libkml` RPM](https://src.fedoraproject.org/rpms/libkml.git)
repository and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`libkml.spec`](../SPECS/el9/libkml.spec)
* [`libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch`](../SOURCES/el9/libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch)
* [`libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch`](../SOURCES/el9/libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch)
* [`libkml-0003-Fix-python-tests.patch`](../SOURCES/el9/libkml-0003-Fix-python-tests.patch)
* [`libkml-fragile_test.patch`](../SOURCES/el9/libkml-fragile_test.patch)
* [`libkml-dont-bytecompile.patch`](../SOURCES/el9/libkml-dont-bytecompile.patch)
* [`minizip-1.3.0.tar.gz`](../SOURCES/el9/minizip-1.3.0.tar.gz)

## libosmium

The [libosmium](http://osmcode.org/libosmium/) library source archives are
obtained directly from [GitHub](https://github.com/osmcode/libosmium)
and is [Boost licensed](https://github.com/osmcode/libosmium/blob/master/LICENSE).

The [`libosmium.spec`](../SPECS/el9/libosmium.spec) originates from
[Fedora's `libosmium` RPM](https://src.fedoraproject.org/rpms/libosmium)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## libpqxx

## Mapnik

The [Mapnik](http://mapnik.org/) source and test data archives are obtained directly from
[GitHub](https://github.com/mapnik/mapnik/releases) and are
[LGPLv2 licensed](https://github.com/mapnik/mapnik/blob/master/COPYING).

The following packaging files originate from
[Fedora's `mapnik` RPM](https://src.fedoraproject.org/rpms/mapnik)
and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`mapnik.spec`](../SPECS/el9/mapnik.spec)
* [`mapnik-viewer.desktop`](../SOURCES/el9/mapnik-viewer.desktop)
* [`mapnik-build-viewer.patch`](../SOURCES/el9/mapnik-build-viewer.patch)
* [`mapnik-system-sparsehash.patch`](../SOURCES/el9/mapnik-system-sparsehash.patch)
* [`mapnik-visual-compare.patch`](../SOURCES/el9/mapnik-visual-compare.patch)
* [`mapnik-rpath.patch`](../SOURCES/el9/mapnik-rpath.patch)
* [`mapnik-proj.patch`](../SOURCES/el9/mapnik-proj.patch)
* [`mapnik-build-json-fix.patch`](../SOURCES/el9/mapnik-build-json-fix.patch)

## ogdi

The [ogdi](http://ogdi.sourceforge.net/) source archives are obtained directly
from [GitHub](https://github.com/libogdi/ogdi/releases) and are
[BSD licensed](https://github.com/libogdi/ogdi/blob/master/LICENSE).

The following packaging files originate from
[Fedora's `ogdi` RPM](https://src.fedoraproject.org/rpms/ogdi)
and are [MIT licensed](./licenses/Fedora-LICENSE):

* [`ogdi.spec`](../SPECS/el9/mapnik.spec)
* [`ogdi-4.1.0-sailer.patch`](../SOURCES/el9/ogdi-4.1.0-sailer.patch)

## openstreetmap-carto

The [openstreetmap-carto](https://github.com/gravitystorm/openstreetmap-carto)
provides cartographic styles for Mapnik tiles.  Source archives are
obtained directly from GitHub and are
[CC0 1.0 licensed](https://github.com/gravitystorm/openstreetmap-carto/blob/master/LICENSE.txt).
Its data package contains archives that are public domain and
[ODbL](https://opendatacommons.org/licenses/odbl/) licensed.

## osm2pgsql

The [osm2pgsql](https://github.com/openstreetmap/osm2pgsql) source archives are
obtained directly from GitHub and are
[GPLv2 licensed](https://github.com/openstreetmap/osm2pgsql/blob/master/COPYING).
Using the same license, the following patch files were derived from changesets in GitHub:

* [`osm2pgsql-replication-analyze.patch`](../SOURCES/el9/osm2pgsql-replication-analyze.patch)
* [`osm2pgsql-replication-older-python.patch`](../SOURCES/el9/osm2pgsql-replication-older-python.patch)
* [`osm2pgsql-replication-prefix-argument.patch`](../SOURCES/el9/osm2pgsql-replication-prefix-argument.patch)
* [`osm2pgsql-replication-status.patch`](../SOURCES/el9/osm2pgsql-replication-status.patch)

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

The [`osmosis-fix_launcher.patch`](../SOURCES/el9/osmosis-fix_launcher.patch) file
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

The following packaging files originate from
[Fedora's `proj` RPM](https://src.fedoraproject.org/rpms/proj)
and are [MIT licensed](./licenses/Fedora-LICENSE):
* [`proj.spec`](../SPECS/el9/proj.spec)
* [`proj-pkgconfig.patch`](../SOURCES/el9/proj-pkgconfig.patch)

## protobuf

The following files originate from [Fedora's `protobuf` RPM](https://src.fedoraproject.org/rpms/protobuf)
and are [MIT licensed](./licenses/Fedora-LICENSE):
* [`protobuf.spec`](../SPECS/el9/protobuf.spec)
* [`protobuf-3.14-disable-IoTest.LargeOutput.patch`](../SOURCES/el9/protobuf-3.14-disable-IoTest.LargeOutput.patch)
* [`protobuf-ftdetect-proto.vim`](../SOURCES/el9/protobuf-ftdetect-proto.vim)
* [`protobuf-init.el`](../SOURCES/el9/protobuf-init.el)

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
* [`postgis-gdalfpic.patch`](../SOURCES/el9/postgis-gdalfpic.patch)

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
* [`python3-osmium-no-extras.patch`](../SOURCES/el9/python3-osmium-no-extras.patch)

## Rack

[Rack](https://rack.github.io/) source archives are obtained
directly from RubyGems  and are MIT/BSD licensed.

The [`rubygem-rack.spec`](../SPECS/el9/rubygem-rack.spec) originates from
[Fedora's `rubygem-rack` RPM](https://src.fedoraproject.org/rpms/rubygem-rack)
and is released under the [Fedora license](./licenses/Fedora-LICENSE).

## rubygem-libxml-ruby

## SBT

The [SBT](http://www.scala-sbt.org) source archives are obtained
directly from [GitHub](https://github.com/sbt/sbt) and are Apache licensed.

## SFCGAL

The [SFCGAL](https://www.sfcgal.org) source archives are obtained
directly from [GitLab](https://gitlab.com/Oslandia/SFCGAL) and
is released under the [LGPLv2 license](https://gitlab.com/Oslandia/SFCGAL/-/blob/master/LICENSE)

## sqlite-pcre

The `sqlite-pcre` package is derived from
[Ubuntu's `sqlite3-pcre`](https://launchpad.net/ubuntu/+source/sqlite3-pcre/0~git20070120091816+4229ecc-2);
its source code and spec file are considered public domain.

## uriparser

The [uriparser](https://uriparser.github.io) library code archives are obtained directly from [GitHub](https://github.com/uriparser/uriparser/releases) and are [BSD licensed](https://github.com/uriparser/uriparser/blob/master/COPYING).

The [`uriparser.spec`](../SPECS/el9/uriparser.spec) file originates from [Fedora's `uriparser` RPM](https://src.fedoraproject.org/rpms/uriparser) and is released under the [Fedora license](./licenses/Fedora-LICENSE).
