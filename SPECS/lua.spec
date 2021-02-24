%global lua_major %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global lua_minor %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global major_version %{lua_major}.%{lua_minor}

Name:           lua%{lua_major}%{lua_minor}
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Powerful light-weight programming language
License:        MIT
URL:            https://www.lua.org/
Source0:        https://www.lua.org/ftp/lua-%{version}.tar.gz
Source1:        https://www.lua.org/tests/lua-%{version}-tests.tar.gz
# copied from doc/readme.html on 2014-07-18
Source2:        lua-mit.txt
# multilib
Source3:        luaconf.h
Patch0:         lua-5.4.0-beta-autotoolize.patch
Patch1:         lua-5.3.0-idsize.patch
Patch3:         lua-5.2.2-configure-linux.patch
Patch4:         lua-5.3.0-configure-compat-module.patch

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  devtoolset-9-gcc
BuildRequires:  devtoolset-9-gcc-c++
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  readline-devel
BuildREquires:  ncurses-devel

Requires:       %{name}-libs = %{version}-%{release}

%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.

%package libs
Summary:        Libraries for %{name}
Provides:       lua(abi) = %{major_version}

%description libs
This package contains the shared libraries for %{name}.

%package static
Summary:        Static library for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description static
This package contains the static version of liblua for %{name}.


%prep
%setup -q -a 0 -a 1 -n lua-%{version}
%{__cp} %{SOURCE2} .
%{__mv} src/luaconf.h src/luaconf.h.template.in
%patch0 -p1 -E -z .autoxxx
%patch1 -p1 -z .idsize
#%% patch2 -p1 -z .luac-shared
%patch3 -p1 -z .configure-linux
%patch4 -p1 -z .configure-compat-all
# Put proper version in configure.ac, patch0 hardcodes 5.3.0
%{__sed} -i 's|5.3.0|%{version}|g' configure.ac
autoreconf -ifv


%build
. /opt/rh/devtoolset-9/enable
%configure --with-readline --with-compat-module
%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Autotools give me a headache sometimes.
%{__sed} -i 's|@pkgdatadir@|%{_datadir}|g' src/luaconf.h.template

# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
%make_build LIBS="-lm -ldl"
# only /usr/bin/lua links with readline now #luac_LDADD="liblua.la -lm -ldl"

%check
pushd lua-%{version}-tests

# Dont skip the fully portable or ram-hungry tests:
# %{__sed} -i.orig -e '
#     /attrib.lua/d;
#     /files.lua/d;
#     /db.lua/d;
#     /errors.lua/d;
#     ' all.lua
# LD_LIBRARY_PATH=%{buildroot}/%{_libdir} %{buildroot}/%{_bindir}/lua all.lua

# Removing tests that fail under mock/koji
%{__sed} -i.orig -e '
    /db.lua/d;
    /errors.lua/d;
    ' all.lua
    LD_LIBRARY_PATH=%{buildroot}/%{_libdir} %{buildroot}/%{_bindir}/lua -e"_U=true" all.lua
popd

%install
%make_install
%{__rm} %{buildroot}%{_libdir}/*.la
%{__mkdir_p} %{buildroot}%{_libdir}/lua/%{major_version}
%{__mkdir_p} %{buildroot}%{_datadir}/lua/%{major_version}

# Rename luaconf.h to luaconf-<arch>.h to avoid file conflicts on
# multilib systems and install luaconf.h wrapper
%{__mv} %{buildroot}%{_includedir}/luaconf.h %{buildroot}%{_includedir}/luaconf-%{_arch}.h
%{__install} -p -m 644 %{SOURCE3} %{buildroot}%{_includedir}/luaconf.h


%files
%doc README doc/*.html doc/*.css doc/*.gif doc/*.png
%license lua-mit.txt
%{_bindir}/lua
%{_bindir}/luac
%{_mandir}/man1/lua*.1*

%files libs
%dir %{_libdir}/lua
%dir %{_libdir}/lua/%{major_version}
%{_libdir}/liblua-%{major_version}.so
%dir %{_datadir}/lua
%dir %{_datadir}/lua/%{major_version}

%files devel
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua.so
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
