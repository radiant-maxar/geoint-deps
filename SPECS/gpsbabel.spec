# Because upstream's website hides tarball behind some ugly php script, we
# have to do some munging for tarball version that GitHub archive provides.
%global tarball_version %(echo %{rpmbuild_version} | tr '.' '_')

Name:          gpsbabel
Version:       %{rpmbuild_version}
Release:       %{rpmbuild_release}%{?dist}
Summary:       A tool to convert between various formats used by GPS devices

License:       GPLv2+
URL:           http://www.gpsbabel.org
Source0:       https://github.com/gpsbabel/gpsbabel/archive/%{name}_%{tarball_version}.tar.gz
Source2:       gpsbabel.png

# No automatic phone home by default (RHBZ 668865)
Patch2:        gpsbabel-0002-No-solicitation.patch

BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: libusb-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtserialport-devel
BuildRequires: qt5-qtwebchannel-devel
BuildRequires: qt5-qtwebengine-devel
BuildRequires: shapelib-devel
BuildRequires: zlib-devel

%description
Converts GPS waypoint, route, and track data from one format type
to another.

%package gui
Summary:        Qt GUI interface for GPSBabel
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}

%description gui
Qt GUI interface for GPSBabel

%prep
%autosetup -p1 -n %{name}-%{name}_%{tarball_version}


%build
%cmake \
  -DGPSBABEL_WITH_ZLIB=pkgconfig \
  -DGPS_BABEL_WITH_SHAPE_LIB=pkgconfig \
  -DGPSBABEL_WITH_SHAPELIB=pkgconfig \
  ..
%cmake_build


%install
%cmake_install

%{__install} -m 0755 -d %{buildroot}%{_bindir}/
%{__install} -m 0755 -p %{_vpath_builddir}/gpsbabel %{buildroot}%{_bindir}/

%{__install} -m 0755 -d %{buildroot}%{_bindir}/
%{__install} -m 0755 -p %{_vpath_builddir}/gui/GPSBabelFE/gpsbabelfe %{buildroot}%{_bindir}/

%{__install} -m 0755 -d %{buildroot}%{_qt5_translationdir}/
%{__install} -m 0644 -p gui/gpsbabelfe_*.qm     %{buildroot}%{_qt5_translationdir}/

%{__install} -m 0755 -d %{buildroot}%{_qt5_translationdir}/
%{__install} -m 0644 -p gui/coretool/gpsbabel_*.qm %{buildroot}%{_qt5_translationdir}/

%{__install} -m 0755 -d %{buildroot}%{_datadir}/gpsbabel
%{__install} -m 0644 -p gui/gmapbase.html %{buildroot}%{_datadir}/gpsbabel

desktop-file-install \
        --dir %{buildroot}/%{_datadir}/applications \
        gui/gpsbabel.desktop

%{__install} -m 0755 -d            %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
%{__install} -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

%find_lang %{name} --with-qt --all-name


%files
%doc README* AUTHORS
%license COPYING
%{_bindir}/gpsbabel

%files gui -f %{name}.lang
%doc gui/{AUTHORS,README*,TODO}
%license gui/COPYING*
%{_bindir}/gpsbabelfe
%{_datadir}/gpsbabel
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/256x256/apps/*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
