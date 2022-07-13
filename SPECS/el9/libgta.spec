Name:          libgta
Version:       %{rpmbuild_version}
Release:       %{rpmbuild_release}%{?dist}
Summary:       Library that implements the Generic Tagged Arrays file format
License:       LGPLv2+
URL:           https://marlam.de/gta/
Source0:       https://marlam.de/gta/releases/%{name}-%{version}.tar.xz

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: doxygen

%description
Libgta is a portable library that implements the GTA (Generic Tagged Arrays)
file format. It provides interfaces for C and C++.


%package devel
Summary:  Development Libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%cmake -D GTA_BUILD_STATIC_LIB:BOOL=FALSE
%cmake_build


%install
%cmake_install
# remove documentation
rm -rf %{buildroot}%{_docdir}


%check
%ctest


%files
%doc COPYING AUTHORS README
%{_libdir}/%{name}.so.1
%{_libdir}/%{name}.so.1.*

%files devel
%{_libdir}/cmake/GTA-%{version}
%{_libdir}/pkgconfig/gta.pc
%{_includedir}/gta
%{_libdir}/%{name}.so


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
