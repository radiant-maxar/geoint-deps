# The following macros are also required:
# * libosmium_min_version
# * protozero_min_version
# * pybind11_version

Name:           python3-osmium
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Python bindings for libosmium

License:        BSD
URL:            https://osmcode.org/pyosmium/
Source0:        https://github.com/osmcode/pyosmium/archive/v%{version}/pyosmium-%{version}.tar.gz
# Disable stripping
Patch0:         python3-osmium-no-strip.patch
# Don't require Shapely/GEOS for tests.
Patch1:         python3-osmium-no-shapely.patch

BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libosmium-devel >= %{libosmium_min_version}
BuildRequires:  make
BuildRequires:  protozero-devel >= %{protozero_min_version}
BuildRequires:  python3-pybind11
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-requests
BuildRequires:  zlib-devel

Requires:       python3-requests

%description
Provides Python bindings for the Libosmium C++ library, a library
for working with OpenStreetMap data in a fast and flexible manner.


%prep
%autosetup -p1 -n pyosmium-%{version}


%build
%set_build_flags
%py3_build


%install
%py3_install


%check
%pytest


%files
%doc README.md README.rst CHANGELOG.md
%license LICENSE.TXT
%{python3_sitearch}/*
%{_bindir}/*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
