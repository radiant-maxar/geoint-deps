Name:           osmium-tool
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Command line tool for working with OpenStreetMap data

License:        GPLv3
URL:            http://osmcode.org/osmium/
Source0:        https://github.com/osmcode/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  man-db
BuildRequires:  libosmium-devel
BuildRequires:  pandoc
BuildRequires:  protozero-devel

# Allows us to use Boost 1.53 instead of 1.55.
Patch1: osmium-tool-boost-version.patch

%description
Command line tool for working with OpenStreetMap data
based on the Osmium library


%prep
%autosetup -p 1
%{__sed} -i -e "s/-O3 -g//" CMakeLists.txt
%{__mkdir} build

%build
pushd build
%cmake3 ..
%cmake3_build
popd


%install
pushd build
%cmake3_install
popd
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions
install -p -m644 zsh_completion/* %{buildroot}%{_datadir}/zsh/site-functions


%check
pushd build
%ctest3
popd


%files
%doc README.md CHANGELOG.md
%license LICENSE.txt
%{_bindir}/osmium
%{_mandir}/man1/osmium*.1.gz
%{_mandir}/man5/osmium*.5.gz
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_osmium


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
