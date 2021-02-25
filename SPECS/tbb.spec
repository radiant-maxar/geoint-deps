Name:    tbb
Summary: The Threading Building Blocks library abstracts low-level threading details
Version: %{rpmbuild_version}
Release: %{rpmbuild_release}%{?dist}
License: ASL 2.0
URL:     http://threadingbuildingblocks.org/

Source0: https://github.com/intel/tbb/archive/v%{version}/%{name}-%{version}.tar.gz
# These three are downstream sources.
Source6: tbb.pc
Source7: tbbmalloc.pc
Source8: tbbmalloc_proxy.pc

# Don't snip -Wall from C++ flags.  Add -fno-strict-aliasing, as that
# uncovers some static-aliasing warnings.
# Related: https://bugzilla.redhat.com/show_bug.cgi?id=1037347
Patch0: tbb-2019-dont-snip-Wall.patch

# Make attributes of aliases match those on the aliased function.
Patch1: tbb-2020-attributes.patch

# Fix test-thread-monitor, which had multiple bugs that could (and did, on
# ppc64le) result in a hang.
Patch2: tbb-2019-test-thread-monitor.patch

# Fix a test that builds a 4-thread barrier, but cannot guarantee that more
# than 2 threads will be available to use it.
Patch3: tbb-2019-test-task-scheduler-init.patch

BuildRequires: cmake3
# A newer C++ toolchain is required to compile.
BuildRequires: devtoolset-9-gcc
BuildRequires: devtoolset-9-gcc-c++
BuildRequires: gcc-c++
BuildRequires: make

%description
Threading Building Blocks (TBB) is a C++ runtime library that
abstracts the low-level threading details necessary for optimal
multi-core performance.  It uses common C++ templates and coding style
to eliminate tedious threading implementation work.

TBB requires fewer lines of code to achieve parallelism than other
threading models.  The applications you write are portable across
platforms.  Since the library is also inherently scalable, no code
maintenance is required as more processor cores become available.


%package devel
Summary: The Threading Building Blocks C++ headers and shared development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and shared object symlinks for the Threading Building
Blocks (TBB) C++ libraries.


%prep
%autosetup -p1 -n oneTBB-%{version}

# For repeatable builds, don't query the hostname or architecture
sed -i 's/"`hostname -s`" ("`uname -m`"/fedorabuild (%{_arch}/' \
    build/version_info_linux.sh

# Insert --as-needed before the libraries to be linked.
sed -i "s/-fPIC/& -Wl,--as-needed/" build/linux.gcc.inc

# Invoke the right python binary directly
sed -i 's,env python,python3,' python/TBB.py python/tbb/__*.py

# Remove shebang from files that don't need it
sed -i '/^#!/d' python/tbb/{pool,test}.py

%build
# Enable the updated compiler toolchain prior to building.
. /opt/rh/devtoolset-9/enable
compiler=""
if [[ %{__cc} == *"gcc"* ]]; then
    compiler="gcc"
elif [[ %{__cc} == *"clang"* ]]; then
    compiler="clang"
else
    compiler="%{__cc}"
fi

%make_build tbb_build_prefix=obj stdver=c++14 \
    compiler=${compiler} \
    CXXFLAGS="%{optflags} -DUSE_PTHREAD" \
    LDFLAGS="$RPM_LD_FLAGS -lpthread"
for file in %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
    base=$(basename ${file})
    sed 's/_FEDORA_VERSION/%{version}/' ${file} > ${base}
    touch -r ${file} ${base}
done


%check
# This test assumes it can create thread barriers for arbitrary numbers of
# threads, but tbb limits the number of threads spawned to a function of the
# number of CPUs available.  Some of the koji builders have a small number of
# CPUs, so the test hangs waiting for threads that have not been created to
# arrive at the barrier.  Skip this test until upstream fixes it.
sed -i '/test_task_scheduler_observer/d' build/Makefile.test

make test tbb_build_prefix=obj stdver=c++14 CXXFLAGS="%{optflags}"

%install
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}

pushd build/obj_release
    for file in libtbb{,malloc{,_proxy}}; do
        install -p -D -m 755 ${file}.so.2 %{buildroot}/%{_libdir}
        ln -s $file.so.2 %{buildroot}/%{_libdir}/$file.so
    done
popd

pushd include
    find tbb -type f ! -name \*.htm\* -exec \
        install -p -D -m 644 {} %{buildroot}/%{_includedir}/{} \
    \;
popd

for file in %{SOURCE6} %{SOURCE7} %{SOURCE8}; do
    install -p -D -m 644 $(basename ${file}) \
        %{buildroot}/%{_libdir}/pkgconfig/$(basename ${file})
done

# Install the rml headers
mkdir -p %{buildroot}%{_includedir}/rml
cp -p src/rml/include/*.h %{buildroot}%{_includedir}/rml

. build/obj_release/tbbvars.sh

# Install the cmake files
%cmake3 \
  -DINSTALL_DIR=%{buildroot}%{_libdir}/cmake/TBB \
  -DSYSTEM_NAME=Linux \
  -DLIB_REL_PATH=../.. \
  -P cmake/tbb_config_installer.cmake

%files
%doc doc/Release_Notes.txt README.md
%license LICENSE
%{_libdir}/libtbb.so.2
%{_libdir}/libtbbmalloc.so.2
%{_libdir}/libtbbmalloc_proxy.so.2

%files devel
%doc CHANGES cmake/README.rst
%{_includedir}/rml/
%{_includedir}/tbb/
%{_libdir}/*.so
%{_libdir}/cmake/TBB/
%{_libdir}/pkgconfig/*.pc
