%global protobuf_min_version 2.6.0

Name:           protobuf-c
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        C bindings for Google's Protocol Buffers

License:        BSD
URL:            https://github.com/protobuf-c/protobuf-c
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  protobuf-devel >= %{protobuf_min_version}

%description
Protocol Buffers are a way of encoding structured data in an efficient yet
extensible format. This package provides a code generator and run-time
libraries to use Protocol Buffers from pure C (not C++).

It uses a modified version of protoc called protoc-c.

%package compiler
Summary:        Protocol Buffers C compiler
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description compiler
This package contains a modified version of the Protocol Buffers
compiler for the C programming language called protoc-c.

%package devel
Summary:        Protocol Buffers C headers and libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-compiler%{?_isa} = %{version}-%{release}

%description devel
This package contains protobuf-c headers and libraries.


%prep
%autosetup -q -p1


%build
%configure --disable-static
%make_build


%check
%{__make} check


%install
%make_install
%{__rm} -vf %{buildroot}/%{_libdir}/libprotobuf-c.la


%files
%{_libdir}/libprotobuf-c.so.*
%doc TODO LICENSE ChangeLog

%files compiler
%{_bindir}/protoc-c
%{_bindir}/protoc-gen-c

%files devel
%dir %{_includedir}/google
%{_includedir}/protobuf-c/
%{_includedir}/google/protobuf-c/
%{_libdir}/libprotobuf-c.so
%{_libdir}/pkgconfig/libprotobuf-c.pc


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
