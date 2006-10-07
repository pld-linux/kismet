#
# TODO: Anybody knows, why it will not build,
#	when kernel-headers are installed?
#
Summary:	Wireless network sniffer
Summary(pl):	Sniffer sieci bezprzewodowych
Name:		kismet
Version:	2006_04_R1
%define	_ver	2006-04-R1
Release:	3
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.kismetwireless.net/code/%{name}-%{_ver}.tar.gz
# Source0-md5:	8ec2de513f2911df1b7edfcba5ad1c26
URL:		http://www.kismetwireless.net/
BuildRequires:	ImageMagick-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel
BuildRequires:	libpcap-devel >= 2:0.9.4-1
BuildRequires:	libstdc++-devel
BuildRequires:	libwiretap-devel
BuildRequires:	ncurses-ext-devel
# it uses internal structures - so strict deps
%requires_eq	libpcap
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
w Linuksie w³±czaj±c w to karty Prism2 wspierane przez projekt Wlan-NG
(Linksys, Dlink, Rangelan, etc), kart które umo¿liwiaj±
przechwytywanie pakietów poprzez libpcap (Cisco), oraz ograniczone
wsparcie dla kart bez obs³ugi Monitora RF.

%prep
%setup -q -n %{name}-%{_ver}

cp Makefile.in Makefile.new
sed -e 's#-o $(INSTUSR)##g' -e 's#-o $(INSTGRP)##g' \
	Makefile.new > Makefile.in

%build
cp -f /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}
CPPFLAGS="-I/usr/include/ncurses"
%configure \
	--enable-syspcap \
	--with-linuxheaders=no \
	--with-ethereal=%{_includedir} \
%ifarch arm
	--enable-zaurus
%endif

%{__make}

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
%doc docs/* CHANGELOG CHANGELOG-OLD README
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/*_manuf
%{_datadir}/%{name}
%{_mandir}/man?/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}*
