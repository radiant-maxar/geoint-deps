Name:           osmosis
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Command line Java application for processing OpenStreetMap (OSM) data

License:        LGPLv3 and Public Domain
URL:            https://github.com/openstreetmap/osmosis

BuildArch:      noarch
Requires:       java-openjdk

Source0:        https://github.com/openstreetmap/osmosis/releases/download/%{version}/osmosis-%{version}.tgz

Patch0:         osmosis-fix_launchers.patch

%description
Osmosis is a command line Java application for processing OSM data.
The tool consists of pluggable components that can be chained to perform a
larger operation. For example, it has components for reading/writing
databases and files, deriving/applying changes to data sources, and sorting
data, (etc.). It has been written to easily add new features without re-writing
common tasks such as file and database handling.

Some examples of the things it can currently do are:

- Generate planet dumps from a database
- Load planet dumps into a database
- Produce change sets using database history tables
- Apply change sets to a local database
- Compare two planet dump files and produce a change set
- Re-sort the data contained in planet dump files
- Extract data inside a bounding box or polygon

Osmosis can also be included as a library in other Java applications


%prep
%autosetup -c -n %{name}-%{version} -p1


%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_datadir}/osmosis/contrib
%{__install} -d %{buildroot}%{_sysconfdir}/osmosis
%{__install} -d %{buildroot}%{_javadir}/osmosis

# Osmosis launch scripts
%{__install} -m 0755 bin/osmosis bin/osmosis-extract-apidb-0.6 %{buildroot}%{_bindir}

# Java JAR files.
%{__install} -m 0644 lib/default/*.jar %{buildroot}%{_javadir}/osmosis

# Configuration files.
%{__cat} > %{buildroot}%{_sysconfdir}/osmosis/osmosis.conf <<EOF
# Some examples for customization and tuning, for more visit:
#  http://wiki.openstreetmap.org/wiki/Osmosis/Tuning
#
# Use server version of JVM.
JAVACMD_OPTIONS=-server
#
# Customize the JVM maximum heap size to 2GB.
#JAVACMD_OPTIONS=-Xmx2G
EOF
%{__chmod} 0644 %{buildroot}%{_sysconfdir}/osmosis/osmosis.conf

%{__cat} > %{buildroot}%{_sysconfdir}/osmosis/plexus.conf <<EOF
main is org.openstreetmap.osmosis.core.Osmosis from osmosis.core

[osmosis.core]
load %{_javadir}/osmosis/*.jar
EOF
%{__chmod} 0644 %{buildroot}%{_sysconfdir}/osmosis/plexus.conf

%{__cat} > %{buildroot}%{_sysconfdir}/osmosis/log4j.properties <<EOF
# Only show WARN or higher messages for org.java.plugin package
log4j.logger.org.java.plugin=WARN
EOF
%{__chmod} 0644 %{buildroot}%{_sysconfdir}/osmosis/log4j.properties

# Contrib scripts and SQL files.
%{__install} -m 0644 script/*.sql %{buildroot}%{_datadir}/osmosis
%{__install} -m 0755 script/contrib/*.sh %{buildroot}%{_datadir}/osmosis/contrib
%{__install} -m 0644 script/contrib/*.sql %{buildroot}%{_datadir}/osmosis/contrib


%files
%doc changes.txt readme.txt script/pgsnapshot_and_pgsimple.txt
%license copying.txt
%{_bindir}/osmosis
%{_bindir}/osmosis-extract-apidb-0.6
%{_datadir}/osmosis
%{_javadir}/osmosis/*.jar
%config(noreplace) %{_sysconfdir}/osmosis/osmosis.conf
%config(noreplace) %{_sysconfdir}/osmosis/log4j.properties
%config(noreplace) %{_sysconfdir}/osmosis/plexus.conf


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
