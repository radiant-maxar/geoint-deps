# The following macros are also required:
# * data_version
# * googletest_version

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
Source3:        https://github.com/google/googletest/archive/release-%{googletest_version}.zip

BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  libtiff-devel
BuildRequires:  sqlite-devel

Requires:       sqlite

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


%package data-europe
Summary:        Compat package for old proj-datumgrid-europe
BuildArch:      noarch
Obsoletes:      proj-datumgrid-europe < 1.6-3
Provides:       deprecated()
Requires:       proj-data-at
Requires:       proj-data-be
Requires:       proj-data-ch
Requires:       proj-data-de
Requires:       proj-data-dk
Requires:       proj-data-es
Requires:       proj-data-eur
Requires:       proj-data-fi
Requires:       proj-data-fo
Requires:       proj-data-fr
Requires:       proj-data-is
Requires:       proj-data-nl
Requires:       proj-data-pl
Requires:       proj-data-pt
Requires:       proj-data-se
Requires:       proj-data-sk
Requires:       proj-data-uk

%description data-europe
Compat package for old proj-datumgrid-europe.
Please do not depend on this package, it will get removed!

%files data-europe


%package data-north-america
Summary:        Compat package for old proj-datumgrid-north-america
BuildArch:      noarch
Obsoletes:      proj-datumgrid-north-america < 1.4-3
Provides:       deprecated()
Requires:       proj-data-ca
Requires:       proj-data-us

%description data-north-america
Compat package for old proj-datumgrid-north-america.
Please do not depend on this package, it will get removed!

%files data-north-america


%package data-oceania
Summary:        Compat package for old proj-datumgrid-oceania
BuildArch:      noarch
Obsoletes:      proj-datumgrid-oceania < 1.2-3
Provides:       deprecated()
Requires:       proj-data-au
Requires:       proj-data-nc
Requires:       proj-data-nz

%description data-oceania
Compat package for old proj-datumgrid-oceania.
Please do not depend on this package, it will get removed!

%files data-oceania


%package data-world
Summary:        Compat package for old proj-datumgrid-world
BuildArch:      noarch
Obsoletes:      proj-datumgrid-world < 1.0-5
Provides:       deprecated()
Requires:       proj-data-br
Requires:       proj-data-jp

%description data-world
Compat package for old proj-datumgrid-world.
Please do not depend on this package, it will get removed!

%files data-world



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
%data_subpkg -c mx -n Mexico
%data_subpkg -c no -n Norway
%data_subpkg -c nc -n New\ Caledonia
%data_subpkg -c nl -n Netherlands
%data_subpkg -c nz -n New\ Zealand
%data_subpkg -c pl -n Poland
%data_subpkg -c pt -n Portugal
%data_subpkg -c se -n Sweden
%data_subpkg -c sk -n Slovakia
%data_subpkg -c uk -n United\ Kingdom
%data_subpkg -c us -n United\ States
%data_subpkg -c za -n South\ Africa


%prep
pushd %{_sourcedir}
%{_bindir}/md5sum -c %{SOURCE1}
popd

%autosetup -p1

# We download the googletest release, not CMake.
%{__mkdir_p} build/googletest-download/googletest-prefix/src
%{__cp} %{SOURCE3} build/googletest-download/googletest-prefix/src/release-%{googletest_version}.zip


%build
%cmake
%cmake_build


%install
%cmake_install

# Install data
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__tar} -xf %{SOURCE2} --directory %{buildroot}%{_datadir}/%{name}


%check
# nkg test is flaky
%ctest -- -E nkg


%files
%doc README.md
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/NEWS
%license %{_docdir}/%{name}/COPYING
%{_bindir}/cct
%{_bindir}/cs2cs
%{_bindir}/geod
%{_bindir}/gie
%{_bindir}/invgeod
%{_bindir}/invproj
%{_bindir}/proj
%{_bindir}/projinfo
%{_bindir}/projsync
%{_libdir}/libproj.so.25*
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
%{_mandir}/man1/*.1*

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
