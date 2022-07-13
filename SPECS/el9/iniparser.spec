Name:		iniparser
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:	C library for parsing "INI-style" files

License:	MIT
URL:		https://github.com/ndevilla/%{name}
Source0:	https://github.com/ndevilla/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:  make

%description
iniParser is an ANSI C library to parse "INI-style" files, often used to
hold application configuration information.

%package devel
Summary:	Header files, libraries and development documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -p1

%build
# remove library rpath from Makefile
%{__sed} -i 's|-Wl,-rpath -Wl,/usr/lib||g' Makefile
%{__sed} -i 's|-Wl,-rpath,/usr/lib||g' Makefile
# set the CFLAGS to Fedora standard
%{__sed} -i 's|^CFLAGS|CFLAGS = %{optflags} -fPIC\nNOCFLAGS|' Makefile
%make_build


%install
# iniParser doesn't have a 'make install' of its own :(
%{__install} -d %{buildroot}%{_includedir}/%{name} %{buildroot}%{_libdir}
%{__install} -m 0644 -t %{buildroot}%{_includedir}/%{name} src/dictionary.h src/iniparser.h
%{__ln_s} %{name}/dictionary.h %{buildroot}%{_includedir}/dictionary.h
%{__ln_s} %{name}/iniparser.h %{buildroot}%{_includedir}/iniparser.h
%{__install} -m 0755 -t %{buildroot}%{_libdir}/ libiniparser.so.1
%{__ln_s} libiniparser.so.1 %{buildroot}%{_libdir}/libiniparser.so


%check
%{__make} check


%files
%doc README.md INSTALL AUTHORS
%license LICENSE
%{_libdir}/libiniparser.so.1

%files devel
%license LICENSE
%{_libdir}/libiniparser.so
%{_includedir}/%{name}
%{_includedir}/*.h


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
