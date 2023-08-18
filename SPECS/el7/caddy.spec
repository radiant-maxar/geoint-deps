%global caddy_config %{_sysconfdir}/caddy
%global caddy_home %{_sharedstatedir}/caddy
%global caddy_run %{_rundir}/caddy
%global caddy_user caddy
%global caddy_group %{caddy_user}
%global caddy_uid 517
%global caddy_gid %{caddy_uid}

Name:           caddy
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Fast and extensible multi-platform HTTP/1-2-3 web server with automatic HTTPS
License:        ASL 2.0 and MIT and BSD
URL:            https://github.com/caddyserver/caddy
Source0:        https://github.com/caddyserver/caddy/archive/v%{version}/caddy-%{version}.tar.gz
Patch0:         caddy-no-binary-mods.patch


%description
Caddy is a powerful, extensible platform to serve your sites, services, and apps, written in Go.


%prep
%autosetup -p1


%build
export CGO_CFLAGS="%{optflags}"
export CGO_LDFLAGS="%{?build_ldflags}"
go build \
 -ldflags '-X github.com/caddyserver/caddy/v2.CustomVersion=v%{version}' \
 -o cmd/caddy/caddy \
 -v \
 ./cmd/caddy


%install
%{__install} -d -m 0755 \
 %{buildroot}%{_bindir} \
 %{buildroot}%{_sysconfdir}/sysconfig \
 %{buildroot}%{_unitdir} \
 %{buildroot}%{_usr}/lib/tmpfiles.d
%{__install} -d -m 0750 \
 %{buildroot}%{caddy_home} \
 %{buildroot}%{caddy_run} \
 %{buildroot}%{caddy_config}
%{__install} -p cmd/caddy/caddy %{buildroot}%{_bindir}
echo "d %{caddy_run} 0750 %{caddy_user} %{caddy_group} -" > \
     %{buildroot}%{_usr}/lib/tmpfiles.d/caddy.conf

# Configuration files.
echo "{}" > %{buildroot}%{caddy_config}/config.json
touch %{buildroot}%{caddy_config}/Caddyfile

# Environment file.
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/%{name}
CADDY_CONFIG_FILE=%{caddy_config}/Caddyfile
EOF
chmod 0750 %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Unit files.
cat <<EOF > %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=Caddy
Documentation=https://caddyserver.com/docs/
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=notify
User=%{caddy_user}
Group=%{caddy_group}
EnvironmentFile=%{_sysconfdir}/sysconfig/%{name}
ExecStart=%{_bindir}/caddy run --environ --config \${CADDY_CONFIG_FILE}
ExecReload=%{_bindir}/caddy reload --config \${CADDY_CONFIG_FILE} --force
TimeoutStopSec=5s
LimitNOFILE=1048576
LimitNPROC=512
PrivateTmp=true
ProtectSystem=full
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > %{buildroot}%{_unitdir}/%{name}-api.service
[Unit]
Description=Caddy
Documentation=https://caddyserver.com/docs/
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=notify
User=%{caddy_user}
Group=%{caddy_group}
EnvironmentFile=%{_sysconfdir}/sysconfig/%{name}
ExecStart=%{_bindir}/caddy run --environ --resume
TimeoutStopSec=5s
LimitNOFILE=1048576
LimitNPROC=512
PrivateTmp=true
ProtectSystem=full
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOF


%check
export CGO_CFLAGS="%{optflags}"
export CGO_LDFLAGS="%{?build_ldflags}"
go test -v ./...
# Test version number
if [ "$(cmd/caddy/caddy version)" != "v%{version}" ]; then
    exit 1
fi


%pre
%{_bindir}/getent group %{caddy_group} >/dev/null || \
    %{_sbindir}/groupadd \
        --force \
        --gid %{caddy_gid} \
        --system \
        %{caddy_group}

%{_bindir}/getent passwd %{caddy_user} >/dev/null || \
    %{_sbindir}/useradd \
        --uid %{caddy_uid} \
        --gid %{caddy_group} \
        --comment "Caddy web user" \
        --shell %{_sbindir}/nologin \
        --home-dir %{caddy_home} \
        --no-create-home \
        --system \
        %{caddy_user}


%post
%{_sbindir}/setcap cap_net_bind_service=+ep %{_bindir}/caddy
if test -f /.dockerenv; then exit 0; fi
%systemd_post %{name}.service
%systemd_post %{name}-api.service


%preun
if test -f /.dockerenv; then exit 0; fi
%systemd_preun %{name}.service
%systemd_preun %{name}-api.service


%postun
if test -f /.dockerenv; then exit 0; fi
%systemd_postun %{name}.service
%systemd_postun %{name}-api.service


%files
%doc AUTHORS README.md
%license LICENSE
%{_bindir}/caddy
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-api.service
%{_usr}/lib/tmpfiles.d/caddy.conf
%defattr(-, root, %{caddy_group}, -)
%config(noreplace) %{caddy_config}/Caddyfile
%config(noreplace) %{caddy_config}/config.json
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%defattr(-, %{caddy_user}, %{caddy_group}, -)
%dir %{caddy_run}
%dir %{caddy_home}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
