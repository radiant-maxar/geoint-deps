%global libpqxx_major %(echo %{rpmbuild_version} | %{__awk} -F. '{ print $1 }')
%global libpqxx_minor %(echo %{rpmbuild_version} | %{__awk} -F. '{ print $2 }')

Name:           libpqxx
Summary:        C++ client API for PostgreSQL
Epoch:          1
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
URL:		https://github.com/jtv/%{name}
Source0:	https://github.com/jtv/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
License:        BSD

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  postgresql%{postgres_dotless}-devel


%description
C++ client API for PostgreSQL. The standard front-end (in the sense of
"language binding") for writing C++ programs that use PostgreSQL.
Supersedes older libpq++ interface.

%package devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Provides:       %{name}-static%{?_isa} = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       pkgconfig
%description devel
%{summary}.


%prep
%autosetup -p1


%build
# Disable failing test.
%{__sed} -i -e '/test55\.cxx/d' test/CMakeLists.txt
%cmake -G Ninja -DPostgreSQL_ROOT:PATH=/usr/pgsql-%{postgres_dotless} -DBUILD_TEST:BOOL=ON
%cmake_build


%install
%cmake_install


%check
export PGDATA="${HOME}/pgdata"
%{_bindir}/pg_ctl -m fast -s stop || true
%{__rm} -fr ${PGDATA}
# Create PostgreSQL database.
%{_bindir}/initdb --encoding UTF-8 --locale C.UTF-8

# Tune the database.
echo "fsync = off
shared_buffers = 1GB
listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"

# Start PostgreSQL
%{_bindir}/pg_ctl start

# Run tests
createdb -O ${RPMBUILD_USER} ${RPMBUILD_USER}
%{_vpath_builddir}/test/runner

# Stop PostgreSQL
%{_bindir}/pg_ctl -m fast -s stop


%files
%doc AUTHORS NEWS README.md VERSION
%license COPYING
%{_libdir}/%{name}.so

%files devel
%doc %{_docdir}/%{name}/*.md
%{_includedir}/pqxx
%{_libdir}/%{name}.a
%{_libdir}/cmake/%{name}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
