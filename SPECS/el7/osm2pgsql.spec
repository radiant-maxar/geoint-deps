# The following macros are also required:
# * libosmium_min_version
# * nlohmann_json_version
# * postgis_min_version
# * postgres_version
# * proj_min_version
# * protobuf_c_min_version

%bcond_without db_tests

Name:           osm2pgsql
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Imports map data from OpenStreetMap to a PostgreSQL database

License:        GPLv2+
URL:            https://github.com/osm2pgsql-dev/osm2pgsql
Source0:        https://github.com/osm2pgsql-dev/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/nlohmann/json/releases/download/v%{nlohmann_json_version}/json.hpp
Patch0:         osm2pgsql-replication.patch

BuildRequires:  argparse-manpage
BuildRequires:  boost169-devel
BuildRequires:  bzip2-devel
BuildRequires:  cmake3
# A newer C++ toolchain and libosmium 2.17.0+ are required to compile 1.5.0+.
BuildRequires:  devtoolset-9-gcc
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  expat-devel
BuildRequires:  libosmium-devel >= %{libosmium_min_version}
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  lua-devel
BuildRequires:  luajit-devel
BuildRequires:  pandoc
BuildRequires:  postgresql%{postgres_version}-devel
BuildRequires:  proj-devel >= %{proj_min_version}
BuildRequires:  protobuf-c-devel >= %{protobuf_c_min_version}
BuildRequires:  zlib-devel
# Need PostgreSQL server, PostGIS, and Psycopg2 to run the tests.
%if %{with db_tests}
BuildRequires:  postgis >= %{postgis_min_version}
BuildRequires:  postgresql%{postgres_version}-contrib
BuildRequires:  postgresql%{postgres_version}-server
BuildRequires:  python3-psycopg2
%endif

%description
Processes the planet file from the community mapping project at
http://www.openstreetmap.org. The map data is converted from XML to a
database stored in PostgreSQL with PostGIS geospatial extensions. This
database may then be used to render maps with Mapnik or for other
geospatial analysis.

%package replication
Summary:        Update an osm2pgsql database with changes from a OSM replication server.
Requires:       %{name} = %{version}-%{release}
Requires:       python3-osmium
Requires:       python3-psycopg2

%description replication
This tool initialises the updating process by looking at the import file
or the newest object in the database. The state is then saved in a table
in the database. Subsequent runs download newly available data and apply
it to the database.


%prep
%autosetup -p1
%{__mkdir} build nlohmann
%{__mv} %{SOURCE1} nlohmann


%build
. /opt/rh/devtoolset-9/enable
pushd build
%cmake3 .. -G "Unix Makefiles" \
    -DBOOST_INCLUDEDIR:PATH=%{_includedir}/boost169 \
    -DBOOST_LIBRARYDIR:PATH=%{_libdir}/boost169 \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DBUILD_TESTS:BOOL=ON \
    -DCMAKE_BUILD_TYPE=Release \
    -DEXTERNAL_LIBOSMIUM:BOOL=ON \
    -DEXTERNAL_PROTOZERO:BOOL=ON \
    -DNLOHMANN_INCLUDE_DIR=.. \
    -DPostgreSQL_INCLUDE_DIR:PATH=$(pg_config --includedir) \
    -DPostgreSQL_LIBRARY:PATH=$(pg_config --libdir)/libpq.so \
    -DWITH_LUAJIT:BOOL=ON
%cmake3_build
popd


%check
pushd build
%if %{with db_tests}
export PGDATA="${HOME}/pgdata"
%{_bindir}/pg_ctl -m fast -s stop || true
%{__rm} -fr ${PGDATA} /tmp/psql-tablespace
# Create PostgreSQL database.
%{_bindir}/initdb --encoding UTF-8 --locale en_US.UTF-8

# Tune the database.
echo "fsync = off
shared_buffers = 1GB
listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"

# Start PostgreSQL
%{_bindir}/pg_ctl start

# Create testing tablespace required by the osm2pgsql tests.
%{__mkdir_p} /tmp/psql-tablespace
%{_bindir}/psql -d postgres -c "CREATE TABLESPACE tablespacetest LOCATION '/tmp/psql-tablespace'"

# Set the SMP flags so only one process is used for the tests, otherwise database
# connections will be exhausted resulting in test failures.
%global _smp_mflags -j1

# Run all tests.
%ctest3

# Stop PostgreSQL
%{_bindir}/pg_ctl -m fast -s stop
%else
# Run tests that don't require a database.
%ctest3 -L NoDB
%endif
popd


%install
pushd build
%cmake3_install
%{_bindir}/find %{buildroot} -name '*.la' -delete
popd


%files
%doc AUTHORS README.md
%license COPYING
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_datadir}/%{name}/

%files replication
%{_bindir}/osm2pgsql-replication
%{_mandir}/man1/osm2pgsql-replication.1*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
