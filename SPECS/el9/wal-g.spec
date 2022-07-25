Name:           wal-g
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Archival and Restoration for Postgres

License:        ASL 2.0
URL:            https://github.com/%{name}/%{name}
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:         wal-g-postgresql15.patch


BuildRequires:  brotli-devel
BuildRequires:  libsodium-devel
BuildRequires:  lzo-devel


%description
WAL-G is an archival restoration tool for PostgreSQL.


%prep
%setup
# Building wal-g depends on a full git checkout, so do this after "tricking"
# rpmbuild everything is normal by using the `autosetup` macro.
cd "${HOME}"
%{__rm} -fr %{_builddir}/%{name}-%{version}
%{__git} clone --single-branch -b v%{rpmbuild_version} %{url} %{_builddir}/%{name}-%{version}
cd %{_builddir}/%{name}-%{version}
%autopatch -p1


%build
export USE_LIBSODIUM=1
export USE_LZO=1
# The error messages about Docker missing are fine since we're not running
# the integration tests.
%{__make} pg_clean
# The `go_deps` target patches cyberdelia/lzo/lzo.go with build flags
# that aren't appropriate, issue its other commands manually.
%{__git} submodule update --init
go mod vendor
# Make the PostgreSQL-specific `wal-g` target.
%{__make} pg_build


%install
%{__install} -p -d -m 0755 %{buildroot}%{_bindir}
GOBIN=%{buildroot}%{_bindir} %{__make} pg_install


%check
# Only run unit tests as the integration tests have extensive Docker
# test harnesses.
%{__make} unittest


%files
%license LICENSE.md
%doc docs/README.md docs/PostgreSQL.md
%{_bindir}/%{name}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
