# The following macros are also required:
# * proj_min_version

Name:           libgeotiff
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GeoTIFF format library
License:        MIT
URL:            http://trac.osgeo.org/geotiff/
Source:         https://github.com/OSGeo/libgeotiff/releases/download/%{version}/libgeotiff-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  make
BuildRequires:  proj-devel >= %{proj_min_version}
BuildRequires:  zlib-devel

Requires:       proj >= %{proj_min_version}

%description
GeoTIFF represents an effort by over 160 different remote sensing,
GIS, cartographic, and surveying related companies and organizations
to establish a TIFF based interchange format for georeferenced
raster imagery.

%package devel
Summary:        Development library and header for the GeoTIFF file format library
Requires:       libtiff-devel
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The GeoTIFF library provides support for development of geotiff image format.


%prep
%autosetup -p1


%build
%configure \
        --prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name}/ \
        --with-proj \
        --with-tiff \
        --with-jpeg \
        --with-zip  \
        --disable-static

%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build %{?_smp_mflags}


%install
%{__make} install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

# install pkgconfig file
%{__cat} > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

%{__mkdir_p} %{buildroot}%{_libdir}/pkgconfig/
%{__install} -p -m 0644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

#clean up junks
%{__rm} -fv %{buildroot}%{_libdir}/lib*.la


%check
# Run tests, but use installed path for libraries.
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{__make} check


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license LICENSE
%doc ChangeLog README
%{_bindir}/applygeo
%{_bindir}/geotifcp
%{_bindir}/listgeo
%{_libdir}/%{name}.so.5*
%{_mandir}/man1/*.1*


%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
