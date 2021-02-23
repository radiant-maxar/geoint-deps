Name:           google-noto-fonts-extra
Version:        %{rpmbuild_version}
Release:        %{rpmbuild_release}%{?dist}
Summary:        Beautiful and free fonts for all languages

License:        OFL 1.1
URL:            https://github.com/googlefonts/noto-source
Source0:        https://github.com/googlefonts/noto-source/archive/%{commit}/noto-source-%{commit}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python3
BuildRequires:  python3-pip


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
%autosetup -p 1 -n noto-source-%{commit}
%{__sed} -i 's#git submodule update --init##g' ./build
%{__sed} -i 's#pip install -r scripts/fontmake/requirements.txt##g' ./build
%{__sed} -i 's#pip install -e scripts/fontmake#pip install fontmake#g' ./build
./build setup


%build
# Only build .ttf files to save time
%{__sed} -i "s#'otf' 'ttf'#'ttf'#g" ./build
# ./build all
./build src/NotoSansAdlam/NotoSansAdlam.designspace
./build src/NotoSansAdlamUnjoined/NotoSansAdlamUnjoined.designspace
./build src/NotoSansArabicUI-MM.glyphs
./build src/NotoSansChakma/NotoSansChakma.glyphs
./build src/NotoSansCherokee/NotoSansCherokee.designspace
./build src/NotoSansOriyaUI-MM.glyphs
./build src/NotoSansOsage/NotoSansOsage.glyphs
./build src/NotoSansSinhala/NotoSansSinhala-MM.glyphs
./build src/NotoSansSymbols/NotoSansSymbols.designspace
./build src/NotoSansSymbols2/NotoSansSymbols2.designspace
./build src/NotoSerifTibetan-MM.glyphs


%install
%{__install} -d -p %{buildroot}%{_datadir}/fonts/%{name}
%{__cp} --preserve instance_ttf/* %{buildroot}%{_datadir}/fonts/%{name}


%files
%doc README.md CONTRIBUTING.md FONT_CONTRIBUTION.md
%license src/LICENSE
%{_datadir}/fonts/%{name}


%changelog
* %(%{_bindir}/date "+%%a %%b %%d %%Y") %{rpmbuild_name} <%{rpmbuild_email}> - %{version}-%{rpmbuild_release}
- %{version}-%{rpmbuild_release}
