Name:           uriparser
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        URI parsing library - RFC 3986

License:        BSD
URL:            https://uriparser.github.io/
Source0:        https://github.com/%{name}/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Uriparser is a strictly RFC 3986 compliant URI parsing library written
in C. uriparser is cross-platform, fast, supports Unicode and is
licensed under the New BSD license.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1

# Remove qhelpgenerator dependency by commenting Doxygen.in:
%{__sed} -i 's/GENERATE_QHP\ =\ yes/GENERATE_QHP\ =\ no/g' doc/Doxyfile.in


%build
%cmake
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%doc THANKS AUTHORS ChangeLog
%license COPYING
%{_bindir}/uriparse
%{_libdir}/lib%{name}.so.1*
%{_libdir}/cmake/%{name}-%{version}/
%exclude %{_docdir}

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
