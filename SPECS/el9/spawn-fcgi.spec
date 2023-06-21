Name:           spawn-fcgi
Summary:        Simple program for spawning FastCGI processes
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}

License:        BSD
URL:            https://redmine.lighttpd.net/projects/spawn-fcgi/
Source0:        https://github.com/lighttpd/spawn-fcgi/archive/refs/tags/spawn-fcgi-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
This package contains the spawn-fcgi program used for spawning FastCGI
processes, which can be local or remote.


%prep
%autosetup -n spawn-fcgi-spawn-fcgi-%{version}


%build
./autogen.sh
%configure
%make_build


%install
%make_install


%files
%doc AUTHORS COPYING NEWS README.md
%{_bindir}/spawn-fcgi
%{_mandir}/man1/spawn-fcgi.1*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
