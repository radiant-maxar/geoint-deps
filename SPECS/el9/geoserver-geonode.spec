%global geoserver_cache %{_var}/cache/geoserver
%global geoserver_data %{_sharedstatedir}/geoserver
%global geoserver_logs %{_var}/log/geoserver
%global geoserver_webapp %{_sharedstatedir}/tomcat/webapps/geoserver
%global tomcat_confd %{_sysconfdir}/tomcat/conf.d

Name:           geoserver-geonode
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GeoServer is an open source server for sharing geospatial data.
License:        Apache-1.1 AND Apache-2.0 AND BSD-3Clause AND EPL-2.0 AND EPSG AND GeoTools AND HSQL AND GPLv2 AND GPLv3 AND LGPL-2.1 AND LGPL-3.0 AND OracleFUTC AND MIT AND OGC-1.0 AND W3C
URL:            https://geoserver.org

BuildArch:      noarch
BuildRequires:  unzip

Conflicts:      geoserver
Requires:       gdal = %{gdal_version}%{?dist}
Requires:       gdal-java = %{gdal_version}%{?dist}
Requires:       tomcat

Source0:        https://artifacts.geonode.org/geoserver/%{version}/geoserver.war

# These libraries are necessary for GeoFence server plugin:
#  https://docs.geonode.org/en/master/install/basic/index.html#geofence-security-rules-on-postgis
#  https://osgeo-org.atlassian.net/jira/core/projects/GEOS/issues/GEOS-9548
Source1:       https://maven.geo-solutions.it/org/hibernatespatial/hibernate-spatial-postgis/1.1.3.2/hibernate-spatial-postgis-1.1.3.2.jar
Source2:       https://repo1.maven.org/maven2/org/postgis/postgis-jdbc/1.3.3/postgis-jdbc-1.3.3.jar

# XXX: The Spring 5.7.8 release breaks OAuth2 authentication with GeoServer
# and unfortunately to keep auth functionality we have to keep libraries
# vulnerable to CVE-2023-20862 in place:
#  https://github.com/GeoNode/geoserver-geonode-ext/issues/170
Source3:       https://repo1.maven.org/maven2/org/springframework/security/spring-security-config/5.7.7/spring-security-config-5.7.7.jar
Source4:       https://repo1.maven.org/maven2/org/springframework/security/spring-security-core/5.7.7/spring-security-core-5.7.7.jar
Source5:       https://repo1.maven.org/maven2/org/springframework/security/spring-security-crypto/5.7.7/spring-security-crypto-5.7.7.jar
Source6:       https://repo1.maven.org/maven2/org/springframework/security/spring-ecurity-web/5.7.7/spring-security-web-5.7.7.jar
Source7:       https://repo1.maven.org/maven2/org/springframework/security/spring-security-ldap/5.7.7/spring-security-ldap-5.7.7.jar


%description
GeoServer is an open source software server written in Java that allows users to share and edit geospatial data. Designed for interoperability AND it publishes data from any major spatial data source using open standards.  This package of GeoServer is customized for use with GeoNode.


%package data
Summary:        GeoServer GeoNode Data
License:        Public Domain
URL:            https://github.com/GeoNode/geoserver-geonode-ext

Conflicts:      geoserver-data
Requires:       geoserver-geonode = %{version}-%{release}

%description data
GeoServer data for use with a GeoNode instance.


%prep
%autosetup -c


%install
%{__install} -m 0770 -d \
 %{buildroot}%{geoserver_data} \
 %{buildroot}%{geoserver_logs} \
 %{buildroot}%{geoserver_cache}
%{__install} -m 0775 -d \
 %{buildroot}%{geoserver_webapp} \
 %{buildroot}%{geoserver_data}
%{__install} -m 0755 -d %{buildroot}%{tomcat_confd}
%{__install} -m 0775 -d %{buildroot}%{geoserver_data}

# Install GeoServer Tomcat webapp and data.
%{__cp} -pr index.html META-INF WEB-INF %{buildroot}%{geoserver_webapp}
%{__cp} -pr data %{buildroot}%{geoserver_data}

# XXX: Replace spring-security components
%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib \
 -type f -name \*spring-security-\*5.7.8\*.jar -print -delete
%{__install} -m 0644 -pv \
 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} \
 %{buildroot}%{geoserver_webapp}/WEB-INF/lib

# Remove execute bits from jars.
%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib \
 -type f -exec %{__chmod} 0644 {} \;


# Create Tomcat configuration file that will set up the environment.
cat >> %{buildroot}%{tomcat_confd}/geoserver-geonode.conf <<EOF
# Necessary for GDAL plugins.
GDAL_DATA="\${GDAL_DATA:-%{_datadir}/gdal}"
export GDAL_DATA

GEOSERVER_DATA_DIR="\${GEOSERVER_DATA_DIR:-%{geoserver_data}/data}"
export GEOSERVER_DATA_DIR

GEOSERVER_ENCODING="\${GEOSERVER_ENCODING:-UTF-8}"
export GEOSERVER_ENCODING

# Necessary to load GDAL via JNI
LD_LIBRARY_PATH="\${GEOSERVER_LD_LIBRARY_PATH:-%{_usr}/lib/java/gdal:%{_libdir}}"
export LD_LIBRARY_PATH

PROXY_BASE_URL="\${GEOSERVER_PROXY_BASE_URL:-http://localhost:8080/geoserver}"
export PROXY_BASE_URL

JDK_JAVA_OPTIONS="\${JDK_JAVA_OPTIONS} \\
-Dgeofence.dir=\${GEOSERVER_DATA_DIR}/geofence \\
-Dgeofence-ovr=file:\${GEOSERVER_DATA_DIR}/geofence/geofence-datasource-ovr.properties \\
-Dfile.encoding=UTF8 \\
-Dgeoserver.xframe.shouldSetPolicy=\${GEOSERVER_XFRAME_OPTIONS:-true} \\
-Dgwc.context.suffix=gwc \\
-Djava.awt.headless=true \\
-Djavax.servlet.request.encoding=\${GEOSERVER_ENCODING} \\
-Djavax.servlet.response.encoding=\${GEOSERVER_ENCODING} \\
-Djts.overlay=ng \\
-Dorg.geotools.coverage.jaiext.enabled=true \\
-Dorg.geotools.localDateTimeHandling=true \\
-Dorg.geotools.referencing.forceXY=true \\
-Dorg.geotools.shapefile.datetime=\${GEOSERVER_SHAPEFILE_DATETIME:-true} \\
-Dsun.java2d.renderer.pixelsize=8192 \\
-Dsun.java2d.renderer.useThreadLocal=false \\
-Dsun.java2d.renderer=org.marlin.pisces.PiscesRenderingEngine \\
-Duser.country=\${GEOSERVER_COUNTRY:-US} \\
-Duser.language=\${GEOSERVER_LANGUAGE:-en} \\
-Duser.region=\${GEOSERVER_REGION:-US} \\
-Duser.timezone=\${GEOSERVER_TIMEZONE:-GMT} \\
-DALLOW_ENV_PARAMETRIZATION=true \\
-DENABLE_JSONP=\${GEOSERVER_ENABLE_JSONP:-true} \\
-DGEOSERVER_CSRF_DISABLED=\${GEOSERVER_CSRF_DISABLED:-false} \\
-DGEOSERVER_CSRF_WHITELIST=\${GEOSERVER_CSRF_WHITELIST:-} \\
-DGEOSERVER_DATA_DIR=\${GEOSERVER_DATA_DIR} \\
-DGEOSERVER_FILEBROWSER_HIDEFS=\${GEOSERVER_FILEBROWSER_HIDEFS:-false} \\
-DGEOSERVER_LOG_LOCATION=\${GEOSERVER_LOG_LOCATION:-%{geoserver_logs}/geoserver.log} \\
-DGS-SHAPEFILE-CHARSET=\${GEOSERVER_ENCODING} \\
-DPRINT_BASE_URL=\${PROXY_BASE_URL}/pdf \\
-DPROXY_BASE_URL=\${PROXY_BASE_URL} \\
-Xbootclasspath/a:%{geoserver_webapp}/WEB-INF/lib/marlin-0.9.3.jar \\
-Xms\${GEOSERVER_MINIMUM_MEMORY:-512m} \\
-Xmx\${GEOSERVER_MAXIMUM_MEMORY:-2048m} \\
-XX:ConcGCThreads=5 \\
-XX:MaxGCPauseMillis=200 \\
-XX:NewRatio=2 \\
-XX:ParallelGCThreads=20 \\
-XX:PerfDataSamplingInterval=500 \\
-XX:SoftRefLRUPolicyMSPerMB=36000 \\
-XX:+CMSClassUnloadingEnabled \\
-XX:+UseG1GC \\
-server"
export JDK_JAVA_OPTIONS
EOF

%post
# Copy in GDAL jar to a versioned location.
%{__cp} -pv %{_javadir}/gdal/gdal.jar %{geoserver_webapp}/WEB-INF/lib/gdal-$(%{_bindir}/rpm --qf '%%{version}' -q gdal-java).jar


%files
%defattr(-, tomcat, tomcat, -)
%dir %{geoserver_cache}
%dir %{geoserver_logs}
%dir %{geoserver_data}
%dir %{geoserver_data}/data
%defattr(-, root, root, -)
%{tomcat_confd}/geoserver-geonode.conf
%{geoserver_webapp}

%files data
%defattr(0664,tomcat,tomcat,0775)
%config(noreplace) %{geoserver_data}/data/*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
