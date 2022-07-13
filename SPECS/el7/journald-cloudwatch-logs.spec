# Original author was `ApsisInternational`, forked from `saymedia`.
%global github_author radiant-maxar

Name:           journald-cloudwatch-logs
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Sends systemd journal data to AWS CloudWatch

License:        BSD
URL:            https://github.com/%{github_author}/%{name}
Source0:        https://github.com/%{github_author}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  systemd-devel

Requires: systemd-libs


%description
This small utility monitors the systemd journal, managed by journald,
and writes journal entries into AWS CloudWatch Logs.

This program is an alternative to the AWS-provided logs agent. The official
logs agent copies data from on-disk text log files into CloudWatch,
while this utility reads directly from the systemd journal.


%prep
%autosetup
cd ${HOME}
# Unpack release archive into appropriate location in GOPATH and
# create link back to proper RPM build location.
%{__rm} -fr ${GOPATH}/src/github.com/%{github_author}/%{name}
%{__mkdir_p} ${GOPATH}/src/github.com/%{github_author}
%{__mv} -v %{_builddir}/%{name}-%{version} ${GOPATH}/src/github.com/%{github_author}/%{name}
%{__ln_s} ${GOPATH}/src/github.com/%{github_author}/%{name} %{_builddir}/%{name}-%{version}


%build
go build -v


%install
# Create directories.
%{__mkdir_p} %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_sysconfdir}
%{__mkdir_p} %{buildroot}%{_sharedstatedir}/%{name}
%{__mkdir_p} %{buildroot}%{_unitdir}

# Install binary.
%{__install} %{name} %{buildroot}%{_bindir}

# Config file.
cat <<EOF > %{buildroot}%{_sysconfdir}/%{name}.conf
# %{name} configuration
# log_group = "my-log-group"
state_file = "%{_sharedstatedir}/%{name}/state"
EOF

# Unit file.
cat <<EOF > %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=%{name}
After=basic.target network.target

[Service]
User=nobody
Group=systemd-journal
ExecStart=%{_bindir}/%{name} %{_sysconfdir}/%{name}.conf
KillMode=process
Restart=on-failure
RestartSec=30s

# Additional Protection
CapabilityBoundingSet=
NoNewPrivileges=yes
PrivateDevices=yes
PrivateTmp=true
ProtectHome=read-only
ProtectSystem=full
RestrictAddressFamilies=AF_UNIX AF_NETLINK AF_INET AF_INET6
%if 0%{?rhel} > 7
LockPersonality=yes
MemoryDenyWriteExecute=yes
ProtectControlGroups=true
ProtectKernelModules=true
ProtectKernelTunables=true
RestrictRealtime=true
RestrictSUIDSGID=true
%endif

[Install]
WantedBy=multi-user.target
EOF


%post
if test -f /.dockerenv; then exit 0; fi
%systemd_post %{name}.service


%preun
if test -f /.dockerenv; then exit 0; fi
%systemd_preun %{name}.service


%postun
if test -f /.dockerenv; then exit 0; fi
%systemd_postun %{name}.service


%files
%doc README.md
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%defattr(0640, nobody, systemd-journal, 0750)
%dir %{_sharedstatedir}/%{name}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
