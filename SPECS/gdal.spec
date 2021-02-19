#TODO: msg needs to have PublicDecompWT.zip from EUMETSAT, which is not free;
#      Building without msg therefore
#TODO: e00compr bundled?
#TODO: There are tests for bindings -- at least for Perl
#TODO: Java has a directory with test data and a build target called test
#      It uses %%{JAVA_RUN}; make test seems to work in the build directory
#TODO: e00compr source is the same in the package and bundled in GDAL
#TODO: Consider doxy patch from Suse, setting EXTRACT_LOCAL_CLASSES  = NO

%global geos_min_version 3.9.0
%global proj_min_version 7.2.0

# Major digit of the proj so version
%global proj_somaj 18

# Tests can be of a different version
%global testversion %{rpmbuild_version}
%global run_tests 1

Name:           gdal
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GIS file format library
License:        MIT
URL:            https://www.gdal.org

Source0:        https://github.com/OSGeo/gdal/releases/download/v%{version}/gdal-%{version}.tar.gz
Source1:        https://github.com/OSGeo/gdal/releases/download/v%{version}/gdalautotest-%{testversion}.zip
Source2:        gdal.pom

# Patch for Armadillo and FileGDBAPI detection.
Patch1:         gdal-configure.patch
# Fedora uses Alternatives for Java
Patch2:         gdal-1.9.0-java.patch
# Ensure rpc/types.h is found by dods driver (indirectly required by libdap/XDRUtils.h)
Patch3:         gdal-tirpcinc.patch
# Use libtool to create libiso8211.a, otherwise broken static lib is created since object files are compiled through libtool
Patch4:         gdal-iso8211.patch
# Fix makefiles installing libtool wrappers instead of actual executables
Patch6:         gdal-installapps.patch
# Don't refer to PDF manual which is not built
Patch7:         gdal-nopdf.patch
# Drop -diag-disable compile flag
Patch9:         gdal-no-diag-disable.patch
# Increase some testing tolerances for new Proj.
Patch10:        gdalautotest-increase-tolerances.patch

# Adding FileGDB API.
BuildRequires: FileGDBAPI

BuildRequires: ant
BuildRequires: armadillo-devel
BuildRequires: bash-completion
BuildRequires: cfitsio-devel
BuildRequires: chrpath
BuildRequires: curl-devel
BuildRequires: doxygen
BuildRequires: expat-devel
BuildRequires: fontconfig-devel
BuildRequires: freexl-devel
BuildRequires: g2clib-static
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: geos-devel >= %{geos_min_version}
BuildRequires: ghostscript
BuildRequires: hdf-devel
BuildRequires: hdf-static
BuildRequires: hdf5-devel
BuildRequires: java-devel
BuildRequires: jasper-devel
BuildRequires: jpackage-utils
# For 'mvn_artifact' and 'mvn_install'
BuildRequires: maven-local
BuildRequires: json-c-devel
BuildRequires: libgeotiff-devel
BuildRequires: libgta-devel

BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libkml-devel

BuildRequires: libtiff-devel
BuildRequires: libtirpc-devel
BuildRequires: libwebp-devel
BuildRequires: libtool
BuildRequires: giflib-devel
BuildRequires: netcdf-devel
BuildRequires: libdap-devel
BuildRequires: librx-devel
BuildRequires: numpy
BuildRequires: python3-numpy
BuildRequires: pcre-devel
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: openjpeg2-devel
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: pkgconfig
BuildRequires: poppler-devel
BuildRequires: postgresql%{postgres_dotless}-devel
BuildRequires: proj-devel >= %{proj_min_version}
BuildRequires: python2-devel
BuildRequires: python3-devel
BuildRequires: python3-pip
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

%if ! (0%{?fedora} || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#TODO: Description on the lib?
%description
Geospatial Data Abstraction Library (GDAL/OGR) is a cross platform
C++ translator library for raster and vector geospatial data formats.
As a library, it presents a single abstract data model to the calling
application for all supported formats. It also comes with a variety of
useful commandline utilities for data translation and processing.

It provides the primary data access engine for many applications.
GDAL/OGR is the most widely used geospatial data access library.


%package devel
Summary:	Development files for the GDAL file format library

# Old rpm didn't figure out
%if 0%{?rhel} < 6
Requires: pkgconfig
%endif

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	%{name}-libs
Obsoletes:	%{name}-static < 1.9.0-1

%description devel
This package contains development files for GDAL.


%package libs
Summary:	GDAL file format library

%description libs
This package contains the GDAL file format library.


%package java
Summary:	Java modules for the GDAL file format library
Requires:	jpackage-utils
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description java
The GDAL Java modules provide support to handle multiple GIS file formats.


%package javadoc
Summary:	Javadocs for %{name}
Requires:	jpackage-utils
BuildArch:	noarch

%description javadoc
This package contains the API documentation for %{name}.


%package perl
Summary:	Perl modules for the GDAL file format library
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
The GDAL Perl modules provide support to handle multiple GIS file formats.


%package -n python2-gdal
Summary:	Python modules for the GDAL file format library
Requires:	numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Provides:	gdal-python = %{version}-%{release}
Provides:	gdal-python%{?_isa} = %{version}-%{release}

%description -n python2-gdal
The GDAL Python modules provide support to handle multiple GIS file formats.
The package also includes a couple of useful utilities in Python.


%package -n python3-gdal
Summary:	Python modules for the GDAL file format library
Requires:	python3-numpy
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Provides:	gdal-python3 = %{version}-%{release}

%description -n python3-gdal
The GDAL Python 3 modules provide support to handle multiple GIS file formats.

%package python-tools
Summary:	Python tools for the GDAL file format library
Requires:	python3-gdal

%description python-tools
The GDAL Python package provides number of tools for programming and
manipulating GDAL file format library

%package doc
Summary:	Documentation for GDAL
BuildArch:	noarch

%description doc
This package contains HTML and PDF documentation for GDAL.

# We don't want to provide private Python extension libs
%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/.*\.so$

%prep
%autosetup -p1 -n gdal-%{version} -a 1

# Delete bundled libraries
rm -rf frmts/zlib
rm -rf frmts/png/libpng
rm -rf frmts/gif/giflib
rm -rf frmts/jpeg/libjpeg
rm -rf frmts/jpeg/libjpeg12
rm -rf frmts/gtiff/libgeotiff
rm -rf frmts/gtiff/libtiff

# Replace hard-coded library- and include paths
sed -i 's|-L\$with_cfitsio -L\$with_cfitsio/lib -lcfitsio|-lcfitsio|g' configure
sed -i 's|-I\$with_cfitsio -I\$with_cfitsio/include|-I\$with_cfitsio/include/cfitsio|g' configure
sed -i 's|-L\$with_netcdf -L\$with_netcdf/lib -lnetcdf|-lnetcdf|g' configure
sed -i 's|-L\$DODS_LIB -ldap++|-ldap++|g' configure
sed -i 's|-L\$with_ogdi -L\$with_ogdi/lib -logdi|-logdi|g' configure
sed -i 's|-L\$with_jpeg -L\$with_jpeg/lib -ljpeg|-ljpeg|g' configure
sed -i 's|-L\$with_libtiff\/lib -ltiff|-ltiff|g' configure
sed -i 's|-lgeotiff -L$with_geotiff $LIBS|-lgeotiff $LIBS|g' configure
sed -i 's|-L\$with_geotiff\/lib -lgeotiff $LIBS|-lgeotiff $LIBS|g' configure

# libproj is dlopened; upstream sources point to .so, which is usually not present
# http://trac.osgeo.org/gdal/ticket/3602
sed -i 's|libproj.so|libproj.so.%{proj_somaj}|g' ogr/ogrct.cpp

# Tests expect to be next to gdal source directory, but we extract them within
# it. And putting tests next to the source directory wouldn't account for the
# version in the directory name, anyway, so we need to correct this.
sed -i \
    -e 's!../../gdal/swig/python/samples!../../swig/python/samples!' \
    %{name}autotest-%{testversion}/gcore/{cog,tiff_write}.py \
    %{name}autotest-%{testversion}/gdrivers/{gpkg,jp2lura,jp2openjpeg,test_validate_jp2}.py \
    %{name}autotest-%{testversion}/ogr/ogr_gpkg.py


# Adjust check for LibDAP version
# http://trac.osgeo.org/gdal/ticket/4545
%if %cpuarch == 64
  sed -i 's|with_dods_root/lib|with_dods_root/lib64|' configure
%endif

# Fix mandir
sed -i "s|^mandir=.*|mandir='\${prefix}/share/man'|" configure

# Add our custom cflags when trying to find geos
# https://bugzilla.redhat.com/show_bug.cgi?id=1284714
sed -i 's|CFLAGS=\"${GEOS_CFLAGS}\"|CFLAGS=\"${CFLAGS} ${GEOS_CFLAGS}\"|g' configure


%build
%global optflags %{optflags} -fPIC -I%{_includedir}/FileGDBAPI
# Ensure PGDG's PostgreSQL pkg-config is in the path.
export PKG_CONFIG_PATH=%{postgres_instdir}/lib/pkgconfig:%{_libdir}/pkgconfig:%{_datadir}/pkgconfig

%configure \
        --with-autoload=%{_libdir}/gdalplugins \
        --includedir=%{_includedir}/gdal/      \
        --prefix=%{_prefix}                    \
        --with-bash-completion                 \
        --with-armadillo                       \
        --with-curl                            \
        --with-cfitsio                         \
        --with-dods-root=%{_prefix}            \
        --with-expat                           \
        --with-fgdb                            \
        --with-freexl                          \
        --with-geos                            \
        --with-geotiff                         \
        --with-gif                             \
        --with-gta                             \
        --with-hdf4                            \
        --with-hdf5                            \
        --with-jasper                          \
        --with-java                            \
        --with-jpeg                            \
        --with-libjson-c                       \
        --without-jpeg12                       \
        --with-liblzma                         \
        --with-libtiff                         \
        --with-libz                            \
        --without-mdb                          \
        --without-msg                          \
        --without-mysql                        \
        --without-ogdi                         \
        --with-netcdf                          \
        --with-odbc                            \
        --with-openjpeg                        \
        --with-pcraster                        \
        --with-pg                              \
        --with-png                             \
        --with-poppler                         \
        --with-proj                            \
        --without-spatialite                   \
        --with-sqlite3                         \
        --with-threads                         \
        --with-webp                            \
        --with-xerces                          \
        --enable-shared                        \
        --with-perl                            \
        --with-python                          \
        --with-libkml                          \
        --with-zstd                            \
        --disable-driver-elastic

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

POPPLER_OPTS="POPPLER_0_20_OR_LATER=yes POPPLER_0_23_OR_LATER=yes POPPLER_BASE_STREAM_HAS_TWO_ARGS=yes"

make %{?_smp_mflags} $POPPLER_OPTS

# Build some utilities, as requested in BZ #1271906
make -C ogr/ogrsf_frmts/s57 all
make -C frmts/iso8211 all

make man
make docs

# Make Java module and documentation
pushd swig/java
  make
  ant maven
popd

%mvn_artifact swig/java/build/maven/gdal-%version.pom swig/java/build/maven/gdal-%version.jar

# Make Python modules
pushd swig/python
  %{py2_build}
  %{py3_build}
popd

# Make Perl modules
pushd swig/perl
  perl Makefile.PL INSTALLDIRS=vendor
  %make_build
popd

# --------- Documentation ----------

# No useful documentation in swig
%global docdirs apps doc doc/br doc/ru ogr ogr/ogrsf_frmts frmts/gxf frmts/iso8211 frmts/pcidsk frmts/sdts frmts/vrt ogr/ogrsf_frmts/dgn/
for docdir in %{docdirs}; do
  # CreateHTML and PDF documentation, if specified
  pushd $docdir
    if [ ! -f Doxyfile ]; then
      doxygen -g
    else
      doxygen -u
    fi
    sed -i -e 's|^GENERATE_LATEX|GENERATE_LATEX = YES\n#GENERATE_LATEX |' Doxyfile
    sed -i -e 's|^GENERATE_HTML|GENERATE_HTML = YES\n#GENERATE_HTML |' Doxyfile
    sed -i -e 's|^USE_PDFLATEX|USE_PDFLATEX = YES\n#USE_PDFLATEX |' Doxyfile

    if [ $docdir == "doc/ru" ]; then
      sed -i -e 's|^OUTPUT_LANGUAGE|OUTPUT_LANGUAGE = Russian\n#OUTPUT_LANGUAGE |' Doxyfile
    fi
    rm -rf latex html
    doxygen

  popd
done


%install
pushd swig/python
  %{py2_install}
  %{py3_install}
popd

pushd swig/perl
  %make_install
popd

make    DESTDIR=%{buildroot}	\
        install	\
        install-man

install -pm 755 ogr/ogrsf_frmts/s57/s57dump %{buildroot}%{_bindir}
install -pm 755 frmts/iso8211/8211createfromxml %{buildroot}%{_bindir}
install -pm 755 frmts/iso8211/8211dump %{buildroot}%{_bindir}
install -pm 755 frmts/iso8211/8211view %{buildroot}%{_bindir}

# Directory for auto-loading plugins
mkdir -p %{buildroot}%{_libdir}/gdalplugins

#TODO: Don't do that?
find %{buildroot}%{perl_vendorarch} -name "*.dox" -exec rm -rf '{}' \;
rm -f %{buildroot}%{perl_archlib}/perllocal.pod

# Correct permissions
#TODO and potential ticket: Why are the permissions not correct?
find %{buildroot}%{perl_vendorarch} -name "*.so" -exec chmod 755 '{}' \;
find %{buildroot}%{perl_vendorarch} -name "*.pm" -exec chmod 644 '{}' \;

# install Java plugin
%mvn_install -J swig/java/java

# 775 on the .so?
# copy JNI libraries and links, non versioned link needed by JNI
# What is linked here?
mkdir -p %{buildroot}%{_jnidir}/gdal
cp -pl swig/java/.libs/*.so*  \
    %{buildroot}%{_jnidir}/gdal/
chrpath --delete %{buildroot}%{_jnidir}/gdal/*jni.so*

# Install Java API documentation in the designated place
mkdir -p %{buildroot}%{_javadocdir}/gdal
cp -pr swig/java/java/org %{buildroot}%{_javadocdir}/gdal

# Install refmans
for docdir in %{docdirs}; do
  pushd $docdir
    path=%{_builddir}/gdal-%{version}/refman
    mkdir -p $path/html/$docdir
    cp -r html $path/html/$docdir
  popd
done

# Install formats documentation
for dir in gdal_frmts ogrsf_frmts; do
  mkdir -p $dir
  find frmts -name "*.html" -exec install -p -m 644 '{}' $dir \;
done

#TODO: Header date lost during installation
# Install multilib cpl_config.h bz#430894
install -p -D -m 644 port/cpl_config.h %{buildroot}%{_includedir}/gdal/cpl_config-%{cpuarch}.h
# Create universal multilib cpl_config.h bz#341231
# The problem is still there in 1.9.
#TODO: Ticket?

#>>>>>>>>>>>>>
cat > %{buildroot}%{_includedir}/gdal/cpl_config.h <<EOF
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
#<<<<<<<<<<<<<
touch -r NEWS port/cpl_config.h

# Create and install pkgconfig file
#TODO: Why does that exist? Does Grass really use it? I don't think so.
# http://trac.osgeo.org/gdal/ticket/3470
#>>>>>>>>>>>>>
cat > gdal.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: GDAL
Description: GIS file format library
Version: %{version}
Libs: -L\${libdir} -lgdal
Cflags: -I\${includedir}/gdal
EOF
#<<<<<<<<<<<<<
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m 644 gdal.pc %{buildroot}%{_libdir}/pkgconfig/
touch -r NEWS %{buildroot}%{_libdir}/pkgconfig/gdal.pc

# Multilib gdal-config
# Rename the original script to gdal-config-$arch (stores arch-specific information)
# and create a script to call one or the other -- depending on detected architecture
# TODO: The extra script will direct you to 64 bit libs on
# 64 bit systems -- whether you like that or not
mv %{buildroot}%{_bindir}/gdal-config %{buildroot}%{_bindir}/gdal-config-%{cpuarch}
#>>>>>>>>>>>>>
cat > %{buildroot}%{_bindir}/gdal-config <<EOF
#!/bin/bash

ARCH=\$(uname -m)
case \$ARCH in
x86_64 | ppc64 | ppc64le | ia64 | s390x | sparc64 | alpha | alphaev6 | aarch64 )
gdal-config-64 \${*}
;;
*)
gdal-config-32 \${*}
;;
esac
EOF
#<<<<<<<<<<<<<
touch -r NEWS %{buildroot}%{_bindir}/gdal-config
chmod 755 %{buildroot}%{_bindir}/gdal-config

#jni-libs and libgdal are also built static (*.a)
#.exists and .packlist stem from Perl
for junk in {*.a,*.la,*.bs,.exists,.packlist} ; do
  find %{buildroot} -name "$junk" -delete
done

# Don't duplicate license files
rm -f %{buildroot}%{_datadir}/gdal/LICENSE.TXT


%check
%if %{run_tests}
pushd gdalautotest-%{testversion}
  # Export test environment variables.
  export PYTHONPATH=%{_usr}/local/lib/python%{python3_version}/site-packages:%{python3_sitearch}:%{buildroot}%{python3_sitearch}
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{buildroot}%{_libdir}
  export GDAL_DATA=%{buildroot}%{_datadir}/gdal
  export GDAL_DRIVER_PATH=%{buildroot}%{_libdir}/gdalplugins

  # Enable these tests on demand
  export GDAL_RUN_SLOW_TESTS=1
  export PYTEST="pytest -vv -p no:sugar --color=no"
  #export GDAL_DOWNLOAD_TEST_DATA=1

  # Remove test cases that require database access.
  rm -f \
     ogr/ogr_pg.py \
     ogr/ogr_mysql.py \
     ogr/ogr_mongodbv3.py

  # On Python 3.6 there's merely cyrillic encoding issues; on 3.7 this
  # test segfaults.
  rm -f ogr/ogr_gmlas.py

  # Run ogr_fgdb test in isolation due to likely conflict with libxml2
  $PYTEST ogr/ogr_fgdb.py
  rm -f ogr/ogr_fgdb.py

  # Run tests with problematic cases deselected.  Some explanations:
  #  * gcore/tiff_read.py: will eventually pass, but consumes all memory
  #      forcing host to swap.
  #  * gdrivers/gdalhttp.py: test_http_4 takes way too long
  #  * gdrivers/pdf.py: disabled tests cause segfaults on EL platforms
  $PYTEST \
    --deselect ogr/ogr_dxf.py::test_ogr_dxf_9 \
    --deselect ogr/ogr_dxf.py::test_ogr_dxf_16 \
    --deselect ogr/ogr_gft.py::test_ogr_gft_read \
    --deselect ogr/ogr_gpkg.py::test_ogr_gpkg_18 \
    --deselect ogr/ogr_ili.py::test_ogr_interlis1_7 \
    --deselect ogr/ogr_ili.py::test_ogr_interlis1_14 \
    --deselect ogr/ogr_mitab.py::test_ogr_mitab_46 \
    --deselect ogr/ogr_mitab.py::test_ogr_mitab_local_encoding_label \
    --deselect ogr/ogr_mvt.py::test_ogr_mvt_point_polygon_clip \
    --deselect ogr/ogr_pds4.py::test_ogr_pds4_read_table_character \
    --deselect ogr/ogr_pds4.py::test_ogr_pds4_delete_from_table_character \
    --deselect gcore/tiff_read.py::test_tiff_read_toomanyblocks \
    --deselect gcore/tiff_read.py::test_tiff_read_toomanyblocks_separate \
    --deselect gcore/tiff_write.py::test_tiff_write_87 \
    --deselect gdrivers/gdalhttp.py::test_http_4 \
    --deselect gdrivers/ignfheightasciigrid.py::test_ignfheightasciigrid_2 \
    --deselect gdrivers/ignfheightasciigrid.py::test_ignfheightasciigrid_3 \
    --deselect gdrivers/ignfheightasciigrid.py::test_ignfheightasciigrid_4 \
    --deselect gdrivers/pdf.py::test_pdf_jp2_auto_compression \
    --deselect gdrivers/pdf.py::test_pdf_jp2openjpeg_compression \
    --deselect gdrivers/pdf.py::test_pdf_jpeg2000_compression \
    --deselect gdrivers/pds4.py::test_pds4_8 \
    --deselect gdrivers/pds4.py::test_pds4_9 \
    --deselect gdrivers/pds4.py::test_pds4_15 \
    --deselect gdrivers/pds4.py::test_pds4_16 \
    --deselect gdrivers/pds4.py::test_pds4_17 \
    --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_6 \
    --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_7 \
    --deselect utilities/test_ogr2ogr.py::test_ogr2ogr_41 \
    --deselect pyscripts/test_ogr2ogr_py.py::test_ogr2ogr_py_6 \
    --deselect pyscripts/test_ogr2ogr_py.py::test_ogr2ogr_py_7
popd
%endif


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%{_sysconfdir}/bash_completion.d/gdal
%{_bindir}/gdallocationinfo
%{_bindir}/gdal_contour
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
%{_bindir}/gdalserver
%{_bindir}/gdalsrsinfo
%{_bindir}/gdaltransform
%{_bindir}/nearblack
%{_bindir}/ogr*
%{_bindir}/8211*
%{_bindir}/s57*
%{_bindir}/testepsg
%{_bindir}/gnmanalyse
%{_bindir}/gnmmanage
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
%doc LICENSE.TXT NEWS PROVENANCE.TXT COMMITTERS
%{_libdir}/libgdal.so.*
%{_datadir}/gdal
#TODO: Possibly remove files like .dxf, .dgn, ...
%dir %{_libdir}/gdalplugins

%files devel
%{_bindir}/gdal-config
%{_bindir}/gdal-config-%{cpuarch}
%{_mandir}/man1/gdal-config.1*
%dir %{_includedir}/gdal
%{_includedir}/gdal/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/gdal.pc

# Can I even have a separate Java package anymore?
%files java -f .mfiles
%doc swig/java/apps
%{_jnidir}/gdal/

%files javadoc
%{_javadocdir}/gdal

%files perl
%doc swig/perl/README
%{perl_vendorarch}/*
%{_mandir}/man3/*.3pm*

%files -n python2-gdal
%doc swig/python/README.rst
%doc swig/python/samples
%{python2_sitearch}/osgeo
%{python2_sitearch}/GDAL-%{version}-py*.egg-info
%{python2_sitearch}/osr.py*
%{python2_sitearch}/ogr.py*
%{python2_sitearch}/gdal*.py*


%files -n python3-gdal
%doc swig/python/README.rst
%doc swig/python3/samples
%{python3_sitearch}/osgeo
%{python3_sitearch}/GDAL-%{version}-py*.egg-info
%{python3_sitearch}/osr.py
%{python3_sitearch}/__pycache__/osr.*.py*
%{python3_sitearch}/ogr.py
%{python3_sitearch}/__pycache__/ogr.*.py*
%{python3_sitearch}/gdal*.py
%{python3_sitearch}/__pycache__/gdal*.*.py*


%files python-tools
%{_bindir}/*.py
%{_mandir}/man1/pct2rgb.1*
%{_mandir}/man1/rgb2pct.1*
%{_mandir}/man1/gdal2tiles.1*
%{_mandir}/man1/gdal_fillnodata.1*
%{_mandir}/man1/gdal_merge.1*
%{_mandir}/man1/gdal_retile.1*
%{_mandir}/man1/gdal_sieve.1*


%files doc
%doc gdal_frmts ogrsf_frmts refman


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
