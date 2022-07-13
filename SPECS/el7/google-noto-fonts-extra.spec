Name:           google-noto-fonts-extra
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Beautiful and free fonts for all languages

License:        OFL 1.1
URL:            https://github.com/notofonts/noto-fonts
Source0:        https://github.com/notofonts/noto-fonts/archive/%{commit}/noto-fonts-%{commit}.tar.gz

BuildArch:      noarch


%description
When text is rendered by a computer, sometimes characters are
displayed as "tofu". They are little boxes to indicate your device
doesn't have a font to display the text.

Google has been developing a font family called Noto, which aims to
support all languages with a harmonious look and feel. Noto is
Google's answer to tofu. The name noto is to convey the idea that
Google's goal is to see "no more tofu". Noto has multiple styles and
weights, and is freely available to all.


%prep
%autosetup -n noto-fonts-%{commit}


%build


%install
%{__install} -d -p %{buildroot}%{_datadir}/fonts/%{name}
%{__install} -p hinted/ttf/NotoSansAdlam/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansAdlamUnjoined/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansArabicUI/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansChakma/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansCherokee/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansOriyaUI/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansOsage/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansSinhala/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansSymbols/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSansSymbols2/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/
%{__install} -p hinted/ttf/NotoSerifTibetan/*.ttf %{buildroot}%{_datadir}/fonts/%{name}/

%files
%doc README.md FAQ.md FAQ-KR.md NEWS.md
%license LICENSE
%{_datadir}/fonts/%{name}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
