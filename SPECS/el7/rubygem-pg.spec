%global gem_name pg

Name: rubygem-%{gem_name}
Version: %{rpmbuild_version}
Release: %{rpmbuild_release}%{?dist}
Summary: A Ruby interface to the PostgreSQL RDBMS
# Upstream license clarification (https://bitbucket.org/ged/ruby-pg/issue/72/)
#
# The portions of the code that are BSD-licensed are licensed under
# the BSD 3-Clause license; the contents of the BSD file are incorrect.
#
License: (BSD or Ruby) and PostgreSQL
URL: https://github.com/ged/ruby-pg
Source0: https://github.com/ged/ruby-pg/archive/v%{version}/ruby-pg-%{version}.tar.gz
# Disable RPATH.
# https://github.com/ged/ruby-pg/issues/183
Patch0: rubygem-pg-1.3.0-remove-rpath.patch

BuildRequires: gcc
BuildRequires: make
BuildRequires: postgresql%{postgres_version}-devel
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: rubygem-bigdecimal
BuildRequires: rubygem-bundler
BuildRequires: rubygem-rake
BuildRequires: rubygems-devel

# Ensure depends on PGDG libraries it was built with.
Requires:      postgresql%{postgres_version}-libs
Requires:      rubygem(bigdecimal)

%description
This is the extension library to access a PostgreSQL database from Ruby.
This library works with PostgreSQL 9.3 and later.


%prep
%autosetup -p1 -n ruby-pg-%{version}


%build
%{_bindir}/rake build
mv pkg/%{gem_name}-%{version}.gem .
%gem_install
%{_bindir}/rake compile


%install
%{__install} -d %{buildroot}%{gem_dir} %{buildroot}%{gem_extdir_mri} %{buildroot}%{gem_instdir}/lib
%{__cp} -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
%{__cp} -a lib/pg lib/pg.rb %{buildroot}%{gem_instdir}/lib
%{__cp} -a .%{gem_extdir_mri}/gem.build_complete lib/*.so %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
%{__rm} -rf %{buildroot}%{gem_instdir}/ext/


%check
# Set --verbose to show detail log by $VERBOSE.
# See https://github.com/ged/ruby-pg/blob/master/spec/helpers.rb $VERBOSE
# Assign a random port to consider a case of multi builds in parallel in a host.
# https://github.com/ged/ruby-pg/pull/39
if ! PGPORT="$((54321 + ${RANDOM} % 1000))" ruby -S --verbose \
  rspec -I$(dirs +1)%{gem_extdir_mri} -f d spec; then
  echo "==== [setup.log start ] ===="
  cat tmp_test_specs/setup.log
  echo "==== [setup.log end ] ===="
  false
fi


%files
%doc %{gem_docdir}
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gemtest
%{gem_extdir_mri}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}



%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
