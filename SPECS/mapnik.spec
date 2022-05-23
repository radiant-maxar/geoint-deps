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
# https://github.com/mapnik/mapnik/pull/4202
Patch4:    mapnik-proj.patch
# https://github.com/mapnik/mapnik/pull/4159
Patch5:    mapnik-scons4.patch

Requires: dejavu-lgc-serif-fonts
Requires: dejavu-lgc-sans-fonts
Requires: dejavu-lgc-sans-mono-fonts
Requires: google-noto-serif-fonts
Requires: google-noto-sans-fonts
Requires: proj >= %{proj_min_version}

BuildRequires: boost-devel
BuildRequires: cairo-devel
BuildRequires: dejavu-lgc-sans-fonts
BuildRequires: desktop-file-utils
BuildRequires: freetype-devel
BuildRequires: gcc-c++
BuildRequires: gdal-devel >= %{gdal_min_version}
BuildRequires: harfbuzz-devel
BuildRequires: libicu-devel
BuildRequires: libtiff-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libpqxx-devel
BuildRequires: libwebp-devel
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: postgresql%{postgres_dotless}-devel
BuildRequires: postgis >= %{postgis_min_version}
BuildRequires: proj-devel >= %{proj_min_version}
BuildRequires: python3-scons
BuildRequires: qt5-qtbase-devel
BuildRequires: sqlite-devel
BuildRequires: sparsehash-devel
BuildRequires: zlib-devel

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
%{__rm} -rf test/data test/data-visual
%{__mv} test-data-%{version} test/data
%{__mv} test-data-visual-%{version} test/data-visual
%{__sed} -i \
 -e 's/+init=epsg/epsg/g' \
 -e 's/+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0.0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs +over/epsg:3857/g' \
 -e 's/+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs/epsg:4326/g' \
 test/data-visual/styles/*.xml
%{_bindir}/iconv -f iso8859-1 -t utf-8 demo/data/COPYRIGHT.txt > COPYRIGHT.conv
%{__mv} -f COPYRIGHT.conv demo/data/COPYRIGHT.txt
%{__rm} -rf deps/mapnik/sparsehash


%build
# configure mapnik
PROJ_LIB=%{_datadir}/proj \
GDAL_DATA=$(gdal-config --datadir) \
%{_bindir}/scons configure FAST=True \
                  DESTDIR=%{buildroot} \
                  PREFIX=%{_prefix} \
                  FULL_LIB_PATH=False \
                  SYSTEM_FONTS=%{_datadir}/fonts \
                  LIBDIR_SCHEMA=%{_lib} \
                  CUSTOM_CFLAGS="%{optflags}" \
                  CUSTOM_CXXFLAGS="%{optflags}" \
                  OPTIMIZATION=2 \
                  SVG2PNG=True \
                  DEMO=False \
                  XMLPARSER=libxml2 \
                  INPUT_PLUGINS=csv,gdal,geojson,ogr,pgraster,postgis,raster,shape,sqlite,topojson

# build mapnik
%{_bindir}/scons %{?_smp_build_ncpus:-j%{_smp_build_ncpus}}

# build mapnik viewer app
pushd demo/viewer
  %qmake_qt5 viewer.pro
  %make_build %{?_smp_mflags}
popd


%install
# install mapnik
%{_bindir}/scons install

# get rid of fonts use external instead
%{__rm} -rf %{buildroot}%{_libdir}/%{name}/fonts

# install more utils
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -p -m 0755 demo/viewer/viewer %{buildroot}%{_bindir}/
%{__install} -p -m 0644 %{SOURCE3} demo/data/

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

%{__mkdir_p} %{buildroot}%{_datadir}/pkgconfig
%{__install} -p -m 0644 %{name}.pc %{buildroot}%{_datadir}/pkgconfig

# install desktop file
%{__cp} %{SOURCE4} viewer.desktop
%{_bindir}/desktop-file-install --dir=%{buildroot}%{_datadir}/applications viewer.desktop


%check
# Create PostgreSQL database.
export PGDATA="${HOME}/pgdata"
%{_bindir}/pg_ctl -m fast -s stop || true
%{__rm} -fr ${PGDATA}
%{_bindir}/initdb --encoding UTF-8 --locale C.UTF-8

# Tune the database.
echo "fsync = off
shared_buffers = 1GB
listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"

# Start PostgreSQL
%{_bindir}/pg_ctl -s start

# Create testing tablespace required by the Mapnik tests.
%{_bindir}/createdb template_postgis
%{_bindir}/psql -c "CREATE EXTENSION postgis" template_postgis

# run tests
LANG="C.UTF-8" %{__make} test

# Stop PostgreSQL
%{_bindir}/pg_ctl -m fast -s stop


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
