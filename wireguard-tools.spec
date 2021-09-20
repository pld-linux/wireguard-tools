Summary:	WireGuard is an extremely simple yet fast and modern VPN that utilizes state-of-the-art cryptography
Name:		wireguard-tools
Version:	1.0.20210914
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	https://git.zx2c4.com/wireguard-tools/snapshot/%{name}-%{version}.tar.xz
# Source0-md5:	1d98fb1623817721466152365aec8c45
URL:		https://www.wireguard.com/
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.701
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Obsoletes:	WireGuard < 1.0.20200319-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WireGuard is an extremely simple yet fast and modern VPN that utilizes
state-of-the-art cryptography. It aims to be faster, simpler, leaner,
and more useful than IPSec, while avoiding the massive headache. It
intends to be considerably more performant than OpenVPN. WireGuard is
designed as a general purpose VPN for running on embedded interfaces
and super computers alike, fit for many different circumstances.

This package contains user space tools. Kernel module is included in
Linux 5.6+. You need to also install kernel module from
kernel-*-misc-wireguard package for kernel < 5.6.

%package -n bash-completion-wireguard
Summary:	bash-completion for WireGuard
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-wireguard
This package provides bash-completion for WireGuard.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags} %{rpmcppflags}" \
%{__make} -C src \
	CC="%{__cc}" \
	RUNSTATEDIR=%{_rundir} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	BINDIR=%{_bindir} \
	MANDIR=%{_mandir} \
	SYSCONFDIR=%{_sysconfdir} \
	SYSTEMDUNITDIR=%{systemdunitdir} \
	BASHCOMPDIR=%{bash_compdir} \
	WITH_BASHCOMPLETION=yes \
	WITH_SYSTEMDUNITS=yes \
	WITH_WGQUICK=yes

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
%{systemdunitdir}/wg-quick.target
%{_mandir}/man8/wg-quick.8*
%{_mandir}/man8/wg.8*

%files -n bash-completion-wireguard
%defattr(644,root,root,755)
%{bash_compdir}/wg
%{bash_compdir}/wg-quick
