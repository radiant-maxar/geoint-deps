Name:		dumb-init
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:	Simple process supervisor and init system for containers
License:	MIT
URL:		https://github.com/Yelp/dumb-init
Source0:	https://github.com/Yelp/dumb-init/archive/v%{version}/dumb-init-%{version}.tar.gz


%description
dumb-init is a simple process supervisor that forwards signals to children,
and designed to run as PID 1 in minimal container environments.


%prep
%setup -q


%build
# Use rpmbuild's optflags.
%{__sed} -i -e 's/^CFLAGS=/CFLAGS\ \?=\ /' Makefile
CFLAGS="%{optflags}" %make_build


%install
%{__install} -p -D -m 0755 dumb-init %{buildroot}%{_bindir}/dumb-init


%files
%doc CONTRIBUTING.md README.md
%license LICENSE
%{_bindir}/dumb-init


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
