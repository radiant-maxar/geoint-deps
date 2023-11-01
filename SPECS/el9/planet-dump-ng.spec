# The following macros are also required:
# * protobuf_min_version

Name:           planet-dump-ng
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Tool for converting an OpenStreetMap database dump into planet files.
License:        BSD
URL:            https://github.com/zerebubuth/%{name}
Source0:        https://github.com/zerebubuth/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  automake
BuildRequires:  boost-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libxml2-devel
BuildRequires:  libosmpbf-devel
BuildRequires:  protobuf >= %{protobuf_min_version}
BuildRequires:  protobuf-devel >= %{protobuf_min_version}
BuildRequires:  protobuf-lite >= %{protobuf_min_version}
BuildRequires:  protobuf-lite-devel >= %{protobuf_min_version}


%description
Tool for converting an OpenStreetMap database dump into planet files.

By operating on the database dump rather than a running server, this means that running the extraction from PostgreSQL dump file to planetfile(s) is completely independent of the database server, and can be done on a disconnected machine without putting any load on any database.


%prep
%autosetup -p1 -n %{name}-%{version}


%build
# XXX: Patch in current version
%{__sed} -i -e 's/1\.2\.4/%{version}/g' configure.ac
./autogen.sh
%configure
%make_build


%install
%make_install


%files
%doc README.md
%license COPYING
%{_bindir}/planet-dump-ng


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
