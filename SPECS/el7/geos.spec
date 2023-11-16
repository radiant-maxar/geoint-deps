Name:           geos
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GEOS is a C++ port of the Java Topology Suite

License:        LGPLv2
URL:            https://trac.osgeo.org/geos/
Source0:        https://download.osgeo.org/%{name}/%{name}-%{version}%{?prerelease}.tar.bz2

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
Summary:	Development files for GEOS
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
%autosetup -p1 -n %{name}-%{version}%{?prerelease}


%build
%cmake3
%cmake3_build


%install
%cmake3_install


%check
%ctest3


%files
%doc AUTHORS README.md
%license COPYING
%{_libdir}/libgeos.so.%{version}
%{_libdir}/libgeos_c.so.1*
# New CLI utility is not ready for prime time, segfaults on usage errors;
# exclude it from the RPM.  See, e.g.:
#   https://trac.osgeo.org/geos/ticket/1126
%exclude %{_bindir}/geosop

%files devel
%{_bindir}/geos-config
%{_includedir}/geos/
%{_includedir}/geos.h
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
