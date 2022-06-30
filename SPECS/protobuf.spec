# Build -python subpackage
%bcond_without python

Summary:        Protocol Buffers - Google's data interchange format
Name:           protobuf
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
License:        BSD
URL:            https://github.com/protocolbuffers/protobuf
Source:         https://github.com/protocolbuffers/protobuf/archive/v%{version}/%{name}-%{version}-all.tar.gz
Source1:        protobuf-ftdetect-proto.vim
Source2:        protobuf-init.el
# For tests (using exactly the same version as the release)
Source3:        https://github.com/google/googletest/archive/5ec7f0c4a113e2f18ac2c6cc7df51ad6afc24081.zip

# https://github.com/protocolbuffers/protobuf/issues/8082
Patch1:         protobuf-3.14-disable-IoTest.LargeOutput.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  emacs
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel

%if %{with python}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
%endif

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package compiler
Summary:        Protocol Buffers compiler
Requires:       %{name} = %{version}-%{release}
Obsoletes:      protobuf-emacs < 3.6.1-4
Obsoletes:      protobuf-emacs-el < 3.6.1-4
Requires:       emacs-filesystem >= %{_emacs_version}

%description compiler
This package contains Protocol Buffers compiler for all programming
languages

%package devel
Summary:        Protocol Buffers C++ headers and libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-compiler = %{version}-%{release}
Requires:       zlib-devel
Requires:       pkgconfig

%description devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package static
Summary:        Static development files for %{name}
Requires:       %{name}-devel = %{version}-%{release}

%description static
Static libraries for Protocol Buffers

%package lite
Summary:        Protocol Buffers LITE_RUNTIME libraries

%description lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-devel
Summary:        Protocol Buffers LITE_RUNTIME development libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-lite = %{version}-%{release}

%description lite-devel
This package contains development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-static
Summary:        Static development files for %{name}-lite
Requires:       %{name}-devel = %{version}-%{release}

%description lite-static
This package contains static development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%if %{with python}
%package -n python2-%{name}
Summary:        Python 2 bindings for Google Protocol Buffers
BuildArch:      noarch
Requires:       python2-six >= 1.9
Conflicts:      %{name}-compiler > %{version}
Conflicts:      %{name}-compiler < %{version}
Provides:       %{name}-python2 = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
This package contains Python 2 libraries for Google Protocol Buffers

%package -n python3-%{name}
Summary:        Python 3 bindings for Google Protocol Buffers
BuildArch:      noarch
Requires:       python3-six >= 1.9
Conflicts:      %{name}-compiler > %{version}
Conflicts:      %{name}-compiler < %{version}
Provides:       %{name}-python3 = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
This package contains Python 3 libraries for Google Protocol Buffers
%endif

%package emacs
Summary:        Emacs mode for Google Protocol Buffers descriptions
BuildArch:      noarch
Requires:       emacs

%description emacs
This package contains syntax highlighting for Google Protocol Buffers
descriptions in the Emacs editor.

%package vim
Summary:        Vim syntax highlighting for Google Protocol Buffers descriptions
BuildArch:      noarch
Requires:       vim-enhanced

%description vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor


%prep
%setup -q -n %{name}-%{version} -a 3
%ifarch %{ix86} armv7hl
# IoTest.LargeOutput fails on 32bit arches
# https://github.com/protocolbuffers/protobuf/issues/8082
%patch1 -p1
%endif
mv googletest-5ec7f0c4a113e2f18ac2c6cc7df51ad6afc24081/* third_party/googletest/
find -name \*.cc -o -name \*.h | xargs chmod -x
chmod 644 examples/*
rm -f src/solaris/libstdc++.la


%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"
./autogen.sh
%configure

# -Wno-error=type-limits:
#     https://bugzilla.redhat.com/show_bug.cgi?id=1838470
#     https://github.com/protocolbuffers/protobuf/issues/7514
#     https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
#  (also set in %%check)
%make_build CXXFLAGS="%{optflags} -std=c++11 -Wno-error=type-limits"

%if %{with python}
pushd python
%py2_build
%py3_build
popd
%endif
%{_emacs_bytecompile} editors/protobuf-mode.el


%check
%make_build check CXXFLAGS="%{optflags} -std=c++11 -Wno-error=type-limits"


%install
%make_install %{?_smp_mflags} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
find %{buildroot} -type f -name "*.la" -delete

%if %{with python}
pushd python
%py2_install
find %{buildroot}%{python2_sitelib} -name \*.py |
  xargs sed -i -e '1{\@^#!@d}'
%py3_install
find %{buildroot}%{python3_sitelib} -name \*.py |
  xargs sed -i -e '1{\@^#!@d}'
popd
%endif
# vim
%{__install} -p -m 0644 -D %{SOURCE1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{__install} -p -m 0644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim
# emacs
%{__mkdir_p} %{buildroot}%{_emacs_sitelispdir}/%{name}
%{__install} -p -m 0644 editors/protobuf-mode.el %{buildroot}%{_emacs_sitelispdir}/%{name}
%{__install} -p -m 0644 editors/protobuf-mode.elc %{buildroot}%{_emacs_sitelispdir}/%{name}
%{__mkdir_p} %{buildroot}%{_emacs_sitestartdir}
%{__install} -p -m 0644 %{SOURCE2} %{buildroot}%{_emacs_sitestartdir}
# extra doc dirs
%{__install} -d -m 0755 %{buildroot}%{_docdir}/%{name}-compiler-%{version}
%{__install} -d -m 0755 %{buildroot}%{_docdir}/%{name}-devel-%{version}
%if %{with python}
%{__install} -d -m 0755 %{buildroot}%{_docdir}/python2-protobuf-%{version}
%{__install} -d -m 0755 %{buildroot}%{_docdir}/python3-protobuf-%{version}
%endif


%files
%doc CHANGES.txt CONTRIBUTORS.txt README.md
%license LICENSE
%{_libdir}/libprotobuf.so.28*

%files compiler
%doc README.md
%license LICENSE
%{_bindir}/protoc
%{_libdir}/libprotoc.so.28*

%files devel
%dir %{_includedir}/google
%{_includedir}/google/protobuf/
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/Makefile examples/README.md

%files static
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%files lite
%{_libdir}/libprotobuf-lite.so.28*

%files lite-devel
%{_libdir}/libprotobuf-lite.so
%{_libdir}/pkgconfig/protobuf-lite.pc

%files lite-static
%{_libdir}/libprotobuf-lite.a

%if %{with python}
%files -n python2-protobuf
%dir %{python2_sitelib}/google
%{python2_sitelib}/google/protobuf/
%{python2_sitelib}/protobuf-%{version}-py2.*.egg-info/
%{python2_sitelib}/protobuf-%{version}-py2.*-nspkg.pth
%doc python/README.md
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto

%files -n python3-protobuf
%dir %{python3_sitelib}/google
%{python3_sitelib}/google/protobuf/
%{python3_sitelib}/protobuf-%{version}-py3.*.egg-info/
%{python3_sitelib}/protobuf-%{version}-py3.*-nspkg.pth
%doc python/README.md
%doc examples/add_person.py examples/list_people.py examples/addressbook.proto
%endif

%files emacs
%{_emacs_sitelispdir}/%{name}
%{_emacs_sitestartdir}/protobuf-init.el

%files vim
%{_datadir}/vim/vimfiles/ftdetect/proto.vim
%{_datadir}/vim/vimfiles/syntax/proto.vim


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post compiler -p /sbin/ldconfig
%postun compiler -p /sbin/ldconfig

%post lite -p /sbin/ldconfig
%postun lite -p /sbin/ldconfig


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
