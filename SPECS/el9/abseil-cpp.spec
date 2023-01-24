# The following macros are also required:
# * lib_version

Name:           abseil-cpp
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        C++ Common Libraries

# The entire source is Apache-2.0, except:
#   - The following files are LicenseRef-Fedora-Public-Domain:
#       absl/time/internal/cctz/src/tzfile.h
#         ** This file is in the public domain, so clarified as of
#         ** 1996-06-05 by Arthur David Olson.
#       absl/time/internal/cctz/testdata/zoneinfo/iso3166.tab
#         # This file is in the public domain, so clarified as of
#         # 2009-05-17 by Arthur David Olson.
#       absl/time/internal/cctz/testdata/zoneinfo/zone1970.tab
#         # This file is in the public domain.
License:        Apache-2.0 AND LicenseRef-Fedora-Public-Domain
URL:            https://abseil.io
Source0:        https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz

# Backport upstream commit 09e96049995584c3489e4bd1467313e3e85af99c, which
# corresponds to:
#
# Do not leak -maes -msse4.1 into pkgconfig
# https://github.com/abseil/abseil-cpp/pull/1216
#
# Fixes RHBZ#2108658.
Patch0:         abseil-cpp-09e96049995584c3489e4bd1467313e3e85af99c.patch
# Workaround until GTest publishes a release including the "GTEST_FLAG_GET" macro.
# Currently only available in the "main" branch: https://github.com/google/googletest/commit/977cffc4423a2d6c0df3fc9a7b5253b8f79c3f18
Patch1:         abseil-cpp-gtest_build_fix.patch
# Workaround until GTest publishes a release including the "::testing::Conditional" matcher.
# Currently only available in the "main" branch: https://github.com/google/googletest/commit/8306020a3e9eceafec65508868d7ab5c63bb41f7
Patch2:         abseil-cpp-disabling_invalid_tests.patch


BuildRequires:  cmake
# The default make backend would work just as well; ninja is observably faster
BuildRequires:  ninja-build
BuildRequires:  gcc-c++

BuildRequires:  gmock-devel
BuildRequires:  gtest-devel


%description
Abseil is an open-source collection of C++ library code designed to augment
the C++ standard library. The Abseil library code is collected from
Google's own C++ code base, has been extensively tested and used in
production, and is the same code we depend on in our daily coding lives.

In some cases, Abseil provides pieces missing from the C++ standard; in
others, Abseil provides alternatives to the standard for special needs we've
found through usage in the Google code base. We denote those cases clearly
within the library code we provide you.

Abseil is not meant to be a competitor to the standard library; we've just
found that many of these utilities serve a purpose within our code base,
and we now want to provide those resources to the C++ community as a whole.


%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}


%description devel
Development headers for %{name}


%prep
%autosetup -p1 -S gendiff


%build
%cmake \
  -GNinja \
  -DABSL_USE_EXTERNAL_GOOGLETEST:BOOL=ON \
  -DABSL_FIND_GOOGLETEST:BOOL=ON \
  -DABSL_ENABLE_INSTALL:BOOL=ON \
  -DABSL_BUILD_TESTING:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING=None \
  -DCMAKE_CXX_STANDARD:STRING=17
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%license LICENSE
%doc FAQ.md README.md UPGRADES.md
%{_libdir}/libabsl_*.so.%{lib_version}


%files devel
%{_includedir}/absl
%{_libdir}/libabsl_*.so
%{_libdir}/cmake/absl
%{_libdir}/pkgconfig/*.pc


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
