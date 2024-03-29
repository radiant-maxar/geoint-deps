%global compiler RHEL7_64

## ESRI File Geodatabase API Library
Name:		FileGDBAPI
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:	ESRI FileGDB API
Group:		System Environment/Libraries
License:	ASL 2.0
URL:		https://github.com/Esri/file-geodatabase-api
Source0:	https://github.com/Esri/file-geodatabase-api/raw/master/FileGDB_API_%{version}/FileGDB_API_%{compiler}.tar.gz

%description
The FileGDB API provides basic tools that allow the creation of file
geodatbases, feature classes and tables. Simple features can be created
and loaded.

Copyright © 2014 ESRI

All rights reserved under the copyright laws of the United States and
applicable international laws, treaties, and conventions.

You may freely redistribute and use the sample code, with or without
modification, provided you include the original copyright notice and use
restrictions.

Disclaimer:  THE SAMPLE CODE IS PROVIDED "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL ESRI OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
OR BUSINESS INTERRUPTION) SUSTAINED BY YOU OR A THIRD PARTY, HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT ARISING IN ANY WAY OUT OF THE USE OF THIS SAMPLE CODE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

For additional information, contact:
Environmental Systems Research Institute, Inc.
Attn: Contracts and Legal Services Department
380 New York Street
Redlands, California, 92373
USA

email: contracts@esri.com


%package devel
Summary:        Development files for FileGDBAPI
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The FileGDBAPI-devel package contains libraries and header files for
developing applications that use FileGDBAPI.


%prep
%autosetup -n FileGDB_API_%{compiler}


%build


%install
%{__install} -d %{buildroot}%{_libdir}
%{__install} -d %{buildroot}%{_includedir}
%{__install} -d %{buildroot}%{_libdir}/pkgconfig
%{__install} -d %{buildroot}%{_datarootdir}/doc/%{name}-%{version}/FileGDB_SQL_files

# TODO: Version dynamic libs?
%{__install} -m 0755 -D \
 %{_builddir}/FileGDB_API_%{compiler}/lib/libFileGDBAPI.so \
 %{_builddir}/FileGDB_API_%{compiler}/lib/libfgdbunixrtl.so \
 %{buildroot}%{_libdir}/

# devel
%{__install} -m 0644 -D %{_builddir}/FileGDB_API_%{compiler}/lib/libfgdbunixrtl.a %{buildroot}%{_libdir}
%{__install} -m 0644 -D %{_builddir}/FileGDB_API_%{compiler}/include/* %{buildroot}%{_includedir}

%{__cat} > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc <<EOF
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: ESRI FileGDB API
Version: %{version}
Cflags: -I\${includedir}
EOF
%{__chmod} 0644 %{buildroot}%{_libdir}/pkgconfig/%{name}.pc


%files
%{_libdir}/libFileGDBAPI.so
%{_libdir}/libfgdbunixrtl.so

%files devel
%{_includedir}/*
%{_libdir}/libfgdbunixrtl.a
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
