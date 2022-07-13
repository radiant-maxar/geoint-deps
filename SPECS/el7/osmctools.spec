Name:           osmctools
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Small and fast tools for OpenStreetMap data files

License:        Affero GPL v3
URL:            https://gitlab.com/osm-c-tools/osmctools
Source0:        https://gitlab.com/osm-c-tools/osmctools/-/archive/%{version}/osmctools-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  zlib-devel

Requires:       wget

%description
A few really fast tools to convert, filter and update OpenStreetMap data files.


%prep
%autosetup -p1


%build
autoreconf --install
%configure
%make_build


%install
%make_install


%files
%doc AUTHORS HACKING README.md
%license COPYING
%{_bindir}/osmconvert
%{_bindir}/osmfilter
%{_bindir}/osmupdate


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
