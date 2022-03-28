# renderd service user details.
%global renderd_home %{_sharedstatedir}/mod_tile
%global renderd_user renderd
%global renderd_group renderd
%global renderd_uid 740


Name:          mod_tile
Version:       %{rpmbuild_version}
Release:       %{rpmbuild_release}%{?dist}
Summary:       A program to efficiently render and serve map tiles for www.openstreetmap.org map using Apache and Mapnik

License:       GPLv2
URL:           https://github.com/openstreetmap/mod_tile
Source0:       https://github.com/openstreetmap/mod_tile/archive/%{rpmbuild_version}/%{name}-%{rpmbuild_version}.tar.gz
Patch0:        mod_tile-20220328.patch

Requires:      httpd >= 2.4.6
Requires:      iniparser

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: glib2-devel
BuildRequires: httpd-devel
BuildRequires: iniparser-devel
BuildRequires: libcurl-devel
BuildRequires: libmemcached-devel
BuildRequires: mapnik-devel


%description
%{summary}.


%prep
%autosetup -p1
%{__mkdir_p} includes/iniparser
%{__ln_s} /usr/include/iniparser.h includes/iniparser/iniparser.h


%build
autoreconf -vfi
%configure
%__make


%install
%make_install
%__make install-mod_tile DESTDIR=%{buildroot}
%__install -d -m 0755 %{buildroot}%{renderd_home}
%__install -d -m 0755 %{buildroot}%{_rundir}/renderd
%__install -d -m 0755 %{buildroot}%{_sysconfdir}/httpd/conf.modules.d
echo "LoadModule tile_module modules/mod_tile.so" > %{buildroot}%{_sysconfdir}/httpd/conf.modules.d/11-tile.conf
# Basic configuration file for mod_tile.
%{__cat} > %{buildroot}%{_sysconfdir}/renderd.conf << EOF
[renderd]
num_threads=4
tile_dir=%{renderd_home}
stats_file=/run/renderd/renderd.stats

[mapnik]
plugins_dir=/usr/lib64/mapnik/input
font_dir=/usr/share/fonts
font_dir_recurse=1
EOF
# Example configuration file for mod_tile.
%{__cat} > mod_tile-example.conf << EOF
<VirtualHost *:80>
  ServerName localhost
  DocumentRoot /var/www/html

  LogLevel warn

  LoadTileConfigFile /etc/renderd.conf

  ModTileRenderdSocketAddr tile-backend 7654

  ModTileEnableStats On
  ModTileBulkMode Off
  ModTileRequestTimeout 3
  ModTileMissingRequestTimeout 10
  ModTileMaxLoadOld 16
  ModTileMaxLoadMissing 50
  ModTileVeryOldThreshold 31536000000000

  ModTileCacheDurationMax 604800
  ModTileCacheDurationDirty 900
  ModTileCacheDurationMinimum 10800
  ModTileCacheDurationMediumZoom 13 86400
  ModTileCacheDurationLowZoom 9 518400
  ModTileCacheLastModifiedFactor 0.20
  ModTileEnableTileThrottling Off
  ModTileEnableTileThrottlingXForward 0
  ModTileThrottlingTiles 10000 1
  ModTileThrottlingRenders 128 0.2
</VirtualHost>
EOF


%check
%__make test


%pre
getent group %{renderd_group} >/dev/null || \
    groupadd \
        --force \
        --gid %{renderd_uid} \
        --system \
        %{renderd_group}

getent passwd %{renderd_user} >/dev/null || \
    useradd \
        --uid %{renderd_uid} \
        --gid %{renderd_group} \
        --comment "Tile Rendering User" \
        --shell /sbin/nologin \
        --home-dir %{renderd_home} \
        --system \
        %{renderd_user}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc mod_tile-example.conf AUTHORS README.rst screenshot.jpg docs
%license COPYING
%{_sysconfdir}/httpd/conf.modules.d/11-tile.conf
%config(noreplace) %{_sysconfdir}/renderd.conf
%{_bindir}/render*
%{_mandir}/man1/render*
%{_libdir}/httpd/modules/mod_tile.so
%defattr(-, %{renderd_user}, apache, -)
%{renderd_home}
%defattr(-, %{renderd_user}, %{renderd_group}, -)
%{_rundir}/renderd


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
