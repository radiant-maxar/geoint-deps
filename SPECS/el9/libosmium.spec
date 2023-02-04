# The following macros are also required:
# * protozero_min_version

Name:           libosmium
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Fast and flexible C++ library for working with OpenStreetMap data

License:        Boost
URL:            http://osmcode.org/libosmium/
Source0:        https://github.com/osmcode/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  gdal-devel
BuildRequires:  geos-devel
BuildRequires:  graphviz
BuildRequires:  lz4-devel
BuildRequires:  protozero-devel >= %{protozero_min_version}
BuildRequires:  ruby
BuildRequires:  rubygem-json
BuildRequires:  sparsehash-devel
BuildRequires:  xmlstarlet
BuildRequires:  zlib-devel


%description
A fast and flexible C++ library for working with OpenStreetMap data.

%package        devel
Summary:        Development files for %{name}
BuildArch:      noarch

Requires:       boost-devel
Requires:       bzip2-devel
Requires:       expat-devel
Requires:       lz4-devel
Requires:       protozero-devel >= %{protozero_min_version}
Requires:       zlib-devel

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
%{__sed} -i -e 's/-O3 -g//' CMakeLists.txt


%build
# LTO appears to cause some issues.
# https://bugzilla.redhat.com/show_bug.cgi?id=2065758
%define _lto_cflags %{nil}
%cmake -DBUILD_HEADERS=OFF -DINSTALL_GDALCPP=ON
%cmake_build


%install
%cmake_install
%{__rm} -rf %{buildroot}%{_docdir}


%check
%ctest


%files devel
%doc README.md CHANGELOG.md
%license LICENSE
%{_includedir}/gdalcpp.hpp
%{_includedir}/osmium


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
