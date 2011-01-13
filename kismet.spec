# TODO
#  - Anybody knows, why it will not build, when kernel-headers are installed?
#  - maybe subpkg server and add initscript to it? especially as kismet server
#    can be remote. kismet_capture would still be in client package?
#  - update ncurses patch for tinfo, make it detect wide versions as well
#
%define		tarver	%(echo %{version} | tr _ -)
Summary:	Wireless network sniffer
Summary(pl.UTF-8):	Sniffer sieci bezprzewodowych
Name:		kismet
Version:	2010_07_R1
Release:	0.4
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.kismetwireless.net/code/%{name}-%{tarver}.tar.gz
# Source0-md5:	85e59186eb529889118b5635f35cf57d
Patch0:		config.patch
URL:		http://www.kismetwireless.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bluez-libs-devel
BuildRequires:	gmp-devel
BuildRequires:	libcap-devel
BuildRequires:	libnl-devel
BuildRequires:	libpcap-devel >= 2:0.9.4-1
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-ext-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
# it uses internal structures - so strict deps
%requires_eq	libpcap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		plugins	plugin-autowep plugin-btscan plugin-ptw plugin-spectools

%description
Kismet is a 802.11b wireless network sniffer. It is capable of
sniffing using almost any wireless card supported in Linux, including
Prism2 based cards supported by the Wlan-NG project (Linksys, Dlink,
Rangelan, etc), cards which support standard packet capture via
libpcap (Cisco), and limited support for cards without RF Monitor
support.

%description -l pl.UTF-8
Kismet to sniffer bezprzewodowych sieci 802.11b. Jest zdolny do
sniffowania używając prawie dowolnych bezprzewodowych kart sieciowych
w Linuksie włączając w to karty Prism2 wspierane przez projekt Wlan-NG
(Linksys, Dlink, Rangelan, etc), kart które umożliwiają
przechwytywanie pakietów poprzez libpcap (Cisco), oraz ograniczone
wsparcie dla kart bez obsługi Monitora RF.

%prep
%setup -q -n %{name}-%{tarver}
%patch0 -p1

# make lib64 aware, include exec bits on install
%{__sed} -i -e 's!\$(prefix)/lib/!%_libdir/!g' plugin-*/Makefile
%{__sed} -i -e '/install/ s!-m644!-m755!' plugin-*/Makefile

# make %doc friendly
for a in plugin-*/README; do
	mv $a README.${a%/README}
done

%build
cp -f /usr/share/automake/config.* .
%{__aclocal}
%{__autoconf}
%configure

%{__make} \
	CLIENTLIBS="-ldl -lncurses -lpanel -ltinfo"  # hack to add -ltinfo

for plugin in %plugins; do
	%{__make} -C $plugin \
		KIS_SRC_DIR=$PWD
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_datadir},/var/log/%{name}}
for dir in . %plugins; do
	%{__make} -C $dir install \
		DESTDIR="$RPM_BUILD_ROOT" \
		KIS_SRC_DIR=$PWD \
		INSTUSR=%(id -un) \
		INSTGRP=%(id -gn) \
		MANGRP=%(id -gn)
done

# do what binsuidinstall would do
install -p kismet_capture $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* CHANGELOG README README.plugin-*
%attr(755,root,root) %{_bindir}/kismet
%attr(755,root,root) %{_bindir}/kismet_client
%attr(755,root,root) %{_bindir}/kismet_drone
%attr(755,root,root) %{_bindir}/kismet_server
# TODO: create kismet group instead
%attr(4750,root,adm) %{_bindir}/kismet_capture
%{_datadir}/%{name}
%{_mandir}/man1/kismet.1*
%{_mandir}/man1/kismet_drone.1*
%{_mandir}/man5/kismet.conf.5*
%{_mandir}/man5/kismet_drone.conf.5*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet_drone.conf
%dir %{_libdir}/kismet
%dir %{_libdir}/kismet_client
%attr(755,root,root) %{_libdir}/kismet/aircrack-kismet.so
%attr(755,root,root) %{_libdir}/kismet/autowep-kismet.so
%attr(755,root,root) %{_libdir}/kismet/btscan.so
%attr(755,root,root) %{_libdir}/kismet/spectool_net.so
%attr(755,root,root) %{_libdir}/kismet_client/btscan_ui.so
%attr(755,root,root) %{_libdir}/kismet_client/spectools_ui.so

# TODO: kismet group
%dir %attr(770,root,adm) /var/log/%{name}
