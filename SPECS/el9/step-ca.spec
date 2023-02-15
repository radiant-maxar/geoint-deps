%global step_ca_home %{_sharedstatedir}/step-ca
%global step_ca_user step-ca
%global step_ca_group %{step_ca_user}
%global step_ca_uid 685
%global step_ca_gid %{step_ca_uid}

Name:           step-ca
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Private certificate authority (X.509 & SSH) & ACME server
License:        ASL 2.0
URL:            https://github.com/smallstep/certificates
Source0:        https://github.com/smallstep/certificates/archive/v%{version}/certificates-%{version}.tar.gz


%description
A private certificate authority (X.509 & SSH) & ACME server for secure automated certificate management, so you can use TLS everywhere & SSO for SSH.


%prep
%autosetup -n certificates-%{version}
cd "${HOME}"
%{__rm} -fr %{_builddir}/certificates-%{version}
%{__git} clone --single-branch -b v%{version} %{url} %{_builddir}/certificates-%{version}
cd %{_builddir}/certificates-%{version}


%build
%{__make} bootstrap
%{__make} download
%{__make} VERSION=v%{version} build


%install
%{__install} -d -m 0755 \
 %{buildroot}%{_bindir} \
 %{buildroot}%{_sysconfdir}/sysconfig \
 %{buildroot}%{_unitdir}
%{__install} -d -m 0700 %{buildroot}%{step_ca_home}
%{__install} -p \
 bin/step-ca \
 %{buildroot}%{_bindir}

# Environment file.
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/step-ca
STEPPATH=%{_sharedstatedir}/step-ca
EOF

# Unit file.
cat <<EOF > %{buildroot}%{_unitdir}/step-ca.service
[Unit]
Description=step-ca
After=basic.target network.target

[Service]
User=%{step_ca_user}
Group=%{step_ca_group}
EnvironmentFile=%{_sysconfdir}/sysconfig/step-ca
ExecStart=%{_bindir}/step-ca "\${STEPPATH}/config/ca.json"
KillMode=process
Restart=on-failure
RestartSec=30s

# Additional Protection
# Allow binding to :443 (only capability we allow).
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=yes
PrivateDevices=yes
PrivateTmp=true
ProtectHome=read-only
ProtectSystem=full
RestrictAddressFamilies=AF_UNIX AF_NETLINK AF_INET AF_INET6
LockPersonality=yes
MemoryDenyWriteExecute=yes
ProtectControlGroups=true
ProtectHostname=yes
ProtectKernelLogs=true
ProtectKernelTunables=true
ProtectKernelModules=true
RestrictRealtime=true
RestrictSUIDSGID=true
SystemCallArchitectures=native

[Install]
WantedBy=multi-user.target
EOF


%pre
getent group %{step_ca_group} >/dev/null || \
    groupadd \
        --force \
        --gid %{step_ca_gid} \
        --system \
        %{step_ca_group}

getent passwd %{step_ca_user} >/dev/null || \
    useradd \
        --uid %{step_ca_uid} \
        --gid %{step_ca_group} \
        --comment "Smallstep CA User" \
        --shell /sbin/nologin \
        --home-dir %{step_ca_home} \
        --no-create-home \
        --system \
        %{step_ca_user}


%check
export CI=true
%{__make} test


%files
%doc CHANGELOG.md README.md
%license LICENSE
%{_bindir}/step-ca
%{_unitdir}/step-ca.service
%config(noreplace) %{_sysconfdir}/sysconfig/step-ca
%defattr(-, %{step_ca_user}, %{step_ca_group}, -)
%dir %{step_ca_home}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
