%global gem_name rack

%bcond_without tests

Name: rubygem-%{gem_name}
Version: %{rpmbuild_version}
# Introduce Epoch (related to bug 552972)
Epoch:  1
Release: %{rpmbuild_release}%{?dist}
Summary: A modular Ruby webserver interface
# lib/rack/show_{status,exceptions}.rb contains snippets from Django under BSD license.
License: MIT and BSD
URL: https://rack.github.io/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if %{with tests}
# To make the rack tests tarball, use the following:
#
#   git clone https://github.com/rack/rack.git
#   cd rack
#   git checkout $VERSION
#   tar --owner 1000 --group 1000 --numeric-owner -czf rack-$VERSION-test.tar.gz test/
#
Source1: https://geoint-deps.s3.amazonaws.com/support-files/%{gem_name}-%{version}-test.tar.gz
%endif

BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: rubygems-devel
%if %{with tests}
BuildRequires: memcached
#BuildRequires: rubygem(memcache-client)
#BuildRequires: rubygem(minitest)
#BuildRequires: rubygem(webrick)
%endif

BuildArch: noarch

%global __brp_mangle_shebangs_exclude_from ^%{gem_instdir}/test/cgi/test.ru$

%description
Rack provides a minimal, modular and adaptable interface for developing
web applications in Ruby.  By wrapping HTTP requests and responses in
the simplest way possible, it unifies and distills the API for web
servers, web frameworks, and software in between (the so-called
middleware) into a single method call.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x
find %{buildroot}%{gem_instdir}/{bin,test/cgi} -type f | \
  xargs sed -i 's|^#!/usr/bin/env ruby$|#!/usr/bin/ruby|'

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}%{gem_instdir} -type f`; do
    [ ! -z "`head -n 1 $file | grep \"^#!\"`" ] && chmod -v 755 $file
done

%check
%if %{with tests}
pushd .%{gem_instdir}

%{__tar} xzf %{SOURCE1}

# During the building on mock environment, the testing process id 1 is owned
# by running user mockbuild's command STUBINIT, though it is owned by root user
# on usual environment.
# The server status does not return ":not_owned".
sed -i '/^  it "check pid file presence and not owned process" do$/,/^  end$/ s/^/#/' \
  test/spec_server.rb

# Get temporary PID file name and start memcached daemon.
PID=%(mktemp)
memcached -d -P "$PID"

# Rack::Session::Memcache#test_0009_maintains freshness
# requires encoding set to UTF-8:
# https://github.com/rack/rack/issues/1305
LC_ALL=en_US.UTF-8 \
ruby -Ilib:test -e 'Dir.glob "./test/spec_*.rb", &method(:require)'

# Kill memcached daemon.
kill -TERM $(< "$PID")

popd
%endif

%files
%dir %{gem_instdir}
%{_bindir}/rackup
%license %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%{gem_instdir}/bin
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/Rakefile
%{gem_instdir}/SPEC.rdoc
%doc %{gem_instdir}/example
%doc %{gem_instdir}/contrib


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
