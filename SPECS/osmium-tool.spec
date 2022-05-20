# The following macros are also required:
# * libosmium_min_version
# * protozero_min_version

Name:           osmium-tool
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Command line tool for working with OpenStreetMap data

License:        GPLv3
URL:            http://osmcode.org/osmium/
Source0:        https://github.com/osmcode/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libosmium-devel >= %{libosmium_min_version}
BuildRequires:  protozero-devel >= %{protozero_min_version}

%description
Command line tool for working with OpenStreetMap data
based on the Osmium library


%prep
%autosetup -p1
%{__sed} -i -e "s/-O3 -g//" CMakeLists.txt


%build
%cmake
%cmake_build


%install
%cmake_install
%{__mkdir_p} %{buildroot}%{_datadir}/zsh/site-functions
%{__install} -p -m 0644 zsh_completion/* %{buildroot}%{_datadir}/zsh/site-functions


%check
%ctest


%files
%doc README.md CHANGELOG.md
%license LICENSE.txt
%{_bindir}/osmium
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_osmium


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
