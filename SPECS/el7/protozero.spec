# The following macros are also required:
# * protobuf_min_version

Name:           protozero
Version:	%{rpmbuild_version}
Release:	%{rpmbuild_release}%{?dist}
Summary:        Minimalistic protocol buffer decoder and encoder in C++

License:        BSD
URL:            https://github.com/mapbox/protozero
Source0:        https://github.com/mapbox/protozero/archive/v%{version}/protozero-%{version}.tar.gz

BuildRequires:  cmake3
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  protobuf-devel >= %{protobuf_min_version}
BuildRequires:  protobuf-lite-devel >= %{protobuf_min_version}
BuildRequires:  protobuf-compiler >= %{protobuf_min_version}

%description
Minimalistic protocol buffer decoder and encoder in C++.

Designed for high performance. Suitable for writing zero copy parsers
and encoders with minimal need for run-time allocation of memory.

Low-level: this is designed to be a building block for writing a
very customized decoder for a stable protobuf schema. If your protobuf
schema is changing frequently or lazy decoding is not critical for your
application then this approach offers no value: just use the decoding
API available via the C++ API that can be generated via the Google
Protobufs protoc program.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}
BuildArch:      noarch

%description    devel
Minimalistic protocol buffer decoder and encoder in C++.

Designed for high performance. Suitable for writing zero copy parsers
and encoders with minimal need for run-time allocation of memory.

Low-level: this is designed to be a building block for writing a
very customized decoder for a stable protobuf schema. If your protobuf
schema is changing frequently or lazy decoding is not critical for your
application then this approach offers no value: just use the decoding
API available via the C++ API that can be generated via the Google
Protobufs protoc program.


%prep
%autosetup -p 1
%{__mkdir} build


%build
pushd build
%cmake3 -DWERROR=OFF ..
%cmake3_build
popd


%install
pushd build
%cmake3_install
popd


%check
pushd build
%ctest3
popd


%files devel
%doc CHANGELOG.md CONTRIBUTING.md README.md UPGRADING.md doc/*.md build/doc/html
%license LICENSE.md LICENSE.from_folly
%{_includedir}/%{name}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
