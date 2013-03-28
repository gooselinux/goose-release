%define debug_package %{nil}
%define product_family GoOSe Linux
%define release_name Pilgrim
%define base_release_version 6
%define full_release_version 6.0
#define beta Beta

Name:           goose-release
Version:        6.0
Release:        6.0.1.gl6
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
URL:            http://github.com/gooseproject/goose-release
Source0:        goose-release-6.0.tar.gz
BuildArch:      noarch

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
%%dist .gl%{full_release_version}
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
%config(noreplace) %attr(0644,root,root) /etc/yum.repos.d/goose-updates.repo
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/*
/etc/rpm/macros.dist

%changelog
* Wed Mar 27 2013 Clint Savage <herlo@gooseproject.org> - 6.0-6.0.1.gl6
- Following the SL model and removed the extra version cruft
- 6.0 is the version, 6.0.1 is the first version of 6.0-updates

* Thu May 17 2012 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.47.gl6
- Removed alpha reference from goose.repo

* Sun May 6 2012 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.46.gl6
- Updated goose.repo to use beta key

* Mon Apr 30 2012 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.45.gl6
- Added gpg keys to the tarball, enabled gpg checking in repo config

* Wed Apr 25 2012 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.44.gl6
- Updated to beta, changed goose.repo to match proper repository url

* Wed Mar 28 2012 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.43.gl6
- Removed RHEL specific firstboot components
- Obsoleted goose-release-server

* Tue Mar 27 2012 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.42.gl6
- Changed to goose-release from goose-release-server
- Added goose.repo and an temporary empty RPM-GPG-KEY-goose

* Sat Jul 10 2011 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.41.gl6
- Added %%rhel tag to macros.dist

* Thu Jun 9 2011 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.40.gl6
- Change dist from el6 to gl6

* Mon Jun 6 2011 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.39.gl6
- Rebuild for GoOSe Linux 6.0 #2

* Mon Jun 6 2011 Clint Savage <herlo@gooseproject.org> - 6-6.0.0.38.gl6
- Rebuild for GoOSe Linux 6.0

