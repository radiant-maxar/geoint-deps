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
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Disable RPATH.
# https://github.com/ged/ruby-pg/issues/183
Patch0: rubygem-pg-remove-rpath.patch

BuildRequires: gcc
BuildRequires: make
BuildRequires: postgresql%{postgres_dotless}-devel
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: rubygem-bigdecimal
BuildRequires: rubygem-rake
BuildRequires: rubygems-devel

# Ensure depends on PGDG libraries it was built with.
Requires:      postgresql%{postgres_dotless}-libs
Requires:      rubygem(bigdecimal)

%description
This is the extension library to access a PostgreSQL database from Ruby.
This library works with PostgreSQL 9.1 and later.


%prep
%setup -c -n %{gem_name}-%{version}
%{__tar} -xzf data.tar.gz
%patch0 -p1


%build
%{_bindir}/rake gemspec
%{__sed} -i -e 's/^  s\.version = ".\+"/  s\.version = "%{version}"/' %{gem_name}.gemspec
%{_bindir}/gem build %{gem_name}.gemspec
%gem_install


%install
%{__mkdir_p} %{buildroot}%{gem_dir} %{buildroot}%{gem_extdir_mri}
%{__cp} -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
%{__cp} -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo (rhbz#878863).
%{__rm} -rf %{buildroot}%{gem_instdir}/ext/

# Remove useless shebangs.
%{__sed} -i -e '/^#!\/usr\/bin\/env/d' %{buildroot}%{gem_instdir}/Rakefile
%{__sed} -i -e '/^#!\/usr\/bin\/env/d' %{buildroot}%{gem_instdir}/Rakefile.cross

# Files under %%{gem_libdir} are not executable.
for file in `find %{buildroot}%{gem_libdir} -type f -name "*.rb"`; do
    %{__sed} -i '/^#!\/usr\/bin\/env/ d' $file \
    && %{__chmod} -v 0644 $file
done


%check
pushd .%{gem_instdir}
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
popd


%files
%doc %{gem_docdir}
%doc %{gem_instdir}/ChangeLog
%doc %{gem_instdir}/Contributors.rdoc
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README-OS_X.rdoc
%doc %{gem_instdir}/README-Windows.rdoc
%doc %{gem_instdir}/README.ja.rdoc
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/Rakefile*
%doc %{gem_instdir}/spec
%license %{gem_instdir}/BSDL
%license %{gem_instdir}/POSTGRES
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%exclude %{gem_instdir}/.gemtest
%{gem_extdir_mri}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}



%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
