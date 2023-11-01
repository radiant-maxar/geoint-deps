# The following macros are also required:
# * protobuf_min_version

Name:           libosmpbf
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        C library for reading and writing OpenStreetMap PBF files
License:        LGPLv3
URL:            https://github.com/openstreetmap/OSM-binary
Source0:        https://github.com/openstreetmap/OSM-binary/archive/v%{version}/OSM-binary-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  protobuf-devel >= %{protobuf_min_version}


%description
%{name} is a C library for reading and writing OpenStreetMap Protocol buffer Binary Format (PBF) files.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       protobuf-devel >= %{protobuf_min_version}

%description    devel
Libraries and header files for developing applications with %{name}.


%package -n     osmpbf
Summary:        Binaries for %{name}

%description -n osmpbf
Binary executables, including %{name}-outline.


%prep
%autosetup -p1 -n OSM-binary-%{version}


%build
%cmake
%cmake_build


%check
%ctest


%install
%cmake_install


%files
%doc README.md
%license LICENSE
%{_libdir}/libosmpbf.so.*


%files devel
%{_includedir}/osmpbf
%{_libdir}/libosmpbf.a
%{_libdir}/libosmpbf.so


%files -n osmpbf
%{_bindir}/osmpbf-outline
%{_mandir}/man1/osmpbf-outline.*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
