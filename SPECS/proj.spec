%global data_version 1.4

Name:           proj
# Also check whether there is a new proj-data release when upgrading!
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Cartographic projection software (PROJ)

License:        MIT
URL:            https://proj.org
Source0:        https://github.com/OSGeo/PROJ/releases/download/%{version}/proj-%{version}.tar.gz
Source1:        https://github.com/OSGeo/PROJ/releases/download/%{version}/proj-%{version}.tar.gz.md5
Source2:        https://github.com/OSGeo/PROJ-data/releases/download/%{data_version}.0/proj-data-%{data_version}.tar.gz

# Ship a pkgconfig file
Patch0:         proj-pkgconfig.patch

BuildRequires:  cmake3
BuildRequires:  curl-devel
BuildRequires:  devtoolset-9-gcc
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  make
BuildRequires:  libtiff-devel
BuildRequires:  sqlite-devel

Obsoletes:      proj-datumgrid

%description
Proj and invproj perform respective forward and inverse transformation of
cartographic data to or from cartesian data with a wide range of selectable
projection functions.


%package devel
Summary:        Development files for PROJ
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-static < 7.2.0

%description devel
This package contains libproj and the appropriate header files and man pages.


%define data_subpkg(c:n:e:s:) \
%define countrycode %{-c:%{-c*}}%{!-c:%{error:Country code not defined}} \
%define countryname %{-n:%{-n*}}%{!-n:%{error:Country name not defined}} \
%define extrafile %{-e:%{_datadir}/%{name}/%{-e*}} \
%define wildcard %{!-s:%{_datadir}/%{name}/%{countrycode}_*} \
\
%package data-%{countrycode}\
Summary:      %{countryname} datum grids for Proj\
BuildArch:    noarch\
# See README.DATA \
License:      CC-BY and MIT and BSD and Public Domain \
\
%description data-%{countrycode}\
%{countryname} datum grids for Proj.\
\
%files data-%{countrycode}\
%{wildcard}\
%{extrafile}


%data_subpkg -c at -n Austria
%data_subpkg -c au -n Australia
%data_subpkg -c be -n Belgium
%data_subpkg -c br -n Brasil
%data_subpkg -c ca -n Canada
%data_subpkg -c ch -n Switzerland
%data_subpkg -c de -n Germany
%data_subpkg -c dk -n Denmark -e DK
%data_subpkg -c es -n Spain
%data_subpkg -c eur -n Nordic\ +\ Baltic -e NKG
%data_subpkg -c fi -n Finland
%data_subpkg -c fo -n Faroe\ Island -e FO -s 1
%data_subpkg -c fr -n France
%data_subpkg -c is -n Island -e ISL
%data_subpkg -c jp -n Japan
%data_subpkg -c nc -n New\ Caledonia
%data_subpkg -c nl -n Netherlands
%data_subpkg -c nz -n New\ Zealand
%data_subpkg -c pt -n Portugal
%data_subpkg -c se -n Sweden
%data_subpkg -c sk -n Slovakia
%data_subpkg -c uk -n United\ Kingdom
%data_subpkg -c us -n United\ States


%prep
pushd %{_sourcedir}
%{_bindir}/md5sum -c %{SOURCE1}
popd
%autosetup -p1


%build
# Enable the updated compiler toolchain prior to building.
. /opt/rh/devtoolset-9/enable
%cmake3
%cmake3_build


%install
%cmake3_install

# Install data
mkdir -p %{buildroot}%{_datadir}/%{name}
tar -xf %{SOURCE2} --directory %{buildroot}%{_datadir}/%{name}


%check
%ctest3


%files
%license COPYING
%doc NEWS AUTHORS README.md
%{_bindir}/cct
%{_bindir}/cs2cs
%{_bindir}/geod
%{_bindir}/gie
%{_bindir}/proj
%{_bindir}/projinfo
%{_bindir}/projsync
%{_libdir}/libproj.so.21*
%{_libdir}/libproj.so.19
%{_mandir}/man1/*.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/CH
%{_datadir}/%{name}/GL27
%{_datadir}/%{name}/ITRF2000
%{_datadir}/%{name}/ITRF2008
%{_datadir}/%{name}/ITRF2014
%{_datadir}/%{name}/nad.lst
%{_datadir}/%{name}/nad27
%{_datadir}/%{name}/nad83
%{_datadir}/%{name}/other.extra
%{_datadir}/%{name}/proj.db
%{_datadir}/%{name}/proj.ini
%{_datadir}/%{name}/world
%{_datadir}/%{name}/README.DATA
%{_datadir}/%{name}/copyright_and_licenses.csv
%{_datadir}/%{name}/deformation_model.schema.json
%{_datadir}/%{name}/projjson.schema.json
%{_datadir}/%{name}/triangulation.schema.json

%files devel
%{_includedir}/*.h
%{_includedir}/proj/
%{_libdir}/libproj.so
%{_libdir}/cmake/proj/
%{_libdir}/cmake/proj4/
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
