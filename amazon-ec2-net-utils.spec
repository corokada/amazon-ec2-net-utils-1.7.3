%if 0%{?amzn} >= 2 || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global systemd 1
%else
%global systemd 0
%endif

Name:      amazon-ec2-net-utils
Summary:   A set of network tools for managing ENIs
Version:   1.7.3
Release:   1%{?dist}
License:   MIT and GPLv2

Source:    https://github.com/aws/amazon-ec2-net-utils/archive/%{version}.tar.gz

URL:       https://github.com/aws/amazon-ec2-net-utils
BuildArch: noarch
Requires:  curl
Requires:  iproute
Requires:  initscripts
BuildRequires: make
BuildRequires: systemd
%if %{systemd}
%{?systemd_requires}
BuildRequires: systemd-units
Requires: systemd-units
%endif # systemd
Requires: dhclient >= 4.2.5-77.amzn2.1.5
Provides: ec2-net-utils = %{version}-%{release}
Obsoletes: ec2-net-utils < 1.7.3
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
amazon-ec2-net-utils contains a set of utilities for managing elastic network
interfaces.

%prep

%setup -q

%build

%install

make install DESTDIR=%{buildroot} prefix=/usr udevdir=%{buildroot}/%{_udevrulesdir}
mv %{buildroot}/%{_mandir}/man8/ec2ifdown.8 %{buildroot}/%{_mandir}/man8/ec2ifdown.8.gz

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with systemd}
%post
%systemd_post ec2net-scan.service
%systemd_post ec2net-ifup@.service

%preun
%systemd_preun ec2net-scan.service
%systemd_preun ec2net-ifup@.service
%endif # systemd

%files
%{_udevrulesdir}/53-ec2-network-interfaces.rules
%{_udevrulesdir}/75-persistent-net-generator.rules
%config(noreplace) %{_sysconfdir}/modprobe.d/ixgbevf.conf
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ec2net-functions
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ec2net-functions-lib
%{_sysconfdir}/sysconfig/network-scripts/ec2net.hotplug
%{_sysconfdir}/dhcp/dhclient.d/ec2dhcp.sh
%config(noreplace) %{_sysconfdir}/dhcp/dhclient-enter-hooks.d/50_ec2_rewrite_primary_enter_hook.sh

%if %{systemd}
%{_sbindir}/ec2ifup
%{_sbindir}/ec2ifdown
%{_sbindir}/ec2ifscan
%attr(0644,root,root) %{_unitdir}/ec2net-scan.service
%attr(0644,root,root) %{_unitdir}/ec2net-ifup@.service
%attr(755, -, -) %{_prefix}/lib/udev/write_net_rules
%{_prefix}/lib/udev/rule_generator.functions
%else
/sbin/ec2ifup
/sbin/ec2ifdown
/sbin/ec2ifscan
%{_sysconfdir}/init/elastic-network-interfaces.conf
%endif # systemd
%doc %{_mandir}/man8/ec2ifup.8.gz
%doc %{_mandir}/man8/ec2ifdown.8.gz
%doc %{_mandir}/man8/ec2ifscan.8.gz

%changelog
* Tue Oct 25 2022 Noah Meyerhans <nmeyerha@amazon.com> 1.7.3-1.amzn2
- Do not delete route-ethX files on ifup

* Thu Oct  6 2022 Noah Meyerhans <nmeyerha@amazon.com> 1.7.2-1.amzn2
- Update to upstream release 1.7.2
- Fix management of policy rules for IPv6 PD prefixes

* Fri Aug 12 2022 Noah Meyerhans <nmeyerha@amazon.com> 1.7.1-1.amzn2
- Update to upstream release 1.7.1
- On interface add, call systemctl directly rather than via SYSTEMD_WANTS

* Tue Jun 21 2022 Noah Meyerhans <nmeyerha@amazon.com> 1.7.0-1.amzn2
- Update to upstream release 1.7.0
- Add support for the EC2PROVISIONPFXIPS ifcfg setting
- Bug: Persistent naming rules are not generated for ENA devices #48
- Bug: 1.x: calls ec2ifup for vlan interfaces #49

* Thu Mar  3 2022 Noah Meyerhans <nmeyerha@amazon.com> 1.6.1-1
- Update to upstream release 1.6.1.
- Update dhclient dependency to require at least 4.2.5-77.amzn2.1.5,
  for /etc/dhcp/dhclient-enter-hooks.d/ support.

* Wed Jan 26 2022 Noah Meyerhans <nmeyerha@amazon.com> 1.6-1
- Update to upstream release 1.6.  Details at
  https://github.com/aws/amazon-ec2-net-utils/releases/tag/1.6

* Mon Dec 14 2020 Noah Meyerhans <nmeyerha@amazon.com> 1.5-1.amzn2
- Update Provides and Obsoletes to define an upgrade path from ec2-net-utils
- Use upstream Makefile during install
- Run upstream's test suite during check
- Support IP prefix delegation

* Mon Jul 13 2020 Frederick Lefebvre <fredlef@amazon.com> 1.4-2
- Provides ec2-net-utils for backward compatibility

* Wed Jun  3 2020 Frederick Lefebvre <fredlef@amazon.com> 1.4-1
- Rename package to match the name of the git repo
- Fix installation on non-systemd environments
- Support toggling default route through {INTERFACE} to main kernel route table [Prithvi Ramesh]

* Thu Mar  5 2020 Frederick Lefebvre <fredlef@amazon.com> 1.3-2
- Fix installation on non-systemd environments

* Wed Jan 15 2020 Frederick Lefebvre <fredlef@amazon.com> 1.3-1
- Add support for IMDSv2

* Wed Jan  8 2020 Frederick Lefebvre <fredlef@amazon.com> 1.2-2.1
- Explicitly set the dhcp timeout for ENIs

* Tue Jul 17 2018 Frederick Lefebvre <fredlef@amazon.com> 1.2-1.1
- Re-license under MIT

* Wed Jun 06 2018 Chad Miller <millchad@amazon.com>
- Loop to get correct MAC address from sysfs when it's
  all 00s

* Mon Dec 04 2017 Frederick Lefebvre <fredlef@amazon.com>
- Add systemd support

* Wed Sep 22 2010 Nathan Blackham <blackham@amazon.com>
- move to ec2-utils
- add udev code for symlinking xvd* devices to sd*

* Tue Sep 07 2010 Nathan Blackham <blackham@amazon.com>
- initial packaging of script as an rpm
