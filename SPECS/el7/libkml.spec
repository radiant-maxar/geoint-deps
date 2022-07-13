Name:           libkml
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Reference implementation of OGC KML 2.2

License:        BSD
URL:            https://github.com/libkml/libkml
Source0:        https://github.com/libkml/libkml/archive/%{version}/libkml-%{version}.tar.gz

## See https://github.com/libkml/libkml/pull/239
Patch0:         libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch
Patch1:         libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch
Patch2:         libkml-0003-Fix-python-tests.patch
Patch3:         libkml-0004-Correctly-build-and-run-java-test.patch
# Fix a fragile test failing on i686
Patch4:         libkml-fragile_test.patch
# Don't bytecompile python sources as part of build process, leave it to rpmbuild
Patch5:         libkml-dont-bytecompile.patch
# Fix possible OOB array access in strcmp due to undersized array
Patch8:         libkml-test_strcmp.patch

BuildRequires:  cmake3
BuildRequires:  curl-devel
BuildRequires:  boost-devel
BuildRequires:  expat-devel
BuildRequires:  gtest-devel
BuildRequires:  java-devel
BuildRequires:  junit
BuildRequires:  minizip-devel
BuildRequires:  python-devel
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  uriparser-devel
BuildRequires:  zlib-devel

%global __requires_exclude_from ^%{_docdir}/.*$
%global __provides_exclude_from ^%{python2_sitearch}/.*\\.so$


%description
Reference implementation of OGC KML 2.2.
It also includes implementations of Google's gx: extensions used by Google
Earth, as well as several utility libraries for working with other formats.


%package -n python2-%{name}
Summary:        Python 2 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
The python2-%{name} package contains Python 2 bindings for %{name}.


%package -n python3-%{name}
Summary:        Python 3 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}


%description -n python3-%{name}
The python3-%{name} package contains Python 3 bindings for %{name}.


%package java
Summary:        Java bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description java
The %{name}-java package contains Java bindings for %{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       expat-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1
%{__mkdir} build_py2
%{__mkdir} build_py3


%build
%global optflags %{optflags} -fPIC

# Allow CMake to proceed with zlib 1.2.7.
%{__sed} -i -e 's/ZLIB 1\.2\.8/ZLIB 1\.2\.7/' CMakeLists.txt

pushd build_py2
%cmake3 -DWITH_SWIG=ON -DWITH_PYTHON=ON -DWITH_JAVA=ON \
  -DJNI_INSTALL_DIR=%{_libdir}/%{name} \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/kml \
  -DPYTHON_LIBRARY=%{_libdir}/libpython%{python2_version}.so \
  -DPYTHON_INCLUDE_DIR=%{_includedir}/python%{python2_version}/ \
  -DPYTHON_INSTALL_DIR=%{python2_sitearch} \
  -DBUILD_TESTING=ON \
  -DBUILD_EXAMPLES=OFF \
  ..
%cmake3_build
popd

pushd build_py3
%cmake3 -DWITH_SWIG=ON -DWITH_PYTHON=ON -DWITH_JAVA=OFF \
  -DJNI_INSTALL_DIR=%{_libdir}/%{name} \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/kml \
  -DPYTHON_LIBRARY=%{_libdir}/libpython%{python3_version}m.so \
  -DPYTHON_INCLUDE_DIR=%{_includedir}/python%{python3_version}m/ \
  -DPYTHON_INSTALL_DIR=%{python3_sitearch} \
  -DBUILD_TESTING=ON \
  -DBUILD_EXAMPLES=ON \
  ..
%cmake3_build
popd


%install
pushd build_py2
%cmake3_install
popd
pushd build_py3
%cmake3_install
popd


%check
pushd build_py2
%ctest3
popd
pushd build_py3
%ctest3
popd


%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libkml*.so.*

%files -n python2-%{name}
%{python2_sitearch}/*.so
%{python2_sitearch}/*.py*

%files -n python3-%{name}
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py
%{python3_sitearch}/__pycache__/*.py*

%files java
%{_javadir}/LibKML.jar
%{_libdir}/%{name}/

%files devel
%doc examples
%{_includedir}/kml/
%{_libdir}/libkml*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
