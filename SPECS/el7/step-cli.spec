Name:           step-cli
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        A zero trust swiss army knife for working with X509, OAuth, JWT, OATH OTP, etc.

License:        ASL 2.0
URL:            https://github.com/smallstep/cli
Source0:        https://github.com/smallstep/cli/archive/v%{version}/cli-%{version}.tar.gz


%description
step is an easy-to-use CLI tool for building, operating, and automating Public Key Infrastructure (PKI) systems and workflows. It's the client counterpart to the step-ca online Certificate Authority (CA). You can use it for many common crypto and X.509 operations—either independently, or with an online CA


%prep
%autosetup -n cli-%{version}
cd "${HOME}"
%{__rm} -fr %{_builddir}/cli-%{version}
%{__git} clone --single-branch -b v%{version} %{url} %{_builddir}/cli-%{version}
cd %{_builddir}/cli-%{version}
# XXX: ensure golangci-lint at latest version, remove when no longer needed.
%{__sed} -i -e 's/v1\.48/latest/g' make/common.mk


%build
%{__make} bootstrap
%{__make} download
%{__make} VERSION=%{version} build


%install
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -p bin/step %{buildroot}%{_bindir}


%files
%doc CHANGELOG.md README.md
%license LICENSE
%{_bindir}/step


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
