Name:           geos
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GEOS is a C++ port of the Java Topology Suite

License:        LGPLv2
URL:            https://trac.osgeo.org/geos/
Source0:        https://download.osgeo.org/%{name}/%{name}-%{version}.tar.bz2
# File missing in tarball
Source1:        geos-check_doxygen_errors.cmake

# Honor libsuffix
Patch1:         geos-libsuffix.patch

BuildRequires:  cmake3
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool

%description
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid().

%package devel
Summary:        Development files for GEOS
Requires:       %{name} = %{version}-%{release}

%description devel
GEOS (Geometry Engine - Open Source) is a C++ port of the Java Topology
Suite (JTS). As such, it aims to contain the complete functionality of
JTS in C++. This includes all the OpenGIS "Simple Features for SQL" spatial
predicate functions and spatial operators, as well as specific JTS topology
functions such as IsValid().

This package contains the development files to build applications that
use GEOS.

%prep
%autosetup -p1
%{__cp} -a %{SOURCE1} doc/check_doxygen_errors.cmake


%build
%cmake3 \
%ifarch armv7hl
    -DDISABLE_GEOS_INLINE=ON \
%endif
    -DBUILD_DOCUMENTATION=ON
%cmake3_build


%install
%cmake3_install
make docs -C %{__cmake3_builddir}


%check
%ctest3


%files
%doc AUTHORS NEWS README.md
%license COPYING
%{_libdir}/libgeos.so.%{version}
%{_libdir}/libgeos_c.so.1*


%files devel
%doc %{__cmake3_builddir}/doc/doxygen_docs
%{_bindir}/geos-config
%{_includedir}/geos/
%{_includedir}/geos_c.h
%{_libdir}/libgeos_c.so
%{_libdir}/libgeos.so
%{_libdir}/cmake/GEOS/
%{_libdir}/pkgconfig/%{name}.pc


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
