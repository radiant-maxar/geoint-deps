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

BuildRequires:  boost169-devel
BuildRequires:  cmake3
# A newer C++ toolchain is required to compile.
BuildRequires:  devtoolset-9-gcc
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  libosmium-devel >= %{libosmium_min_version}
BuildRequires:  man-db
BuildRequires:  pandoc
BuildRequires:  protozero-devel >= %{protozero_min_version}

%description
Command line tool for working with OpenStreetMap data
based on the Osmium library


%prep
%autosetup -p 1
%{__sed} -i -e "s/-O3 -g//" CMakeLists.txt
%{__mkdir_p} build

%build
pushd build
. /opt/rh/devtoolset-9/enable
%cmake3 .. \
    -DBOOST_INCLUDEDIR:PATH=%{_includedir}/boost169 \
    -DBOOST_LIBRARYDIR:PATH=%{_libdir}/boost169
%cmake3_build
popd


%install
pushd build
%cmake3_install
popd
%{__mkdir_p} %{buildroot}%{_datadir}/zsh/site-functions
%{__install} -p -m 0644 zsh_completion/* %{buildroot}%{_datadir}/zsh/site-functions


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
