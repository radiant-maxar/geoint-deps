# Required macro parameters to build a Ruby RPM, all must match with
# what's bundled with the Ruby source:
#
#  * bundler_version
#  * bundler_connection_pool_version
#  * bundler_fileutils_version
#  * bundler_molinillo_version
#  * bundler_net_http_persistent_version
#  * bundler_thor_version
#  * bigdecimal_version
#  * did_you_mean_version
#  * io_console_version
#  * irb_version
#  * json_version
#  * minitest_version
#  * net_telnet_version
#  * openssl_version
#  * power_assert_version
#  * psych_version
#  * racc_version
#  * rake_version
#  * rdoc_version
#  * rubygems_version
#  * rubygems_molinillo_version
#  * test_unit_version
#  * xmlrpc_version
#
%global major_version %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global minor_version %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global teeny_version %(echo %{rpmbuild_version} | awk -F. '{ print $3 }')
%global major_minor_version %{major_version}.%{minor_version}

%global ruby_version %{major_minor_version}.%{teeny_version}
%global ruby_release %{ruby_version}

# Specify the named version. It has precedense to revision.
#%%global milestone rc1

# Keep the revision enabled for pre-releases from SVN.
#%%global revision af11efd377

%global ruby_archive %{name}-%{ruby_version}

# If revision and milestone are removed/commented out, the official release build is expected.
%if 0%{?milestone:1}%{?revision:1} != 0
%global ruby_archive %{ruby_archive}-%{?milestone}%{?!milestone:%{?revision}}
%define ruby_archive_timestamp %(stat --printf='@%Y' %{ruby_archive}.tar.xz | date -f - +"%Y%m%d")
%define development_release %{?milestone}%{?!milestone:%{?revision:%{ruby_archive_timestamp}git%{revision}}}
%endif

%global release %{rpmbuild_release}
%{!?release_string:%global release_string %{?development_release:0.}%{release}%{?development_release:.%{development_release}}%{?dist}}

# The RubyGems library has to stay out of Ruby directory tree, since the
# RubyGems should be share by all Ruby implementations.
%global rubygems_dir %{_datadir}/rubygems

# Might not be needed in the future, if we are lucky enough.
# https://bugzilla.redhat.com/show_bug.cgi?id=888262
%global tapset_root %{_datadir}/systemtap
%global tapset_dir %{tapset_root}/tapset
%global tapset_libdir %(echo %{_libdir} | sed 's/64//')*

%global _normalized_cpu %(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/')

# LTO appears to cause some issue to SEGV handler.
# https://bugs.ruby-lang.org/issues/17052
%define _lto_cflags %{nil}

# Allow a way to disable problematic tests on hosts using ZFS on Linux.
%bcond_with zfs_host

Summary: An interpreter of object-oriented scripting language
Name: ruby
Version: %{ruby_version}
Release: %{release_string}
# Public Domain for example for: include/ruby/st.h, strftime.c, missing/*, ...
# MIT and CCO: ccan/*
# zlib: ext/digest/md5/md5.*, ext/nkf/nkf-utf8/nkf.c
# UCD: some of enc/trans/**/*.src
License: (Ruby or BSD) and Public Domain and MIT and CC0 and zlib and UCD
URL: http://ruby-lang.org/
Source0: https://cache.ruby-lang.org/pub/%{name}/%{major_minor_version}/%{ruby_archive}.tar.xz
Source1: ruby-operating_system.rb
# TODO: Try to push SystemTap support upstream.
Source2: ruby-libruby.stp
Source3: ruby-exercise.stp
Source4: ruby-macros
Source5: rubygems-macros
# RPM dependency generators.
Source8: rubygems.attr
Source9: rubygems.req
Source10: rubygems.prov
Source11: rubygems.con
# ABRT hoook test case.
Source13: test_abrt.rb
# SystemTap tests.
Source14: test_systemtap.rb

# Include the constants defined in macros files.
# http://rpm.org/ticket/866
%{lua:

function source_macros(file)
  local macro = nil

  for line in io.lines(file) do
    if not macro and line:match("^%%") then
      macro = line:match("^%%(.*)$")
      line = nil
    end

    if macro then
      if line and macro:match("^.-%s*\\%s*$") then
        macro = macro .. '\n' .. line
      end

      if not macro:match("^.-%s*\\%s*$") then
        rpm.define(macro)
        macro = nil
      end
    end
  end
end

source_macros(rpm.expand("%{SOURCE4}"))
source_macros(rpm.expand("%{SOURCE5}"))

}

# Fix ruby_version abuse.
# https://bugs.ruby-lang.org/issues/11002
Patch0: ruby-2.3.0-ruby_version.patch
# http://bugs.ruby-lang.org/issues/7807
Patch1: ruby-2.1.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
# Allows to override libruby.so placement. Hopefully we will be able to return
# to plain --with-rubyarchprefix.
# http://bugs.ruby-lang.org/issues/8973
Patch2: ruby-2.1.0-Enable-configuration-of-archlibdir.patch
# Force multiarch directories for i.86 to be always named i386. This solves
# some differencies in build between Fedora and RHEL.
Patch3: ruby-2.1.0-always-use-i386.patch
# Allows to install RubyGems into custom directory, outside of Ruby's tree.
# http://bugs.ruby-lang.org/issues/5617
Patch4: ruby-2.1.0-custom-rubygems-location.patch
# Make mkmf verbose by default
Patch5: ruby-1.9.3-mkmf-verbose.patch
# The ABRT hook used to be initialized by preludes via following patches:
# https://bugs.ruby-lang.org/issues/8566
# https://bugs.ruby-lang.org/issues/15306
# Unfortunately, due to https://bugs.ruby-lang.org/issues/16254
# and especially since https://github.com/ruby/ruby/pull/2735
# this would require boostrapping:
# https://lists.fedoraproject.org/archives/list/ruby-sig@lists.fedoraproject.org/message/LH6L6YJOYQT4Y5ZNOO4SLIPTUWZ5V45Q/
# For now, load the ABRT hook via this simple patch:
Patch6: ruby-2.7.0-Initialize-ABRT-hook.patch
# Disable EACCESS socket tests that won't work in a Docker build container.
Patch7: ruby-2.7.2-disable-eaccess-tests.patch
# Workaround "an invalid stdio handle" error on PPC, due to recently introduced
# hardening features of glibc (rhbz#1361037).
# https://bugs.ruby-lang.org/issues/12666
Patch9: ruby-2.3.1-Rely-on-ldd-to-detect-glibc.patch
# Revert commit which breaks bundled net-http-persistent version check.
# https://github.com/drbrain/net-http-persistent/pull/109
Patch10: ruby-2.7.0-Remove-RubyGems-dependency.patch
# Avoid possible timeout errors in TestBugReporter#test_bug_reporter_add.
# https://bugs.ruby-lang.org/issues/16492
Patch19: ruby-2.7.1-Timeout-the-test_bug_reporter_add-witout-raising-err.patch
# Revert autoconf changes from 2.7.4 that cause regressions in JIT tests.
Patch20: ruby-2.7.4-autoconf-revert.patch
# [Bug #19187] Fix for tzdata-2022g
Patch21: ruby-tzdata-2022g.patch

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: ruby(rubygems) >= %{rubygems_version}
Requires: rubygem(bigdecimal) >= %{bigdecimal_version}
Requires: rubygem(openssl) >= %{openssl_version}


BuildRequires: autoconf
BuildRequires: gcc
BuildRequires: epel-release
BuildRequires: gdbm-devel
BuildRequires: gmp-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: libyaml-devel
BuildRequires: readline-devel
BuildRequires: multilib-rpm-config
# For test TestExtLibs#test_existence_of_zlib
BuildRequires: zlib-devel
# Needed to pass test_set_program_name(TestRubyOptions)
BuildRequires: procps
BuildRequires: systemtap-sdt-devel
# RubyGems test suite optional dependencies.
BuildRequires: git
BuildRequires: cmake
# Required to test hardening.
BuildRequires: openssl
BuildRequires: checksec
Provides: ruby(runtime_executable) = %{ruby_release}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package devel
Summary:    A Ruby development environment
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   redhat-rpm-config
Requires:   rubygems-devel = %{rubygems_version}

%description devel
Header files and libraries for building an extension library for the
Ruby or an application embedding Ruby.

%package libs
Summary:    Libraries necessary to run Ruby
License:    Ruby or BSD
Provides:   ruby(release) = %{ruby_release}

# Virtual provides for CCAN copylibs.
# https://fedorahosted.org/fpc/ticket/364
Provides: bundled(ccan-build_assert)
Provides: bundled(ccan-check_type)
Provides: bundled(ccan-container_of)
Provides: bundled(ccan-list)

# StdLib default gems.
Provides: bundled(rubygem-did_you_mean) = %{did_you_mean_version}
Provides: bundled(rubygem-racc) = %{racc_version}

# Tcl/Tk support was removed from stdlib in Ruby 2.4, i.e. F27 timeframe
# so lets obsolete it. This is not the best place, but we don't have
# better, unless https://fedorahosted.org/fpc/ticket/645 provides some
# generic solution.
Obsoletes: ruby-tcltk < 2.4.0


%description libs
This package includes the libruby, necessary to run Ruby.


# TODO: Rename or not rename to ruby-rubygems?
%package -n rubygems
Summary:    The Ruby standard for packaging ruby libraries
Version:    %{rubygems_version}
License:    Ruby or MIT
Requires:   ca-certificates
Requires:   ruby(release)
Requires:   rubygem(rdoc) >= %{rdoc_version}
Requires:   rubygem(io-console) >= %{io_console_version}
Requires:   rubygem(openssl) >= %{openssl_version}
Requires:   rubygem(psych) >= %{psych_version}
Provides:   gem = %{version}-%{release}
Provides:   ruby(rubygems) = %{version}-%{release}
# https://github.com/rubygems/rubygems/pull/1189#issuecomment-121600910
Provides:   bundled(rubygem-molinillo) = %{rubygems_molinillo_version}
BuildArch:  noarch

%description -n rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.


%package -n rubygems-devel
Summary:    Macros and development tools for packaging RubyGems
Version:    %{rubygems_version}
License:    Ruby or MIT
Requires:   ruby(rubygems) >= %{version}-%{release}
# Needed for RDoc documentation format generation.
Requires:   rubygem(json) >= %{json_version}
Requires:   rubygem(rdoc) >= %{rdoc_version}
BuildArch:  noarch

%description -n rubygems-devel
Macros and development tools for packaging RubyGems.


# Default gems
#
# These packages are part of Ruby StdLib and are expected to be loadable even
# with disabled RubyGems.

%package default-gems
Summary:    Default gems which are part of Ruby StdLib.
Requires:   ruby(rubygems) >= %{rubygems_version}
# Obsoleted by Ruby 2.7 in F32 timeframe.
Obsoletes: rubygem-did_you_mean < 1.4.0-130
Obsoletes: rubygem-racc < 1.4.16-130
BuildArch:  noarch

%description default-gems
The .gemspec files and executables of default gems, which are part of Ruby
StdLib.


%package -n rubygem-irb
Summary:    The Interactive Ruby
Version:    %{irb_version}
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
# ruby-default-gems is required to run irb.
# https://bugs.ruby-lang.org/issues/16951
Requires:   ruby-default-gems >= %{ruby_version}
Provides:   irb = %{version}-%{release}
Provides:   rubygem(irb) = %{version}-%{release}
# Obsoleted by Ruby 2.6 in F30 timeframe.
Provides:   ruby(irb) = %{ruby_version}-%{release}
Provides:   ruby-irb = %{ruby_version}-%{release}
Obsoletes:  ruby-irb < %{ruby_version}-%{release}
BuildArch:  noarch

%description -n rubygem-irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.


%package -n rubygem-rdoc
Summary:    A tool to generate HTML and command-line documentation for Ruby projects
Version:    %{rdoc_version}
# SIL: lib/rdoc/generator/template/darkfish/css/fonts.css
License:    GPLv2 and Ruby and MIT and OFL
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Requires:   rubygem(irb) >= %{irb_version}
Requires:   rubygem(io-console) >= %{io_console_version}
Requires:   rubygem(json) >= %{json_version}
Provides:   rdoc = %{version}-%{release}
Provides:   ri = %{version}-%{release}
Provides:   rubygem(rdoc) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-rdoc
RDoc produces HTML and command-line documentation for Ruby projects.  RDoc
includes the 'rdoc' and 'ri' tools for generating and displaying online
documentation.


%package doc
Summary:    Documentation for %{name}
Requires:   %{_bindir}/ri
BuildArch:  noarch

%description doc
This package contains documentation for %{name}.


%package -n rubygem-bigdecimal
Summary:    BigDecimal provides arbitrary-precision floating point decimal arithmetic
Version:    %{bigdecimal_version}
License:    Ruby or BSD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(bigdecimal) = %{version}-%{release}

%description -n rubygem-bigdecimal
Ruby provides built-in support for arbitrary precision integer arithmetic.
For example:

42**13 -> 1265437718438866624512

BigDecimal provides similar support for very large or very accurate floating
point numbers. Decimal arithmetic is also useful for general calculation,
because it provides the correct answers people expect–whereas normal binary
floating point arithmetic often introduces subtle errors because of the
conversion between base 10 and base 2.


%package -n rubygem-io-console
Summary:    IO/Console is a simple console utilizing library
Version:    %{io_console_version}
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(io-console) = %{version}-%{release}

%description -n rubygem-io-console
IO/Console provides very simple and portable access to console. It does not
provide higher layer features, such like curses and readline.


%package -n rubygem-json
Summary:    This is a JSON implementation as a Ruby extension in C
Version:    %{json_version}
# UCD: ext/json/generator/generator.c
License:    (Ruby or GPLv2) and UCD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(json) = %{version}-%{release}

%description -n rubygem-json
This is a implementation of the JSON specification according to RFC 4627.
You can think of it as a low fat alternative to XML, if you want to store
data to disk or transmit it over a network rather than use a verbose
markup language.


%package -n rubygem-openssl
Summary:    OpenSSL provides SSL, TLS and general purpose cryptography
Version:    %{openssl_version}
License:    Ruby or BSD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(openssl) = %{version}-%{release}

%description -n rubygem-openssl
OpenSSL provides SSL, TLS and general purpose cryptography. It wraps the
OpenSSL library.


%package -n rubygem-psych
Summary:    A libyaml wrapper for Ruby
Version:    %{psych_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(psych) = %{version}-%{release}

%description -n rubygem-psych
Psych is a YAML parser and emitter. Psych leverages
libyaml[http://pyyaml.org/wiki/LibYAML] for its YAML parsing and emitting
capabilities. In addition to wrapping libyaml, Psych also knows how to
serialize and de-serialize most Ruby objects to and from the YAML format.


%package -n rubygem-bundler
Summary:    Library and utilities to manage a Ruby application's gem dependencies
Version:    %{bundler_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Requires:   rubygem(io-console)
Provides:   rubygem(bundler) = %{version}-%{release}
# https://github.com/bundler/bundler/issues/3647
Provides:   bundled(connection_pool) = %{bundler_connection_pool_version}
Provides:   bundled(rubygem-fileutils) = %{bundler_fileutils_version}
Provides:   bundled(rubygem-molinillo) = %{bundler_molinillo_version}
Provides:   bundled(rubygem-net-http-persisntent) = %{bundler_net_http_persistent_version}
Provides:   bundled(rubygem-thor) = %{bundler_thor_version}
BuildArch:  noarch

%description -n rubygem-bundler
Bundler manages an application's dependencies through its entire life, across
many machines, systematically and repeatably.


# Bundled gems
#
# These are regular packages, which might be installed just optionally. Users
# should list them among their dependencies (in Gemfile).

%package -n rubygem-minitest
Summary:    Minitest provides a complete suite of testing facilities
Version:    %{minitest_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(minitest) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-minitest
minitest/unit is a small and incredibly fast unit testing framework.

minitest/spec is a functionally complete spec engine.

minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.

minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.

minitest/pride shows pride in testing and adds coloring to your test
output.


%package -n rubygem-power_assert
Summary:    Power Assert for Ruby
Version:    %{power_assert_version}
License:    Ruby or BSD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(power_assert) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-power_assert
Power Assert shows each value of variables and method calls in the expression.
It is useful for testing, providing which value was not correct when the
condition is not satisfied.


%package -n rubygem-rake
Summary:    Ruby based make-like utility
Version:    %{rake_version}
License:    MIT
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rake = %{version}-%{release}
Provides:   rubygem(rake) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-rake
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.


%package -n rubygem-net-telnet
Summary:    Provides telnet client functionality
Version:    %{net_telnet_version}
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(net-telnet) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-net-telnet
Provides telnet client functionality.

This class also has, through delegation, all the methods of a socket object
(by default, a TCPSocket, but can be set by the Proxy option to new()). This
provides methods such as close() to end the session and sysread() to read data
directly from the host, instead of via the waitfor() mechanism. Note that if
you do use sysread() directly when in telnet mode, you should probably pass
the output through preprocess() to extract telnet command sequences.


%package -n rubygem-test-unit
Summary:    An xUnit family unit testing framework for Ruby
Version:    %{test_unit_version}
# lib/test/unit/diff.rb is a double license of the Ruby license and PSF license.
# lib/test-unit.rb is a dual license of the Ruby license and LGPLv2.1 or later.
License:    (Ruby or BSD) and (Ruby or BSD or Python) and (Ruby or BSD or LGPLv2+)
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Requires:   rubygem(power_assert)
Provides:   rubygem(test-unit) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-test-unit
Test::Unit (test-unit) is unit testing framework for Ruby, based on xUnit
principles. These were originally designed by Kent Beck, creator of extreme
programming software development methodology, for SUnit from Smalltalk.
It allows writing tests, checking results and automated testing in Ruby.


%package -n rubygem-xmlrpc
Summary:    XMLRPC is a lightweight protocol that enables remote procedure calls over HTTP
Version:    %{xmlrpc_version}
License:    Ruby or BSD
Requires:   ruby(release)
Requires:   ruby(rubygems) >= %{rubygems_version}
Provides:   rubygem(xmlrpc) = %{version}-%{release}
BuildArch:  noarch

%description -n rubygem-xmlrpc
XMLRPC is a lightweight protocol that enables remote procedure calls over
HTTP.


%prep
%setup -q -n %{ruby_archive}

# Remove bundled libraries to be sure they are not used.
rm -rf ext/psych/yaml
rm -rf ext/fiddle/libffi*

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch10 -p1
%patch19 -p1
%patch20 -p1

# Provide an example of usage of the tapset:
cp -a %{SOURCE3} .

%build
autoconf

%configure \
        --with-rubylibprefix='%{ruby_libdir}' \
        --with-archlibdir='%{_libdir}' \
        --with-rubyarchprefix='%{ruby_libarchdir}' \
        --with-sitedir='%{ruby_sitelibdir}' \
        --with-sitearchdir='%{ruby_sitearchdir}' \
        --with-vendordir='%{ruby_vendorlibdir}' \
        --with-vendorarchdir='%{ruby_vendorarchdir}' \
        --with-rubyhdrdir='%{_includedir}' \
        --with-rubyarchhdrdir='%{_includedir}' \
        --with-sitearchhdrdir='$(sitehdrdir)/$(arch)' \
        --with-vendorarchhdrdir='$(vendorhdrdir)/$(arch)' \
        --with-rubygemsdir='%{rubygems_dir}' \
        --with-ruby-pc='%{name}.pc' \
        --with-compress-debug-sections=no \
        --disable-rpath \
        --enable-shared \
        --with-ruby-version='' \
        --enable-multiarch

# Q= makes the build output more verbose and allows to check Fedora
# compiler options.
make %{?_smp_mflags} COPY="cp -p" Q=

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Rename ruby/config.h to ruby/config-<arch>.h to avoid file conflicts on
# multilib systems and install config.h wrapper
%multilib_fix_c_header --file %{_includedir}/%{name}/config.h
# TODO: The correct patch should be %%{_includedir}/%%{name}/rb_mjit_min_header-%%{ruby_version}.h
# https://bugs.ruby-lang.org/issues/15425
%multilib_fix_c_header --file %{_includedir}/rb_mjit_min_header-%{ruby_version}.h

# Version is empty if --with-ruby-version is specified.
# http://bugs.ruby-lang.org/issues/7807
sed -i 's/Version: \${ruby_version}/Version: %{ruby_version}/' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Kill bundled certificates, as they should be part of ca-certificates.
for cert in \
  rubygems.global.ssl.fastly.net/DigiCertHighAssuranceEVRootCA.pem \
  rubygems.org/AddTrustExternalCARoot.pem \
  index.rubygems.org/GlobalSignRootCA.pem
do
  rm %{buildroot}%{rubygems_dir}/rubygems/ssl_certs/$cert
  rm -r $(dirname %{buildroot}%{rubygems_dir}/rubygems/ssl_certs/$cert)
done
# Ensure there is not forgotten any certificate.
test ! "$(ls -A  %{buildroot}%{rubygems_dir}/rubygems/ssl_certs/ 2>/dev/null)"

# Move macros file into proper place and replace the %%{name} macro, since it
# would be wrongly evaluated during build of other packages.
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE4} %{buildroot}%{_rpmconfigdir}/macros.d/macros.ruby
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_rpmconfigdir}/macros.d/macros.ruby
install -m 644 %{SOURCE5} %{buildroot}%{_rpmconfigdir}/macros.d/macros.rubygems
sed -i "s/%%{name}/%{name}/" %{buildroot}%{_rpmconfigdir}/macros.d/macros.rubygems

# Install dependency generators.
mkdir -p %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 644 %{SOURCE8} %{buildroot}%{_rpmconfigdir}/fileattrs
install -m 755 %{SOURCE9} %{buildroot}%{_rpmconfigdir}
install -m 755 %{SOURCE10} %{buildroot}%{_rpmconfigdir}
install -m 755 %{SOURCE11} %{buildroot}%{_rpmconfigdir}

# Install custom operating_system.rb.
mkdir -p %{buildroot}%{rubygems_dir}/rubygems/defaults
cp %{SOURCE1} %{buildroot}%{rubygems_dir}/rubygems/defaults/operating_system.rb

# Move gems root into common direcotry, out of Ruby directory structure.
mv %{buildroot}%{ruby_libdir}/gems %{buildroot}%{gem_dir}

# Create folders for gem binary extensions.
# TODO: These folders should go into rubygem-filesystem but how to achieve it,
# since noarch package cannot provide arch dependent subpackages?
# http://rpm.org/ticket/78
mkdir -p %{buildroot}%{_exec_prefix}/lib{,64}/gems/%{name}

# Move bundled rubygems to %%gem_dir and %%gem_extdir_mri
# make symlinks for io-console and bigdecimal, which are considered to be part of stdlib by other Gems
mkdir -p %{buildroot}%{gem_dir}/gems/irb-%{irb_version}/lib
mv %{buildroot}%{ruby_libdir}/irb* %{buildroot}%{gem_dir}/gems/irb-%{irb_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/irb-%{irb_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/irb-%{irb_version}/lib/irb.rb %{buildroot}%{ruby_libdir}/irb.rb
# TODO: This should be possible to replaced by simple directory symlink
# after ~ F31 EOL (rhbz#1691039).
mkdir -p %{buildroot}%{ruby_libdir}/irb
pushd %{buildroot}%{gem_dir}/gems/irb-%{irb_version}/lib
find irb -type d -mindepth 1 -exec mkdir %{buildroot}%{ruby_libdir}/'{}' \;
find irb -type f -exec ln -s %{gem_dir}/gems/irb-%{irb_version}/lib/'{}' %{buildroot}%{ruby_libdir}/'{}' \;
popd

mkdir -p %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_version}/lib
mv %{buildroot}%{ruby_libdir}/rdoc* %{buildroot}%{gem_dir}/gems/rdoc-%{rdoc_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/rdoc-%{rdoc_version}.gemspec %{buildroot}%{gem_dir}/specifications

mkdir -p %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/bigdecimal
mv %{buildroot}%{ruby_libdir}/bigdecimal %{buildroot}%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib
mv %{buildroot}%{ruby_libarchdir}/bigdecimal.so %{buildroot}%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}
mv %{buildroot}%{gem_dir}/specifications/default/bigdecimal-%{bigdecimal_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/bigdecimal-%{bigdecimal_version}/lib/bigdecimal %{buildroot}%{ruby_libdir}/bigdecimal
ln -s %{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}/bigdecimal.so %{buildroot}%{ruby_libarchdir}/bigdecimal.so

# TODO: Put help files into proper location.
# https://bugs.ruby-lang.org/issues/15359
mkdir -p %{buildroot}%{gem_dir}/gems/bundler-%{bundler_version}/lib
mv %{buildroot}%{ruby_libdir}/bundler.rb %{buildroot}%{gem_dir}/gems/bundler-%{bundler_version}/lib
mv %{buildroot}%{ruby_libdir}/bundler %{buildroot}%{gem_dir}/gems/bundler-%{bundler_version}/lib
mv %{buildroot}%{gem_dir}/specifications/default/bundler-%{bundler_version}.gemspec %{buildroot}%{gem_dir}/specifications

mkdir -p %{buildroot}%{gem_dir}/gems/io-console-%{io_console_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/io-console-%{io_console_version}/io
mv %{buildroot}%{ruby_libdir}/io %{buildroot}%{gem_dir}/gems/io-console-%{io_console_version}/lib
mv %{buildroot}%{ruby_libarchdir}/io/console.so %{buildroot}%{_libdir}/gems/%{name}/io-console-%{io_console_version}/io
mv %{buildroot}%{gem_dir}/specifications/default/io-console-%{io_console_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/io-console-%{io_console_version}/lib/io %{buildroot}%{ruby_libdir}/io
ln -s %{_libdir}/gems/%{name}/io-console-%{io_console_version}/io/console.so %{buildroot}%{ruby_libarchdir}/io/console.so

mkdir -p %{buildroot}%{gem_dir}/gems/json-%{json_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/json-%{json_version}
mv %{buildroot}%{ruby_libdir}/json* %{buildroot}%{gem_dir}/gems/json-%{json_version}/lib
mv %{buildroot}%{ruby_libarchdir}/json/ %{buildroot}%{_libdir}/gems/%{name}/json-%{json_version}/
mv %{buildroot}%{gem_dir}/specifications/default/json-%{json_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/json-%{json_version}/lib/json.rb %{buildroot}%{ruby_libdir}/json.rb
ln -s %{gem_dir}/gems/json-%{json_version}/lib/json %{buildroot}%{ruby_libdir}/json
ln -s %{_libdir}/gems/%{name}/json-%{json_version}/json/ %{buildroot}%{ruby_libarchdir}/json

mkdir -p %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/openssl-%{openssl_version}
mv %{buildroot}%{ruby_libdir}/openssl* %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib
mv %{buildroot}%{ruby_libarchdir}/openssl.so %{buildroot}%{_libdir}/gems/%{name}/openssl-%{openssl_version}/
mv %{buildroot}%{gem_dir}/specifications/default/openssl-%{openssl_version}.gemspec %{buildroot}%{gem_dir}/specifications
# This used to be directory when OpenSSL was integral part of StdLib => Keep
# it as directory and link everything in it to prevent directory => symlink
# conversion RPM issues.
mkdir -p %{buildroot}%{ruby_libdir}/openssl
find %{buildroot}%{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl -maxdepth 1 -type f -exec \
  sh -c 'ln -s %{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl/`basename {}` %{buildroot}%{ruby_libdir}/openssl' \;
ln -s %{gem_dir}/gems/openssl-%{openssl_version}/lib/openssl.rb %{buildroot}%{ruby_libdir}/openssl.rb
ln -s %{_libdir}/gems/%{name}/openssl-%{openssl_version}/openssl.so %{buildroot}%{ruby_libarchdir}/openssl.so

mkdir -p %{buildroot}%{gem_dir}/gems/psych-%{psych_version}/lib
mkdir -p %{buildroot}%{_libdir}/gems/%{name}/psych-%{psych_version}
mv %{buildroot}%{ruby_libdir}/psych* %{buildroot}%{gem_dir}/gems/psych-%{psych_version}/lib
mv %{buildroot}%{ruby_libarchdir}/psych.so %{buildroot}%{_libdir}/gems/%{name}/psych-%{psych_version}/
mv %{buildroot}%{gem_dir}/specifications/default/psych-%{psych_version}.gemspec %{buildroot}%{gem_dir}/specifications
ln -s %{gem_dir}/gems/psych-%{psych_version}/lib/psych %{buildroot}%{ruby_libdir}/psych
ln -s %{gem_dir}/gems/psych-%{psych_version}/lib/psych.rb %{buildroot}%{ruby_libdir}/psych.rb
ln -s %{_libdir}/gems/%{name}/psych-%{psych_version}/psych.so %{buildroot}%{ruby_libarchdir}/psych.so

# Move the binary extensions into proper place (if no gem has binary extension,
# the extensions directory might be empty).
find %{buildroot}%{gem_dir}/extensions/*-%{_target_os}/%{ruby_version}/* -maxdepth 0 \
  -exec mv '{}' %{buildroot}%{_libdir}/gems/%{name}/ \; \
  || echo "No gem binary extensions to move."

# Move man pages into proper location
mv %{buildroot}%{gem_dir}/gems/rake-%{rake_version}/doc/rake.1 %{buildroot}%{_mandir}/man1

# Install a tapset and fix up the path to the library.
mkdir -p %{buildroot}%{tapset_dir}
sed -e "s|@LIBRARY_PATH@|%{tapset_libdir}/libruby.so.%{major_minor_version}|" \
  %{SOURCE2} > %{buildroot}%{tapset_dir}/libruby.so.%{major_minor_version}.stp
# Escape '*/' in comment.
sed -i -r "s|( \*.*\*)\/(.*)|\1\\\/\2|" %{buildroot}%{tapset_dir}/libruby.so.%{major_minor_version}.stp

# Prepare -doc subpackage file lists.
find doc -maxdepth 1 -type f ! -name '.*' ! -name '*.ja*' > .ruby-doc.en
echo 'doc/images' >> .ruby-doc.en
echo 'doc/syntax' >> .ruby-doc.en

find doc -maxdepth 1 -type f -name '*.ja*' > .ruby-doc.ja
echo 'doc/irb' >> .ruby-doc.ja
echo 'doc/pty' >> .ruby-doc.ja

sed -i 's/^/%doc /' .ruby-doc.*
sed -i 's/^/%lang(ja) /' .ruby-doc.ja

# Remove useless .github directory from Rake.
# https://github.com/ruby/rake/pull/333
rm -rf %{buildroot}%{gem_dir}/gems/rake-%{rake_version}/.github

# Remove accidentaly added files
# https://bugs.ruby-lang.org/issues/17784
rm -rf %{buildroot}%{ruby_libdir}/exe/


%check
# Check Ruby hardening.
checksec --file=libruby.so.%{ruby_version} | \
  grep "Full RELRO.*Canary found.*NX enabled.*DSO.*No RPATH.*No RUNPATH.*Yes.*\d*.*\d*.*libruby.so.%{ruby_version}"

# Check RubyGems version.
[ "`make runruby TESTRUN_SCRIPT='bin/gem -v' | tail -1`" == '%{rubygems_version}' ]

# Check Rubygems bundled dependencies versions.

# Molinillo.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Gem; module Resolver; end; end; \
  require 'rubygems/resolver/molinillo/lib/molinillo/gem_metadata'; \
  puts Gem::Resolver::Molinillo::VERSION\\\"\" | tail -1`" \
  == '%{rubygems_molinillo_version}' ]

# Check Bundler bundled dependencies versions.

# connection_pool.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Bundler; end; \
  require 'bundler/vendor/connection_pool/lib/connection_pool/version'; \
  puts Bundler::ConnectionPool::VERSION\\\"\" | tail -1`" \
  == '%{bundler_connection_pool_version}' ]

# FileUtils.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Bundler; end; \
  require 'bundler/vendor/fileutils/lib/fileutils/version'; \
  puts Bundler::FileUtils::VERSION\\\"\" | tail -1`" \
  == '%{bundler_fileutils_version}' ]

# Molinillo.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Bundler; end; \
  require 'bundler/vendor/molinillo/lib/molinillo/gem_metadata'; \
  puts Bundler::Molinillo::VERSION\\\"\" | tail -1`" \
  == '%{bundler_molinillo_version}' ]

# Net::HTTP::Persistent.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Bundler; module Persistent; module Net; module HTTP; \
  end; end; end; end; \
  require 'bundler/vendor/net-http-persistent/lib/net/http/persistent'; \
  puts Bundler::Persistent::Net::HTTP::Persistent::VERSION\\\"\" | tail -1`" \
  == '%{bundler_net_http_persistent_version}' ]

# Thor.
[ "`make runruby TESTRUN_SCRIPT=\"-e \\\" \
  module Bundler; end; \
  require 'bundler/vendor/thor/lib/thor/version'; \
  puts Bundler::Thor::VERSION\\\"\" | tail -1`" \
  == '%{bundler_thor_version}' ]


# test_debug(TestRubyOptions) fails due to LoadError reported in debug mode,
# when abrt.rb cannot be required (seems to be easier way then customizing
# the test suite).
touch abrt.rb

# Check if abrt hook is required (RubyGems are disabled by default when using
# runruby, so re-enable them).
make runruby TESTRUN_SCRIPT="--enable-gems %{SOURCE13}"

# Check if systemtap is supported.
make runruby TESTRUN_SCRIPT=%{SOURCE14}

DISABLE_TESTS=""
MSPECOPTS=""

# Avoid `hostname' dependency.
%{!?with_hostname:MSPECOPTS="-P 'Socket.gethostname returns the host name'"}

# Avoid dependency on IPv6 to run the tests.
sed -i -e 's/localhost/127.0.0.1/g' test/net/http/test_http.rb
rm -f test/net/smtp/test_smtp.rb

%if %{with zfs_host}
# Remove tests that make assumptions of underlying filesystem and crash
# with ZFS on Linux.
rm -f \
   test/ruby/test_dir_m17n.rb \
   test/ruby/test_io.rb \
   test/ruby/test_io_m17n.rb \
   test/ruby/test_require.rb

%endif
# Disable "File.utime allows Time instances in the far future to set
# mtime and atime".
# https://bugs.ruby-lang.org/issues/16410
MSPECOPTS="$MSPECOPTS -P 'File.utime allows Time instances in the far future to set mtime and atime'"

# Give an option to increase the timeout in tests.
# https://bugs.ruby-lang.org/issues/16921
%{?test_timeout_scale:RUBY_TEST_TIMEOUT_SCALE="%{test_timeout_scale}"} \
  make check TESTS="-v $DISABLE_TESTS" MSPECOPT="-fs $MSPECOPTS"


%files
%license BSDL
%license COPYING
%lang(ja) %license COPYING.ja
%license GPL
%license LEGAL
%{_bindir}/erb
%{_bindir}/%{name}
%{_mandir}/man1/erb*
%{_mandir}/man1/ruby*

%files devel
%license BSDL
%license COPYING
%lang(ja) %license COPYING.ja
%license GPL
%license LEGAL

%{_rpmconfigdir}/macros.d/macros.ruby

%{_includedir}/*
%{_libdir}/libruby.so
%{_libdir}/pkgconfig/%{name}.pc

%files libs
%license COPYING
%lang(ja) %license COPYING.ja
%license GPL
%license LEGAL
%doc README.md
%doc NEWS
# Exclude /usr/local directory since it is supposed to be managed by
# local system administrator.
%exclude %{ruby_sitelibdir}
%exclude %{ruby_sitearchdir}
%dir %{ruby_vendorlibdir}
%dir %{ruby_vendorarchdir}

# List all these files explicitly to prevent surprises
# Platform independent libraries.
%dir %{ruby_libdir}
%exclude %{ruby_libdir}/bigdecimal*
%exclude %{ruby_libdir}/irb*
%exclude %{ruby_libdir}/json*
%exclude %{ruby_libdir}/openssl*
%exclude %{ruby_libdir}/psych*
%{ruby_libdir}/abbrev.rb
%{ruby_libdir}/base64.rb
%{ruby_libdir}/benchmark*
%{ruby_libdir}/cgi*
%{ruby_libdir}/coverage.rb
%{ruby_libdir}/csv*
%{ruby_libdir}/date.rb
%{ruby_libdir}/debug.rb
%{ruby_libdir}/delegate*
%{ruby_libdir}/digest*
%{ruby_libdir}/drb*
%{ruby_libdir}/English.rb
%{ruby_libdir}/erb.rb
%{ruby_libdir}/expect.rb
%{ruby_libdir}/fiddle*
%{ruby_libdir}/fileutils.rb
%{ruby_libdir}/find.rb
%{ruby_libdir}/forwardable*
%{ruby_libdir}/getoptlong*
%{ruby_libdir}/io
%{ruby_libdir}/ipaddr.rb
%{ruby_libdir}/kconv.rb
%{ruby_libdir}/logger*
%{ruby_libdir}/matrix*
%{ruby_libdir}/mkmf.rb
%{ruby_libdir}/monitor.rb
%{ruby_libdir}/mutex_m.rb
%{ruby_libdir}/net
%{ruby_libdir}/observer*
%{ruby_libdir}/open-uri.rb
%{ruby_libdir}/open3*
%{ruby_libdir}/optionparser.rb
%{ruby_libdir}/optparse*
%{ruby_libdir}/ostruct*
%{ruby_libdir}/pathname.rb
%{ruby_libdir}/pp.rb
%{ruby_libdir}/prettyprint.rb
%{ruby_libdir}/prime.rb
%{ruby_libdir}/pstore*
%{ruby_libdir}/readline.rb
%{ruby_libdir}/reline*
%{ruby_libdir}/resolv.rb
%{ruby_libdir}/resolv-replace.rb
%{ruby_libdir}/rexml
%{ruby_libdir}/rinda
%{ruby_libdir}/ripper*
%{ruby_libdir}/rss*
%{ruby_libdir}/securerandom.rb
%{ruby_libdir}/set.rb
%{ruby_libdir}/shellwords.rb
%{ruby_libdir}/singleton*
%{ruby_libdir}/socket.rb
%{ruby_libdir}/syslog
%{ruby_libdir}/tempfile.rb
%{ruby_libdir}/timeout*
%{ruby_libdir}/time.rb
%{ruby_libdir}/tmpdir.rb
%{ruby_libdir}/tracer*
%{ruby_libdir}/tsort.rb
%{ruby_libdir}/unicode_normalize
%{ruby_libdir}/un.rb
%{ruby_libdir}/uri*
%{ruby_libdir}/weakref*
%{ruby_libdir}/webrick*
%{ruby_libdir}/yaml*

# Platform specific libraries.
%{_libdir}/libruby.so.*
%dir %{ruby_libarchdir}
%dir %{ruby_libarchdir}/cgi
%{ruby_libarchdir}/cgi/escape.so
%{ruby_libarchdir}/continuation.so
%{ruby_libarchdir}/coverage.so
%{ruby_libarchdir}/date_core.so
%{ruby_libarchdir}/dbm.so
%dir %{ruby_libarchdir}/digest
%{ruby_libarchdir}/digest.so
%{ruby_libarchdir}/digest/bubblebabble.so
%{ruby_libarchdir}/digest/md5.so
%{ruby_libarchdir}/digest/rmd160.so
%{ruby_libarchdir}/digest/sha1.so
%{ruby_libarchdir}/digest/sha2.so
%dir %{ruby_libarchdir}/enc
%{ruby_libarchdir}/enc/big5.so
%{ruby_libarchdir}/enc/cesu_8.so
%{ruby_libarchdir}/enc/cp949.so
%{ruby_libarchdir}/enc/emacs_mule.so
%{ruby_libarchdir}/enc/encdb.so
%{ruby_libarchdir}/enc/euc_jp.so
%{ruby_libarchdir}/enc/euc_kr.so
%{ruby_libarchdir}/enc/euc_tw.so
%{ruby_libarchdir}/enc/gb18030.so
%{ruby_libarchdir}/enc/gb2312.so
%{ruby_libarchdir}/enc/gbk.so
%{ruby_libarchdir}/enc/iso_8859_1.so
%{ruby_libarchdir}/enc/iso_8859_10.so
%{ruby_libarchdir}/enc/iso_8859_11.so
%{ruby_libarchdir}/enc/iso_8859_13.so
%{ruby_libarchdir}/enc/iso_8859_14.so
%{ruby_libarchdir}/enc/iso_8859_15.so
%{ruby_libarchdir}/enc/iso_8859_16.so
%{ruby_libarchdir}/enc/iso_8859_2.so
%{ruby_libarchdir}/enc/iso_8859_3.so
%{ruby_libarchdir}/enc/iso_8859_4.so
%{ruby_libarchdir}/enc/iso_8859_5.so
%{ruby_libarchdir}/enc/iso_8859_6.so
%{ruby_libarchdir}/enc/iso_8859_7.so
%{ruby_libarchdir}/enc/iso_8859_8.so
%{ruby_libarchdir}/enc/iso_8859_9.so
%{ruby_libarchdir}/enc/koi8_r.so
%{ruby_libarchdir}/enc/koi8_u.so
%{ruby_libarchdir}/enc/shift_jis.so
%dir %{ruby_libarchdir}/enc/trans
%{ruby_libarchdir}/enc/trans/big5.so
%{ruby_libarchdir}/enc/trans/cesu_8.so
%{ruby_libarchdir}/enc/trans/chinese.so
%{ruby_libarchdir}/enc/trans/ebcdic.so
%{ruby_libarchdir}/enc/trans/emoji.so
%{ruby_libarchdir}/enc/trans/emoji_iso2022_kddi.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_docomo.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_kddi.so
%{ruby_libarchdir}/enc/trans/emoji_sjis_softbank.so
%{ruby_libarchdir}/enc/trans/escape.so
%{ruby_libarchdir}/enc/trans/gb18030.so
%{ruby_libarchdir}/enc/trans/gbk.so
%{ruby_libarchdir}/enc/trans/iso2022.so
%{ruby_libarchdir}/enc/trans/japanese.so
%{ruby_libarchdir}/enc/trans/japanese_euc.so
%{ruby_libarchdir}/enc/trans/japanese_sjis.so
%{ruby_libarchdir}/enc/trans/korean.so
%{ruby_libarchdir}/enc/trans/single_byte.so
%{ruby_libarchdir}/enc/trans/transdb.so
%{ruby_libarchdir}/enc/trans/utf8_mac.so
%{ruby_libarchdir}/enc/trans/utf_16_32.so
%{ruby_libarchdir}/enc/utf_16be.so
%{ruby_libarchdir}/enc/utf_16le.so
%{ruby_libarchdir}/enc/utf_32be.so
%{ruby_libarchdir}/enc/utf_32le.so
%{ruby_libarchdir}/enc/windows_1250.so
%{ruby_libarchdir}/enc/windows_1251.so
%{ruby_libarchdir}/enc/windows_1252.so
%{ruby_libarchdir}/enc/windows_1253.so
%{ruby_libarchdir}/enc/windows_1254.so
%{ruby_libarchdir}/enc/windows_1257.so
%{ruby_libarchdir}/enc/windows_31j.so
%{ruby_libarchdir}/etc.so
%{ruby_libarchdir}/fcntl.so
%{ruby_libarchdir}/fiber.so
%{ruby_libarchdir}/fiddle.so
%{ruby_libarchdir}/gdbm.so
%dir %{ruby_libarchdir}/io
%{ruby_libarchdir}/io/nonblock.so
%{ruby_libarchdir}/io/wait.so
%{ruby_libarchdir}/monitor.so
%{ruby_libarchdir}/nkf.so
%{ruby_libarchdir}/objspace.so
%{ruby_libarchdir}/pathname.so
%{ruby_libarchdir}/pty.so
%dir %{ruby_libarchdir}/rbconfig
%{ruby_libarchdir}/rbconfig.rb
%{ruby_libarchdir}/rbconfig/sizeof.so
%{ruby_libarchdir}/readline.so
%{ruby_libarchdir}/ripper.so
%{ruby_libarchdir}/sdbm.so
%{ruby_libarchdir}/socket.so
%{ruby_libarchdir}/stringio.so
%{ruby_libarchdir}/strscan.so
%{ruby_libarchdir}/syslog.so
%{ruby_libarchdir}/zlib.so

# Default gems
%{ruby_libdir}/did_you_mean*
%{ruby_libdir}/racc*
%dir %{ruby_libarchdir}/racc
%{ruby_libarchdir}/racc/cparse.so

%{tapset_root}

%files -n rubygems
%{_bindir}/gem
%dir %{rubygems_dir}
%{rubygems_dir}/rubygems
%{rubygems_dir}/rubygems.rb

# Explicitly include only RubyGems directory strucure to avoid accidentally
# packaged content.
%dir %{gem_dir}
%dir %{gem_dir}/build_info
%dir %{gem_dir}/cache
%dir %{gem_dir}/doc
%dir %{gem_dir}/extensions
%dir %{gem_dir}/gems
%dir %{gem_dir}/specifications
%dir %{gem_dir}/specifications/default
%dir %{_exec_prefix}/lib*/gems
%dir %{_exec_prefix}/lib*/gems/ruby

%exclude %{gem_dir}/cache/*

%files -n rubygems-devel
%{_rpmconfigdir}/macros.d/macros.rubygems
%{_rpmconfigdir}/fileattrs/rubygems.attr
%{_rpmconfigdir}/rubygems.req
%{_rpmconfigdir}/rubygems.prov
%{_rpmconfigdir}/rubygems.con

%files default-gems
%{gem_dir}/specifications/default/benchmark-0.1.0.gemspec
%{gem_dir}/specifications/default/cgi-0.1.0.2.gemspec
%{gem_dir}/specifications/default/csv-3.1.2.gemspec
%{gem_dir}/specifications/default/date-3.0.3.gemspec
%{gem_dir}/specifications/default/dbm-1.1.0.gemspec
%{gem_dir}/specifications/default/delegate-0.1.0.gemspec
%{gem_dir}/specifications/default/did_you_mean-%{did_you_mean_version}.gemspec
%{gem_dir}/specifications/default/etc-1.1.0.gemspec
%{gem_dir}/specifications/default/fcntl-1.0.0.gemspec
%{gem_dir}/specifications/default/fiddle-1.0.0.gemspec
%{gem_dir}/specifications/default/fileutils-1.4.1.gemspec
%{gem_dir}/specifications/default/forwardable-1.3.1.gemspec
%{gem_dir}/specifications/default/gdbm-2.1.0.gemspec
%{gem_dir}/specifications/default/getoptlong-0.1.0.gemspec
%{gem_dir}/specifications/default/ipaddr-1.2.2.gemspec
%{gem_dir}/specifications/default/logger-1.4.2.gemspec
%{gem_dir}/specifications/default/matrix-0.2.0.gemspec
%{gem_dir}/specifications/default/mutex_m-0.1.0.gemspec
%{gem_dir}/specifications/default/net-pop-0.1.0.gemspec
%{gem_dir}/specifications/default/net-smtp-0.1.0.gemspec
%{gem_dir}/specifications/default/observer-0.1.0.gemspec
%{gem_dir}/specifications/default/open3-0.1.0.gemspec
%{gem_dir}/specifications/default/ostruct-0.2.0.gemspec
%{gem_dir}/specifications/default/prime-0.1.1.gemspec
%{gem_dir}/specifications/default/pstore-0.1.0.gemspec
%{gem_dir}/specifications/default/racc-%{racc_version}.gemspec
%{gem_dir}/specifications/default/readline-0.0.2.gemspec
%{gem_dir}/specifications/default/readline-ext-0.1.0.gemspec
%{gem_dir}/specifications/default/reline-0.1.5.gemspec
%{gem_dir}/specifications/default/rexml-3.2.3.1.gemspec
%{gem_dir}/specifications/default/rss-0.2.8.gemspec
%{gem_dir}/specifications/default/sdbm-1.0.0.gemspec
%{gem_dir}/specifications/default/singleton-0.1.0.gemspec
%{gem_dir}/specifications/default/stringio-0.1.0.gemspec
%{gem_dir}/specifications/default/strscan-1.0.3.gemspec
%{gem_dir}/specifications/default/timeout-0.1.0.gemspec
%{gem_dir}/specifications/default/tracer-0.1.0.gemspec
%{gem_dir}/specifications/default/uri-0.10.0.gemspec
%{gem_dir}/specifications/default/webrick-1.6.1.gemspec
%{gem_dir}/specifications/default/yaml-0.1.0.gemspec
%{gem_dir}/specifications/default/zlib-1.1.0.gemspec

# Use standalone rubygem-racc if Racc binary is required. Shipping this
# executable in both packages might possibly cause conflicts. The situation
# could be better if Ruby generated these files:
# https://github.com/ruby/ruby/pull/2545
%exclude %{_bindir}/racc
# These have wrong shebangs. Exclude them for now and let's see what upstream
# thinks about them.
# https://bugs.ruby-lang.org/issues/15982
%exclude %{_bindir}/racc2y
%exclude %{_bindir}/y2racc
%exclude %{gem_dir}/gems/racc-%{racc_version}/bin/racc2y
%exclude %{gem_dir}/gems/racc-%{racc_version}/bin/y2racc
%{gem_dir}/gems/racc-%{racc_version}

%files -n rubygem-irb
%{_bindir}/irb
%{ruby_libdir}/irb*
%{gem_dir}/gems/irb-%{irb_version}
%{gem_dir}/specifications/irb-%{irb_version}.gemspec
%{_mandir}/man1/irb.1*

%files -n rubygem-rdoc
%{_bindir}/rdoc
%{_bindir}/ri
%{gem_dir}/gems/rdoc-%{rdoc_version}
%{gem_dir}/specifications/rdoc-%{rdoc_version}.gemspec
%{_mandir}/man1/ri*

%files doc -f .ruby-doc.en -f .ruby-doc.ja
%doc README.md
%doc ChangeLog
%doc ruby-exercise.stp
%{_datadir}/ri

%files -n rubygem-bigdecimal
%{ruby_libdir}/bigdecimal*
%{ruby_libarchdir}/bigdecimal*
%{_libdir}/gems/%{name}/bigdecimal-%{bigdecimal_version}
%{gem_dir}/gems/bigdecimal-%{bigdecimal_version}
%{gem_dir}/specifications/bigdecimal-%{bigdecimal_version}.gemspec

%files -n rubygem-io-console
%{ruby_libdir}/io
%{ruby_libarchdir}/io/console.so
%{_libdir}/gems/%{name}/io-console-%{io_console_version}
%{gem_dir}/gems/io-console-%{io_console_version}
%{gem_dir}/specifications/io-console-%{io_console_version}.gemspec

%files -n rubygem-json
%{ruby_libdir}/json*
%{ruby_libarchdir}/json*
%{_libdir}/gems/%{name}/json-%{json_version}
%{gem_dir}/gems/json-%{json_version}
%{gem_dir}/specifications/json-%{json_version}.gemspec

%files -n rubygem-openssl
%{ruby_libdir}/openssl
%{ruby_libdir}/openssl.rb
%{ruby_libarchdir}/openssl.so
%{_libdir}/gems/%{name}/openssl-%{openssl_version}
%{gem_dir}/gems/openssl-%{openssl_version}
%{gem_dir}/specifications/openssl-%{openssl_version}.gemspec

%files -n rubygem-psych
%{ruby_libdir}/psych
%{ruby_libdir}/psych.rb
%{ruby_libarchdir}/psych.so
%{_libdir}/gems/%{name}/psych-%{psych_version}
%{gem_dir}/gems/psych-%{psych_version}
%{gem_dir}/specifications/psych-%{psych_version}.gemspec

%files -n rubygem-bundler
%{_bindir}/bundle
%{_bindir}/bundler
%{gem_dir}/gems/bundler-%{bundler_version}
%{gem_dir}/specifications/bundler-%{bundler_version}.gemspec
%{_mandir}/man1/bundle*.1*
%{_mandir}/man5/gemfile.5*

%files -n rubygem-minitest
%{gem_dir}/gems/minitest-%{minitest_version}
%exclude %{gem_dir}/gems/minitest-%{minitest_version}/.*
%{gem_dir}/specifications/minitest-%{minitest_version}.gemspec

%files -n rubygem-net-telnet
%{gem_dir}/gems/net-telnet-%{net_telnet_version}
%exclude %{gem_dir}/gems/net-telnet-%{net_telnet_version}/.*
%{gem_dir}/specifications/net-telnet-%{net_telnet_version}.gemspec

%files -n rubygem-power_assert
%{gem_dir}/gems/power_assert-%{power_assert_version}
%exclude %{gem_dir}/gems/power_assert-%{power_assert_version}/.*
%{gem_dir}/specifications/power_assert-%{power_assert_version}.gemspec

%files -n rubygem-rake
%{_bindir}/rake
%{gem_dir}/gems/rake-%{rake_version}
%{gem_dir}/specifications/rake-%{rake_version}.gemspec
%{_mandir}/man1/rake.1*

%files -n rubygem-test-unit
%{gem_dir}/gems/test-unit-%{test_unit_version}
%{gem_dir}/specifications/test-unit-%{test_unit_version}.gemspec

%files -n rubygem-xmlrpc
%license %{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/LICENSE.txt
%dir %{gem_dir}/gems/xmlrpc-%{xmlrpc_version}
%exclude %{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/.*
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/Gemfile
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/Rakefile
%doc %{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/README.md
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/bin
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/lib
%{gem_dir}/gems/xmlrpc-%{xmlrpc_version}/xmlrpc.gemspec
%{gem_dir}/specifications/xmlrpc-%{xmlrpc_version}.gemspec


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
