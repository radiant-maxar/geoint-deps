Name:           armadillo
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Fast C++ matrix library with syntax similar to MATLAB and Octave

License:        ASL 2.0
URL:            http://arma.sourceforge.net/
Source:         http://sourceforge.net/projects/arma/files/%{name}-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  arpack-devel
BuildRequires:  flexiblas-devel
BuildRequires:  SuperLU-devel

%description
Armadillo is a C++ linear algebra library (matrix maths)
aiming towards a good balance between speed and ease of use.
Integer, floating point and complex numbers are supported,
as well as a subset of trigonometric and statistics functions.
Various matrix decompositions are provided through optional
integration with LAPACK and ATLAS libraries.
A delayed evaluation approach is employed (during compile time)
to combine several operations into one and reduce (or eliminate)
the need for temporaries. This is accomplished through recursive
templates and template meta-programming.
This library is useful if C++ has been decided as the language
of choice (due to speed and/or integration capabilities), rather
than another language like Matlab or Octave.


%package devel
Summary:        Development headers and documentation for the Armadillo C++ library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libstdc++-devel
Requires:       arpack-devel
Requires:       flexiblas-devel
Requires:       SuperLU-devel

%description devel
This package contains files necessary for development using the
Armadillo C++ library. It contains header files, example programs,
and user documentation (API reference guide).


%prep
%autosetup -p1
%{__sed} -i 's/\r//' README.md
%{__rm} -rf examples/*win64*


%build
%cmake -DALLOW_FLEXIBLAS_LINUX=ON
%cmake_build


%install
%cmake_install


%check
%cmake -DALLOW_FLEXIBLAS_LINUX=ON -DBUILD_SMOKE_TEST=ON
%{__make} -C "%{_vpath_builddir}"
%ctest


%files
%{_libdir}/libarmadillo.so.11*
%license LICENSE.txt NOTICE.txt

%files devel
%{_libdir}/libarmadillo.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/armadillo
%{_includedir}/armadillo_bits/
%{_datadir}/Armadillo/
%doc README.md
%doc index.html
%doc docs.html
%doc examples
%doc armadillo_icon.png
%doc mex_interface
%doc armadillo_nicta_2010.pdf
%doc rcpp_armadillo_csda_2014.pdf
%doc armadillo_joss_2016.pdf
%doc armadillo_spcs_2017.pdf
%doc armadillo_lncs_2018.pdf
%doc armadillo_solver_2020.pdf


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
