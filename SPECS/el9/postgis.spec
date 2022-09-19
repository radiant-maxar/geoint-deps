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

%{!?postgis_prev_version: %global postgis_prev_version 2.5.8}
%global postgis_prev_major %(echo %{postgis_prev_version} | awk -F. '{ print $1 }')
%global postgis_prev_minor %(echo %{postgis_prev_version} | awk -F. '{ print $2 }')
%global postgis_prev_micro %(echo %{postgis_prev_version} | awk -F. '{ print $3 }')
%global postgis_prev_majorversion %{postgis_prev_major}.%{postgis_prev_minor}
%global postgis_prev_dotless %(echo %{postgis_prev_majorversion}|tr -d '.')

%global sname postgis
%if 0%{postgis_major} >= 3
%global postgisliblabel %{postgis_major}
%else
%global postgisliblabel %{postgis_majorversion}
%endif

Summary:	Geographic Information Systems Extensions to PostgreSQL
Name:           postgis
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
License:        GPLv2+
Source0:        https://download.osgeo.org/%{name}/source/%{name}-%{version}%{?prerelease}.tar.gz
Source2:        https://download.osgeo.org/%{name}/docs/%{name}-%{version}%{?prerelease}.pdf
Source3:        https://download.osgeo.org/%{name}/source/%{name}-%{postgis_prev_version}.tar.gz
Source4:        postgis-filter-requires-perl-Pg.sh
Patch0:         postgis-3.1-gdalfpic.patch

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

Provides:       %{name}%{postgis_prev_dotless}_%{postgres_version} = %{version}-%{release}

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
Provides:       %{name}%{postgis_prev_dotless}_%{postgres_version}-devel = %{version}-%{release}

%description devel
The %{name}-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with PostGIS.

%package docs
Summary:	Extra documentation for PostGIS
Provides:	%{name}%{postgis_prev_dotless}_%{postgres_version}-docs = %{version}-%{release}

%description docs
The %{name}-docs package includes PDF documentation of PostGIS.

%package utils
Summary:	The utils for PostGIS
Requires:	%{name} = %{version}-%{release}
Requires:	perl-DBD-Pg
Provides:	%{name}%{postgis_prev_dotless}_%{postgres_version}-utils = %{version}-%{release}

%description utils
The %{name}-utils package provides the utilities for PostGIS.

%global __perl_requires %{SOURCE4}


%prep
%autosetup -p1 -n %{name}-%{version}%{?prerelease}
# Copy .pdf file to top directory before installing.
%{__cp} -p %{SOURCE2} .


%build
export LDFLAGS="$LDFLAGS -L%{postgres_instdir}/lib"
%configure \
    --enable-rpath --libdir=%{postgres_instdir}/lib \
    --with-pgconfig=%{postgres_instdir}/bin/pg_config \
    --with-protobuf \
    --with-sfcgal=%{_bindir}/sfcgal-config

%make_build LPATH=`%{postgres_instdir}/bin/pg_config --pkglibdir` shlib="%{name}.so"


%install
%make_install
%make_install -C utils
%make_install -C extensions

%{__install} -d %{buildroot}%{_datadir}/%{name}
%{__install} -m 0644 utils/*.pl %{buildroot}%{_datadir}/%{name}

%{__install} -d %{buildroot}%{_docdir}/%{name}-docs-%{version}
%{__install} -d %{buildroot}%{_docdir}/%{name}-utils-%{version}

# Create symlink of .so files to previous versions. PostGIS hackers said that this is safe:
%{__ln_s} %{postgres_instdir}/lib/postgis-%{postgisliblabel}.so %{buildroot}%{postgres_instdir}/lib/postgis-%{postgis_prev_majorversion}.so
%{__ln_s} %{postgres_instdir}/lib/postgis_topology-%{postgisliblabel}.so %{buildroot}%{postgres_instdir}/lib/postgis_topology-%{postgis_prev_majorversion}.so
%if 0%{postgis_major} >= 3
%{__ln_s} %{postgres_instdir}/lib/address_standardizer-%{postgisliblabel}.so %{buildroot}%{postgres_instdir}/lib/address_standardizer-%{postgis_prev_majorversion}.so
%else
%{__ln_s} %{postgres_instdir}/lib/rtpostgis-%{postgisliblabel}.so %{buildroot}%{postgres_instdir}/lib/rtpostgis-%{postgis_prev_majorversion}.so
%endif


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
%{_sbindir}/update-alternatives --install /usr/bin/pgsql2shp postgis-pgsql2shp %{postgres_instdir}/bin/pgsql2shp %{postgres_version}0
%{_sbindir}/update-alternatives --install /usr/bin/shp2pgsql postgis-shp2pgsql %{postgres_instdir}/bin/shp2pgsql %{postgres_version}0


# Drop alternatives entries for common binaries and man files
%postun
if [ "$1" -eq 0 ]
  then
        # Only remove these links if the package is completely removed from the system (vs.just being upgraded)
        %{_sbindir}/update-alternatives --remove postgis-pgsql2shp	%{postgres_instdir}/bin/pgsql2shp
        %{_sbindir}/update-alternatives --remove postgis-shp2pgsql	%{postgres_instdir}/bin/shp2pgsql
fi


%files
%defattr(-,root,root)
%doc COPYING CREDITS NEWS TODO README.postgis doc/html loader/README.* doc/postgis.xml doc/ZMSgeoms.txt
%license LICENSE.TXT
%{postgres_instdir}/doc/extension/README.address_standardizer
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis_comments.sql
%if 0%{postgis_major} < 3
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis_for_extension.sql
%endif
%if 0%{postgis_major} == 3
%if 0%{postgis_minor} < 1
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis_proc_set_search_path.sql
%endif
%endif
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis_upgrade*.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/postgis_restore.pl
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/uninstall_postgis.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/legacy*.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/*topology*.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/*sfcgal*.sql
%{postgres_instdir}/lib/postgis-%{postgis_prev_majorversion}.so
%attr(0755,root,root) %{postgres_instdir}/lib/postgis-%{postgisliblabel}.so
%{postgres_instdir}/share/extension/postgis-*.sql
%{postgres_instdir}/share/extension/postgis_sfcgal*.sql
%{postgres_instdir}/share/extension/postgis_sfcgal.control
%{postgres_instdir}/share/extension/postgis.control
%if 0%{postgis_major} < 3
%{postgres_instdir}/lib/liblwgeom*.so.*
%{postgres_instdir}/lib/liblwgeom.so
%endif
%{postgres_instdir}/lib/postgis_topology-%{postgisliblabel}.so
%{postgres_instdir}/lib/postgis_topology-%{postgis_prev_majorversion}.so
%if 0%{postgis_major} >= 3
%{postgres_instdir}/lib/address_standardizer-%{postgisliblabel}.so
%{postgres_instdir}/lib/address_standardizer-%{postgis_prev_majorversion}.so
%if 0%{postgis_major} == 3
%if 0%{postgis_minor} >= 1
%{postgres_instdir}/lib/bitcode/
%endif
%endif
%else
%{postgres_instdir}/lib/address_standardizer.so
%endif
%{postgres_instdir}/share/extension/address_standardizer*.sql
%{postgres_instdir}/share/extension/address_standardizer*.control
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/raster_comments.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/*rtpostgis*.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/uninstall_legacy.sql
%{postgres_instdir}/share/contrib/postgis-%{postgis_majorversion}/spatial*.sql
%if 0%{postgis_major} >= 3
%{postgres_instdir}/lib/postgis_raster-%{postgisliblabel}.so
%{postgres_instdir}/lib/postgis_sfcgal-%{postgisliblabel}.so
%{postgres_instdir}/share/extension/postgis_raster-*.sql
%{postgres_instdir}/share/extension/postgis_raster.control
%else
%{postgres_instdir}/lib/rtpostgis-%{postgisliblabel}.so
%{postgres_instdir}/lib/rtpostgis-%{postgis_prev_majorversion}.so
%endif
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
%attr(0755,root,root) %{postgres_instdir}/bin/raster2pgsql
%attr(0755,root,root) %{postgres_instdir}/bin/shp2pgsql


%files docs
%defattr(-,root,root)
%doc postgis-%{version}%{?prerelease}.pdf


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
