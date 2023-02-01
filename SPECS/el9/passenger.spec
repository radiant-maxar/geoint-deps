# Based on http://pkgs.fedoraproject.org/cgit/rubygem-passenger.git/tree/

%global bundled_boost_version 1.80.0

%global passenger_datadir %{_datadir}/passenger
%global passenger_libdir %{_libdir}/passenger

%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}
%{!?_httpd_confdir:     %{expand: %%global _httpd_confdir     %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir:  %{expand: %%global _httpd_modconfdir  %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:      %{expand: %%global _httpd_moddir      %%{_libdir}/httpd/modules}}

%{!?ruby_vendorlibdir: %global ruby_vendorlibdir %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorlibdir"]')}
%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %(ruby -rrbconfig -e 'puts RbConfig::CONFIG["vendorarchdir"]')}
%global passenger_ruby_libdir %{ruby_vendorlibdir}
%global locations_ini %{passenger_ruby_libdir}/phusion_passenger/locations.ini

# We leave out the 'mls', 'minimum', 'strict' and 'sandbox' variants on purpose.
#
# 'mls' lacks unconfined_t.
# 'minimum' lacks httpd_t.
# 'sandbox' is only for the policycoreutils-sandbox tool.
#
# 'strict' is omitted because Passenger’s policy essentially introduces a way for
# the web server to run PassengerAgent (and subprocesses) in the unconfined domain,
# which is philosophically incompatible with the idea of the strict policy
#
# REMINDER: if you change this list, don't forget to update the 'triggerin'
# sections.


Summary: Phusion Passenger application server
Name: passenger
Version: %{rpmbuild_version}
Release: %{rpmbuild_release}%{?dist}
# Passenger code uses MIT license.
# Bundled(Boost) uses Boost Software License
# BCrypt and Blowfish files use BSD license.
# Documentation is CC-BY-SA
# See: https://bugzilla.redhat.com/show_bug.cgi?id=470696#c146
License: Boost and BSD and BSD with advertising and MIT and zlib
URL: https://www.phusionpassenger.com
Vendor: Phusion

# passenger do currently not build on the armv7hl architecture
ExcludeArch: armv7hl

Source: https://phusion-passenger.s3.amazonaws.com/releases/%{name}-%{version}.tar.gz
Source10: passenger.logrotate
Source100: apache-passenger.conf.in
Source101: apache-passenger-module.conf
# Configuration file at /usr/lib/tmpfiles.d/passenger.conf
Source102: passenger.tmpfiles

Requires: procps-ng
Requires: rubygems
# XXX: Needed to run passenger standalone
Requires: rubygem(rack)
Requires: rubygem(rake)
Requires: ruby(release)
Requires: logrotate

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: httpd-devel
BuildRequires: libcurl-devel
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: rubygems
BuildRequires: rubygems-devel
BuildRequires: rubygem-rake
BuildRequires: rubygem-rack
BuildRequires: zlib-devel

%if 0%{?rhel} >= 8 || 0%{?fedora} >= 28
BuildRequires: /usr/bin/pathfix.py
BuildRequires: python3-devel
%endif

# Phusion Passenger includes bundled software (boost, libev, jsoncpp) at the
# place: src/cxx_supportlib/vendor-modified
Provides: bundled(boost)  = %{bundled_boost_version}

Obsoletes: rubygem-passenger < %{version}-%{release}
Provides:  rubygem-passenger = %{version}-%{release}
Provides:  rubygem-passenger%{?_isa} = %{version}-%{release}


%description
Phusion Passenger® is a web server and application server, designed to be fast,
robust and lightweight. It takes a lot of complexity out of deploying web apps,
adds powerful enterprise-grade features that are useful in production,
and makes administration much easier and less complex. It supports Ruby,
Python, Node.js and Meteor.


%package -n mod_passenger
Summary: Apache Module for Phusion Passenger
BuildRequires:  httpd-devel
Requires: httpd-mmn = %{_httpd_mmn}
Requires: %{name}%{?_isa} = %{version}-%{release}
License: Boost and BSD and BSD with advertising and MIT and zlib


%description -n mod_passenger
This package contains the pluggable Apache server module for Phusion Passenger®.


%package devel
Summary: Phusion Passenger development files
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: bundled(boost-devel) = %{bundled_boost_version}
License: Boost and BSD and BSD with advertising and GPL+ and MIT and zlib


%description devel
This package contains development files for Phusion Passenger®. Installing this
package allows it to compile native extensions for non-standard Ruby interpreters,
and allows Passenger Standalone to use a different Nginx core version.


%prep
%setup -q


%build
export EXTRA_CFLAGS="${CFLAGS:-%optflags} -Wno-deprecated"
export EXTRA_CXXFLAGS="${CXXFLAGS:-%optflags} -Wno-deprecated"

# Remove default optimization flags and use Phusion Passenger's recommended optimization flags.
export EXTRA_CFLAGS=`echo "$EXTRA_CFLAGS" | sed 's|-O2||g'`
export EXTRA_CXXFLAGS=`echo "$EXTRA_CXXFLAGS" | sed 's|-O2||g'`
export OPTIMIZE=yes

export CACHING=false

# Speed up ccache (reduce I/O) by lightly compressing things.
export CCACHE_COMPRESS=1
export CCACHE_COMPRESSLEVEL=3

export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Build Passenger.
rake fakeroot \
    NATIVE_PACKAGING_METHOD=rpm \
    FS_PREFIX=%{_prefix} \
    FS_BINDIR=%{_bindir} \
    FS_SBINDIR=%{_sbindir} \
    FS_DATADIR=%{_datadir} \
    FS_DOCDIR=%{_docdir} \
    FS_LIBDIR=%{_libdir} \
    RUBYLIBDIR=%{ruby_vendorlibdir} \
    RUBYARCHDIR=%{ruby_vendorarchdir} \
    APACHE2_MODULE_PATH=%{_httpd_moddir}/mod_passenger.so


%install
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

%{__rm} -rf %{buildroot}
%{__mkdir} %{buildroot}
%{__cp} -a pkg/fakeroot/* %{buildroot}/

# Install Apache config.
%{__mkdir_p} %{buildroot}%{_httpd_confdir} %{buildroot}%{_httpd_modconfdir}
%{__sed} -e 's|@PASSENGERROOT@|%{passenger_ruby_libdir}/phusion_passenger/locations.ini|g' %{SOURCE100} > passenger.conf
%if !(0%{?rhel} >= 7 || 0%{?fedora} >= 19)
    %{__sed} -i -e '/^# *Require all granted/d' passenger.conf
%endif

touch -r %{SOURCE100} passenger.conf
%{__install} -pm 0644 passenger.conf %{buildroot}%{_httpd_confdir}/passenger.conf
%{__install} -pm 0644 %{SOURCE101} %{buildroot}%{_httpd_modconfdir}/10-passenger.conf
touch -r %{SOURCE101} %{buildroot}%{_httpd_modconfdir}/10-passenger.conf

# Make our ghost log and tmpfile configuration directories...
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/passenger-analytics
%{__mkdir_p} %{buildroot}%{_localstatedir}/run/passenger-instreg
%{__mkdir_p} %{buildroot}%{_usr}/lib/tmpfiles.d
%{__install} -m 644 -p %{SOURCE102} \
        %{buildroot}%{_usr}/lib/tmpfiles.d/passenger.conf

# logrotate
%{__mkdir_p} %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -pm 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/logrotate.d/passenger

# Install man pages into the proper location.
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__mkdir_p} %{buildroot}%{_mandir}/man8
%{__cp} man/*.1 %{buildroot}%{_mandir}/man1
%{__cp} man/*.8 %{buildroot}%{_mandir}/man8

# Fix Python scripts with shebang which are not executable
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 28
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{passenger_datadir}/helper-scripts/wsgi-loader.py
%endif
%{__chmod} +x %{buildroot}%{passenger_datadir}/helper-scripts/wsgi-loader.py


%files
%license LICENSE
%doc CONTRIBUTORS CHANGELOG doc/*
%{_bindir}/%{name}*
%{_sbindir}/*
%{_usr}/lib/tmpfiles.d/passenger.conf
%{passenger_datadir}/helper-scripts
%{passenger_datadir}/templates
%{passenger_datadir}/standalone_default_root
%{passenger_datadir}/node
%{passenger_datadir}/*.types
%{passenger_datadir}/*.crt
%{passenger_datadir}/*.txt
%{passenger_datadir}/*.pem
%{passenger_datadir}/*.p12
%dir %{_localstatedir}/log/passenger-analytics
%dir %attr(0755, root, root) %{_localstatedir}/run/passenger-instreg
%config(noreplace) %{_sysconfdir}/logrotate.d/passenger
%{_mandir}/*/*
%{passenger_libdir}/support-binaries
%{ruby_vendorlibdir}/phusion_passenger.rb
%{ruby_vendorlibdir}/phusion_passenger/
%{ruby_vendorarchdir}/passenger_native_support.so
%exclude %{_docdir}


%files devel
%{passenger_datadir}/ngx_http_passenger_module
%{passenger_datadir}/ruby_extension_source
%{passenger_datadir}/include
%{_libdir}/%{name}/common
%exclude %{_libdir}/%{name}/nginx_dynamic


%files -n mod_passenger
%config(noreplace) %{_httpd_modconfdir}/*.conf
%config(noreplace) %{_httpd_confdir}/*.conf
%{_httpd_moddir}/mod_passenger.so


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
