# The following macros are also required:
# * libosmium_min_version
# * postgres_version
# * postgres_instdir
%bcond_without db_tests

Name:           osmdbt
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        OpenStreetMap database replication tools

License:        GPLv3
URL:            https://github.com/openstreetmap/%{name}
# The `commit` variable must be defined because the project doesn't use tags.
Source0:        https://github.com/openstreetmap/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz

Patch1:         osmdbt-boost-version.patch
Patch2:         osmdbt-boost-directory-iterator.patch
Patch3:         osmdbt-tests.patch

BuildRequires:  boost-devel
BuildRequires:  bzip2-devel
BuildRequires:  cmake3
# A newer C++ toolchain is required to compile.
BuildRequires:  devtoolset-9-gcc
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  expat-devel
BuildRequires:  gettext-devel
BuildRequires:  libosmium-devel >= %{libosmium_min_version}
BuildRequires:  libpqxx-devel
BuildRequires:  pandoc
BuildRequires:  postgresql%{postgres_version}-devel
BuildRequires:  yaml-cpp-devel
BuildRequires:  zlib-devel
# Need PostgreSQL server, PostGIS, and Psycopg2 to run the tests.
%if %{with db_tests}
BuildRequires:  postgresql%{postgres_version}-contrib
BuildRequires:  postgresql%{postgres_version}-server
%endif

# Ensure depends on PGDG libraries it was built with.
Requires:       postgresql%{postgres_version}-libs

%description
Tools for creating replication feeds from the main OSM database.


%package -n postgresql%{postgres_version}-osm-logical
License:        ASL 2.0
Summary:        PostgreSQL plugin for OpenStreetMap replication

# Ensure depends on PGDG server version it was built with.
Requires:       postgresql%{postgres_version}-server

%description -n postgresql%{postgres_version}-osm-logical
PostgreSQL plugin to support logical replication of OpenStreetMap API databases.


%prep
%autosetup -p1 -n %{name}-%{commit}
%{__mkdir_p} build


%build
# Enable the updated compiler toolchain prior to building.
. /opt/rh/devtoolset-9/enable
pushd build
%cmake3 \
    -DBOOST_INCLUDEDIR=/usr/include/boost \
    -DPROJECT_VERSION=%{version} \
    ..
%cmake3_build
popd


%check
%if %{with db_tests}
pushd build
# Run all tests, using a single process.
%global _smp_mflags -j1
%ctest3 -V
popd
%endif


%install
pushd build
%cmake3_install
popd
%{__install} -d %{buildroot}%{_sysconfdir}
%{__install} -m 0644 osmdbt-config.yaml %{buildroot}%{_sysconfdir}


%files
%doc README.md
%license LICENSE.txt
%config(noreplace) %{_sysconfdir}/osmdbt-config.yaml
%{_bindir}/%{name}-*
%{_mandir}/man1/*

%files -n postgresql%{postgres_version}-osm-logical
%doc postgresql-plugin/README.md
%license postgresql-plugin/LICENSE.md
%{_usr}/pgsql-%{postgres_version}/lib


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
