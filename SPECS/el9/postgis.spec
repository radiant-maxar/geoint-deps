# The following macros are also required:
# * gdal_min_version
# * geos_min_version
# * postgres_version
# * postgres_instdir
# * proj_min_version
# * protobuf_c_min_version
# * protobuf_min_version

%global postgis_major %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global postgis_minor %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global postgis_micro %(echo %{rpmbuild_version} | awk -F. '{ print $3 }')
%global postgis_majorversion %{postgis_major}.%{postgis_minor}
%global postgiscurrmajorversion %(echo %{postgis_majorversion}|tr -d '.')
%global sname postgis
%global postgisliblabel %{postgis_major}


Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:           postgis
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
License:        GPLv2+
Source0:        https://download.osgeo.org/%{name}/source/%{name}-%{version}%{?prerelease}.tar.gz
Source1:        https://download.osgeo.org/%{name}/docs/%{name}-%{version}%{?prerelease}-en.pdf
Source2:        postgis-filter-requires-perl-Pg.sh
Patch0:         postgis-3.4-gdalfpic.patch
Patch1:         postgis-fix-regress-delaunaytriangles.patch
# XXX: GML/KML test failures since PostgreSQL 15.5 / LLVM 17;
#      packages from PGDG exhibit same failures.
Patch2:         postgis-disable-xml-tests.patch

URL:		http://www.postgis.net/

BuildRequires:  ccache
BuildRequires:  flex
BuildRequires:  gdal-devel >= %{gdal_min_version}
BuildRequires:  geos-devel >= %{geos_min_version}
BuildRequires:  json-c-devel
BuildRequires:  libxml2-devel
BuildRequires:  pcre-devel
BuildRequires:  perl-Time-HiRes
BuildRequires:  proj-devel >= %{proj_min_version}
BuildRequires:  postgresql%{postgres_version}-devel
BuildRequires:  protobuf-devel >= %{protobuf_min_version}
BuildRequires:  protobuf-c-devel >= %{protobuf_c_min_version}
BuildRequires:  SFCGAL-devel

Provides:       %{name}%{postgiscurrmajorversion}_%{postgres_version}

Requires:       postgresql%{postgres_version}
Requires:       postgresql%{postgres_version}-contrib
Requires(post):	%{_sbindir}/update-alternatives

%description
PostGIS adds support for geographic objects to the PostgreSQL object-relational
database. In effect, PostGIS "spatially enables" the PostgreSQL server,
allowing it to be used as a backend spatial database for geographic information
systems (GIS), much like ESRI's SDE or Oracle's Spatial extension. PostGIS
follows the OpenGIS "Simple Features Specification for SQL" and has been
certified as compliant with the "Types and Functions" profile.

%package devel
Summary:        Development headers and libraries for PostGIS
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS

%description docs
The %{name}-docs package includes PDF documentation of PostGIS.

%package utils
Summary:	The utils for PostGIS
Requires:	%{name} = %{version}-%{release}
Requires:	perl-DBD-Pg

%description utils
The %{name}-utils package provides the utilities for PostGIS.


# Excludes requiring Perl PostgreSQL module packages.
%global __perl_requires %{SOURCE2}


%prep
%autosetup -p1 -n %{name}-%{version}%{?prerelease}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE1} .


%build
%configure \
    --enable-rpath \
    --bindir=%{postgres_instdir}/bin \
    --prefix=%{postgres_instdir} \
    --with-pgconfig=%{postgres_instdir}/bin/pg_config \
    --with-protobuf \
    --with-sfcgal=%{_bindir}/sfcgal-config
%make_build


%install
%make_install
%make_install -C utils
%make_install -C extensions

%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -m 0644 utils/*.pl %{buildroot}%{_datadir}/%{name}

%{__install} -d %{buildroot}%{_docdir}/%{name}-docs-%{version}
%{__install} -d %{buildroot}%{_docdir}/%{name}-utils-%{version}


%check
# Create PostgreSQL database.
export PGDATA="${HOME}/pgdata"
export TZ=Etc/UTC
%{_bindir}/pg_ctl -m fast -s stop || true
%{__rm} -fr ${PGDATA}
%{_bindir}/initdb --encoding UTF-8 --locale en_US.UTF-8

# Tune the database.
echo "fsync = off" >> "${PGDATA}/postgresql.conf"
echo "shared_buffers = 1GB" >> "${PGDATA}/postgresql.conf"
echo "listen_addresses = '127.0.0.1'" >> "${PGDATA}/postgresql.conf"

# Start PostgreSQL
%{_bindir}/pg_ctl -s start

# run tests
LANG="C.UTF-8" %{__make} check

# Stop PostgreSQL
%{_bindir}/pg_ctl -m fast -s stop


# Create alternatives entries for common binaries
%post
%{_sbindir}/update-alternatives --install /usr/bin/postgis postgis-postgis %{postgres_instdir}/bin/postgis %{postgres_version}0
%{_sbindir}/update-alternatives --install /usr/bin/postgis_restore postgis-postgis_restore %{postgres_instdir}/bin/postgis_restore %{postgres_version}0
%{_sbindir}/update-alternatives --install /usr/bin/pgsql2shp postgis-pgsql2shp %{postgres_instdir}/bin/pgsql2shp %{postgres_version}0
%{_sbindir}/update-alternatives --install /usr/bin/shp2pgsql postgis-shp2pgsql %{postgres_instdir}/bin/shp2pgsql %{postgres_version}0


# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
        # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
        %{_sbindir}/update-alternatives --remove postgis-postgis	 %{postgres_instdir}/bin/postgis
        %{_sbindir}/update-alternatives --remove postgis-postgis_restore %{postgres_instdir}/bin/postgis_restore
        %{_sbindir}/update-alternatives --remove postgis-pgsql2shp	 %{postgres_instdir}/bin/pgsql2shp
        %{_sbindir}/update-alternatives --remove postgis-shp2pgsql	 %{postgres_instdir}/bin/shp2pgsql
fi


%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.postgis doc/html loader/README.* doc/postgis.xml doc/ZMSgeoms.txt
%license LICENSE.TXT
%{postgres_instdir}/doc/extension/README.address_standardizer
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis_comments.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis_upgrade*.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/uninstall_postgis.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/legacy*.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/*topology*.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/*sfcgal*.sql
%attr(0755,root,root) %{postgres_instdir}/lib/postgis-%{postgisliblabel}.so
%{postgres_instdir}/share/extension/postgis-*.sql
%{postgres_instdir}/share/extension/postgis_sfcgal*.sql
%{postgres_instdir}/share/extension/postgis_sfcgal.control
%{postgres_instdir}/share/extension/postgis.control
%{postgres_instdir}/lib/postgis_topology-%{postgisliblabel}.so
%{postgres_instdir}/lib/address_standardizer-%{postgisliblabel}.so
%{postgres_instdir}/lib/bitcode/
%{postgres_instdir}/share/extension/address_standardizer*.sql
%{postgres_instdir}/share/extension/address_standardizer*.control
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/raster_comments.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/*rtpostgis*.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/uninstall_legacy.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/spatial*.sql
%{postgres_instdir}/lib/postgis_raster-%{postgisliblabel}.so
%{postgres_instdir}/lib/postgis_sfcgal-%{postgisliblabel}.so
%{postgres_instdir}/share/extension/postgis_raster-*.sql
%{postgres_instdir}/share/extension/postgis_raster.control
%{postgres_instdir}/share/extension/postgis_topology-*.sql
%{postgres_instdir}/share/extension/postgis_topology.control
%{postgres_instdir}/share/extension/postgis_tiger_geocoder*.sql
%{postgres_instdir}/share/extension/postgis_tiger_geocoder.control


%files devel
%defattr(0644,root,root)
%if 0%{postgis_major} < 3
%{_includedir}/liblwgeom.h
%{_includedir}/liblwgeom_topo.h
%{postgres_instdir}/lib/liblwgeom*.a
%{postgres_instdir}/lib/liblwgeom*.la
%endif


%files utils
%defattr(-,root,root)
%doc utils/README
%attr(0755,root,root) %{_datadir}/%{name}/*.pl
%attr(0755,root,root) %{postgres_instdir}/bin/pgsql2shp
%attr(0755,root,root) %{postgres_instdir}/bin/pgtopo_export
%attr(0755,root,root) %{postgres_instdir}/bin/pgtopo_import
%attr(0755,root,root) %{postgres_instdir}/bin/postgis
%attr(0755,root,root) %{postgres_instdir}/bin/postgis_restore
%attr(0755,root,root) %{postgres_instdir}/bin/raster2pgsql
%attr(0755,root,root) %{postgres_instdir}/bin/shp2pgsql


%files docs
%defattr(-,root,root)
%doc postgis-%{version}%{?prerelease}-en.pdf
%{_mandir}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
