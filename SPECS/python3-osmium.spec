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
Source1:        https://github.com/pybind/pybind11/archive/v%{pybind11_version}/pybind11-%{pybind11_version}.tar.gz
# Disable stripping
Patch1:         python3-osmium-no-strip.patch
# Disable link time optimization (LTO).
Patch2:         python3-osmium-no-extras.patch
# Don't require Shapely/GEOS for tests.
Patch3:         python3-osmium-no-shapely.patch

BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  lz4-devel
BuildRequires:  libosmium-devel >= %{libosmium_min_version}
BuildRequires:  protozero-devel >= %{protozero_min_version}
BuildRequires:  python3-devel
BuildRequires:  python36-nose
BuildRequires:  python36-requests
BuildRequires:  zlib-devel

%description
Provides Python bindings for the Libosmium C++ library, a library
for working with OpenStreetMap data in a fast and flexible manner.


%prep
%autosetup -p1 -n pyosmium-%{version}


%build
# Extract pybind11 into contrib/pybind11.
mkdir -p contrib/pybind11
tar -C contrib/pybind11 --strip-components 1 -xzf %{SOURCE1}
export PYBIND11_PREFIX=$(pwd)/contrib/pybind11

# Manual %%set_build_flags macro.
export CFLAGS="${CFLAGS:-%optflags}"
export CXXFLAGS="${CXXFLAGS:-%optflags}"
export FFLAGS="${FFLAGS:-%optflags -I%_fmoddir}"
export FCFLAGS="${FCFLAGS:-%optflags -I%_fmoddir}"
export LDFLAGS="${LDFLAGS:-%__global_ldflags}"

# Ensure CMake that uses Python 3 on EL7.
%if 0%{?rhel} <= 7
%{__sed} -i -e "s/'cmake'/'cmake3'/g" setup.py
%endif

%py3_build


%install
%py3_install


%check
cd test
%{__python3} run_tests.py


%files
%doc README.md README.rst CHANGELOG.md
%license LICENSE.TXT
%{python3_sitearch}/*
%{_bindir}/*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
