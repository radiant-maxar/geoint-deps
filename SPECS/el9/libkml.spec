Name:           libkml
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Reference implementation of OGC KML 2.2

License:        BSD
URL:            https://github.com/libkml/libkml
Source0:        https://github.com/libkml/libkml/archive/%{version}/libkml-%{version}.tar.gz
Source1:        https://sourceforge.net/projects/libkml-files/files/1.3.0/minizip.tar.gz

## See https://github.com/libkml/libkml/pull/239
Patch0:         libkml-0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch
Patch1:         libkml-0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch
Patch2:         libkml-0003-Fix-python-tests.patch
# Fix a fragile test failing on i686
Patch4:         libkml-fragile_test.patch
# Don't bytecompile python sources as part of build process, leave it to rpmbuild
Patch5:         libkml-dont-bytecompile.patch
# Fix possible OOB array access in strcmp due to undersized array
Patch8:         libkml-test_strcmp.patch

BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  boost-devel
BuildRequires:  expat-devel
BuildRequires:  gtest-devel
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  uriparser-devel
BuildRequires:  zlib-devel

Provides:       bundled(minizip) = 1.3.0

%global __requires_exclude_from ^%{_docdir}/.*$
%global __provides_exclude_from ^%{python2_sitearch}/.*\\.so$


%description
Reference implementation of OGC KML 2.2.
It also includes implementations of Google's gx: extensions used by Google
Earth, as well as several utility libraries for working with other formats.


%package -n python3-%{name}
Summary:        Python 3 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}


%description -n python3-%{name}
The python3-%{name} package contains Python 3 bindings for %{name}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       expat-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -a1


%build
pushd minizip
(
%cmake -DBUILD_SHARED_LIBS=OFF
%cmake_build
)
popd
%cmake -DWITH_SWIG=ON -DWITH_PYTHON=ON \
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/kml \
  -DPYTHON_LIBRARY=%{_libdir}/libpython%{python3_version}$(python3-config --abiflags).so \
  -DPYTHON_INCLUDE_DIR=%{_includedir}/python%{python3_version}$(python3-config --abiflags)/ \
  -DPYTHON_INSTALL_DIR=%{python3_sitearch} \
  -DMINIZIP_INCLUDE_DIR=$PWD -DMINIZIP_LIBRARY=$PWD/minizip/%{_vpath_builddir}/libminizip.a \
  -DBUILD_TESTING=ON \
  -DBUILD_EXAMPLES=ON
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libkml*.so.*

%files -n python3-%{name}
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py
%{python3_sitearch}/__pycache__/*.py*

%files devel
%doc examples
%{_includedir}/kml/
%{_libdir}/libkml*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
