# The following macros are also required:
# * data_fossgis_version
# * data_natural_earth_version

%global openstreetmap_carto_home %{_datadir}/%{name}
%global openstreetmap_carto_data %{_localstatedir}/lib/%{name}
%global openstreetmap_carto_sysconf %{_sysconfdir}/%{name}

%global __python %{__python3}
%global _python_bytecompile_errors_terminate_build 0

Name:           openstreetmap-carto
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        A general-purpose OpenStreetMap mapnik style, in CartoCSS

License:        CC0 1.0
URL:            https://github.com/gravitystorm/openstreetmap-carto
Source0:        https://github.com/gravitystorm/openstreetmap-carto/archive/v%{version}.tar.gz

Source1:        https://github.com/nvkelso/natural-earth-vector/blob/v%{data_natural_earth_version}/LICENSE.md
Source2:        https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_boundary_lines_land.zip
Source3:        https://osmdata.openstreetmap.de/download/antarctica-icesheet-outlines-%{data_fossgis_version}.zip
Source4:        https://osmdata.openstreetmap.de/download/antarctica-icesheet-polygons-%{data_fossgis_version}.zip
Source5:        https://osmdata.openstreetmap.de/download/simplified-water-polygons-split-%{data_fossgis_version}.zip
Source6:        https://osmdata.openstreetmap.de/download/water-polygons-split-%{data_fossgis_version}.zip

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  mapnik-utils
BuildRequires:  lua

Requires:       dejavu-fonts-common
Requires:       dejavu-lgc-sans-fonts
Requires:       dejavu-lgc-sans-mono-fonts
Requires:       dejavu-lgc-serif-fonts
Requires:       dejavu-sans-fonts
Requires:       dejavu-sans-mono-fonts
Requires:       dejavu-serif-fonts
Requires:       gdal
Requires:       google-noto-cjk-fonts
Requires:       google-noto-emoji-color-fonts
Requires:       google-noto-emoji-fonts
Requires:       google-noto-fonts-common
Requires:       google-noto-kufi-arabic-fonts
Requires:       google-noto-naskh-arabic-fonts
Requires:       google-noto-naskh-arabic-ui-fonts
Requires:       google-noto-sans-armenian-fonts
Requires:       google-noto-sans-avestan-fonts
Requires:       google-noto-sans-balinese-fonts
Requires:       google-noto-sans-bamum-fonts
Requires:       google-noto-sans-batak-fonts
Requires:       google-noto-sans-bengali-fonts
Requires:       google-noto-sans-bengali-ui-fonts
Requires:       google-noto-sans-brahmi-fonts
Requires:       google-noto-sans-buginese-fonts
Requires:       google-noto-sans-buhid-fonts
Requires:       google-noto-sans-canadian-aboriginal-fonts
Requires:       google-noto-sans-carian-fonts
Requires:       google-noto-sans-cham-fonts
Requires:       google-noto-sans-cherokee-fonts
Requires:       google-noto-sans-cjk-fonts
Requires:       google-noto-sans-coptic-fonts
Requires:       google-noto-sans-cuneiform-fonts
Requires:       google-noto-sans-cypriot-fonts
Requires:       google-noto-sans-deseret-fonts
Requires:       google-noto-sans-devanagari-fonts
Requires:       google-noto-sans-devanagari-ui-fonts
Requires:       google-noto-sans-egyptian-hieroglyphs-fonts
Requires:       google-noto-sans-ethiopic-fonts
Requires:       google-noto-sans-fonts
Requires:       google-noto-sans-georgian-fonts
Requires:       google-noto-sans-glagolitic-fonts
Requires:       google-noto-sans-gothic-fonts
Requires:       google-noto-sans-gujarati-fonts
Requires:       google-noto-sans-gujarati-ui-fonts
Requires:       google-noto-sans-gurmukhi-fonts
Requires:       google-noto-sans-gurmukhi-ui-fonts
Requires:       google-noto-sans-hanunoo-fonts
Requires:       google-noto-sans-hebrew-fonts
Requires:       google-noto-sans-imperial-aramaic-fonts
Requires:       google-noto-sans-inscriptional-pahlavi-fonts
Requires:       google-noto-sans-inscriptional-parthian-fonts
Requires:       google-noto-sans-japanese-fonts
Requires:       google-noto-sans-javanese-fonts
Requires:       google-noto-sans-kaithi-fonts
Requires:       google-noto-sans-kannada-fonts
Requires:       google-noto-sans-kannada-ui-fonts
Requires:       google-noto-sans-kayah-li-fonts
Requires:       google-noto-sans-kharoshthi-fonts
Requires:       google-noto-sans-khmer-fonts
Requires:       google-noto-sans-khmer-ui-fonts
Requires:       google-noto-sans-korean-fonts
Requires:       google-noto-sans-lao-fonts
Requires:       google-noto-sans-lao-ui-fonts
Requires:       google-noto-sans-lepcha-fonts
Requires:       google-noto-sans-limbu-fonts
Requires:       google-noto-sans-linear-b-fonts
Requires:       google-noto-sans-lisu-fonts
Requires:       google-noto-sans-lycian-fonts
Requires:       google-noto-sans-lydian-fonts
Requires:       google-noto-sans-malayalam-fonts
Requires:       google-noto-sans-malayalam-ui-fonts
Requires:       google-noto-sans-mandaic-fonts
Requires:       google-noto-sans-meetei-mayek-fonts
Requires:       google-noto-sans-mongolian-fonts
Requires:       google-noto-sans-myanmar-fonts
Requires:       google-noto-sans-myanmar-ui-fonts
Requires:       google-noto-sans-new-tai-lue-fonts
Requires:       google-noto-sans-nko-fonts
Requires:       google-noto-sans-ogham-fonts
Requires:       google-noto-sans-ol-chiki-fonts
Requires:       google-noto-sans-old-italic-fonts
Requires:       google-noto-sans-old-persian-fonts
Requires:       google-noto-sans-old-south-arabian-fonts
Requires:       google-noto-sans-old-turkic-fonts
Requires:       google-noto-sans-osmanya-fonts
Requires:       google-noto-sans-phags-pa-fonts
Requires:       google-noto-sans-phoenician-fonts
Requires:       google-noto-sans-rejang-fonts
Requires:       google-noto-sans-runic-fonts
Requires:       google-noto-sans-samaritan-fonts
Requires:       google-noto-sans-saurashtra-fonts
Requires:       google-noto-sans-shavian-fonts
Requires:       google-noto-sans-simplified-chinese-fonts
Requires:       google-noto-sans-sinhala-fonts
Requires:       google-noto-sans-sundanese-fonts
Requires:       google-noto-sans-syloti-nagri-fonts
Requires:       google-noto-sans-symbols-fonts
Requires:       google-noto-sans-syriac-eastern-fonts
Requires:       google-noto-sans-syriac-estrangela-fonts
Requires:       google-noto-sans-syriac-western-fonts
Requires:       google-noto-sans-tagalog-fonts
Requires:       google-noto-sans-tagbanwa-fonts
Requires:       google-noto-sans-tai-le-fonts
Requires:       google-noto-sans-tai-tham-fonts
Requires:       google-noto-sans-tai-viet-fonts
Requires:       google-noto-sans-tamil-fonts
Requires:       google-noto-sans-tamil-ui-fonts
Requires:       google-noto-sans-telugu-fonts
Requires:       google-noto-sans-telugu-ui-fonts
Requires:       google-noto-sans-thaana-fonts
Requires:       google-noto-sans-thai-fonts
Requires:       google-noto-sans-thai-ui-fonts
Requires:       google-noto-sans-tifinagh-fonts
Requires:       google-noto-sans-traditional-chinese-fonts
Requires:       google-noto-sans-ugaritic-fonts
Requires:       google-noto-sans-ui-fonts
Requires:       google-noto-sans-vai-fonts
Requires:       google-noto-sans-yi-fonts
Requires:       google-noto-serif-armenian-fonts
Requires:       google-noto-serif-fonts
Requires:       google-noto-serif-georgian-fonts
Requires:       google-noto-serif-khmer-fonts
Requires:       google-noto-serif-lao-fonts
Requires:       google-noto-serif-thai-fonts


%description
These are the CartoCSS map stylesheets for the Standard map layer on
OpenStreetMap.org.

These stylesheets can be used in your own cartography projects, and
are designed to be easily customised. They work with Kosmtik and also
with the command-line CartoCSS processor.

Since August 2013 these stylesheets have been used on the OSMF
tileservers (tile.openstreetmap.org), and are updated from each point
release. They supersede the previous XML-based stylesheets.


%package data-natural-earth
Summary:   Natural Earth's country boundary shapefiles required by %{name}, indexed through shapeindex
Requires:  %{name} >= %{version}-%{release}
License:   PD
URL:       https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-boundary-lines


%description data-natural-earth
%{summary}.


%package data-fossgis
Summary:   FOSSGIS's water/icesheet polygon/outline shapefiles required by %{name}, indexed through shapeindex
Requires:  %{name} >= %{version}-%{release}
License:   ODbL
URL:       https://osmdata.openstreetmap.de


%description data-fossgis
%{summary}.


%prep
%autosetup -p 1 -n %{name}-%{version}

%{__mkdir} data

%{__mv} %{SOURCE1} LICENSE.ne_110m_admin_0_boundary_lines_land.md

%{__cp} %{SOURCE2} data
%{__unzip} %{SOURCE2} ne_110m_admin_0_boundary_lines_land.README.html ne_110m_admin_0_boundary_lines_land.VERSION.txt
%{__mv} ne_110m_admin_0_boundary_lines_land.README.html README.ne_110m_admin_0_boundary_lines_land.html
%{__mv} ne_110m_admin_0_boundary_lines_land.VERSION.txt VERSION.ne_110m_admin_0_boundary_lines_land.txt
%{__grep} -q %{data_natural_earth_version} VERSION.ne_110m_admin_0_boundary_lines_land.txt

%{__cp} %{SOURCE3} data
%{__unzip} %{SOURCE3} antarctica-icesheet-outlines-%{data_fossgis_version}/README
%{__mv} antarctica-icesheet-outlines-%{data_fossgis_version}/README README.antarctica-icesheet-outlines.txt
rmdir antarctica-icesheet-outlines-%{data_fossgis_version}

%{__cp} %{SOURCE4} data
%{__unzip} %{SOURCE4} antarctica-icesheet-polygons-%{data_fossgis_version}/README
%{__mv} antarctica-icesheet-polygons-%{data_fossgis_version}/README README.antarctica-icesheet-polygons.txt
rmdir antarctica-icesheet-polygons-%{data_fossgis_version}

%{__cp} %{SOURCE5} data
%{__unzip} %{SOURCE5} simplified-water-polygons-split-%{data_fossgis_version}/README.txt
%{__mv} simplified-water-polygons-split-%{data_fossgis_version}/README.txt README.simplified-water-polygons-split.txt
rmdir simplified-water-polygons-split-%{data_fossgis_version}

%{__cp} %{SOURCE6} data
%{__unzip} %{SOURCE6} water-polygons-split-%{data_fossgis_version}/README.txt
%{__mv} water-polygons-split-%{data_fossgis_version}/README.txt README.water-polygons-split.txt
rmdir water-polygons-split-%{data_fossgis_version}
%{__sed} -n '/^LICENSE$/,$p' README.water-polygons-split.txt > LICENSE.%{name}-data-fossgis.txt


%build


%check
lua scripts/lua/test.lua


%install
%{__install} -d %{buildroot}%{openstreetmap_carto_data}
%{__cp} --recursive --preserve data %{buildroot}%{openstreetmap_carto_data}

%{__install} -d %{buildroot}%{openstreetmap_carto_home}
%{__install} -d %{buildroot}%{openstreetmap_carto_home}/scripts
%{__cp} --preserve scripts/*.py %{buildroot}%{openstreetmap_carto_home}/scripts
%{__cp} --recursive --preserve scripts/lua %{buildroot}%{openstreetmap_carto_home}/scripts
%{__cp} --recursive --preserve style symbols %{buildroot}%{openstreetmap_carto_home}
%{__cp} --preserve indexes.* openstreetmap-carto.* road-colors.yaml %{buildroot}%{openstreetmap_carto_home}

%{__ln_s} %{openstreetmap_carto_data}/data %{buildroot}%{openstreetmap_carto_home}

%{__install} -d %{buildroot}%{openstreetmap_carto_sysconf}
%{__cp} --preserve project.mml %{buildroot}%{openstreetmap_carto_sysconf}
%{__ln_s} %{openstreetmap_carto_home}/data %{buildroot}%{openstreetmap_carto_sysconf}
%{__ln_s} %{openstreetmap_carto_home}/style %{buildroot}%{openstreetmap_carto_sysconf}
%{__ln_s} %{openstreetmap_carto_home}/symbols %{buildroot}%{openstreetmap_carto_sysconf}


%files
%doc CARTOGRAPHY.md CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md INSTALL.md README.md RELEASES.md USECASES.md
%license LICENSE.txt
%{openstreetmap_carto_home}/*
%dir %{openstreetmap_carto_sysconf}
%{openstreetmap_carto_sysconf}/data
%{openstreetmap_carto_sysconf}/style
%{openstreetmap_carto_sysconf}/symbols
%config(noreplace) %{openstreetmap_carto_sysconf}/project.mml


%files data-natural-earth
%doc README.ne_110m_admin_0_boundary_lines_land.html VERSION.ne_110m_admin_0_boundary_lines_land.txt
%license LICENSE.ne_110m_admin_0_boundary_lines_land.md
%{openstreetmap_carto_data}/data/ne_110m_admin_0_boundary_lines_land.zip


%files data-fossgis
%doc README.antarctica-icesheet-outlines.txt README.antarctica-icesheet-polygons.txt README.simplified-water-polygons-split.txt README.water-polygons-split.txt
%license LICENSE.%{name}-data-fossgis.txt
%{openstreetmap_carto_data}/data/antarctica-icesheet-outlines-%{data_fossgis_version}.zip
%{openstreetmap_carto_data}/data/antarctica-icesheet-polygons-%{data_fossgis_version}.zip
%{openstreetmap_carto_data}/data/simplified-water-polygons-split-%{data_fossgis_version}.zip
%{openstreetmap_carto_data}/data/water-polygons-split-%{data_fossgis_version}.zip


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
