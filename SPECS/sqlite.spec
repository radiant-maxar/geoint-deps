# Extract SQLite version numbers and zerofill some for use only in manipulating
# the source code archive.
%global sqlite_major_version %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global sqlite_minor_version %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global sqlite_minor_zversion %(printf "%%02d" %{sqlite_minor_version})
%global sqlite_subminor_version %(echo %{rpmbuild_version} | awk -F. '{ print $3 }')
%global sqlite_subminor_zversion %(printf "%%02d" %{sqlite_subminor_version})

%define realver %{sqlite_major_version}%{sqlite_minor_zversion}%{sqlite_subminor_zversion}00
%define docver %{realver}
%define year 2021

# Tcl is required to run SQLite tests.
%if 0%{?rhel} < 8
%global tcl_version 8.5
%else
%global tcl_version 8.6
%endif
%global tcl_sitearch %{_libdir}/tcl%{tcl_version}

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: %{rpmbuild_version}
Release: %{rpmbuild_release}%{?dist}
License: Public Domain
URL: http://www.sqlite.org/

Source0: http://www.sqlite.org/%{year}/sqlite-src-%{realver}.zip
Source1: http://www.sqlite.org/%{year}/sqlite-doc-%{docver}.zip
Source2: http://www.sqlite.org/%{year}/sqlite-autoconf-%{realver}.tar.gz

# Support a system-wide lemon template
Patch1: sqlite-3.6.23-lemon-system-template.patch
# sqlite >= 3.7.10 is buggy if malloc_usable_size() is detected, disable it:
# https://bugzilla.redhat.com/show_bug.cgi?id=801981
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=665363
Patch2: sqlite-3.12.2-no-malloc-usable-size.patch
# Temporary workaround for failed percentile test, see patch for details
Patch3: sqlite-3.8.0-percentile-test.patch
# Modify sync2.test to pass with DIRSYNC turned off
Patch5: sqlite-3.18.0-sync2-dirsync.patch

BuildRequires: autoconf
BuildRequires: make
BuildRequires: gcc
BuildRequires: glibc-devel
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: tcl-devel

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development documentation
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%package doc
Summary: Documentation for sqlite
BuildArch: noarch

%description doc
This package contains most of the static HTML files that comprise the
www.sqlite.org website, including all of the SQL Syntax and the
C/C++ interface specs and other miscellaneous documentation.

%package -n lemon
Summary: A parser generator

%description -n lemon
Lemon is an LALR(1) parser generator for C or C++. It does the same
job as bison and yacc. But lemon is not another bison or yacc
clone. It uses a different grammar syntax which is designed to reduce
the number of coding errors. Lemon also uses a more sophisticated
parsing engine that is faster than yacc and bison and which is both
reentrant and thread-safe. Furthermore, Lemon implements features
that can be used to eliminate resource leaks, making is suitable for
use in long-running programs such as graphical user interfaces or
embedded controllers.

%package tools
Summary: %{name} tools

%description tools
%{name} related tools. Currently contains only sqldiff.
- sqldiff: The sqldiff binary is a command-line utility program
  that displays the differences between SQLite databases.

%package tcl
Summary: Tcl module for the sqlite3 embeddable SQL database engine
Requires: %{name} = %{version}-%{release}
Requires: tcl(abi) = %{tcl_version}

%description tcl
This package contains the tcl modules for %{name}.

%package analyzer
Summary: An analysis program for sqlite3 database files
Requires: %{name} = %{version}-%{release}
Requires: tcl(abi) = %{tcl_version}

%description analyzer
This package contains the analysis program for %{name}.


%prep
%setup -q -a1 -n %{name}-src-%{realver}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch5 -p1

# Remove backup-file
%{__rm} -f %{name}-doc-%{docver}/sqlite.css~ || true


%build
export CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS -DSQLITE_ENABLE_COLUMN_METADATA=1 \
               -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_SECURE_DELETE=1 \
               -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
               -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 -fno-strict-aliasing"
export TCLLIBDIR=%{tcl_sitearch}/sqlite3
%configure --enable-all \
           --enable-threadsafe \
           --enable-threads-override-locks \
           --enable-load-extension


# rpath removal
%{__sed} -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%{__sed} -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build
%make_build sqlite3_analyzer
%make_build sqldiff


%install
%make_install

%{__install} -D -m 0644 sqlite3.1 %{buildroot}/%{_mandir}/man1/sqlite3.1
%{__install} -D -m 0755 lemon %{buildroot}/%{_bindir}/lemon
%{__install} -D -m 0644 tool/lempar.c %{buildroot}/%{_datadir}/lemon/lempar.c

# fix up permissions to enable dep extraction
%{__chmod} 0755 %{buildroot}/%{tcl_sitearch}/sqlite3/*.so
# Install sqlite3_analyzer
%{__install} -D -m 0755 sqlite3_analyzer %{buildroot}/%{_bindir}/sqlite3_analyzer
# Install sqldiff
%{__install} -D -m 0755 sqldiff %{buildroot}/%{_bindir}/sqldiff


%check
# XXX shell tests are broken due to loading system libsqlite3, work around...
export LD_LIBRARY_PATH=`pwd`/.libs
export MALLOC_CHECK_=3

%if 0%{?rhel} < 8
# This test is failing on CentOS 7.
%{__rm} -f \
 test/fts3corrupt4.test

# Disable tests that require Tcl 8.6.
%{__rm} -f \
 ext/session/session4.test \
 test/wapp.tcl \
 test/zipfile.test \
 test/zipfile2.test
%endif

# csv01 hangs on all non-intel archs i've tried
%ifarch x86_64 %{ix86}
%else
%{__rm} test/csv01.test
%endif

%{__make} test


%files
%doc README.md
%{_bindir}/sqlite3
%{_mandir}/man?/*
%{_libdir}/*.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%exclude %{_libdir}/*.la

%files doc
%doc %{name}-doc-%{docver}/*

%files -n lemon
%{_bindir}/lemon
%{_datadir}/lemon

%files tcl
%{tcl_sitearch}/sqlite3

%files tools
%{_bindir}/sqldiff

%files analyzer
%{_bindir}/sqlite3_analyzer


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
