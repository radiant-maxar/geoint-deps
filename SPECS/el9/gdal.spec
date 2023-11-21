# The following macros are also required:
# * geos_min_version
# * postgres_version
# * proj_min_version

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
Source1:        https://github.com/OSGeo/gdal/releases/download/v%{version}/gdalautotest-%{testversion}.tar.gz
Source2:        gdal.pom

BuildRequires: ant
BuildRequires: armadillo-devel
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: bash-completion
BuildRequires: ccache
BuildRequires: cfitsio-devel
BuildRequires: chrpath
BuildRequires: cryptopp-devel
BuildRequires: curl-devel
BuildRequires: doxygen
BuildRequires: expat-devel
BuildRequires: FileGDBAPI-devel
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
BuildRequires: libzstd-devel
BuildRequires: lz4-devel
# For 'mvn_artifact' and 'mvn_install'
BuildRequires: maven-local
BuildRequires: pcre-devel
BuildRequires: ogdi-devel
BuildRequires: openjpeg2-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: poppler-devel
BuildRequires: postgresql%{postgres_version}-contrib
BuildRequires: postgresql%{postgres_version}-devel
BuildRequires: postgresql%{postgres_version}-server
BuildRequires: proj-devel >= %{proj_min_version}
BuildRequires: python3-devel
BuildRequires: python3-filelock
BuildRequires: python3-jsonschema
BuildRequires: python3-lxml
BuildRequires: python3-numpy
BuildRequires: python3-pip
BuildRequires: python3-psutil
BuildRequires: python3-pytest
BuildRequires: python3-pytest-benchmark
BuildRequires: python3-pytest-env
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
BuildRequires: sqlite-devel
BuildRequires: swig
BuildRequires: unixODBC-devel
BuildRequires: xerces-c-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel

# Run time dependency for gpsbabel driver.
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
Summary:        GDAL file format library
Requires:       FileGDBAPI

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
# LTO appears to cause some issues.
# https://bugzilla.redhat.com/show_bug.cgi?id=2065758
%define _lto_cflags %{nil}
%cmake \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir}/%{name} \
    -DGDAL_USE_POSTGRESQL:BOOL=ON \
    -DPostgreSQL_ADDITIONAL_VERSIONS=%{postgres_version} \
    -DUSE_CCACHE:BOOL=ON
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
%{__mv} %{buildroot}%{_bindir}/%{name}-config %{buildroot}%{_bindir}/%{name}-config-%{cpuarch}
%{_bindir}/cat > %{buildroot}%{_bindir}/%{name}-config <<EOF
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
touch -r NEWS.md %{buildroot}%{_bindir}/%{name}-config
%{__chmod} 0755 %{buildroot}%{_bindir}/%{name}-config

# Fix malformed include directory probably due to "unexpected" use of `CMAKE_INSTALL_INCLUDEDIR`.
%{__sed} -i -e 's|usr//usr|usr|g' \
%{buildroot}%{_bindir}/%{name}-config-%{cpuarch} \
%{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Don't duplicate license files
%{__rm} %{buildroot}%{_datadir}/%{name}/LICENSE.TXT

# Fix Java install location.
%{__install} -d \
 %{buildroot}%{_jnidir}/%{name} \
 %{buildroot}%{_javadir}/%{name} \
 %{buildroot}%{_mavenpomdir}
%{__rm} -v %{buildroot}%{_javadir}/%{name}-%{version}-{javadoc,sources}.jar
%{__mv} -v %{buildroot}%{_javadir}/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/gdal.jar
%{__mv} -v %{buildroot}%{_javadir}/%{name}-%{version}.pom %{buildroot}%{_mavenpomdir}/gdal.pom
%{__mv} -v %{buildroot}%{_libdir}/jni/libgdalalljni.so %{buildroot}%{_jnidir}/%{name}
%{_bindir}/chrpath --delete %{buildroot}%{_jnidir}/%{name}/libgdalalljni.so


%check
%if %{run_tests}
# Run CMake tests.
%ctest

# Create and start PostgreSQL database for running GDAL autotest suite.
export PGDATA="${HOME}/pgdata"
%{_bindir}/pg_ctl -m fast -s stop || true
%{__rm} -fr ${PGDATA}
%{_bindir}/initdb --encoding UTF-8 --locale en_US.UTF-8
echo "fsync = off
shared_buffers = 1GB
listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"
%{_bindir}/pg_ctl -s start
%{_bindir}/createdb autotest

pushd gdalautotest-%{testversion}

# Remove this test due to conflicts with EL TIFF library:
#  RuntimeError: /vsimem/test.tif: MissingRequired:TIFF directory is missing required "StripOffsets" field
%{__rm} -v test_random_tiff.py

# Tests disabled for performance and/or reliability reasons:
#  * gcore/tiff_{ovr,read,write}.py: Slow.
#  * gdrivers/vrtwarp.py: Slow.
#  * gdrivers/wms.py: Brittle URL.
#  * ogr/ogr_wfs.py: Slow tests and brittle URLs.
#  * pyscripts/test_gdal_ls_py.py: Slow.
# Tests with know failures/errors:
#  * ogr/ogr_fgdb: Tests randomly fail possibly to conflict with XML library.
#  * ogr/ogr_pg.py: Invalid PostGIS usage.
#  * pyscripts/test_ogr2ogr_py: Invalid PostGIS usage.
#  * utilities/test_ogr2ogr.py: Invalid PostGIS usage.


# Create pytest.ini
%{_bindir}/cat > pytest.ini <<EOF
[pytest]
python_files = *.py
testpaths = ogr gcore gdrivers osr alg gnm utilities pyscripts benchmark
norecursedirs = ogr/data gdrivers/data cpp
log_file = autotest.log
log_file_level = INFO
gdal_version = %{version}

markers =
    random_order: Indicates whether tests can be run non-sequentially
    require_curl: Skip test(s) if curl support is absent
    require_creation_option: Skip test(s) if required creation option is not available
    require_driver: Skip test(s) if driver isn't present
    require_geos: Skip test(s) if required GEOS version is not available
    require_proj: Skip test(s) if required PROJ version is not available
    require_run_on_demand: Skip test(s) if RUN_ON_DEMAND environment variable is not set
    slow: Skip test(s) if GDAL_RUN_SLOW_TESTS environment variable is not set

# Make sure that all markers are declared above, and deselect problematic test cases.
addopts =
    -vv
    -p no:sugar
    --color=no
    --strict-markers
    --deselect gcore/tiff_ovr.py::test_tiff_ovr_46
    --deselect gcore/tiff_read.py::test_tiff_read_toomanyblocks
    --deselect gcore/tiff_read.py::test_tiff_read_toomanyblocks_separate
    --deselect gcore/tiff_write.py::test_tiff_write_deflate_4GB
    --deselect gdrivers/vrtwarp.py::test_vrtwarp_read_blocks_larger_than_2_gigapixels
    --deselect gdrivers/wms.py::test_wms_16
    --deselect gdrivers/wms.py::test_wms_19
    --deselect ogr/ogr_fgdb.py::test_ogr_fgdb_19
    --deselect ogr/ogr_fgdb.py::test_ogr_fgdb_19bis
    --deselect ogr/ogr_fgdb.py::test_ogr_fgdb_20
    --deselect ogr/ogr_fgdb.py::test_ogr_fgdb_21
    --deselect ogr/ogr_pg.py::test_ogr_pg_70
    --deselect ogr/ogr_pg.py::test_ogr_pg_skip_views
    --deselect ogr/ogr_wfs.py::test_ogr_wfs_esri_2
    --deselect ogr/ogr_wfs.py::test_ogr_wfs_erdas_apollo
    --deselect ogr/ogr_wfs.py::test_ogr_wfs_tinyows
    --deselect pyscripts/test_gdal_ls_py.py::test_gdal_ls_py_8
    --deselect pyscripts/test_ogr2ogr_py.py::test_ogr2ogr_py_6
    --deselect pyscripts/test_ogr2ogr_py.py::test_ogr2ogr_py_7
    --deselect pyscripts/test_ogr2ogr_py.py::test_ogr2ogr_py_41
    --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_6
    --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_7
    --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_41
EOF

# Export test environment variables.
export CI=YES
export GDAL_DATA=%{buildroot}%{_datadir}/gdal
export GDAL_DOWNLOAD_TEST_DATA=NO
export GDAL_DRIVER_PATH=%{buildroot}%{_libdir}/gdalplugins
export GDAL_RUN_SLOW_TESTS=YES
export GDAL_ENABLE_DEPRECATED_DRIVER_DODS=YES
export GDAL_ENABLE_DEPRECATED_DRIVER_JDEM=YES
export GDAL_ENABLE_DEPRECATED_DRIVER_ZMAP=YES
export GDAL_ENABLE_DEPRECATED_DRIVER_OGR_DODS=YES
export GDAL_ENABLE_DEPRECATED_DRIVER_TIGER=YES
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:%{buildroot}%{_libdir}
export PG_USE_POSTGIS=NO
export PROJ_NETWORK=OFF
export PYTHONPATH=%{buildroot}%{python3_sitearch}

# Run autotests with pytest.
pytest
popd

# Stop PostgreSQL
%{_bindir}/pg_ctl -m fast -s stop
%endif


%files
%{_bindir}/gdal_contour
%{_bindir}/gdal_create
%{_bindir}/gdal_footprint
%{_bindir}/gdal_grid
%{_bindir}/gdal_rasterize
%{_bindir}/gdal_translate
%{_bindir}/gdal_viewshed
%{_bindir}/gdaladdo
%{_bindir}/gdalbuildvrt
%{_bindir}/gdaldem
%{_bindir}/gdalenhance
%{_bindir}/gdalinfo
%{_bindir}/gdallocationinfo
%{_bindir}/gdalmanage
%{_bindir}/gdalmdiminfo
%{_bindir}/gdalmdimtranslate
%{_bindir}/gdalsrsinfo
%{_bindir}/gdaltindex
%{_bindir}/gdaltransform
%{_bindir}/gdalwarp
%{_bindir}/gnmanalyse
%{_bindir}/gnmmanage
%{_bindir}/nearblack
%{_bindir}/ogr*
%{_bindir}/sozip
%{_datadir}/bash-completion/completions/*
%exclude %{_mandir}/man1/gdal_fillnodata.1*
%exclude %{_mandir}/man1/gdal_merge.1*
%exclude %{_mandir}/man1/gdal_retile.1*
%exclude %{_mandir}/man1/gdal_sieve.1*
%exclude %{_mandir}/man1/gdal-config.1*
%exclude %{_mandir}/man1/gdal2tiles.1*
%{_mandir}/man1/gdal*.1*
%{_mandir}/man1/nearblack.1*
%{_mandir}/man1/ogr*.1*
%{_mandir}/man1/gnm*.1.*
%{_mandir}/man1/sozip.1.*

%files libs
%license LICENSE.TXT
%doc NEWS.md PROVENANCE.TXT COMMITTERS
%{_libdir}/libgdal.so.*
%{_datadir}/%{name}
%dir %{_libdir}/gdalplugins
%exclude %{_libdir}/gdalplugins/drivers.ini

%files devel
%{_bindir}/%{name}-config
%{_bindir}/%{name}-config-%{cpuarch}
%{_mandir}/man1/gdal-config.1*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%files java
%{_javadir}/%{name}
%{_jnidir}/%{name}
%{_mavenpomdir}/gdal.pom

%files -n python3-gdal
%doc swig/python/README.rst
%{python3_sitearch}/GDAL-%{version}-py*.egg-info/
%{python3_sitearch}/osgeo/
%{python3_sitearch}/osgeo_utils/

%files python-tools
%{_bindir}/*.py
%{_mandir}/man1/gdal_fillnodata.1*
%{_mandir}/man1/gdal_merge.1*
%{_mandir}/man1/gdal_retile.1*
%{_mandir}/man1/gdal_sieve.1*
%{_mandir}/man1/gdal2tiles.1*
%{_mandir}/man1/pct2rgb.1*
%{_mandir}/man1/rgb2pct.1*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
