Name:           SFCGAL
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        C++ wrapper for CGAL providing ISO and OGC operations

License:        LGPLv2
URL:            https://gitlab.com/Oslandia/SFCGAL/
Source0:        https://gitlab.com/Oslandia/SFCGAL/-/archive/v%{version}/SFCGAL-v%{version}.tar.bz2

# Required devel packages.
BuildRequires: doxygen
BuildRequires: CGAL-devel
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: gmp-devel
BuildRequires: boost-devel
BuildRequires: make
BuildRequires: mpfr-devel


%description
SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations.

SFCGAL provides standard compliant geometry types and operations, that
can be accessed from its C or C++ APIs. PostGIS uses the C API, to
expose some SFCGAL's functions in spatial databases (cf. PostGIS
manual).

Geometry coordinates have an exact rational number representation and
can be either 2D or 3D.

%package devel
Summary:        Development files and tools for SFCGAL
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides the headers files and tools to develop
SFCGAL applications.


%prep
%autosetup -p1 -n %{name}-v%{version}


%build
%cmake
%cmake_build
(cd doc; doxygen)


%install
%cmake_install


%files
%doc AUTHORS NEWS README.md
%license LICENSE
%{_libdir}/libSFCGAL.so.*

%files devel
%{_bindir}/sfcgal-config
%{_includedir}/SFCGAL
%{_libdir}/libSFCGAL.so
%{_libdir}/pkgconfig


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
