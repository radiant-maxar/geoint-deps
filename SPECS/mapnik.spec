# The following macros are also required:
# * gdal_min_version
# * postgis_min_version
# * proj_min_version

Name:      mapnik
Version:   %{rpmbuild_version}
Release:   %{rpmbuild_release}%{?dist}
Summary:   Free Toolkit for developing mapping applications
License:   LGPLv2+
URL:       http://mapnik.org/
Source0:   https://github.com/mapnik/mapnik/releases/download/v%{version}/mapnik-v%{version}.tar.bz2
Source1:   https://github.com/mapnik/test-data/archive/v%{version}/test-data-v%{version}.tar.gz
Source2:   https://github.com/mapnik/test-data-visual/archive/v%{version}/test-data-visual-v%{version}.tar.gz
Source3:   mapnik-data.license
Source4:   mapnik-viewer.desktop
# Allow the viewer to be built against uninstalled libraries
Patch0:    mapnik-build-viewer.patch
# Build against the system version of sparsehash
Patch1:    mapnik-system-sparsehash.patch
# Allow some minor differences in the visual tests
Patch2:    mapnik-visual-compare.patch
# Patch out attempt to set rpath
Patch3:    mapnik-rpath.patch
# Update projection tests for changes in proj
Patch4:    mapnik-proj.patch
# Fix issue in include/mapnik/json/properties_generator_grammar_impl.hpp:71:27:
#   error: ‘boost::phoenix::at_c’ has not been declared
Patch5:    mapnik-build-json-fix.patch

Requires: dejavu-serif-fonts
Requires: dejavu-sans-fonts
Requires: dejavu-sans-mono-fonts
Requires: google-noto-serif-fonts
Requires: google-noto-sans-fonts
Requires: proj >= %{proj_min_version}

BuildRequires: libpqxx-devel
BuildRequires: pkgconfig
BuildRequires: gdal-devel >= %{gdal_min_version}
BuildRequires: proj-devel >= %{proj_min_version}
BuildRequires: python2-scons
BuildRequires: desktop-file-utils
BuildRequires: gcc-c++
BuildRequires: qt-devel
BuildRequires: libxml2-devel
BuildRequires: boost-devel
BuildRequires: libicu-devel
BuildRequires: libtiff-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libwebp-devel
BuildRequires: cairo-devel
BuildRequires: freetype-devel
BuildRequires: harfbuzz-devel
BuildRequires: sqlite-devel
BuildRequires: sparsehash-devel
BuildRequires: zlib-devel
BuildRequires: dejavu-sans-fonts
BuildRequires: postgis >= %{postgis_min_version}

# Bundled version has many local patches and upstream is essentially dead
Provides: bundled(agg) = 2.4

# Bundles a couple of files from the unreleased "toolbox" extension
# of the boost GIL library. Attempts are being made to establish the
# status of these files (https://svn.boost.org/trac/boost/ticket/11819)
# in the hope of unbundling them
Provides: bundled(boost)

%global __provides_exclude_from ^%{_libdir}/%{name}/input/.*$

%description
Mapnik is a Free Toolkit for developing mapping applications.
It's written in C++ and there are Python bindings to
facilitate fast-paced agile development. It can comfortably
be used for both desktop and web development, which was something
I wanted from the beginning.

Mapnik is about making beautiful maps. It uses the AGG library
and offers world class anti-aliasing rendering with subpixel
accuracy for geographic data. It is written from scratch in
modern C++ and doesn't suffer from design decisions made a decade
ago. When it comes to handling common software tasks such as memory
management, filesystem access, regular expressions, parsing and so
on, Mapnik doesn't re-invent the wheel, but utilises best of breed
industry standard libraries from boost.org


%package devel
Summary: Mapnik is a Free toolkit for developing mapping applications
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: proj-devel libxml2-devel
Requires: boost-devel libicu-devel
Requires: libtiff-devel libjpeg-devel libpng-devel libwebp-devel
Requires: cairo-devel freetype-devel harfbuzz-devel
Requires: sparsehash-devel

%description devel
Mapnik is a Free Toolkit for developing mapping applications.
It's written in C++ and there are Python bindings to
facilitate fast-paced agile development. It can comfortably
be used for both desktop and web development, which was something
I wanted from the beginning.

Mapnik is about making beautiful maps. It uses the AGG library
and offers world class anti-aliasing rendering with subpixel
accuracy for geographic data. It is written from scratch in
modern C++ and doesn't suffer from design decisions made a decade
ago. When it comes to handling common software tasks such as memory
management, filesystem access, regular expressions, parsing and so
on, Mapnik doesn't re-invent the wheel, but utilises best of breed
industry standard libraries from boost.org


%package static
Summary: Static libraries for the Mapnik spatial visualization library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description static
Static libraries for the Mapnik spatial visualization library.


%package utils
License:  GPLv2+
Summary:  Utilities distributed with the Mapnik spatial visualization library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Miscellaneous utilities distributed with the Mapnik spatial visualization
library.


%package demo
Summary:  Demo utility and some sample data distributed with mapnik
License:  GPLv2+ and GeoGratis
Requires: %{name}-devel = %{version}-%{release}
Requires: python3-%{name}

%description demo
Demo application and sample vector datas distributed with the Mapnik
spatial visualization library.


%prep
%setup -q -n mapnik-v%{version} -a 1 -a 2
%autopatch -p1
rm -rf test/data test/data-visual
mv test-data-%{version} test/data
mv test-data-visual-%{version} test/data-visual
iconv -f iso8859-1 -t utf-8 demo/data/COPYRIGHT.txt > COPYRIGHT.conv && mv -f COPYRIGHT.conv demo/data/COPYRIGHT.txt
sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python3|' demo/python/rundemo.py
sed -i -e 's|#!/usr/bin/env python|#!/usr/bin/python3|' demo/simple-renderer/render.py
rm -rf deps/mapnik/sparsehash


%build
# start with default compiler flags
local_optflags="%{optflags}"

# enable deprecated legacy proj api
local_optflags="${local_optflags} -DACCEPT_USE_OF_DEPRECATED_PROJ_API_H"

# configure mapnik
PROJ_LIB=%{_datadir}/proj \
GDAL_DATA=$(gdal-config --datadir) \
scons configure FAST=True \
                  DESTDIR=%{buildroot} \
                  PREFIX=%{_prefix} \
                  FULL_LIB_PATH=False \
                  SYSTEM_FONTS=%{_datadir}/fonts \
                  LIBDIR_SCHEMA=%{_lib} \
                  CUSTOM_CFLAGS="${local_optflags}" \
                  CUSTOM_CXXFLAGS="${local_optflags}" \
                  OPTIMIZATION=2 \
                  SVG2PNG=True \
                  DEMO=False \
                  XMLPARSER=libxml2 \
                  INPUT_PLUGINS=csv,gdal,geojson,ogr,pgraster,postgis,raster,shape,sqlite,topojson

# build mapnik
scons %{?_smp_mflags}

# build mapnik viewer app
pushd demo/viewer
  %qmake_qt4 viewer.pro
  %make_build %{?_smp_mflags}
popd


%install
# install mapnik
scons install

# get rid of fonts use external instead
rm -rf %{buildroot}%{_libdir}/%{name}/fonts

# install more utils
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 demo/viewer/viewer %{buildroot}%{_bindir}/
install -p -m 644 %{SOURCE3} demo/data/

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Libs: -lmapnik
Cflags: -I\${includedir}/%{name}
EOF

mkdir -p %{buildroot}%{_datadir}/pkgconfig
install -p -m 644 %{name}.pc %{buildroot}%{_datadir}/pkgconfig

# install desktop file
cp %{SOURCE4} viewer.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications viewer.desktop


%check
# Create PostgreSQL database.
export PGDATA="${HOME}/pgdata"
pg_ctl -s stop || true
rm -fr ${PGDATA}
initdb --encoding UTF-8 --locale en_US.UTF-8

# Tune the database.
echo "fsync = off" >> "${PGDATA}/postgresql.conf"
echo "shared_buffers = 1GB" >> "${PGDATA}/postgresql.conf"
echo "listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"

# Start PostgreSQL
pg_ctl -s start

# Create testing tablespace required by the Mapnik tests.
createdb template_postgis
psql -c "CREATE EXTENSION postgis" template_postgis

# run tests
LANG="C.UTF-8" make test

# Stop PostgreSQL
pg_ctl -s stop


%files
%doc AUTHORS.md CHANGELOG.md README.md
%license COPYING
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/input
%{_libdir}/%{name}/input/*.input
%{_libdir}/lib%{name}*.so.*


%files devel
%doc docs/
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/lib%{name}*.so
%{_datadir}/pkgconfig/%{name}.pc
%{_bindir}/mapnik-config


%files static
%{_libdir}/lib%{name}*.a


%files utils
%{_bindir}/mapnik-index
%{_bindir}/mapnik-render
%{_bindir}/shapeindex
%{_bindir}/svg2png
%{_bindir}/viewer
%{_datadir}/applications/viewer.desktop


%files demo
%doc demo/c++
%doc demo/data
%doc demo/python
%doc demo/simple-renderer
%license demo/data/mapnik-data.license


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
