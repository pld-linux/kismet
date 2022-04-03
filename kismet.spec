%define		tarver	%(echo %{version} | tr _ -)
Summary:	Wireless network sniffer
Summary(pl.UTF-8):	Sniffer sieci bezprzewodowych
Name:		kismet
Version:	2021_05_R1
Release:	3
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.kismetwireless.net/code/%{name}-%{tarver}.tar.xz
# Source0-md5:	df4cc90d5183b7fd45846a33bf598339
Patch0:		opt.patch
URL:		http://www.kismetwireless.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bluez-libs-devel
BuildRequires:	gmp-devel
BuildRequires:	libcap-devel
BuildRequires:	libnl-devel
BuildRequires:	libpcap-devel >= 2:0.9.4-1
BuildRequires:	libstdc++-devel
BuildRequires:	libwebsockets-devel >= 3.1.0
BuildRequires:	ncurses-ext-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/sbin/groupadd
Provides:	group(kismet)
Obsoletes:	kismet-server < 2021_05_R1
# it uses internal structures - so strict deps
%requires_eq	libpcap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		plugins	plugin-alertsyslog plugin-dashboard

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

# -j1 due to OOM
%{__make} -j1

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
		SUIDGROUP=%(id -gn) \
		MANGRP=%(id -gn)
done

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -P %{name} -g 180 kismet

%preun
if [ "$1" = "0" ]; then
	%groupremove kismet
fi

%triggerpostun -- kismet-server < 2021_05_R1
%groupadd -P %{name} -g 180 kismet

%files
%defattr(644,root,root,755)
%doc README.md README.plugin-alertsyslog README.plugin-dashboard
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet_80211.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet_alerts.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet_filter.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet_httpd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet_logging.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet_memory.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet_uav.conf
%attr(755,root,root) %{_bindir}/kismet
%attr(755,root,root) %{_bindir}/kismet_cap_freaklabs_zigbee
%attr(755,root,root) %{_bindir}/kismet_cap_kismetdb
%attr(755,root,root) %{_bindir}/kismet_cap_linux_bluetooth
%attr(755,root,root) %{_bindir}/kismet_cap_linux_wifi
%attr(755,root,root) %{_bindir}/kismet_cap_nrf_51822
%attr(755,root,root) %{_bindir}/kismet_cap_nrf_52840
%attr(755,root,root) %{_bindir}/kismet_cap_nrf_mousejack
%attr(755,root,root) %{_bindir}/kismet_cap_nxp_kw41z
%attr(755,root,root) %{_bindir}/kismet_cap_pcapfile
%attr(755,root,root) %{_bindir}/kismet_cap_rz_killerbee
%attr(755,root,root) %{_bindir}/kismet_cap_sdr_rtl433
%attr(755,root,root) %{_bindir}/kismet_cap_sdr_rtladsb
%attr(755,root,root) %{_bindir}/kismet_cap_sdr_rtlamr
%attr(755,root,root) %{_bindir}/kismet_cap_ti_cc_2531
%attr(755,root,root) %{_bindir}/kismet_cap_ti_cc_2540
%attr(755,root,root) %{_bindir}/kismet_discovery
%attr(755,root,root) %{_bindir}/kismet_server
%attr(755,root,root) %{_bindir}/kismetdb_clean
%attr(755,root,root) %{_bindir}/kismetdb_dump_devices
%attr(755,root,root) %{_bindir}/kismetdb_statistics
%attr(755,root,root) %{_bindir}/kismetdb_strip_packets
%attr(755,root,root) %{_bindir}/kismetdb_to_gpx
%attr(755,root,root) %{_bindir}/kismetdb_to_kml
%attr(755,root,root) %{_bindir}/kismetdb_to_pcap
%attr(755,root,root) %{_bindir}/kismetdb_to_wiglecsv
%{_datadir}/%{name}
%dir %{_libdir}/kismet
%dir %{_libdir}/kismet/alertsyslog
%attr(755,root,root) %{_libdir}/kismet/alertsyslog/alertsyslog.so
%{_libdir}/kismet/alertsyslog/manifest.conf
%{_libdir}/kismet/dashboard
%{py3_sitescriptdir}/KismetCapture*
