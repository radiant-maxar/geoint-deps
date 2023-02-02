%global gem_name libxml-ruby

Name: rubygem-%{gem_name}
Version: %{rpmbuild_version}
Release: %{rpmbuild_release}%{?dist}
Summary: Ruby Bindings for LibXML2
License: MIT
URL: https://github.com/xml4r/libxml-ruby
Source0: https://rubygems.org/gems/libxml-ruby-%{version}.gem
Patch0: rubygem-libxml-ruby-fix-tests.patch

BuildRequires: gcc
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: rubygem-bundler
BuildRequires: rubygem-rake
BuildRequires: rubygems-devel

%description
The Libxml-Ruby project provides Ruby language bindings for the GNOME
Libxml2 XML toolkit. It is free software, released under the MIT License.
Libxml-ruby's primary advantage over REXML is performance - if speed
is your need, this is a good library to consider.


%prep
%setup -c -n %{gem_name}-%{version}
%{__tar} -xzf data.tar.gz
%patch0 -p1


%build
%{_bindir}/gem build %{gem_name}.gemspec
%gem_install


%install
%{__mkdir_p} %{buildroot}%{gem_dir} %{buildroot}%{gem_extdir_mri}
%{__cp} -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
%{__cp} -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/


%check
%{_bindir}/rake compile
%{_bindir}/rake test


%files
%doc %{gem_instdir}/HISTORY
%doc %{gem_instdir}/README.rdoc
%doc %{gem_docdir}
%doc %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/script
%doc %{gem_instdir}/test
%doc %{gem_instdir}/Rakefile
%license %{gem_instdir}/LICENSE
%dir %{gem_instdir}
%{gem_extdir_mri}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/ext
%{gem_spec}



%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
