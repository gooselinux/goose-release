%define debug_package %{nil}
%define product_family GoOSe Linux
%define variant_titlecase Server
%define variant_lowercase server
%define release_name Pilgrim
%define base_release_version 6
%define full_release_version 6.0
%define beta Alpha

Name:           goose-release
Version:        6
Release:        6.0.0.43.gl6
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
URL:            http://github.com/gooseproject/goose-release
Source0:        goose-release-6.tar.gz
BuildArch:	    noarch

Obsoletes:      rawhide-release redhat-release-as redhat-release-es 
Obsoletes:      redhat-release-ws redhat-release-de comps rpmdb-redhat 
Obsoletes:      fedora-release redhat-release-server goose-release-server 
Provides:       redhat-release system-release goose-release-server

%description
%{product_family} release files

%prep
%setup -q -n goose-release-6

%build
echo "Building %{product_family} %{full_release_version}%{?beta: %{beta}}"

%install
rm -rf $RPM_BUILD_ROOT

# create /etc
mkdir -p $RPM_BUILD_ROOT/etc

# create /etc/system-release and /etc/goose-release
echo "%{product_family} release %{full_release_version}%{?beta: %{beta}} (%{release_name})" > $RPM_BUILD_ROOT/etc/goose-release
ln -s goose-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s goose-release $RPM_BUILD_ROOT/etc/system-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:goose:linux:%{version}:%{?beta:beta}%{!?beta:GA}" | tr [A-Z] [a-z] > $RPM_BUILD_ROOT/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
cp $RPM_BUILD_ROOT/etc/goose-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m" >> $RPM_BUILD_ROOT/etc/issue
cp $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue

# copy GPG keys
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file $RPM_BUILD_ROOT/etc/pki/rpm-gpg
done

install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
for file in goose*repo ; do
  install -m 644 $file $RPM_BUILD_ROOT/etc/yum.repos.d
done

# set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT/etc/rpm
cat >> $RPM_BUILD_ROOT/etc/rpm/macros.dist << EOF
# dist macros.

%%rhel %{base_release_version}
%%goose %{base_release_version}
%%dist .gl%{base_release_version}
%%gl%{base_release_version} 1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- firstboot
if [ -f /usr/share/firstboot/modules/additional_cds.py ] ; then
  rm -f /usr/share/firstboot/modules/additional_cds.py*
fi
if [ -f /usr/share/firstboot/modules/eula.py ] ; then
  rm -f /usr/share/firstboot/modules/eula.py*
fi
%triggerin -- rhn-setup-gnome
if [ -f /usr/share/firstboot/modules/rhn_register.py ] ; then
  rm -f /usr/share/firstboot/modules/rhn_register.py*
fi

%files
%defattr(-,root,root)
%doc GPL autorun-template
%attr(0644,root,root) /etc/goose-release
/etc/system-release 
/etc/redhat-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%config(noreplace) %attr(0644,root,root) /etc/yum.repos.d/goose.repo
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*
/etc/rpm/macros.dist

%changelog
* Wed Mar 28 2012 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.43
- Removed RHEL specific firstboot components
- Obsoleted goose-release-server

* Tue Mar 27 2012 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.42
- Changed to goose-release from goose-release-server
- Added goose.repo and an temporary empty RPM-GPG-KEY-goose

* Sat Jul 10 2011 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.41
- Added %%rhel tag to macros.dist

* Thu Jun 9 2011 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.40
- Change dist from el6 to gl6

* Mon Jun 6 2011 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.39
- Rebuild for GoOSe Linux 6.0 #2

* Mon Jun 6 2011 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.38
- Rebuild for GoOSe Linux 6.0

* Fri Sep  3 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.37
- Update EULA
- Resolves: rhbz#591512

* Tue Aug 31 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.36
- Remove beta text
- Update EULA
- Resolves: rhbz#622251, rhbz#591512

* Mon Aug 16 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.35
- Bump for GA
- Resolves: rhbz#622251

* Mon Jul 26 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.91-6.0.0.34
- Update yum repos for GA

* Tue Jun 29 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.91-6.0.0.33
- Update GPL to match standard text

* Tue Jun 29 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.91-6.0.0.32
- Bump version for post-Beta2

* Wed Jun 16 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.90-6.0.0.32
- Fix logic for AddOn repos

* Tue Jun 15 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.90-6.0.0.31
- Only include the AddOn repos in the appropriate arches/variants
- Update the Beta GPG key locations

* Tue Jun  8 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.90-6.0.0.29
- Combine GPG keys

* Fri May 28 2010 Dennis Gregorovic <dgregor@redhat.com> - 5.90-6.0.0.28
- Use a different version value so as to not conflict with GA

* Fri May 28 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.28
- Include the variant in the version field (needed for RHN)
- Update repos for Beta 2

* Mon Apr 26 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.27
- Make 'Beta' lowercase in the cpe
- Provide system-release

* Wed Mar 31 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.25
- Temporarily disable beta repos

* Mon Mar 29 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.24
- Add beta debuginfo repos

* Mon Mar 29 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.23
- Enable yum repo for Beta

* Wed Mar 10 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.21
- Update yum repos for Beta 1

* Fri Feb  5 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.20
- Use the %%{?dist} macro

* Wed Feb  3 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.19
- Mark the yum repos as configuration files

* Tue Feb  2 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.18
- Use %setup -q to keeep rpmlint happy

* Thu Jan 28 2010 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.17
- Bump for Beta

* Tue Nov 17 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.16
- Fix newline issue in RPM-GPG-KEY-redhat-beta-2
- spec file cleanup

* Thu Oct  22 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.15
- Spec cleanup (dmach@redhat.com)
- Add the beta-2 and release-2 keys
- Rename the older keys
- Comment out eula.py code until it gets cleaned up

* Mon Sep 21 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.14
- Fix typo in cpe name

* Fri Sep 18 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.13
- Fix the cpe name

* Thu Sep 17 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.12
- Update the release name

* Thu Sep 17 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.11
- Add system-release-cpe

* Tue Sep 15 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.10
- Add the 'el6' macro

* Tue Sep  1 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.9
- Bump for rebuild

* Tue Aug 11 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.8
- Indicate Alpha instead of Beta

* Wed Jun 24 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.7
- Updated eula.py

* Tue Jun 23 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.6
- Add eula.py back

* Mon Jun 15 2009 Dennis Gregorovic <dgregor@redhat.com> - 6-6.0.0.5
- add /etc/system-release
- some minor cleanup

* Fri Jun  5 2009 Dennis Gregorovic <dgregor@redhat.com> - 6Server-6.0.0.4
- bump for rebuild

* Fri Jun  5 2009 Dennis Gregorovic <dgregor@redhat.com> - 6Server-6.0.0.3
- Drop firstboot files as they conflict with the firstboot package

* Wed Jun  3 2009 Mike McLean <mikem@redhat.com> - 6Server-6.0.0.1
- initial build for version 6
