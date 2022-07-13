%global build_gui 1
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
Source21:      gpsbabel-style3.css
# Remove network access requirement for XML doc builds and HTML doc reading
Patch1:        gpsbabel-0001-xmldoc-nonet.patch
# No automatic phone home by default (RHBZ 668865)
Patch2:        gpsbabel-0002-No-solicitation.patch
# Pickup gmapbase.html from /usr/share/gpsbabel
Patch3:        gpsbabel-0003-1.4.3-gmapbase.patch
# Pickup translations from /usr/share/qt5 instead of /usr/bin
Patch4:        gpsbabel-0004-Pickup-translations-from-usr-share-qt5-translations.patch
# Use system shapelib - not suitable for upstream in this form.
Patch5:        gpsbabel-0005-Use-system-shapelib.patch
# Use system zlib
Patch6:        gpsbabel-0006-Use-system-zlib.patch
# gcc-11 fixes
Patch7:        gpsbabel-0007-gcc11.patch
# Patch for disabling usb support.
Patch8:        gpsbabel-0008-disable-libusb.patch

# A newer C++ toolchain is required to compile 1.6+.
BuildRequires: devtoolset-9-gcc
BuildRequires: devtoolset-9-gcc-c++
BuildRequires: desktop-file-utils
BuildRequires: docbook-style-xsl
BuildRequires: expat-devel
BuildRequires: libxslt
BuildRequires: make
BuildRequires: minizip-devel
BuildRequires: perl
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtwebkit-devel
BuildRequires: qt5-linguist
BuildRequires: shapelib-devel
BuildRequires: zlib-devel

%description
Converts GPS waypoint, route, and track data from one format type
to another.

%if 0%{?build_gui}
%package gui
Summary:        Qt GUI interface for GPSBabel
License:        GPLv2+
Requires:       %{name} = %{version}-%{release}

%description gui
Qt GUI interface for GPSBabel
%endif

%prep
%setup -q -n %{name}-%{name}_%{tarball_version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# Use system shapelib instead of bundled partial shapelib
%{__rm} -rf shapelib

# Get rid of bundled zlib
%{__rm} -rf zlib

%{__cp} -p %{SOURCE21} gpsbabel.org-style3.css

%if 0%{?rhel} < 8
# FIXME: RHEL7 does not have qtwebengine
# Add define USE_GUI to switch between qtwebengine and qtwebkit
%{__sed} -i -e 's|greaterThan(QT_MINOR_VERSION, 5)|!equals(USE_GUI, "qtwebkit")|' gui/app.pro
%endif

# Avoid calling autoconf from Makefile
touch -r configure.ac configure Makefile.in

%build
# Enable the updated compiler toolchain prior to building.
. /opt/rh/devtoolset-9/enable
%global optflags %{optflags} 
%configure --with-zlib=system --with-doc=./manual --without-libusb
%{__make} %{?_smp_mflags}
%{__perl} xmldoc/makedoc
%{__make} gpsbabel.html

%if 0%{?build_gui}
pushd gui
%{qmake_qt5} USE_GUI=qtwebkit
/usr/bin/lrelease-qt5 *.ts
%{__make} %{?_smp_mflags}
popd
%endif

%install
%{__make} DESTDIR=%{buildroot} install

%if 0%{?build_gui}
%{__make} -C gui DESTDIR=%{buildroot} install

install -m 0755 -d                            %{buildroot}%{_bindir}/
install -m 0755 -p gui/objects/gpsbabelfe %{buildroot}%{_bindir}/
install -m 0755 -d                            %{buildroot}%{_qt5_translationdir}/
install -m 0644 -p gui/gpsbabel*_*.qm         %{buildroot}%{_qt5_translationdir}/

install -m 0755 -d %{buildroot}%{_datadir}/gpsbabel
install -m 0644 -p gui/gmapbase.html %{buildroot}%{_datadir}/gpsbabel

desktop-file-install \
        --dir %{buildroot}/%{_datadir}/applications \
        gui/gpsbabel.desktop

install -m 0755 -d            %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/
install -m 0644 -p %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

%find_lang %{name} --with-qt --all-name
%endif

%files
%doc README* AUTHORS
%license COPYING
%doc gpsbabel.html gpsbabel.org-style3.css
%{_bindir}/gpsbabel

%if 0%{?build_gui}
%files gui -f %{name}.lang
%doc gui/{AUTHORS,README*,TODO}
%license gui/COPYING*
%{_bindir}/gpsbabelfe
%{_datadir}/gpsbabel
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/256x256/apps/*
%endif


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
