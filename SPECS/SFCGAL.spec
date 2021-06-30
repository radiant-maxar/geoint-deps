Name:           SFCGAL
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        C++ wrapper for CGAL providing ISO and OGC operations

License:        GPLv2
URL:            http://www.sfcgal.org/
Source0:        https://gitlab.com/Oslandia/SFCGAL/-/archive/v%{version}/SFCGAL-v%{version}.tar.gz

# Required devel packages.
BuildRequires: doxygen
BuildRequires: CGAL-devel
BuildRequires: cmake3
BuildRequires: gcc-c++
BuildRequires: gmp-devel
BuildRequires: boost-devel
BuildRequires: make
BuildRequires: mpfr-devel


%description
SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations.

%package devel
Summary:        Development files and tools for SFCGAL
Requires:       CGAL-devel
Requires:       cmake3
Requires:       boost-devel%{?_isa}
Requires:       gmp-devel%{?_isa}
Requires:       mpfr-devel%{?_isa}

%description devel
This package provides the headers files and tools to develop
SFCGAL applications.


%prep
%setup -q -n %{name}-v%{version}
%{__mkdir} build


%build
pushd build
%cmake3 ..
%make_build
popd


%install
pushd build
%make_install
popd


%check
CGAL_DIR=%{buildroot}%{_usr} %cmake3 -DSFCGAL_BUILD_TESTS=ON
%make_build
%ctest3


%files
%doc AUTHORS NEWS README.md
%license LICENSE
%{_libdir}/libSFCGAL.so.*

%files devel
%{_bindir}/sfcgal-config
%{_includedir}/SFCGAL
%{_libdir}/libSFCGAL.so
%{_libdir}/pkgconfig


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
