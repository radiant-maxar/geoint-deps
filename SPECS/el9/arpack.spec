# We are linking FORTRAN symbols.  Thus we cannot link --as-needed.
%undefine _ld_as_needed

Name:		arpack
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:	Fortran 77 subroutines for solving large scale eigenvalue problems

License:	BSD
URL:		https://github.com/opencollab/arpack-ng
Source0:	https://github.com/opencollab/arpack-ng/archive/%{version}/arpack-ng-%{version}.tar.gz
# https://bugzilla.redhat.com/show_bug.cgi?id=1990366
Patch0:         arpack-install-arpackicb_h.patch

BuildRequires:	gcc-c++
BuildRequires:	gcc-gfortran
BuildRequires:	flexiblas-devel
BuildRequires:	libtool
BuildRequires:	make
Provides:	arpack-ng = %{version}-%{release}
Provides:	arpack-ng%{?_isa} = %{version}-%{release}

%description
ARPACK is a collection of Fortran 77 subroutines designed to solve large
scale eigenvalue problems.

The package is designed to compute a few eigenvalues and corresponding
eigenvectors of a general n by n matrix A. It is most appropriate for
large sparse or structured matrices A where structured means that a
matrix-vector product w <- Av requires order n rather than the usual
order n**2 floating point operations. This software is based upon an
algorithmic variant of the Arnoldi process called the Implicitly
Restarted Arnoldi Method (IRAM).


%package devel
Summary:	Files needed for developing arpack based applications
Requires:	arpack%{?_isa} = %{version}-%{release}
Provides:	arpack-ng-devel = %{version}-%{release}
Provides:	arpack-ng-devel%{?_isa} = %{version}-%{release}

%description devel
ARPACK is a collection of Fortran 77 subroutines designed to solve
large scale eigenvalue problems. This package contains the so
library links used for building arpack based applications.


%package doc
Summary:	Examples for the use of arpack
BuildArch:	noarch

%description doc
This package contains examples for the use of arpack.


%package static
Summary:	Static library for developing arpack based applications
Requires:	arpack-devel%{?_isa} = %{version}-%{release}
Provides:	arpack-ng-static = %{version}-%{release}
Provides:	arpack-ng-static%{?_isa} = %{version}-%{release}

%description static
ARPACK is a collection of Fortran 77 subroutines designed to solve
large scale eigenvalue problems. This package contains the static
library and so links used for building arpack based applications.


%prep
%setup -qc
mv arpack-ng-%{version} src
pushd src
%patch0 -p1
autoreconf -vif
popd
cp -pr src src64


%build
pushd src
%configure --enable-shared --enable-static \
    --with-blas=-lflexiblas \
    --with-lapack=-lflexiblas \
    --enable-icb
%make_build
popd
pushd src64
%configure --enable-shared --enable-static \
    LIBSUFFIX=64 \
    INTERFACE64=1 \
    --with-blas=-lflexiblas64 \
    --with-lapack=-lflexiblas64 \
    --enable-icb
%make_build
popd

%install
pushd src
%make_install
popd
pushd src64
%make_install
popd
# Get rid of .la files
rm -r %{buildroot}%{_libdir}/*.la

%check
pushd src
%make_build check
pushd EXAMPLES ; make clean ; popd
popd
pushd src64
%make_build check
pushd EXAMPLES ; make clean ; popd
popd

%files
%doc src/CHANGES src/README.md
%license src/COPYING
%{_libdir}/libarpack.so.*
%{_libdir}/libarpack64.so.*

%files devel
%{_libdir}/pkgconfig/arpack.pc
%{_libdir}/libarpack.so
%{_libdir}/pkgconfig/arpack64.pc
%{_libdir}/libarpack64.so
%{_libdir}/cmake/arpack-ng/arpack-ng-config-version.cmake
%{_libdir}/cmake/arpack-ng/arpack-ng-config.cmake
%{_includedir}/arpack/

%files doc
%doc src/EXAMPLES/ src/DOCUMENTS/
%doc src/CHANGES src/README.md
%license src/COPYING


%files static
%{_libdir}/libarpack.a
%{_libdir}/libarpack64.a


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
