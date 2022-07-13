Name:           g2clib
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GRIB2 encoder/decoder and search/indexing routines in C

License:        LGPLv3
URL:            https://github.com/NOAA-EMC/NCEPLIBS-g2c
Source0:        https://github.com/NOAA-EMC/NCEPLIBS-g2c/archive/v%{version}/%{name}-%{version}.tar.gz

# Patch from Wesley Ebisuzaki <wesley.ebisuzaki@noaa.gov> to fix sigfault
# if simunpack() is called with 0 values to unpack
Patch2:         g2clib-simunpack.patch
# Fix build with Jasper 2
Patch4:         g2clib-jasper2.patch
# jasper3 now hides internal encoder / decoder. Use wrapper entry point
# c.f. https://github.com/jasper-software/jasper/commit/5fe57ac5829ec31396e7eaab59a688da014660af
Patch5:         g2clib-1.6.3-jasper3-use-wrapper-entry-point.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  jasper-devel
BuildRequires:  libpng-devel

# static only library - no debuginfo
%global debug_package %{nil}
%global g2clib g2c

%description
This library contains "C" decoder/encoder
routines for GRIB edition 2.  The user API for the GRIB2 routines
is described in ASCII file "grib2c.doc".


%package        devel
Summary:        Development files for %{name}
#Requires:       %%{name} = %%{version}-%%{release}
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name}-static%{?_isa} = %{version}-%{release}
Requires:       jasper-devel%{?_isa}
Requires:       libpng-devel%{?_isa}

%description    devel
This library contains "C" decoder/encoder
routines for GRIB edition 2.  The user API for the GRIB2 routines
is described in file "grib2c.doc".

The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n NCEPLIBS-g2c-%{version}


%build
%cmake
%cmake_build


%check
%ctest


%install
%cmake_install
%{__install} -p -m0644 src/drstemplates.h %{buildroot}%{_includedir}
%{__install} -p -m0644 src/gridtemplates.h %{buildroot}%{_includedir}
%{__install} -p -m0644 src/pdstemplates.h %{buildroot}%{_includedir}
%{__mkdir_p} %{buildroot}%{_rpmconfigdir}/macros.d
echo %%g2clib %g2clib > %{buildroot}%{_rpmconfigdir}/macros.d/macros.g2clib


%files devel
%license LICENSE.md
%{_libdir}/cmake/%{g2clib}
%{_libdir}/lib%{g2clib}.a
%{_includedir}/grib2.h
%{_includedir}/drstemplates.h
%{_includedir}/gridtemplates.h
%{_includedir}/pdstemplates.h
%{_rpmconfigdir}/macros.d/macros.g2clib


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
