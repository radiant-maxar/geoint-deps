%global caddy_config %{_sysconfdir}/caddy
%global caddy_home %{_sharedstatedir}/caddy
%global caddy_user caddy
%global caddy_group %{caddy_user}
%global caddy_uid 517
%global caddy_gid %{caddy_uid}

Name:           caddy
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Fast and extensible multi-platform HTTP/1-2-3 web server with automatic HTTPS
License:        ASL 2.0
URL:            https://github.com/caddyserver/caddy
Source0:        https://github.com/caddyserver/caddy/archive/v%{version}/caddy-%{version}.tar.gz

BuildRequires:  git

%description
Caddy is a powerful, extensible platform to serve your sites, services, and apps, written in Go.


%prep
%autosetup -n caddy-%{version}
cd "${HOME}"
%{__rm} -fr %{_builddir}/caddy-%{version}
%{__git} clone --single-branch -b v%{version} %{url} %{_builddir}/caddy-%{version}
cd %{_builddir}/caddy-%{version}


%build
%{__mkdir_p} caddy@%{version}
%{__install} cmd/caddy/main.go caddy@%{version}
pushd caddy@%{version}
go mod init caddy
go get -v
go build -v
popd


%install
%{__install} -d -m 0755 \
 %{buildroot}%{_bindir} \
 %{buildroot}%{_sysconfdir}/sysconfig \
 %{buildroot}%{_unitdir} \
 %{buildroot}%{_usr}/lib/tmpfiles.d
%{__install} -d -m 0750 \
 %{buildroot}%{caddy_home} \
 %{buildroot}%{_rundir}/caddy \
 %{buildroot}%{caddy_config}
%{__install} -p caddy@%{version}/caddy %{buildroot}%{_bindir}
echo "d %{_rundir}/%{name} 0750 %{caddy_user} %{caddy_group} -" > \
     %{buildroot}%{_usr}/lib/tmpfiles.d/caddy.conf

# Configuration files.
touch %{buildroot}%{_sysconfdir}/sysconfig/caddy \
      %{buildroot}%{caddy_config}/Caddyfile
chmod 0750 %{buildroot}%{_sysconfdir}/sysconfig/caddy

# Unit files.
cat <<EOF > %{buildroot}%{_unitdir}/caddy.service
[Unit]
Description=Caddy
Documentation=https://caddyserver.com/docs/
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=notify
User=%{caddy_user}
Group=%{caddy_group}
EnvironmentFile=%{_sysconfdir}/sysconfig/caddy
ExecStart=%{_bindir}/caddy run --environ --config %{caddy_config}/Caddyfile
ExecReload=%{_bindir}/caddy reload --config %{caddy_config}/Caddyfile --force
TimeoutStopSec=5s
LimitNOFILE=1048576
LimitNPROC=512
PrivateTmp=true
ProtectSystem=full
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > %{buildroot}%{_unitdir}/caddy-api.service
[Unit]
Description=Caddy
Documentation=https://caddyserver.com/docs/
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=notify
User=%{caddy_user}
Group=%{caddy_group}
EnvironmentFile=%{_sysconfdir}/sysconfig/caddy
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
go get -v
pushd cmd/caddy
go build -v
popd
go test -v


%pre
%{_bindir}/getent group %{caddy_group} >/dev/null || \
    groupadd \
        --force \
        --gid %{caddy_gid} \
        --system \
        %{caddy_group}

%{_bindir}/getent passwd %{caddy_user} >/dev/null || \
    useradd \
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


%files
%doc AUTHORS README.md
%license LICENSE
%{_bindir}/caddy
%{_unitdir}/caddy.service
%{_unitdir}/caddy-api.service
%{_usr}/lib/tmpfiles.d/caddy.conf
%defattr(-, root, %{caddy_group}, -)
%config(noreplace) %{caddy_config}/Caddyfile
%config(noreplace) %{_sysconfdir}/sysconfig/caddy
%defattr(-, %{caddy_user}, %{caddy_group}, -)
%dir %{_rundir}/caddy
%dir %{caddy_home}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
