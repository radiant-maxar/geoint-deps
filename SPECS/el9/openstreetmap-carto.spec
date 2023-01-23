# The following macros are also required:
# * data_natural_earth_version
# * fonts_google_noto_cjk_git_ref
# * fonts_google_noto_git_ref
# * fonts_hanazono_version

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
Source1:        https://github.com/nvkelso/natural-earth-vector/raw/master/LICENSE.md
Source2:        https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_boundary_lines_land.zip
Source3:        https://osmdata.openstreetmap.de/download/antarctica-icesheet-outlines-3857.zip
Source4:        https://osmdata.openstreetmap.de/download/antarctica-icesheet-polygons-3857.zip
Source5:        https://osmdata.openstreetmap.de/download/simplified-water-polygons-split-3857.zip
Source6:        https://osmdata.openstreetmap.de/download/water-polygons-split-3857.zip

Source7:        https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/LICENSE
Source8:        https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/README.md

Source9:        https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSans/NotoSans-Bold.ttf
Source10:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSans/NotoSans-Italic.ttf
Source11:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSans/NotoSans-Regular.ttf
Source14:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansAdlamUnjoined/NotoSansAdlamUnjoined-Bold.ttf
Source15:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansAdlamUnjoined/NotoSansAdlamUnjoined-Regular.ttf
Source16:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansArabicUI/NotoSansArabicUI-Bold.ttf
Source17:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansArabicUI/NotoSansArabicUI-Regular.ttf
Source18:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansArmenian/NotoSansArmenian-Bold.ttf
Source19:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansArmenian/NotoSansArmenian-Regular.ttf
Source20:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBalinese/NotoSansBalinese-Bold.ttf
Source21:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBalinese/NotoSansBalinese-Regular.ttf
Source22:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBamum/NotoSansBamum-Bold.ttf
Source23:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBamum/NotoSansBamum-Regular.ttf
Source24:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBatak/NotoSansBatak-Regular.ttf
Source25:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBengaliUI/NotoSansBengaliUI-Bold.ttf
Source26:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBengaliUI/NotoSansBengaliUI-Regular.ttf
Source27:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBuginese/NotoSansBuginese-Regular.ttf
Source28:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansBuhid/NotoSansBuhid-Regular.ttf
Source29:       https://github.com/googlefonts/noto-cjk/raw/%{fonts_google_noto_cjk_git_ref}/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf
Source30:       https://github.com/googlefonts/noto-cjk/raw/%{fonts_google_noto_cjk_git_ref}/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf
Source31:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansCanadianAboriginal/NotoSansCanadianAboriginal-Bold.ttf
Source32:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansCanadianAboriginal/NotoSansCanadianAboriginal-Regular.ttf
Source33:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansChakma/NotoSansChakma-Regular.ttf
Source34:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansCham/NotoSansCham-Bold.ttf
Source35:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansCham/NotoSansCham-Regular.ttf
Source36:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansCherokee/NotoSansCherokee-Bold.ttf
Source37:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansCherokee/NotoSansCherokee-Regular.ttf
Source38:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansCoptic/NotoSansCoptic-Regular.ttf
Source39:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansDevanagariUI/NotoSansDevanagariUI-Bold.ttf
Source40:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansDevanagariUI/NotoSansDevanagariUI-Regular.ttf
Source41:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansEthiopic/NotoSansEthiopic-Bold.ttf
Source42:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansEthiopic/NotoSansEthiopic-Regular.ttf
Source43:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansGeorgian/NotoSansGeorgian-Bold.ttf
Source44:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansGeorgian/NotoSansGeorgian-Regular.ttf
Source45:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansGujaratiUI/NotoSansGujaratiUI-Bold.ttf
Source46:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansGujaratiUI/NotoSansGujaratiUI-Regular.ttf
Source47:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansGurmukhiUI/NotoSansGurmukhiUI-Bold.ttf
Source48:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansGurmukhiUI/NotoSansGurmukhiUI-Regular.ttf
Source49:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansHanunoo/NotoSansHanunoo-Regular.ttf
Source50:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansHebrew/NotoSansHebrew-Bold.ttf
Source51:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansHebrew/NotoSansHebrew-Regular.ttf
Source52:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansJavanese/NotoSansJavanese-Bold.ttf
Source53:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansJavanese/NotoSansJavanese-Regular.ttf
Source54:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansKannadaUI/NotoSansKannadaUI-Bold.ttf
Source55:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansKannadaUI/NotoSansKannadaUI-Regular.ttf
Source56:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansKayahLi/NotoSansKayahLi-Bold.ttf
Source57:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansKayahLi/NotoSansKayahLi-Regular.ttf
Source58:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansKhmerUI/NotoSansKhmerUI-Bold.ttf
Source59:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansKhmerUI/NotoSansKhmerUI-Regular.ttf
Source60:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansLaoUI/NotoSansLaoUI-Bold.ttf
Source61:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansLaoUI/NotoSansLaoUI-Regular.ttf
Source62:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansLepcha/NotoSansLepcha-Regular.ttf
Source63:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansLimbu/NotoSansLimbu-Regular.ttf
Source64:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansLisu/NotoSansLisu-Bold.ttf
Source65:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansLisu/NotoSansLisu-Regular.ttf
Source66:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansMalayalamUI/NotoSansMalayalamUI-Bold.ttf
Source67:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansMalayalamUI/NotoSansMalayalamUI-Regular.ttf
Source68:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansMandaic/NotoSansMandaic-Regular.ttf
Source69:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansMongolian/NotoSansMongolian-Regular.ttf
Source70:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansMyanmarUI/NotoSansMyanmarUI-Bold.ttf
Source71:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansMyanmarUI/NotoSansMyanmarUI-Regular.ttf
Source72:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansNKo/NotoSansNKo-Regular.ttf
Source73:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansNewTaiLue/NotoSansNewTaiLue-Regular.ttf
Source74:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansOlChiki/NotoSansOlChiki-Bold.ttf
Source75:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansOlChiki/NotoSansOlChiki-Regular.ttf
Source76:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansOriyaUI/NotoSansOriyaUI-Bold.ttf
Source77:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansOriyaUI/NotoSansOriyaUI-Regular.ttf
Source78:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansOsage/NotoSansOsage-Regular.ttf
Source79:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansOsmanya/NotoSansOsmanya-Regular.ttf
Source80:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSamaritan/NotoSansSamaritan-Regular.ttf
Source81:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSaurashtra/NotoSansSaurashtra-Regular.ttf
Source82:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansShavian/NotoSansShavian-Regular.ttf
Source83:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSinhalaUI/NotoSansSinhalaUI-Bold.ttf
Source84:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSinhalaUI/NotoSansSinhalaUI-Regular.ttf
Source85:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSundanese/NotoSansSundanese-Bold.ttf
Source86:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSundanese/NotoSansSundanese-Regular.ttf
Source87:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSymbols/NotoSansSymbols-Bold.ttf
Source88:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSymbols/NotoSansSymbols-Regular.ttf
Source89:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSymbols2/NotoSansSymbols2-Regular.ttf
Source90:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSyriac/NotoSansSyriac-Black.ttf
Source91:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansSyriac/NotoSansSyriac-Regular.ttf
Source92:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTagalog/NotoSansTagalog-Regular.ttf
Source93:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTagbanwa/NotoSansTagbanwa-Regular.ttf
Source94:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTaiLe/NotoSansTaiLe-Regular.ttf
Source95:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTaiTham/NotoSansTaiTham-Bold.ttf
Source96:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTaiTham/NotoSansTaiTham-Regular.ttf
Source97:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTaiViet/NotoSansTaiViet-Regular.ttf
Source98:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTamilUI/NotoSansTamilUI-Bold.ttf
Source99:       https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTamilUI/NotoSansTamilUI-Regular.ttf
Source100:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTeluguUI/NotoSansTeluguUI-Bold.ttf
Source101:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTeluguUI/NotoSansTeluguUI-Regular.ttf
Source102:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansThaana/NotoSansThaana-Bold.ttf
Source103:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansThaana/NotoSansThaana-Regular.ttf
Source104:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansThaiUI/NotoSansThaiUI-Bold.ttf
Source105:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansThaiUI/NotoSansThaiUI-Regular.ttf
Source106:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansTifinagh/NotoSansTifinagh-Regular.ttf
Source107:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansVai/NotoSansVai-Regular.ttf
Source108:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSansYi/NotoSansYi-Regular.ttf
Source109:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSerifTibetan/NotoSerifTibetan-Bold.ttf
Source110:      https://github.com/notofonts/noto-fonts/raw/%{fonts_google_noto_git_ref}/hinted/ttf/NotoSerifTibetan/NotoSerifTibetan-Regular.ttf

Source111:      https://fonts.google.com/download?family=Noto%20Emoji#/NotoEmoji.zip
Source112:      https://osdn.net/projects/hanazono-font/downloads/68253/hanazono-%{fonts_hanazono_version}.zip

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  lua

Requires:       %{name}-data-fossgis = %{version}-%{release}
Requires:       %{name}-data-natural-earth = %{version}-%{release}
Requires:       %{name}-fonts-google-noto = %{version}-%{release}
Requires:       %{name}-fonts-hanazono = %{version}-%{release}
Requires:       gdal
Requires:       python3-psycopg2
Requires:       python3-pyyaml
Requires:       python3-requests


%description
These are the CartoCSS map stylesheets for the Standard map layer on
OpenStreetMap.org.

These stylesheets can be used in your own cartography projects, and
are designed to be easily customised. They work with Kosmtik and also
with the command-line CartoCSS processor.

Since August 2013 these stylesheets have been used on the OSMF
tileservers (tile.openstreetmap.org), and are updated from each point
release. They supersede the previous XML-based stylesheets.


%package data-fossgis
Summary:   FOSSGIS's water/icesheet polygon/outline shapefiles required by %{name}, indexed through shapeindex
License:   ODbL
URL:       https://osmdata.openstreetmap.de


%description data-fossgis
%{summary}.


%package data-natural-earth
Summary:   Natural Earth's country boundary shapefiles required by %{name}, indexed through shapeindex
License:   PD
URL:       https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-boundary-lines


%description data-natural-earth
%{summary}.


%package fonts-google-noto
Summary:   Fonts required by %{name} (Google Noto)
License:   OFL 1.1
URL:       https://github.com/notofonts/noto-fonts


%description fonts-google-noto
%{summary}.


%package fonts-hanazono
Summary:   Fonts required by %{name} (Hanazono)
License:   Hanazono Font License & OFL 1.1
URL:       http://fonts.jp/hanazono


%description fonts-hanazono
%{summary}.


%prep
%autosetup -p1 -n %{name}-%{version}

%{__mkdir} data

%{__mv} %{SOURCE1} LICENSE.ne_110m_admin_0_boundary_lines_land.md

%{__cp} %{SOURCE2} data
echo -n "$(date --utc '+%a, %d %b %Y %T GMT')" > %{SOURCE2}.lastmod
%{__mv} %{SOURCE2}.lastmod data
%{__unzip} %{SOURCE2} ne_110m_admin_0_boundary_lines_land.README.html ne_110m_admin_0_boundary_lines_land.VERSION.txt
%{__mv} ne_110m_admin_0_boundary_lines_land.README.html README.ne_110m_admin_0_boundary_lines_land.html
%{__mv} ne_110m_admin_0_boundary_lines_land.VERSION.txt VERSION.ne_110m_admin_0_boundary_lines_land.txt
%{__grep} -q %{data_natural_earth_version} VERSION.ne_110m_admin_0_boundary_lines_land.txt

%{__cp} %{SOURCE3} data
echo -n "$(date --utc '+%a, %d %b %Y %T GMT')" > %{SOURCE3}.lastmod
%{__mv} %{SOURCE3}.lastmod data
%{__unzip} %{SOURCE3} antarctica-icesheet-outlines-3857/README
%{__mv} antarctica-icesheet-outlines-3857/README README.antarctica-icesheet-outlines.txt
rmdir antarctica-icesheet-outlines-3857

%{__cp} %{SOURCE4} data
echo -n "$(date --utc '+%a, %d %b %Y %T GMT')" > %{SOURCE4}.lastmod
%{__mv} %{SOURCE4}.lastmod data
%{__unzip} %{SOURCE4} antarctica-icesheet-polygons-3857/README
%{__mv} antarctica-icesheet-polygons-3857/README README.antarctica-icesheet-polygons.txt
rmdir antarctica-icesheet-polygons-3857

%{__cp} %{SOURCE5} data
echo -n "$(date --utc '+%a, %d %b %Y %T GMT')" > %{SOURCE5}.lastmod
%{__mv} %{SOURCE5}.lastmod data
%{__unzip} %{SOURCE5} simplified-water-polygons-split-3857/README.txt
%{__mv} simplified-water-polygons-split-3857/README.txt README.simplified-water-polygons-split.txt
rmdir simplified-water-polygons-split-3857

%{__cp} %{SOURCE6} data
echo -n "$(date --utc '+%a, %d %b %Y %T GMT')" > %{SOURCE6}.lastmod
%{__mv} %{SOURCE6}.lastmod data
%{__unzip} %{SOURCE6} water-polygons-split-3857/README.txt
%{__mv} water-polygons-split-3857/README.txt README.water-polygons-split.txt
rmdir water-polygons-split-3857
%{__sed} -n '/^LICENSE$/,$p' README.water-polygons-split.txt > LICENSE.%{name}-data-fossgis.txt

%{__mkdir} fonts-google-noto
%{__mv} %{SOURCE7} fonts-google-noto/LICENSE
%{__mv} %{SOURCE8} fonts-google-noto/README.md

# scripts/get-fonts.sh

%{__mkdir} fonts
%{__cp} %{_sourcedir}/Noto*.?tf fonts

%{__unzip} %{SOURCE111} static/NotoEmoji-Bold.ttf static/NotoEmoji-Regular.ttf -d fonts
%{__mv} fonts/static/*.ttf fonts
rmdir fonts/static

%{__unzip} %{SOURCE112} HanaMinA.ttf HanaMinB.ttf LICENSE.txt README.txt -d fonts
%{__mkdir} fonts-hanazono
%{__mv} fonts/LICENSE.txt fonts/README.txt fonts-hanazono


%build


%check
lua scripts/lua/test.lua


%install
%{__install} -d %{buildroot}%{openstreetmap_carto_data}
%{__cp} --recursive --preserve data %{buildroot}%{openstreetmap_carto_data}

%{__install} -d %{buildroot}%{_datadir}/fonts
%{__cp} --recursive --preserve fonts %{buildroot}%{_datadir}/fonts/%{name}

%{__install} -d %{buildroot}%{openstreetmap_carto_home}
%{__install} -d %{buildroot}%{openstreetmap_carto_home}/scripts
%{__cp} --preserve scripts/*.py %{buildroot}%{openstreetmap_carto_home}/scripts
%{__cp} --recursive --preserve scripts/lua %{buildroot}%{openstreetmap_carto_home}/scripts
%{__cp} --recursive --preserve patterns style symbols %{buildroot}%{openstreetmap_carto_home}
%{__cp} --preserve indexes.* openstreetmap-carto.* road-colors.yaml %{buildroot}%{openstreetmap_carto_home}

%{__ln_s} %{openstreetmap_carto_data}/data %{buildroot}%{openstreetmap_carto_home}
%{__ln_s} %{_datadir}/fonts/%{name} %{buildroot}%{openstreetmap_carto_home}/fonts

%{__install} -d %{buildroot}%{openstreetmap_carto_sysconf}
%{__cp} --preserve project.mml external-data.yml %{buildroot}%{openstreetmap_carto_sysconf}
%{__ln_s} %{openstreetmap_carto_sysconf}/external-data.yml %{buildroot}%{openstreetmap_carto_home}
%{__ln_s} %{_datadir}/fonts/%{name} %{buildroot}%{openstreetmap_carto_sysconf}/fonts
%{__ln_s} %{openstreetmap_carto_home}/patterns %{buildroot}%{openstreetmap_carto_sysconf}
%{__ln_s} %{openstreetmap_carto_home}/style %{buildroot}%{openstreetmap_carto_sysconf}
%{__ln_s} %{openstreetmap_carto_home}/symbols %{buildroot}%{openstreetmap_carto_sysconf}


%files
%doc CARTOGRAPHY.md CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md INSTALL.md README.md RELEASES.md USECASES.md
%license LICENSE.txt
%{openstreetmap_carto_home}/*
%dir %{openstreetmap_carto_sysconf}
%{openstreetmap_carto_sysconf}/fonts
%{openstreetmap_carto_sysconf}/patterns
%{openstreetmap_carto_sysconf}/style
%{openstreetmap_carto_sysconf}/symbols
%config(noreplace) %{openstreetmap_carto_sysconf}/project.mml
%config(noreplace) %{openstreetmap_carto_sysconf}/external-data.yml


%files data-natural-earth
%doc README.ne_110m_admin_0_boundary_lines_land.html VERSION.ne_110m_admin_0_boundary_lines_land.txt
%license LICENSE.ne_110m_admin_0_boundary_lines_land.md
%{openstreetmap_carto_data}/data/ne_110m_admin_0_boundary_lines_land.zip*


%files data-fossgis
%doc README.antarctica-icesheet-outlines.txt README.antarctica-icesheet-polygons.txt README.simplified-water-polygons-split.txt README.water-polygons-split.txt
%license LICENSE.%{name}-data-fossgis.txt
%{openstreetmap_carto_data}/data/antarctica-icesheet-outlines-3857.zip*
%{openstreetmap_carto_data}/data/antarctica-icesheet-polygons-3857.zip*
%{openstreetmap_carto_data}/data/simplified-water-polygons-split-3857.zip*
%{openstreetmap_carto_data}/data/water-polygons-split-3857.zip*


%files fonts-google-noto
%doc fonts-google-noto/README.md
%license fonts-google-noto/LICENSE
%{_datadir}/fonts/%{name}/Noto*.?tf


%files fonts-hanazono
%doc fonts-hanazono/README.txt
%license fonts-hanazono/LICENSE.txt
%{_datadir}/fonts/%{name}/Hana*.ttf


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
