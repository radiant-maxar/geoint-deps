# The following macros are also required:
# * geos_min_version
# * postgres_dotless
# * postgres_instdir
# * proj_min_version

#TODO: msg needs to have PublicDecompWT.zip from EUMETSAT, which is not free;
#      Building without msg therefore
#TODO: e00compr bundled?
#TODO: Java has a directory with test data and a build target called test
#      It uses %%{JAVA_RUN}; make test seems to work in the build directory
#TODO: e00compr source is the same in the package and bundled in GDAL
#TODO: Consider doxy patch from Suse, setting EXTRACT_LOCAL_CLASSES  = NO

# Major digit of the proj so version
%global proj_somaj 19

# Tests can be of a different version
%global testversion %{rpmbuild_version}
%global run_tests 1

# Make RPM python packaging happy.
%global __python %{__python3}
%global _python_bytecompile_errors_terminate_build 0

Name:           gdal
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GIS file format library
License:        MIT
URL:            https://www.gdal.org

Source0:        https://github.com/OSGeo/gdal/releases/download/v%{version}/gdal-%{version}.tar.gz
Source1:        https://github.com/OSGeo/gdal/releases/download/v%{version}/gdalautotest-%{testversion}.zip
Source2:        gdal.pom

# Fedora uses Alternatives for Java
Patch2:         gdal-1.9.0-java.patch
# Use libtool to create libiso8211.a, otherwise broken static lib is created since object files are compiled through libtool
Patch4:         gdal-iso8211.patch
# Fix makefiles installing libtool wrappers instead of actual executables
Patch6:         gdal-installapps.patch
# Drop -diag-disable compile flag
Patch9:         gdal-no-diag-disable.patch
# Increase some testing tolerances for new Proj.
#Patch10:        gdalautotest-increase-tolerances.patch


BuildRequires: automake
BuildRequires: autoconf
BuildRequires: ant
BuildRequires: armadillo-devel
BuildRequires: bash-completion
BuildRequires: cfitsio-devel
BuildRequires: chrpath
BuildRequires: cryptopp-devel
BuildRequires: curl-devel
BuildRequires: doxygen
BuildRequires: expat-devel
#BuildRequires: FileGDBAPI-devel
BuildRequires: fontconfig-devel
BuildRequires: freexl-devel
BuildRequires: g2clib-static
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: geos-devel >= %{geos_min_version}
BuildRequires: ghostscript
BuildRequires: giflib-devel
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: json-c-devel
BuildRequires: libdeflate-devel
BuildRequires: libgeotiff-devel
BuildRequires: libgta-devel
BuildRequires: libjpeg-devel
BuildRequires: libkml-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libtirpc-devel
BuildRequires: libtool
BuildRequires: libwebp-devel
BuildRequires: libxml2-devel
BuildRequires: librx-devel
BuildRequires: lz4-devel
# For 'mvn_artifact' and 'mvn_install'
BuildRequires: maven-local
BuildRequires: pcre-devel
BuildRequires: openjpeg2-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: poppler-devel
BuildRequires: postgresql%{postgres_dotless}-devel
BuildRequires: proj-devel >= %{proj_min_version}
BuildRequires: python3-devel
BuildRequires: python3-lxml
BuildRequires: python3-numpy
BuildRequires: python3-pip
BuildRequires: python3-pytest
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
BuildRequires: shapelib-devel
BuildRequires: sqlite-devel
BuildRequires: swig
BuildRequires: unixODBC-devel
BuildRequires: xerces-c-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel
BuildRequires: libzstd-devel

# Run time dependency for gpsbabel driver
Requires:	gpsbabel

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

# We have multilib triage
%if "%{_lib}" == "lib"
  %global cpuarch 32
%else
  %global cpuarch 64
%endif
%description
Geospatial Data Abstraction Library (GDAL/OGR) is a cross platform
C++ translator library for raster and vector geospatial data formats.
As a library, it presents a single abstract data model to the calling
application for all supported formats. It also comes with a variety of
useful commandline utilities for data translation and processing.

It provides the primary data access engine for many applications.
GDAL/OGR is the most widely used geospatial data access library.


%package devel
Summary:       Development files for the GDAL file format library
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for GDAL.


%package libs
Summary:       GDAL file format library

%description libs
This package contains the GDAL file format library.


%package java
Summary:        Java modules for the GDAL file format library
Requires:       jpackage-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description java
The GDAL Java modules provide support to handle multiple GIS file formats.


%package -n python3-gdal
%{?python_provide:%python_provide python3-gdal}
Summary:        Python modules for the GDAL file format library
Requires:       python3-numpy
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:      gdal-python3 < 2.3.1
Provides:       gdal-python3 = %version-%release

%description -n python3-gdal
The GDAL Python 3 modules provide support to handle multiple GIS file formats.


%package python-tools
Summary:        Python tools for the GDAL file format library
Requires:       python3-gdal

%description python-tools
The GDAL Python package provides number of tools for programming and
manipulating GDAL file format library

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^%{python3_sitearch}/.*\.so$


%prep
%autosetup -p1 -n %{name}-%{version} -a 1


%build
%cmake
%cmake_build


%install
%cmake_install
#TODO: Header date lost during installation
# Install multilib cpl_config.h bz#430894
%{__install} -p -D -m 644 %{_vpath_builddir}/port/cpl_config.h %{buildroot}%{_includedir}/%{name}/cpl_config-%{cpuarch}.h
cat > %{buildroot}%{_includedir}/%{name}/cpl_config.h <<EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "gdal/cpl_config-32.h"
#else
#if __WORDSIZE == 64
#include "gdal/cpl_config-64.h"
#else
#error "Unknown word size"
#endif
#endif
EOF
touch -r NEWS.md %{buildroot}%{_includedir}/%{name}/cpl_config.h

# Multilib gdal-config
# Rename the original script to gdal-config-$arch (stores arch-specific information)
# and create a script to call one or the other -- depending on detected architecture
# TODO: The extra script will direct you to 64 bit libs on
# 64 bit systems -- whether you like that or not
mv %{buildroot}%{_bindir}/%{name}-config %{buildroot}%{_bindir}/%{name}-config-%{cpuarch}
#>>>>>>>>>>>>>
cat > %{buildroot}%{_bindir}/%{name}-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | ppc64 | ppc64le | ia64 | s390x | sparc64 | alpha | alphaev6 | aarch64 )
%{name}-config-64 \${*}
;;
*)
%{name}-config-32 \${*}
;;
esac
EOF
#<<<<<<<<<<<<<
touch -r NEWS.md %{buildroot}%{_bindir}/%{name}-config
chmod 0755 %{buildroot}%{_bindir}/%{name}-config

# Don't duplicate license files
%{__rm} %{buildroot}%{_datadir}/%{name}/LICENSE.TXT


%check
%if %{run_tests}
export PGDATA="${HOME}/pgdata"
pg_ctl -s stop || true
%{__rm} -fr ${PGDATA}
# Create PostgreSQL database.
initdb --encoding UTF-8 --locale en_US.UTF-8

# Tune the database.
echo "fsync = off" >> "${PGDATA}/postgresql.conf"
echo "shared_buffers = 1GB" >> "${PGDATA}/postgresql.conf"
echo "listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"

# Start and setup to use PostgreSQL *without* PostGIS.
export PG_USE_POSTGIS=NO
pg_ctl -s start
createdb autotest

pushd gdalautotest-%{testversion}
  # Export test environment variables.
  export PYTHONPATH=%{_usr}/local/lib/python%{python3_version}/site-packages:%{_usr}/local/lib64/python%{python3_version}/site-packages:%{python3_sitearch}:%{buildroot}%{python3_sitearch}
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
  export GDAL_DATA=%{buildroot}%{_datadir}/gdal
  export GDAL_DRIVER_PATH=%{buildroot}%{_libdir}/gdalplugins

  # Enable these tests on demand
  export GDAL_RUN_SLOW_TESTS=1
  export PYTEST="pytest -vv -p no:sugar --color=no"
  #export GDAL_DOWNLOAD_TEST_DATA=1

  # Remove test cases that require database access.
  rm -f \
     ogr/ogr_mysql.py \
     ogr/ogr_mongodbv3.py

  # Run ogr_fgdb test in isolation due to likely conflict with libxml2;
  # unfortunately, this test suite may also fail randomly due to this.
  # Thanks, ESRI!
  $PYTEST ogr/ogr_fgdb.py || true
  rm -f ogr/ogr_fgdb.py

  $PYTEST

  # Run tests with problematic cases deselected.  Some possible explanations:
  #  * gcore/tiff_read.py: will eventually pass, but consumes all memory
  #      forcing host to swap.
  #  * gdrivers/gdalhttp.py: test_http_4 takes way too long
  #  * gdrivers/pdf.py: disabled tests cause segfaults on EL platforms;
  #      most likely due to old poppler library
  #  * ogr/ogr_gmlas: FGDB expat conflict with libxml
  #  * ogr/ogr_gpkg: newer SQLite
  #  * ogr/ogr_mvt: newer protobuf library
  #  * ogr/ogr_pg: trying to use PostGIS when it's not supposed to
  #  * ogr/ogr_sqlite: newer SQLite
  #  * osr/osr_ct: newer PROJ 7
  # $PYTEST \
  #   --deselect gcore/tiff_read.py::test_tiff_read_toomanyblocks \
  #   --deselect gcore/tiff_read.py::test_tiff_read_toomanyblocks_separate \
  #   --deselect gcore/tiff_write.py::test_tiff_write_87 \
  #   --deselect gdrivers/gdalhttp.py::test_http_4 \
  #   --deselect gdrivers/pdf.py::test_pdf_jp2_auto_compression \
  #   --deselect gdrivers/pdf.py::test_pdf_jp2openjpeg_compression \
  #   --deselect gdrivers/pdf.py::test_pdf_jpeg2000_compression \
  #   --deselect ogr/ogr_geojson.py::test_ogr_geojson_57 \
  #   --deselect ogr/ogr_gmlas.py::test_ogr_gmlas_basic \
  #   --deselect ogr/ogr_gmlas.py::test_ogr_gmlas_writer_check_xml_read_back \
  #   --deselect ogr/ogr_gpkg.py::test_ogr_gpkg_46 \
  #   --deselect ogr/ogr_gpkg.py::test_ogr_gpkg_unique \
  #   --deselect ogr/ogr_mvt.py::test_ogr_mvt_point_polygon_clip \
  #   --deselect ogr/ogr_pg.py::test_ogr_pg_70 \
  #   --deselect ogr/ogr_sqlite.py::test_ogr_sqlite_unique \
  #   --deselect ogr/ogr_vrt.py::test_ogr_vrt_33 \
  #   --deselect osr/osr_ct.py::test_osr_ct_options_area_of_interest \
  #   --deselect pyscripts/test_ogr2ogr_py.py::test_ogr2ogr_py_6 \
  #   --deselect pyscripts/test_ogr2ogr_py.py::test_ogr2ogr_py_7 \
  #   --deselect utilities/test_gdal_create.py::test_gdal_create_pdf_composition \
  #   --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_6 \
  #   --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_7 \
  #   --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_18 \
  #   --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_41
popd

# Stop PostgreSQL
pg_ctl -s stop
%endif


%files
%{_bindir}/gdallocationinfo
%{_bindir}/gdal_contour
%{_bindir}/gdal_create
%{_bindir}/gdal_rasterize
%{_bindir}/gdal_translate
%{_bindir}/gdaladdo
%{_bindir}/gdalinfo
%{_bindir}/gdaldem
%{_bindir}/gdalbuildvrt
%{_bindir}/gdaltindex
%{_bindir}/gdalwarp
%{_bindir}/gdal_grid
%{_bindir}/gdalenhance
%{_bindir}/gdalmanage
%{_bindir}/gdalsrsinfo
%{_bindir}/gdaltransform
%{_bindir}/nearblack
%{_bindir}/gdal_viewshed
%{_bindir}/gdalmdiminfo
%{_bindir}/gdalmdimtranslate
%{_bindir}/ogr*
%{_bindir}/gnmanalyse
%{_bindir}/gnmmanage
%{_datadir}/bash-completion/completions/*
%{_mandir}/man1/gdal*.1*
%exclude %{_mandir}/man1/gdal-config.1*
%exclude %{_mandir}/man1/gdal2tiles.1*
%exclude %{_mandir}/man1/gdal_fillnodata.1*
%exclude %{_mandir}/man1/gdal_merge.1*
%exclude %{_mandir}/man1/gdal_retile.1*
%exclude %{_mandir}/man1/gdal_sieve.1*
%{_mandir}/man1/nearblack.1*
%{_mandir}/man1/ogr*.1*
%{_mandir}/man1/gnm*.1.*

%files libs
%license LICENSE.TXT
%doc NEWS.md PROVENANCE.TXT COMMITTERS
%{_libdir}/libgdal.so.30
%{_libdir}/libgdal.so.30.*
%{_datadir}/%{name}
%dir %{_libdir}/%{name}plugins

%files devel
%{_bindir}/%{name}-config
%{_bindir}/%{name}-config-%{cpuarch}
%{_mandir}/man1/gdal-config.1*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n python3-gdal
%doc swig/python/README.rst
%{python3_sitearch}/GDAL-%{version}-py*.egg-info/
%{python3_sitearch}/osgeo/
%{python3_sitearch}/osgeo_utils/

%files python-tools
%_bindir/*.py
%{_mandir}/man1/pct2rgb.1*
%{_mandir}/man1/rgb2pct.1*
%{_mandir}/man1/gdal2tiles.1*
%{_mandir}/man1/gdal_fillnodata.1*
%{_mandir}/man1/gdal_merge.1*
%{_mandir}/man1/gdal_retile.1*
%{_mandir}/man1/gdal_sieve.1*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
