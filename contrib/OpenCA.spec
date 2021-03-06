# OpenCA RPM File
# (c) 2006 by Massimiliano Pala and OpenCA Team
# OpenCA Licensed Software

%define __find_requires %{nil}
%define debug_package %{nil}

# %define _unpackaged_files_terminate_build 0
# %define _missing_doc_files_terminate_build 0

# Basic Definitions
%define nobody    nobody
%define nogroup   nobody
%define httpd_usr apache
%define httpd_grp apache
%define openca_usr madwolf
%define openca_grp madwolf
%define httpd_fs_prefix /var/www

%define is_mandrake %(test -e /etc/mandrake-release && echo 1 || echo 0)
%define is_suse %(test -e /etc/SuSE-release && echo 1 || echo 0)
%define is_fedora %(test -e /etc/fedora-release && echo 1 || echo 0)
%define is_ubuntu %(test -e /usr/bin/ubuntu-bug && echo 1 || echo 0)

# %define is_centos  %(echo `rpm -qf /etc/redhat-release --qf '%{name} 0' 2> /dev /null | sed -e 's@centos-release@1@' | awk {'print $1'}`)
%define is_centos  %(echo `rpm -qf /etc/redhat-release --qf '%{name} 0' 2>/dev/null | sed -e 's@centos-release@1 1@' | sed -e 's@[^ ]*@@' | awk {'print $1'}`)

%define dist redhat
%define disttag rh

%if %is_mandrake
%define dist mandrake
%define disttag mdk
%endif

%if %is_suse
%define dist suse
%define disttag suse
%define nogroup nogroup
%define httpd_usr wwwwrun
%define httpd_grp nogroup
%endif

%if %is_fedora
%define dist fedora
%define disttag rhfc
%endif

%define distver %(release="`rpm -q --queryformat='%{VERSION}' %{dist}-release 2> /dev/null | tr . : | sed s/://g`" ; if test $? != 0 ; then release="" ; fi ; echo "$release")

%if %is_ubuntu
%define dist ubuntu
%define disttag ub
%define distver %(cat /etc/issue | grep -o -e '[0-9.]*' | sed -e 's/\\.//' )
%else
%if %is_centos
%define dist centos
%define disttag el
%endif
%endif


%define packer %(finger -lp `echo "$USER"` | head -n 1 | cut -d ' ' -f 2)

%define ver      	1.5.0
%define RELEASE 	1
%define rel     	%{?CUSTOM_RELEASE}%{!?CUSTOM_RELEASE:%RELEASE}
%define prefix   	/opt/openca
%define mand		/opt/openca/man
%define sslprefix	/usr
%define openssl_req 	0.9.7
%define openldap_req 	2.2
%define openca_tools_req 1.1.0
%define openca_common_req 1.1.0

%define working_release %rel.%{disttag}%{distver}

%if %is_ubuntu
%define working_release %rel.ubu
%endif

Summary: Open Source Certification Authority Software (PKI)
Name: openca-base
Version: %ver
Release: %{working_release}
License: OpenCA License (BSD Style)
Group: Security/PKI
Source: openca-base-%{ver}.tar.gz
Packager:  %packer
Vendor: OpenCA Labs
BuildRoot: /tmp/build-openca-base-1.5.0
URL: http://www.openca.org/projects/openca/
# Docdir: %{prefix}/doc
Prefix: %{prefix}
Requires: openssl >= %openssl_req openca-tools

%description
The OpenCA package implements a full featured Certification Authority
to issue and managed digital certificates.

%define openca_prefix	%{prefix}
%define openssl_prefix /usr

%package common
Summary: Basic Components for OpenCA
Group: Security/PKI
AutoReq: no
Requires: openssl >= %openssl_req openca-tools >= %openca_tools_req

%description common

%package online
Summary: OnLine PKI Components for OpenCA
Group: Security/PKI
Requires: openca-base-common >= %openca_common_req

%description online

%package offline
Summary: OffLine PKI Components for OpenCA
Group: Security/PKI
Requires: openca-base-common >= %openca_common_req

%description offline

%prep
#echo %_target
#echo %_target_alias
#echo %_target_cpu
#echo %_target_os
#echo %_target_vendor

echo Building %{name}-%{version}-%{release} in %{buildroot}

# %setup -q -n %{name}-%{version}

%setup

if [ ! -f configure ]; then
  CFLAGS="$RPM_OPT_FLAGS" ./autogen.sh
fi

./configure \
  --prefix=%{prefix} \
  --with-build-dir="%{buildroot}" \
  --with-openca-user=%{openca_usr} \
  --with-openca-group=%{openca_grp} \
  --with-ca-organization="OpenCA Labs" \
  --with-ldap-port=389 \
  --with-ldap-root="cn=Manager,o=OpenCA Labs" \
  --with-ldap-root-pwd="openca" \
  --with-openssl-prefix=%{openssl_prefix} \
  --enable-openscep \
  --with-db-type=mysql \
  --with-db-name=openca \
  --with-db-host=localhost \
  --with-db-port=3306 \
  --with-db-user=openca \
  --with-db-passwd="openca" \
  --with-service-mail-account="pki@openca.org" \
  --with-language=en_EN

%build

make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

# make install-common install-modules install-ca install-batch install-ldap install-pub install-ra install-scep install-node
DESTDIR="$RPM_BUILD_ROOT" make install-online install-offline

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files common
%defattr(-, -, -)

# %{openca_prefix}
%{openca_prefix}/bin/*
%{openca_prefix}/etc/openca/loa.xml
%{openca_prefix}/etc/openca/log.xml
%{openca_prefix}/etc/openca/token.xml
%{openca_prefix}/etc/openca/config.xml
%{openca_prefix}/etc/openca/ldap.xml.template
%{openca_prefix}/etc/openca/backup.xml.template
%{openca_prefix}/etc/openca/browser_req.xml.template
%{openca_prefix}/etc/openca/auth_browser_req.xml.template
%{openca_prefix}/etc/openca/server_req.xml.template
%{openca_prefix}/etc/openca/datasources.xml.template
%{openca_prefix}/etc/openca/configure_etc.sh
%{openca_prefix}/etc/init.d/openca
%{openca_prefix}/etc/openca/openca_start.template
%{openca_prefix}/etc/openca/openca_stop.template
%{openca_prefix}/etc/openca/utf8_latin1_selector.sh.template
%{openca_prefix}/etc/openca/bp/*
%{openca_prefix}/etc/openca/database/*
%{openca_prefix}/etc/openca/openssl/*
%{openca_prefix}/etc/openca/rbac/*
%{openca_prefix}/etc/openca/agreements/*
%{openca_prefix}/etc/openca/contrib/apache/*
%{openca_prefix}/etc/openca/contrib/openldap/*
%{openca_prefix}/lib/openca/*
%{openca_prefix}/var/openca/bp/*
%{openca_prefix}/var/openca/mail/*
%{openca_prefix}/var/openca/session/cookie/node
%{openca_prefix}/etc/openca/access_control/node.xml.template
%{openca_prefix}/etc/openca/servers/node.conf.template
%{openca_prefix}/etc/openca/includes/*
%{openca_prefix}/etc/openca/menus/node-menu.xml.template
%{httpd_fs_prefix}/html/pki/node/*
%{httpd_fs_prefix}/cgi-bin/pki/node/*

%defattr( -, %{httpd_usr}, %{httpd_grp})

%dir %{openca_prefix}/var/openca/log
%dir %{openca_prefix}/var/openca/crypto
%dir %{openca_prefix}/var/openca/crypto/cacerts
%dir %{openca_prefix}/var/openca/crypto/chain
%dir %{openca_prefix}/var/openca/crypto/certs
%dir %{openca_prefix}/var/openca/crypto/keys
%dir %{openca_prefix}/var/openca/crypto/reqs
%dir %{openca_prefix}/var/openca/tmp
%dir %{openca_prefix}/var/openca/db

%{openca_prefix}/var/openca/crypto/cacerts/*
%{openca_prefix}/var/openca/crypto/chain/*
%{openca_prefix}/var/openca/crypto/crlnumber
%{openca_prefix}/var/openca/crypto/index.txt
%{openca_prefix}/var/openca/crypto/index.txt.attr
%{openca_prefix}/var/openca/crypto/keys/bp_key.pem
%{openca_prefix}/var/openca/crypto/keys/keybackup_key.pem
%{openca_prefix}/var/openca/crypto/keys/log_key.pem
%{openca_prefix}/var/openca/crypto/serial
%{openca_prefix}/var/openca/log/*

%files offline
%defattr(-, -, -)

%{httpd_fs_prefix}/html/pki/ca/*
%{httpd_fs_prefix}/cgi-bin/pki/ca/*
%{openca_prefix}/var/openca/session/cookie/ca
%{openca_prefix}/etc/openca/access_control/ca.xml.template
%{openca_prefix}/etc/openca/servers/ca.conf.template
%{httpd_fs_prefix}/html/pki/batch/*
%{httpd_fs_prefix}/cgi-bin/pki/batch/*
%{openca_prefix}/var/openca/session/cookie/batch
%{openca_prefix}/etc/openca/access_control/batch.xml.template
%{openca_prefix}/etc/openca/servers/batch.conf.template
%{openca_prefix}/etc/openca/menus/ca-menu.xml.template
%{openca_prefix}/etc/openca/menus/batch-menu.xml.template

%files online
%defattr(-, -, -)

# LDAP
%{httpd_fs_prefix}/html/pki/ldap/*
%{httpd_fs_prefix}/cgi-bin/pki/ldap/*
%dir %{openca_prefix}/var/openca/session/cookie/ldap
%{openca_prefix}/etc/openca/access_control/ldap.xml.template
%{openca_prefix}/etc/openca/servers/ldap.conf.template
%{openca_prefix}/etc/openca/menus/ldap-menu.xml.template

# PUB
%{httpd_fs_prefix}/html/pki/pub/*
%{httpd_fs_prefix}/cgi-bin/pki/pub/*
%{openca_prefix}/var/openca/session/cookie/pub
%{openca_prefix}/etc/openca/access_control/pub.xml.template
%{openca_prefix}/etc/openca/servers/pub.conf.template
%{openca_prefix}/etc/openca/menus/pub-menu.xml.template

# RA
%{httpd_fs_prefix}/html/pki/ra/*
%{httpd_fs_prefix}/cgi-bin/pki/ra/*
%{openca_prefix}/var/openca/session/cookie/ra
%{openca_prefix}/etc/openca/access_control/ra.xml.template
%{openca_prefix}/etc/openca/servers/ra.conf.template
%{openca_prefix}/etc/openca/menus/ra-menu.xml.template

#SCEP
%{httpd_fs_prefix}/cgi-bin/pki/scep/*
%{openca_prefix}/var/openca/session/cookie/scep
%{openca_prefix}/etc/openca/access_control/scep.xml.template
%{openca_prefix}/etc/openca/servers/scep.conf.template

%post

%post offline

echo
echo "Entering POST Install Configuration of OpenCA..."
cd %{openca_prefix}/etc/openca && sh configure_etc.sh CA
echo "Done."

%post online

echo
echo "Entering POST Install Configuration of OpenCA..."
cd %{openca_prefix}/etc/openca && sh configure_etc.sh RA
echo "Done."

%post common

echo
echo -n "Copying startup script (openca) in init.d/ dir ... "
if [ -f "/etc/init.d/openca" ] ; then
	cp %{openca_prefix}/etc/init.d/openca /etc/init.d/openca.new
else
	cp %{openca_prefix}/etc/init.d/openca /etc/init.d/openca
fi
echo "Done."

%postun common

echo "Removing init.d/openca link ... "
rm -f /etc/init.d/openca
echo "Done."

echo -n "Removing empty directories ... "
rmdir %{prefix}/bin 2>/dev/null
rmdir %{openca_prefix}/lib/openca/perl-modules 2>/dev/null
rm -rf %{openca_prefix}/lib/openca/mails/* 2>/dev/null
rmdir %{openca_prefix}/lib/openca/mails 2>/dev/null
rmdir %{openca_prefix}/lib/openca 2>/dev/null
echo "Done."

echo
echo "Please check the %{prefix} directory for remaining files."
echo


%changelog
* Mon Oct 13 2008 R P Herrold <info@owlriver.com> 1.0.2-1
-add Centos test and support
* Mon Sep 18 2006 Massimiliano Pala <madwolf@openca.org>
-First Packaging for OpenCA-Base

