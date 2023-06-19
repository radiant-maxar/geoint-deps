# The following macros are also required:
# * gdal_version

%global geoserver_major_version %(echo %{rpmbuild_version} | awk -F. '{ print $1 }')
%global geoserver_minor_version %(echo %{rpmbuild_version} | awk -F. '{ print $2 }')
%global geoserver_major_minor %{geoserver_major_version}.%{geoserver_minor_version}

%global geoserver_cache %{_var}/cache/geoserver
%global geoserver_data %{_sharedstatedir}/geoserver
%global geoserver_logs %{_var}/log/geoserver
%global geoserver_webapp %{_sharedstatedir}/tomcat/webapps/geoserver
%global geoserver_source_base_url https://prdownloads.sourceforge.net/geoserver/GeoServer/%{rpmbuild_version}
%global geoserver_source_url %{geoserver_source_base_url}/extensions/geoserver-%{rpmbuild_version}
%global geoserver_community_url https://build.geoserver.org/geoserver/%{geoserver_major_minor}.x/community-latest/geoserver-%{geoserver_major_minor}-SNAPSHOT
%global tomcat_confd %{_sysconfdir}/tomcat/conf.d

Name:           geoserver
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        GeoServer is an open source server for sharing geospatial data.

License:        Apache-1.1 AND Apache-2.0 AND BSD-3Clause AND EPL-2.0 AND EPSG AND GeoTools AND HSQL AND GPLv2 AND GPLv3 AND LGPL-2.1 AND LGPL-3.0 AND MIT AND OGC-1.0 AND W3C
URL:            https://geoserver.org

BuildArch:      noarch
BuildRequires:  unzip

Requires:       gdal = %{gdal_version}%{?dist}
Requires:       gdal-java = %{gdal_version}%{?dist}
Requires:       tomcat

Source0:        %{geoserver_source_base_url}/geoserver-%{version}-war.zip
Source1:        %{geoserver_source_url}-app-schema-plugin.zip
Source2:        %{geoserver_source_url}-authkey-plugin.zip
Source4:        %{geoserver_source_url}-charts-plugin.zip
Source5:        %{geoserver_source_url}-control-flow-plugin.zip
Source6:        %{geoserver_source_url}-css-plugin.zip
Source10:       %{geoserver_source_url}-dxf-plugin.zip
Source11:       %{geoserver_source_url}-excel-plugin.zip
Source12:       %{geoserver_source_url}-feature-pregeneralized-plugin.zip
Source13:       %{geoserver_source_url}-gdal-plugin.zip
Source15:       %{geoserver_source_url}-geofence-server-plugin.zip
Source16:       %{geoserver_source_url}-geofence-wps-plugin.zip
Source17:       %{geoserver_source_url}-geopkg-output-plugin.zip
Source20:       %{geoserver_source_url}-h2-plugin.zip
Source21:       %{geoserver_source_url}-imagemap-plugin.zip
Source22:       %{geoserver_source_url}-importer-plugin.zip
Source26:       %{geoserver_source_url}-mapml-plugin.zip
Source27:       %{geoserver_source_url}-mbstyle-plugin.zip
Source30:       %{geoserver_source_url}-monitor-plugin.zip
Source31:       %{geoserver_source_url}-mysql-plugin.zip
Source34:       %{geoserver_source_url}-ogr-wfs-plugin.zip
Source35:       %{geoserver_source_url}-ogr-wps-plugin.zip
Source37:       %{geoserver_source_url}-params-extractor-plugin.zip
Source38:       %{geoserver_source_url}-printing-plugin.zip
Source39:       %{geoserver_source_url}-pyramid-plugin.zip
Source40:       %{geoserver_source_url}-querylayer-plugin.zip
Source41:       %{geoserver_source_url}-sldservice-plugin.zip
Source42:       %{geoserver_source_url}-sqlserver-plugin.zip
Source43:       %{geoserver_source_url}-vectortiles-plugin.zip
Source45:       %{geoserver_source_url}-web-resource-plugin.zip
Source46:       %{geoserver_source_url}-wmts-multi-dimensional-plugin.zip
Source48:       %{geoserver_source_url}-wps-download-plugin.zip
Source50:       %{geoserver_source_url}-wps-plugin.zip
Source51:       %{geoserver_source_url}-xslt-plugin.zip
Source52:       %{geoserver_source_url}-ysld-plugin.zip

# Community plugins.
Source100:      %{geoserver_community_url}-gdal-wcs-plugin.zip
Source101:      %{geoserver_community_url}-gdal-wps-plugin.zip
Source102:      %{geoserver_community_url}-geopkg-plugin.zip
Source103:      %{geoserver_community_url}-ogr-datastore-plugin.zip
Source104:      %{geoserver_community_url}-s3-geotiff-plugin.zip
Source107:      %{geoserver_community_url}-sec-oauth2-geonode-plugin.zip
Source108:      %{geoserver_community_url}-sec-oauth2-github-plugin.zip
Source109:      %{geoserver_community_url}-sec-oauth2-google-plugin.zip
Source110:      %{geoserver_community_url}-sec-oauth2-openid-connect-plugin.zip
Source113:      %{geoserver_community_url}-vsi-plugin.zip
Source114:      %{geoserver_community_url}-webp-plugin.zip

%description
GeoServer is an open source software server written in Java that allows users to share and edit geospatial data. Designed for interoperability AND it publishes data from any major spatial data source using open standards.


%package data
Summary:       GeoServer Data
License:       GeoSolutions
Requires:      geoserver = %{version}-%{release}

%description data
Default data for use with a GeoServer instance.


%prep
%autosetup -c
for plugin in app-schema authkey charts control-flow css dxf excel feature-pregeneralized gdal geofence geopkg geonode h2 imagemap importer mapml mbstyle monitor mysql oauth2 params-extractor printing pyramid querylayer saml s3-geotiff sldservice sqlserver vectortiles web-resource webp wmts-multi-dimensional wps xslt ysld; do
    %{__mkdir_p} plugins/${plugin}
done
%{__unzip} %{SOURCE1}  -d plugins/app-schema
%{__unzip} %{SOURCE2}  -d plugins/authkey
%{__unzip} %{SOURCE4}  -d plugins/charts
%{__unzip} %{SOURCE5}  -d plugins/control-flow
%{__unzip} %{SOURCE6}  -d plugins/css
%{__unzip} %{SOURCE10} -d plugins/dxf
%{__unzip} %{SOURCE11} -d plugins/excel
%{__unzip} %{SOURCE12} -d plugins/feature-pregeneralized
%{__unzip} %{SOURCE13} -d plugins/gdal
%{__unzip} -o %{SOURCE34} -d plugins/gdal
%{__unzip} -o %{SOURCE35} -d plugins/gdal
%{__unzip} -o %{SOURCE100} -d plugins/gdal
%{__unzip} -o %{SOURCE101} -d plugins/gdal
%{__unzip} -o %{SOURCE103} -d plugins/gdal
%{__unzip} -o %{SOURCE113} -d plugins/gdal
%{__unzip} %{SOURCE15} -d plugins/geofence
%{__unzip} -o %{SOURCE16} -d plugins/geofence
%{__unzip} %{SOURCE17} -d plugins/geopkg
%{__unzip} -o %{SOURCE102} -d plugins/geopkg
%{__unzip} %{SOURCE20} -d plugins/h2
%{__unzip} %{SOURCE21} -d plugins/imagemap
%{__unzip} %{SOURCE22} -d plugins/importer
%{__unzip} %{SOURCE26} -d plugins/mapml
%{__unzip} %{SOURCE27} -d plugins/mbstyle
%{__unzip} %{SOURCE30} -d plugins/monitor
%{__unzip} %{SOURCE31} -d plugins/mysql
%{__unzip} %{SOURCE37} -d plugins/params-extractor
%{__unzip} %{SOURCE38} -d plugins/printing
%{__unzip} %{SOURCE39} -d plugins/pyramid
%{__unzip} %{SOURCE40} -d plugins/querylayer
%{__unzip} -o %{SOURCE107} -d plugins/oauth2
%{__unzip} -o %{SOURCE108} -d plugins/oauth2
%{__unzip} -o %{SOURCE109} -d plugins/oauth2
%{__unzip} -o %{SOURCE110} -d plugins/oauth2
%{__unzip} %{SOURCE104} -d plugins/s3-geotiff
%{__unzip} %{SOURCE41} -d plugins/sldservice
%{__unzip} %{SOURCE42} -d plugins/sqlserver
%{__unzip} %{SOURCE43} -d plugins/vectortiles
%{__unzip} %{SOURCE45} -d plugins/web-resource
%{__unzip} %{SOURCE114} -d plugins/webp
%{__unzip} %{SOURCE46} -d plugins/wmts-multi-dimensional
%{__unzip} %{SOURCE48} -d plugins/wps
%{__unzip} -o %{SOURCE50} -d plugins/wps
%{__unzip} %{SOURCE51} -d plugins/xslt
%{__unzip} %{SOURCE52} -d plugins/ysld


%install
%{__install} -m 0770 -d \
 %{buildroot}%{geoserver_data} \
 %{buildroot}%{geoserver_logs} \
 %{buildroot}%{geoserver_cache}
%{__install} -m 0775 -d %{buildroot}%{geoserver_webapp}
%{__install} -m 0755 -d %{buildroot}%{tomcat_confd}

# Install GeoServer Tomcat webapp and plugin libraries.
%{__unzip} geoserver.war -d %{buildroot}%{geoserver_webapp}
for plugin in app-schema authkey charts control-flow css dxf excel feature-pregeneralized gdal geopkg h2 imagemap importer mapml mbstyle monitor mysql oauth2 params-extractor printing pyramid querylayer s3-geotiff sldservice sqlserver vectortiles web-resource webp wmts-multi-dimensional wps xslt ysld; do
    %{__install} plugins/${plugin}/*.jar %{buildroot}%{geoserver_webapp}/WEB-INF/lib
done

# Remove execute bits from jars.
%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib \
 -type f -exec %{__chmod} 0644 {} \;

# Install GeoServer data.
%{__mv} -v %{buildroot}%{geoserver_webapp}/data %{buildroot}%{geoserver_data}
%{_bindir}/touch %{buildroot}%{geoserver_data}/data/s3.properties

# Remove execute bits from jars.
%{_bindir}/find %{buildroot}%{geoserver_webapp}/WEB-INF/lib \
 -type f -exec %{__chmod} 0644 {} \;

# Create Tomcat configuration file that will set up the environment.
cat >> %{buildroot}%{tomcat_confd}/geoserver.conf <<EOF
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
-Ds3.properties.location=\${GEOSERVER_S3_PROPERTIES_LOCATION:-\${GEOSERVER_DATA_DIR}/s3.properties} \\
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
%doc README.html target/VERSION.txt
%license license/*.html
%{geoserver_webapp}
%{tomcat_confd}/geoserver.conf
%defattr(-, tomcat, tomcat, -)
%dir %{geoserver_cache}
%dir %{geoserver_logs}
%dir %{geoserver_data}
%dir %{geoserver_data}/data

%files data
%defattr(0664,tomcat,tomcat,0775)
%config(noreplace) %{geoserver_data}/data/*


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
