# The following macros are also required:
# * protozero_min_version

Name:           libosmium
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Fast and flexible C++ library for working with OpenStreetMap data

License:        Boost
URL:            http://osmcode.org/libosmium/
Source0:        https://github.com/osmcode/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  bzip2-devel
BuildRequires:  boost-devel
BuildRequires:  cmake3
BuildRequires:  doxygen
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  xmlstarlet
BuildRequires:  zlib-devel


%description
A fast and flexible C++ library for working with OpenStreetMap data.

%package        devel
Summary:        Development files for %{name}
BuildArch:      noarch

Requires:       bzip2-devel
Requires:       boost-devel
Requires:       expat-devel
Requires:       protozero-devel >= %{protozero_min_version}
Requires:       zlib-devel

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
%{__sed} -i -e 's/-O3 -g//' CMakeLists.txt
%{__mkdir} build


%build
pushd build
%cmake3 -DBUILD_EXAMPLES=OFF -DBUILD_HEADERS=OFF -DINSTALL_GDALCPP=ON ..
%cmake3_build
popd


%install
pushd build
%cmake3_install
%{__rm} -rf %{buildroot}%{_docdir}
popd


%check
pushd build
%ctest3
popd


%files devel
%doc README.md CHANGELOG.md
%license LICENSE
%{_includedir}/gdalcpp.hpp
%{_includedir}/osmium


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
