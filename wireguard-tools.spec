Summary:	WireGuard is an extremely simple yet fast and modern VPN that utilizes state-of-the-art cryptography
Name:		wireguard-tools
Version:	1.0.20200319
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	https://git.zx2c4.com/wireguard-tools/snapshot/%{name}-%{version}.tar.xz
# Source0-md5:	36cd9411f56bc5dcaac29bbab6fd9c67
URL:		https://www.wireguard.com/
BuildRequires:	libmnl-devel
BuildRequires:	rpmbuild(macros) >= 1.701
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WireGuard is an extremely simple yet fast and modern VPN that utilizes
state-of-the-art cryptography. It aims to be faster, simpler, leaner,
and more useful than IPSec, while avoiding the massive headache. It
intends to be considerably more performant than OpenVPN. WireGuard is
designed as a general purpose VPN for running on embedded interfaces
and super computers alike, fit for many different circumstances.

This package contains user space tools. You need to also install
kernel module from kernel-*-misc-wireguard package.

%prep
%setup -q

%build
%{make} -C src V=1

%install
rm -rf $RPM_BUILD_ROOT

%{make} -C src install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	SYSCONFDIR=$RPM_BUILD_ROOT%{_sysconfdir} \
	SYSTEMDUNITDIR=$RPM_BUILD_ROOT%{systemdunitdir} \
	WITH_SYSTEMDUNITS=yes

%clean
rm -rf $RPM_BUILD_ROOT

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc contrib README.md
%attr(755,root,root) %{_bindir}/wg
%attr(755,root,root) %{_bindir}/wg-quick
%dir %{_sysconfdir}/wireguard
%{systemdunitdir}/wg-quick@.service
%{_mandir}/man8/wg-quick.8*
%{_mandir}/man8/wg.8*
