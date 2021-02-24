Name:           python-mapnik
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Python bindings for Mapnik

License:        LGPLv2+
URL:            https://github.com/mapnik/python-mapnik
Source0:        https://github.com/mapnik/python-mapnik/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1:        https://github.com/mapnik/test-data/archive/v%{version}/test-data-v%{version}.tar.gz
Source2:        https://github.com/mapnik/test-data-visual/archive/v%{version}/test-data-visual-v%{version}.tar.gz
# The expected version of white0.webp from the repository varies from what this system produces
Source3:        python-mapnik-white0.webp
# Update test results for proj 6.x
Patch0:         python-mapnik-proj6.patch
# Another proj 6.x test results patch
Patch1:         python-mapnik-proj6-b.patch
# CSV datasource plugin is not supported with Mapnik's Boost version
# *** "WARNING: skipping building the optional CSV datasource plugin which requires boost >= 1.56"
Patch2:         python-mapnik-csv-unsupported.patch
Patch3:         python-mapnik-fix-postgis-test.patch

BuildRequires:  boost-devel
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  mapnik-devel
BuildRequires:  mapnik-static
BuildRequires:  mapnik-utils
BuildRequires:  postgis
BuildRequires:  pycairo-devel
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-nose

Provides:       python2-mapnik


%description
%{summary}.


%prep
%autosetup -p1 -n %{name}-%{commit}
tar --directory=test/data --strip-components=1 --gunzip --extract --file=%{SOURCE1}
tar --directory=test/data-visual --strip-components=1 --gunzip --extract --file=%{SOURCE2}
cp %{SOURCE1} test/python_tests/images/support/transparency/white0.webp


%build
export PYCAIRO=true
%py_build


%install
%py_install


%check
export PGDATA="$HOME/pgdata"
pg_ctl -m fast -s stop || true
%{__rm} -fr "${PGDATA}"
# Create PostgreSQL database.
initdb --encoding UTF-8 --locale en_US.UTF-8

# Tune the database.
echo "fsync = off" >> "$HOME/pgdata/postgresql.conf"
echo "shared_buffers = 1GB" >> "$HOME/pgdata/postgresql.conf"
echo "listen_addresses = '127.0.0.1'" >> "$HOME/pgdata/postgresql.conf"

# Start PostgreSQL
pg_ctl -s start

# Create testing tablespace required by the Mapnik tests.
createdb template_postgis
psql -c "CREATE EXTENSION postgis" template_postgis

# run tests
rm test/python_tests/pdf_printing_test.py
LANG="C.UTF-8" %{__python} setup.py test

# Stop PostgreSQL
pg_ctl -m fast -s stop


%files
%doc README.md AUTHORS.md CHANGELOG.md CONTRIBUTING.md
%license COPYING
%{python_sitearch}/*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
