# The following macros are also required:
# * gdal_min_version
# * geos_min_version
# * proj_min_version

%global ini_name 40-mapserver.ini
%global project_owner MapServer
%global project_name MapServer

Name:           mapserver
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Environment for building spatially-enabled internet applications
%global dashver %(echo %version | sed 's|\\.|-|g')

License:        BSD
URL:            http://www.mapserver.org

Source0:        https://github.com/%{project_owner}/%{project_name}/archive/rel-%{dashver}%{?prerelease}/%{project_name}-%{version}%{?prerelease}.tar.gz

BuildRequires:  autoconf
BuildRequires:  gcc-c++
BuildRequires:  cairo-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  dejavu-sans-fonts
BuildRequires:  fcgi-devel
BuildRequires:  freetype-devel
BuildRequires:  fribidi-devel
BuildRequires:  gd-devel
BuildRequires:  gdal-devel >= %{gdal_min_version}
BuildRequires:  geos-devel >= %{geos_min_version}
BuildRequires:  giflib-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  httpd-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libpq-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libtiff-devel
BuildRequires:  libxml2-devel
BuildRequires:  libXpm-devel
BuildRequires:  libxslt-devel
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  proj-devel >= %{proj_min_version}
BuildRequires:  protobuf-c-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  ruby-devel
BuildRequires:  readline-devel
BuildRequires:  swig
BuildRequires:  zlib-devel

Requires:       dejavu-sans-fonts

%description
Mapserver is an internet mapping program that converts GIS data to
map images in real time. With appropriate interface pages,
Mapserver can provide an interactive internet map based on
custom GIS data.


%package  libs
Summary:  %{summary}

%description libs
This package contains the libs for mapserver.


%package  devel
Summary:        Development files for mapserver
Requires:       %{name} = %{version}

%description devel
This package contains development files for mapserver.


%package perl
Summary:        Perl/Mapscript map making extensions to Perl
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
The Perl/Mapscript extension provides full map customization capabilities
within the Perl programming language.


%package -n python3-mapserver
%{?python_provide:%python_provide python3-mapserver}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Summary:        Python/Mapscript map making extensions to Python
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-mapserver
The Python/Mapscript extension provides full map customization capabilities
within the Python programming language.


%package ruby
Summary:       Ruby/Mapscript map making extensions to Ruby
Requires:      %{name} = %{version}-%{release}

%description ruby
The Ruby/Mapscript extension provides full map customization capabilities within
the ruby programming language.


%prep
%autosetup -p1 -n %{project_owner}-rel-%{dashver}%{?prerelease}

# replace fonts for tests with symlinks
ln -sf /usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf tests/vera/Vera.ttf
ln -sf /usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf tests/vera/VeraBd.ttf

# Force swig to regenerate the wrapper
rm -rf mapscript/perl/mapscript_wrap.c


%build
%cmake \
    -DINSTALL_LIB_DIR:PATH=%{_libdir} \
    -DCMAKE_SKIP_RPATH:BOOL=TRUE \
    -DCMAKE_SKIP_INSTALL_RPATH:BOOL=TRUE \
    -DWITH_CAIRO:BOOL=TRUE \
    -DWITH_CLIENT_WFS:BOOL=TRUE \
    -DWITH_CLIENT_WMS:BOOL=TRUE \
    -DWITH_CURL:BOOL=TRUE \
    -DWITH_FCGI:BOOL=TRUE \
    -DWITH_FRIBIDI:BOOL=TRUE \
    -DWITH_GD:BOOL=TRUE \
    -DWITH_GDAL:BOOL=TRUE \
    -DWITH_GEOS:BOOL=TRUE \
    -DWITH_GIF:BOOL=TRUE \
    -DWITH_ICONV:BOOL=TRUE \
    -DWITH_JAVA:BOOL=FALSE \
    -DWITH_KML:BOOL=TRUE \
    -DWITH_LIBXML2:BOOL=TRUE \
    -DWITH_OGR:BOOL=TRUE \
    -DWITH_MYSQL:BOOL=TRUE \
    -DWITH_PERL:BOOL=TRUE \
    -DCUSTOM_PERL_SITE_ARCH_DIR:PATH="%{perl_vendorarch}" \
    -DWITH_POSTGIS:BOOL=TRUE \
    -DWITH_PROJ:BOOL=TRUE \
    -DWITH_PYTHON:BOOL=TRUE \
    -DWITH_RSVG:BOOL=TRUE \
    -DWITH_RUBY:BOOL=TRUE \
    -DWITH_V8:BOOL=FALSE \
    -DWITH_SOS:BOOL=TRUE \
    -DWITH_THREAD_SAFETY:BOOL=TRUE \
    -DWITH_WCS:BOOL=TRUE \
    -DWITH_WMS:BOOL=TRUE \
    -DWITH_WFS:BOOL=TRUE \
    -DWITH_XMLMAPFILE:BOOL=TRUE \
    -DWITH_POINT_Z_M:BOOL=TRUE \
    -DWITH_APACHE_MODULE:BOOL=FALSE \
    -DWITH_SVGCAIRO:BOOL=FALSE \
    -DWITH_CSHARP:BOOL=FALSE \
    -DWITH_ORACLESPATIAL:BOOL=FALSE \
    -DWITH_ORACLE_PLUGIN:BOOL=FALSE \
    -DWITH_MSSQL2008:BOOL=FALSE \
    -DWITH_SDE:BOOL=FALSE \
    -DWITH_SDE_PLUGIN:BOOL=FALSE \
    -DWITH_EXEMPI:BOOL=FALSE \
    -Wno-dev
%cmake_build


%install
%cmake_install

%{__mkdir_p} %{buildroot}%{_datadir}/%{name} %{buildroot}
%{__install} -p -m 0644 xmlmapfile/mapfile.xsd %{buildroot}%{_datadir}/%{name}
%{__install} -p -m 0644 xmlmapfile/mapfile.xsl %{buildroot}%{_datadir}/%{name}

# fix cmake install
%{__mkdir_p} %{buildroot}%{_libdir}/cmake
%{__mv} -v %{buildroot}%{_datadir}/%{name}/cmake %{buildroot}%{_libdir}/cmake/%{name}

# fix python3 install
%{__mv} -v %{buildroot}/usr/lib/python%{__default_python3_version} %{buildroot}%{_libdir}

# remove example config file
%{__rm} %{buildroot}%{_sysconfdir}/mapserver-sample.conf


%files
%doc README.rst
%{_bindir}/coshp
%{_bindir}/legend
%{_bindir}/map2img
%{_bindir}/mapserv
%{_bindir}/msencrypt
%{_bindir}/scalebar
%{_bindir}/shptree
%{_bindir}/shptreetst
%{_bindir}/shptreevis
%{_bindir}/sortshp
%{_bindir}/tile4ms
%{_datadir}/%{name}

%files libs
%doc README.rst
%{_libdir}/libmapserver.so.*

%files devel
%doc README.rst
%{_libdir}/libmapserver.so
%{_libdir}/cmake/%{name}
%{_includedir}/%{name}

%files perl
%doc README.rst
%doc mapscript/perl/examples
%dir %{perl_vendorarch}/auto/mapscript
%{perl_vendorarch}/auto/mapscript/*
%{perl_vendorarch}/mapscript.pm

%files -n python3-mapserver
%doc mapscript/python/README.rst
%doc mapscript/python/examples
%doc mapscript/python/tests
%{python3_sitearch}/*mapscript*

%files ruby
%doc mapscript/ruby/README
%doc mapscript/ruby/examples
%{ruby_sitearchdir}/mapscript.so


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
