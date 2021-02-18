%global datumgrid_version 1.8

Name:           proj
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Cartographic projection software (PROJ)
License:        MIT
URL:            https://proj4.org
Source0:        https://github.com/OSGeo/PROJ/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/OSGeo/proj-datumgrid/releases/download/%{datumgrid_version}/proj-datumgrid-%{datumgrid_version}.tar.gz

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  sqlite-devel

Provides:       proj-epsg = %{version}-%{release}
Requires:       proj-datumgrid = %{datumgrid_version}-%{release}

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions.


%package devel
Summary:        Development files for PROJ
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-static < 6.3.2

%description devel
This package contains libproj and the appropriate header files and man pages.

%package datumgrid
Summary:        Additional datum shift grids for PROJ
Version:        %{datumgrid_version}
# See README.DATUMGRID
License:        CC-BY and Freely Distributable and Ouverte and Public Domain
BuildArch:      noarch

Provides:       proj-nad = %{version}-%{release}

%description datumgrid
This package contains additional datum shift grids.


%prep
%autosetup -p1

# Prepare datumgrid and file list (in {datadir}/proj and README marked as doc)
%{__tar} xvf %{SOURCE1} -C data | \
    %{__sed} -e 's!^!%{_datadir}/%{name}/!' -e '/README/s!^!%%doc !' > datumgrid.files


%build
%cmake3
%cmake3_build


%install
%cmake3_install
%{__install} -p -m 0644 \
 data/{alaska,conus,hawaii,ntv1_can.dat,prvi,stgeorge,stlrnc,stpaul,FL,MD,TN,WI,README.DATUMGRID} \
 %{buildroot}%{_datadir}/%{name}
# Generate pkgconfig file cause CMake was used instead of autotools.
%{__install} -d -m 0755 %{buildroot}%{_libdir}/pkgconfig
%{__cat} > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}
datadir=%{_datadir}/%{name}

Name: %{name}
Description: Coordinate transformation software library
Requires:
Version: %{version}
Libs: -L\${libdir} -lproj
Libs.Private: -lsqlite3   -lstdc++
Cflags: -I\${includedir}
EOF


%check
%ctest3


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc NEWS AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_libdir}/libproj.so.18*
%{_datadir}/%{name}/CH
%{_datadir}/%{name}/GL27
%{_datadir}/%{name}/ITRF2000
%{_datadir}/%{name}/ITRF2008
%{_datadir}/%{name}/ITRF2014
%{_datadir}/%{name}/nad.lst
%{_datadir}/%{name}/nad27
%{_datadir}/%{name}/nad83
%{_datadir}/%{name}/null
%{_datadir}/%{name}/other.extra
%{_datadir}/%{name}/proj.db
%{_datadir}/%{name}/world

%files devel
%{_mandir}/man3/*.3*
%{_includedir}/*.h
%{_includedir}/%{name}/*.hpp
%{_libdir}/libproj.so
%{_libdir}/pkgconfig/
%{_libdir}/cmake/proj4/


%files datumgrid -f datumgrid.files
%dir %{_datadir}/%{name}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
