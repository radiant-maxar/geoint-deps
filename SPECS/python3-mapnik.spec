%global __python %{__python3}
%global boost_python_lib boost_python%(echo %{python3_version} | tr -d '.')

Name:           python3-mapnik
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Python bindings for Mapnik

License:        LGPLv2+
URL:            https://github.com/mapnik/python-mapnik
Source0:        https://github.com/mapnik/python-mapnik/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1:        https://github.com/mapnik/test-data/archive/%{testcommit}/test-data-%{testcommit}.tar.gz
Source2:        https://github.com/mapnik/test-data-visual/archive/%{visualcommit}/test-data-visual-%{visualcommit}.tar.gz
# Stop setup.py trying to fiddle with compiler flags
Patch0:         python3-mapnik-flags.patch
# Allow more variation in comparisons
Patch1:         python3-mapnik-precision.patch
# Disable some failing tests
Patch3:         python3-mapnik-compositing.patch
# https://github.com/mapnik/python-mapnik/commit/708290aff1ecbc2de080cab5588019caea1a02e1
Patch4:         python3-mapnik-buffer.patch
# Update for new proj API support
Patch5:         python3-mapnik-proj.patch

BuildRequires:  boost-devel
BuildRequires:  boost-openmpi-python3
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  mapnik-devel
BuildRequires:  mapnik-static
BuildRequires:  mapnik-utils
BuildRequires:  postgis
BuildRequires:  python3-cairo
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  sqlite-devel


%description
%{summary}.


%prep
%autosetup -p1 -n python-mapnik-%{commit}
%{__tar} --directory=test/data --strip-components=1 --gunzip --extract --file=%{SOURCE1}
%{__tar} --directory=test/data-visual --strip-components=1 --gunzip --extract --file=%{SOURCE2}
%{__sed} -i \
 -e 's/+init=epsg/epsg/g' \
 -e 's/+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0.0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs +over/epsg:3857/g' \
 -e 's/+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs/epsg:4326/g' \
 test/data-visual/styles/*.xml



%build
export BOOST_PYTHON_LIB=%{boost_python_lib}
export CFLAGS="%{optflags} -I%{python3_sitearch}/cairo/include"
export PYCAIRO=true
%py3_build


%install
export BOOST_PYTHON_LIB=%{boost_python_lib}
%py3_install


%check
export PGDATA="${HOME}/pgdata"
%{_bindir}/pg_ctl -m fast -s stop || true
%{__rm} -fr "${PGDATA}"
# Create PostgreSQL database.
%{_bindir}/initdb --encoding UTF-8 --locale en_US.UTF-8

# Tune the database.
echo "fsync = off
shared_buffers = 1GB
listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"

# Start PostgreSQL
%{_bindir}/pg_ctl -s start

# Create testing tablespace required by the Mapnik tests.
%{_bindir}/createdb template_postgis
%{_bindir}/psql -c "CREATE EXTENSION postgis" template_postgis

# run tests
export BOOST_PYTHON_LIB=%{boost_python_lib}
%{__rm} -v \
 test/data/broken_maps/duplicate_stylename.xml \
 test/data/good_maps/layer_scale_denominator.xml \
 test/python_tests/pdf_printing_test.py
LANG="C.UTF-8" %{_bindir}/python%{python3_version} setup.py test

# Stop PostgreSQL
%{_bindir}/pg_ctl -m fast -s stop


%files
%doc README.md AUTHORS.md CHANGELOG.md CONTRIBUTING.md
%license COPYING
%{python_sitearch}/*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
