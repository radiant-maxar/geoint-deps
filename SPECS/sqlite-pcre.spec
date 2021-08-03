Name: sqlite-pcre
Version: %{rpmbuild_version}
Release: %{rpmbuild_release}%{?dist}

Summary: Perl-compatible regular expression support for SQLite
License: Public Domain
URL: http://git.altlinux.org/people/at/packages/?p=sqlite3-pcre.git
Source: http://archive.ubuntu.com/ubuntu/pool/universe/s/sqlite3-pcre/sqlite3-pcre_0~git20070120091816+4229ecc.orig.tar.gz

BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: sqlite-devel


%description
This SQLite loadable extension enables the REGEXP operator,
which is not implemented by default, to call PCRE routines
for regular expression matching.


%prep
%autosetup -n sqlite3-pcre -p 1


%build
libs=$(pkg-config --libs sqlite3 libpcre)
%{_bindir}/gcc -shared -o pcre.so %{optflags} -fPIC -W -Werror pcre.c $libs -Wl,-z,defs


%check
%{_bindir}/sqlite3 >out <<EOF
.load ./pcre.so
SELECT "asdf" REGEXP "(?i)^A";
EOF
%{_bindir}/grep 1 out


%install
%{__install} -pD -m0755 pcre.so %{buildroot}%{_libdir}/sqlite/pcre.so


%files
%{_libdir}/sqlite/pcre.so


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
