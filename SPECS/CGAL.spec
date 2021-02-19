%global fullversion %{rpmbuild_version}
#global fullversion 5.2-beta1


Name:           CGAL
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Computational Geometry Algorithms Library

License:        LGPLv3+ and GPLv3+ and Boost
URL:            http://www.cgal.org/
Source0:        https://github.com/CGAL/cgal/releases/download/releases/%{name}-%{fullversion}/%{name}-%{fullversion}.tar.xz

# Required devel packages.
BuildRequires: cmake3
BuildRequires: gcc-c++
BuildRequires: gmp-devel
BuildRequires: boost-devel
BuildRequires: make
BuildRequires: mpfr-devel


%description
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.


%package devel
Summary:        Development files and tools for CGAL applications
Provides:       CGAL-static = %{version}-%{release}
Requires:       cmake3
Requires:       boost-devel%{?_isa}
Requires:       gmp-devel%{?_isa}
Requires:       mpfr-devel%{?_isa}

%description devel
Libraries for CGAL applications.
CGAL is a collaborative effort of several sites in Europe and
Israel. The goal is to make the most important of the solutions and
methods developed in computational geometry available to users in
industry and academia in a C++ library. The goal is to provide easy
access to useful, reliable geometric algorithms.
The %{name}-devel package provides the headers files and tools you may need to
develop applications using CGAL.

%package demos-source
Summary:        Examples and demos of CGAL algorithms
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description demos-source
The %{name}-demos-source package provides the sources of examples and demos of
CGAL algorithms.


%prep
%setup -q -n %{name}-%{fullversion}

# Fix some file permissions
#chmod a-x include/CGAL/export/ImageIO.h


%build
mkdir build
pushd build
%cmake3 -DCGAL_DO_NOT_WARN_ABOUT_CMAKE_BUILD_TYPE=ON -DCGAL_INSTALL_LIB_DIR=%{_lib} -DCGAL_INSTALL_DOC_DIR= ..
%cmake3_build
popd


%install
DESTDIR="%{buildroot}" %__cmake3 --install build

# Install demos and examples
mkdir -p %{buildroot}%{_datadir}/CGAL
touch -r demo %{buildroot}%{_datadir}/CGAL/
cp -a demo %{buildroot}%{_datadir}/CGAL/demo
cp -a examples %{buildroot}%{_datadir}/CGAL/examples

%check
rm -rf include/
mkdir build-example
cd build-example
%{__cmake3} -L "-DCMAKE_PREFIX_PATH=%{buildroot}/usr" %{buildroot}%{_datadir}/CGAL/examples/Triangulation_2
make constrained_plus
ldd ./constrained_plus
./constrained_plus


%files
%doc AUTHORS LICENSE LICENSE.FREE_USE LICENSE.LGPL LICENSE.GPL CHANGES.md
%{_libdir}/libCGAL*.so.13
%{_libdir}/libCGAL*.so.13.0.3
%{_libdir}/libCGAL_ImageIO.so.14
%{_libdir}/libCGAL_ImageIO.so.14.0.0

%files devel
%{_includedir}/CGAL
%{_libdir}/libCGAL*.so
%{_libdir}/cmake/CGAL
%dir %{_datadir}/CGAL
%{_bindir}/*
%exclude %{_bindir}/cgal_make_macosx_app
%{_mandir}/man1/cgal_create_cmake_script.1.gz

%files demos-source
%dir %{_datadir}/CGAL
%{_datadir}/CGAL/demo
%{_datadir}/CGAL/examples
%exclude %{_datadir}/CGAL/*/*/skip_vcproj_auto_generation



%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
