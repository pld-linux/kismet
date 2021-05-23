# TODO
#  - Anybody knows, why it will not build, when kernel-headers are installed?
#
%define		tarver	%(echo %{version} | tr _ -)
Summary:	Wireless network sniffer
Summary(pl.UTF-8):	Sniffer sieci bezprzewodowych
Name:		kismet
Version:	2021_05_R1
Release:	0.1
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.kismetwireless.net/code/%{name}-%{tarver}.tar.xz
# Source0-md5:	df4cc90d5183b7fd45846a33bf598339
Patch0:		config.patch
URL:		http://www.kismetwireless.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bluez-libs-devel
BuildRequires:	gmp-devel
BuildRequires:	libcap-devel
BuildRequires:	libnl-devel
BuildRequires:	libpcap-devel >= 2:0.9.4-1
BuildRequires:	libwebsockets-devel >= 3.1.0
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-ext-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
Suggests:	%{name}-server
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

%package server
Summary:	Server for Kismet
Group:		Networking/Daemons
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/sbin/groupadd
Provides:	group(kismet)

%description server
This package contains kismet_server which you can access with kismet
protocol compatible clients.

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

%pre server
%groupadd -P %{name}-server -g 180 kismet

%preun server
if [ "$1" = "0" ]; then
	%groupremove kismet
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG README.md README.plugin-alertsyslog README.plugin-dashboard
%attr(755,root,root) %{_bindir}/kismet
%{_datadir}/%{name}

%files server
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kismet.conf
%attr(755,root,root) %{_bindir}/kismet_server
%dir %{_libdir}/kismet
#%attr(755,root,root) %{_libdir}/kismet/alertsyslog.so
#%attr(755,root,root) %{_libdir}/kismet/spectool_net.so
%dir %attr(770,root,kismet) /var/log/%{name}
