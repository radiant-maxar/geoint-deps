Name:           sbt
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        The simple build tool for Scala and Java projects

BuildArch:      noarch

License:        ASL 2.0
URL:            http://www.scala-sbt.org
Source0:        https://github.com/sbt/sbt/releases/download/v%{version}/sbt-%{version}.tgz
Source1:        https://github.com/sbt/sbt/releases/download/v%{version}/sbt-%{version}.tgz.sha256
Source2:        https://github.com/sbt/sbt/releases/download/v%{version}/sbt-%{version}.tgz.asc
Source3:        sbt.gpg


Requires:       java-devel-openjdk
Requires:       java-openjdk


%description
sbt is the simple build tool for Scala and Java projects.


%prep
# Verify GPG signature of the release.
pushd %{_sourcedir}
%{_bindir}/sha256sum -c %{SOURCE1}
%{_bindir}/gpgv --keyring %{SOURCE3} %{SOURCE2} %{SOURCE0}
popd
%autosetup -p 1 -n %{name}


%install
%{__install} -d -m 0755 %{buildroot}%{_datadir}/%{name}
%{__install} -d -m 0755 %{buildroot}%{_datadir}/%{name}/bin
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d -m 0755 %{buildroot}%{_bindir}

# Move the configuration directory to /etc/sbt and link back to /usr/share/sbt/conf.
%{__cp} -pv conf/* %{buildroot}%{_sysconfdir}/%{name}
%{__ln_s} %{_sysconfdir}/%{name} %{buildroot}%{_datadir}/%{name}/conf

# Install script and jar.
%{__install} -m 0755 \
 bin/sbt-launch.jar \
 bin/sbt \
 %{buildroot}%{_datadir}/%{name}/bin

# Link /usr/bin/sbt to /usr/share/sbt/bin/sbt.
%{__ln_s} %{_datadir}/%{name}/bin/sbt %{buildroot}%{_bindir}/sbt


%files
%license LICENSE NOTICE
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/sbt
%{_datadir}/%{name}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
