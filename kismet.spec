Summary:	Wireless network sniffer
Summary(pl):	Sniffer sieci bezprzewodowych
Name:		kismet
Version:	2.8.1
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.kismetwireless.net/code/%{name}-%{version}.tar.gz
URL:		http://www.kismetwireless.net/
BuildRequires:	ImageMagick-devel
BuildRequires:	XFree86-devel
BuildRequires:	expat-devel
BuildRequires:	libpcap-devel
BuildRequires:	ncurses-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
Kismet is a 802.11b wireless network sniffer. It is capable of
sniffing using almost any wireless card supported in Linux, including
Prism2 based cards supported by the Wlan-NG project (Linksys, Dlink,
Rangelan, etc), cards which support standard packet capture via
libpcap (Cisco), and limited support for cards without RF Monitor
support.

%description -l pl
Kismet to sniffer bezprzewodowych sieci 802.11b. Jest zdolny do
sniffowania u¿ywaj±c prawie dowolnych bezprzewodowych kart sieciowych
w Linuxie w³±czaj±c w to karty Prism2 wspierane przez projekt Wlan-NG
(Linksys, Dlink, Rangelan, etc), kart które umo¿liwiaj±
przechwytywanie pakietów poprzez libpcap (Cisco), oraz ograniczone
wsparcie dla kart bez obs³ugi Monitora RF.

%prep
%setup -q

%build
cp Makefile.in Makefile.new
sed -e 's#-o $(INSTUSR)##g' -e 's#-o $(INSTGRP)##g' \
	Makefile.new > Makefile.in

%configure \
	CPPFLAGS="-I%{_includedir}/X11 -I/usr/include/ncurses" \
%ifarch arm
	--enable-zaurus \
%endif
	--enable-syspcap
%{__make} dep all

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_datadir}}

%{__make} install \
	INSTGRP=$(id -g) \
	MANGRP=$(id -g) \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec_prefix=$RPM_BUILD_ROOT%{_prefix} \
	ETC=$RPM_BUILD_ROOT%{_sysconfdir} \
	BIN=$RPM_BUILD_ROOT%{_bindir} \
	SHARE=$RPM_BUILD_ROOT%{_datadir}/%{name} \
	MAN=$RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* CHANGELOG FAQ README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/man?/*
%config(noreplace) %{_sysconfdir}/%{name}*
