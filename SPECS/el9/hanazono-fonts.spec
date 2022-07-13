%global  fontname    hanazono
%global  archivename %{fontname}-%{version}
%global  priority    66
%global  fontconf    %{priority}-%{fontname}.conf

Name:    %{fontname}-fonts
Version: %{rpmbuild_version}
Release: %{rpmbuild_release}%{?dist}
Summary: Japanese Mincho-typeface TrueType font

License: Hanazono Font License & OFL 1.1
URL:     http://fonts.jp/hanazono/
Source0: https://osdn.net/projects/hanazono-font/downloads/68253/%{archivename}.zip
Source1: %{name}-fontconfig.conf

BuildArch: noarch

BuildRequires: fontpackages-devel

Requires: fontpackages-filesystem


%description
Hanazono Mincho typeface is a Japanese TrueType font that developed with
a support of Grant-in-Aid for Publication of Scientific Research Results from
Japan Society for the Promotion of Science and the International Research
Institute for Zen Buddhism (IRIZ), Hanazono University. also with volunteers
who work together on glyphwiki.org.

This font contains 107518 characters in ISO/IEC 10646 and Unicode Standard,
also supports character sets:
 - 6355 characters in JIS X 0208:1997
 - 5801 characters in JIS X 0212:1990
 - 3695 characters in JIS X 0213:2004
 - 6763 characters in GB 2312-80
 - 13053 characters in Big-5
 - 4888 characters in KS X 1001:1992
 - 360 characters in IBM extensions
 - 9810 characters in IICORE
 - Kanji characters in GB18030-2000
 - Kanji characters in Adobe-Japan1-6


%prep
%setup -q -T -c -a 0


%build


%install
%{__install} -dm 0755 $RPM_BUILD_ROOT%{_fontdir}
%{__install} -pm 0644 *.ttf $RPM_BUILD_ROOT%{_fontdir}
%{__install} -dm 0755 $RPM_BUILD_ROOT%{_fontconfig_templatedir} \
                 $RPM_BUILD_ROOT%{_fontconfig_confdir}
%{__install} -pm 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_fontconfig_templatedir}/%{fontconf}

ln -s %{_fontconfig_templatedir}/%{fontconf} $RPM_BUILD_ROOT%{_fontconfig_confdir}/%{fontconf}


%files
%_font_pkg -f %{fontconf} *.ttf
%doc LICENSE.txt README.txt THANKS.txt


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
