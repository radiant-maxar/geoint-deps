# The following macros are also required:
# * proj_min_version

Name:           libgeotiff
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GeoTIFF format library
License:        MIT
URL:            http://trac.osgeo.org/geotiff/
Source:         https://github.com/OSGeo/libgeotiff/releases/download/%{version}/libgeotiff-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
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
%cmake -DGEOTIFF_BIN_SUBDIR=bin -DGEOTIFF_INCLUDE_SUBDIR=include/%{name} -DGEOTIFF_LIB_SUBDIR=%{_lib}
%cmake_build



%install
%cmake_install

# install pkgconfig file
%{__mkdir_p} %{buildroot}%{_libdir}/pkgconfig/
%{__cat} > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc <<EOF
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


%check
%ctest


%files
%license COPYING
%doc ChangeLog README
%{_bindir}/applygeo
%{_bindir}/geotifcp
%{_bindir}/invgeod
%{_bindir}/invproj
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
