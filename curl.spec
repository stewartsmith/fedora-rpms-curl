Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl
Version: 7.75.0
Release: 2%{?dist}
License: MIT
Source: https://curl.se/download/%{name}-%{version}.tar.xz

# patch making libcurl multilib ready
Patch101: 0101-curl-7.32.0-multilib.patch

# prevent configure script from discarding -g in CFLAGS (#496778)
Patch102: 0102-curl-7.36.0-debug.patch

# use localhost6 instead of ip6-localhost in the curl test-suite
Patch104: 0104-curl-7.73.0-localhost6.patch

# prevent valgrind from reporting false positives on x86_64
Patch105: 0105-curl-7.63.0-lib1560-valgrind.patch

Provides: curl-full = %{version}-%{release}
Provides: webclient
URL: https://curl.se/
BuildRequires: automake
BuildRequires: brotli-devel
BuildRequires: coreutils
BuildRequires: gcc
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn2-devel
BuildRequires: libmetalink-devel
BuildRequires: libnghttp2-devel
BuildRequires: libpsl-devel
BuildRequires: libssh-devel
BuildRequires: libtool
BuildRequires: make
BuildRequires: openldap-devel
BuildRequires: openssh-clients
BuildRequires: openssh-server
BuildRequires: openssl-devel
BuildRequires: perl-interpreter
BuildRequires: pkgconfig
BuildRequires: python-unversioned-command
BuildRequires: python3-devel
BuildRequires: sed
BuildRequires: zlib-devel

# needed to compress content of tool_hugehelp.c after changing curl.1 man page
BuildRequires: perl(IO::Compress::Gzip)

# needed for generation of shell completions
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Pod::Usage)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)

# gnutls-serv is used by the upstream test-suite
BuildRequires: gnutls-utils

# hostname(1) is used by the test-suite but it is missing in armv7hl buildroot
BuildRequires: hostname

# nghttpx (an HTTP/2 proxy) is used by the upstream test-suite
BuildRequires: nghttp2

# perl modules used in the test suite
BuildRequires: perl(Cwd)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IPC::Open2)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(Time::Local)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(vars)

%if 0%{?fedora}
# needed for upstream test 1451
BuildRequires: python3-impacket
%endif

# The test-suite runs automatically through valgrind if valgrind is available
# on the system.  By not installing valgrind into mock's chroot, we disable
# this feature for production builds on architectures where valgrind is known
# to be less reliable, in order to avoid unnecessary build failures (see RHBZ
# #810992, #816175, and #886891).  Nevertheless developers are free to install
# valgrind manually to improve test coverage on any architecture.
%ifarch x86_64
BuildRequires: valgrind
%endif

# stunnel is used by upstream tests but it does not seem to work reliably
# on s390x and occasionally breaks some tests (mainly 1561 and 1562)
%ifnarch s390x
BuildRequires: stunnel
%endif

# using an older version of libcurl could result in CURLE_UNKNOWN_OPTION
Requires: libcurl%{?_isa} >= %{version}-%{release}

# require at least the version of libpsl that we were built against,
# to ensure that we have the necessary symbols available (#1631804)
%global libpsl_version %(pkg-config --modversion libpsl 2>/dev/null || echo 0)

# require at least the version of libssh that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%global libssh_version %(pkg-config --modversion libssh 2>/dev/null || echo 0)

# require at least the version of openssl-libs that we were built against,
# to ensure that we have the necessary symbols available (#1462184, #1462211)
%global openssl_version %(pkg-config --modversion openssl 2>/dev/null || echo 0)

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks. 

%package -n libcurl
Summary: A library for getting files from web servers
Requires: libpsl%{?_isa} >= %{libpsl_version}
Requires: libssh%{?_isa} >= %{libssh_version}
Requires: openssl-libs%{?_isa} >= 1:%{openssl_version}
Provides: libcurl-full = %{version}-%{release}
Provides: libcurl-full%{?_isa} = %{version}-%{release}

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, http proxy tunneling and more.

%package -n libcurl-devel
Summary: Files needed for building applications with libcurl
Requires: libcurl%{?_isa} = %{version}-%{release}

Provides: curl-devel = %{version}-%{release}
Provides: curl-devel%{?_isa} = %{version}-%{release}
Obsoletes: curl-devel < %{version}-%{release}

%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs which use the libcurl library. It contains the API
documentation of the library, too.

%package -n curl-minimal
Summary: Conservatively configured build of curl for minimal installations
Provides: curl = %{version}-%{release}
Conflicts: curl
RemovePathPostfixes: .minimal

# using an older version of libcurl could result in CURLE_UNKNOWN_OPTION
Requires: libcurl%{?_isa} >= %{version}-%{release}

%description -n curl-minimal
This is a replacement of the 'curl' package for minimal installations.  It
comes with a limited set of features compared to the 'curl' package.  On the
other hand, the package is smaller and requires fewer run-time dependencies to
be installed.

%package -n libcurl-minimal
Summary: Conservatively configured build of libcurl for minimal installations
Requires: openssl-libs%{?_isa} >= 1:%{openssl_version}
Provides: libcurl = %{version}-%{release}
Provides: libcurl%{?_isa} = %{version}-%{release}
Conflicts: libcurl%{?_isa}
RemovePathPostfixes: .minimal
# needed for RemovePathPostfixes to work with shared libraries
%undefine __brp_ldconfig

%description -n libcurl-minimal
This is a replacement of the 'libcurl' package for minimal installations.  It
comes with a limited set of features compared to the 'libcurl' package.  On the
other hand, the package is smaller and requires fewer run-time dependencies to
be installed.

%prep
%setup -q

# upstream patches

# Fedora patches
%patch101 -p1
%patch102 -p1
%patch104 -p1
%patch105 -p1

# regenerate the configure script and Makefile.in files
autoreconf -fiv

# disable test 1112 (#565305), test 1455 (occasionally fails with 'bind failed
# with errno 98: Address already in use' in Koji environment), and test 1801
# <https://github.com/bagder/curl/commit/21e82bd6#commitcomment-12226582>
printf "1112\n1455\n1801\n" >> tests/data/DISABLED

# disable test 1319 on ppc64 (server times out)
%ifarch ppc64
echo "1319" >> tests/data/DISABLED
%endif

# temporarily disable test 582 on s390x (client times out)
%ifarch s390x
echo "582" >> tests/data/DISABLED
%endif

# temporarily disable tests 702 703 716 on armv7hl (#1829180)
%ifarch armv7hl
printf "702\n703\n716\n" >> tests/data/DISABLED
%endif

# adapt test 323 for updated OpenSSL
sed -e 's/^35$/35,52/' -i tests/data/test323

%build
mkdir build-{full,minimal}
export common_configure_opts=" \
    --cache-file=../config.cache \
    --disable-static \
    --enable-symbol-hiding \
    --enable-ipv6 \
    --enable-threaded-resolver \
    --with-gssapi \
    --with-nghttp2 \
    --with-ssl --with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt"

%global _configure ../configure

# configure minimal build
(
    cd build-minimal
    %configure $common_configure_opts \
        --disable-ldap \
        --disable-ldaps \
        --disable-manual \
        --without-brotli \
        --without-libidn2 \
        --without-libmetalink \
        --without-libpsl \
        --without-libssh
)

# configure full build
(
    cd build-full
    %configure $common_configure_opts \
        --enable-ldap \
        --enable-ldaps \
        --enable-manual \
        --with-brotli \
        --with-libidn2 \
        --with-libmetalink \
        --with-libpsl \
        --with-libssh
)

# avoid using rpath
sed -e 's/^runpath_var=.*/runpath_var=/' \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/' \
    -i build-{full,minimal}/libtool

%make_build V=1 -C build-minimal
%make_build V=1 -C build-full

%check
# we have to override LD_LIBRARY_PATH because we eliminated rpath
LD_LIBRARY_PATH="${PWD}/build-full/lib/.libs"
export LD_LIBRARY_PATH

# compile upstream test-cases
cd build-full/tests
%make_build V=1

# relax crypto policy for the test-suite to make it pass again (#1610888)
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=XXX
export OPENSSL_CONF=

# run the upstream test-suite
srcdir=../../tests perl -I../../tests ../../tests/runtests.pl -a -p -v '!flaky'

%install
# install and rename the library that will be packaged as libcurl-minimal
%make_install -C build-minimal/lib
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.{la,so}
for i in ${RPM_BUILD_ROOT}%{_libdir}/*; do
    mv -v $i $i.minimal
done

# install and rename the executable that will be packaged as curl-minimal
%make_install -C build-minimal/src
mv -v ${RPM_BUILD_ROOT}%{_bindir}/curl{,.minimal}

# install libcurl.m4
install -d $RPM_BUILD_ROOT%{_datadir}/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal

# install the executable and library that will be packaged as curl and libcurl
cd build-full
%make_install

# install zsh completion for curl
# (we have to override LD_LIBRARY_PATH because we eliminated rpath)
LD_LIBRARY_PATH="$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH" \
    %make_install -C scripts

# do not install /usr/share/fish/completions/curl.fish which is also installed
# by fish-3.0.2-1.module_f31+3716+57207597 and would trigger a conflict
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/fish

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la

%ldconfig_scriptlets -n libcurl

%ldconfig_scriptlets -n libcurl-minimal

%files
%doc CHANGES
%doc README
%doc docs/BUGS.md
%doc docs/FAQ
%doc docs/FEATURES.md
%doc docs/TODO
%doc docs/TheArtOfHttpScripting.md
%{_bindir}/curl
%{_mandir}/man1/curl.1*
%{_datadir}/zsh

%files -n libcurl
%license COPYING
%{_libdir}/libcurl.so.4
%{_libdir}/libcurl.so.4.[0-9].[0-9]

%files -n libcurl-devel
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS.md
%doc docs/CONTRIBUTE.md docs/libcurl/ABI.md
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

%files -n curl-minimal
%{_bindir}/curl.minimal
%{_mandir}/man1/curl.1*

%files -n libcurl-minimal
%license COPYING
%{_libdir}/libcurl.so.4.minimal
%{_libdir}/libcurl.so.4.[0-9].[0-9].minimal

%changelog
* Tue Feb 23 2021 Kamil Dudka <kdudka@redhat.com> - 7.75.0-2
- build-require python3-impacket only on Fedora

* Wed Feb 03 2021 Kamil Dudka <kdudka@redhat.com> - 7.75.0-1
- new upstream release

* Tue Jan 26 2021 Kamil Dudka <kdudka@redhat.com> - 7.74.0-4
- do not use stunnel for tests on s390x builds to avoid spurious failures

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.74.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Kamil Dudka <kdudka@redhat.com> - 7.74.0-2
- do not rewrite shebangs in test-suite to use python3 explicitly

* Wed Dec 09 2020 Kamil Dudka <kdudka@redhat.com> - 7.74.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2020-8286 - curl: Inferior OCSP verification
    CVE-2020-8285 - libcurl: FTP wildcard stack overflow
    CVE-2020-8284 - curl: trusting FTP PASV responses

* Wed Oct 14 2020 Kamil Dudka <kdudka@redhat.com> - 7.73.0-2
- prevent upstream test 1451 from being skipped

* Wed Oct 14 2020 Kamil Dudka <kdudka@redhat.com> - 7.73.0-1
- new upstream release

* Thu Sep 10 2020 Jinoh Kang <aurhb20@protonmail.ch> - 7.72.0-2
- fix multiarch conflicts in libcurl-minimal (#1877671)

* Wed Aug 19 2020 Kamil Dudka <kdudka@redhat.com> - 7.72.0-1
- new upstream release, which fixes the following vulnerability
    CVE-2020-8231 - libcurl: wrong connect-only connection

* Thu Aug 06 2020 Kamil Dudka <kdudka@redhat.com> - 7.71.1-5
- setopt: unset NOBODY switches to GET if still HEAD

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.71.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 7.71.1-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jul 03 2020 Kamil Dudka <kdudka@redhat.com> - 7.71.1-2
- curl: make the --krb option work again (#1833193)

* Wed Jul 01 2020 Kamil Dudka <kdudka@redhat.com> - 7.71.1-1
- new upstream release

* Wed Jun 24 2020 Kamil Dudka <kdudka@redhat.com> - 7.71.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2020-8169 - curl: Partial password leak over DNS on HTTP redirect
    CVE-2020-8177 - curl: overwrite local file with -J

* Wed Apr 29 2020 Kamil Dudka <kdudka@redhat.com> - 7.70.0-1
- new upstream release

* Mon Apr 20 2020 Kamil Dudka <kdudka@redhat.com> - 7.69.1-3
- SSH: use new ECDSA key types to check known hosts (#1824926)

* Fri Apr 17 2020 Tom Stellard <tstellar@redhat.com> - 7.69.1-2
- Prevent discarding of -g when compiling with clang

* Wed Mar 11 2020 Kamil Dudka <kdudka@redhat.com> - 7.69.1-1
- new upstream release

* Mon Mar 09 2020 Kamil Dudka <kdudka@redhat.com> - 7.69.0-2
- make Flatpak work again (#1810989)

* Wed Mar 04 2020 Kamil Dudka <kdudka@redhat.com> - 7.69.0-1
- new upstream release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.68.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Kamil Dudka <kdudka@redhat.com> - 7.68.0-1
- new upstream release

* Thu Nov 14 2019 Kamil Dudka <kdudka@redhat.com> - 7.67.0-2
- fix infinite loop on upload using a glob (#1771025)

* Wed Nov 06 2019 Kamil Dudka <kdudka@redhat.com> - 7.67.0-1
- new upstream release

* Wed Sep 11 2019 Kamil Dudka <kdudka@redhat.com> - 7.66.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2019-5481 - double free due to subsequent call of realloc()
    CVE-2019-5482 - heap buffer overflow in function tftp_receive_packet()

* Tue Aug 27 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.3-4
- avoid reporting spurious error in the HTTP2 framing layer (#1690971)

* Thu Aug 01 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.3-3
- improve handling of gss_init_sec_context() failures

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.65.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 Paul Howarth <paul@city-fan.org> - 7.65.3-1
- new upstream release

* Wed Jul 17 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.2-1
- new upstream release

* Wed Jun 05 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.1-1
- new upstream release

* Thu May 30 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.0-2
- fix spurious timeout events with speed-limit (#1714893)

* Wed May 22 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2019-5436 - TFTP receive buffer overflow
    CVE-2019-5435 - integer overflows in curl_url_set()

* Thu May 09 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.1-2
- do not treat failure of gss_init_sec_context() with --negotiate as fatal

* Wed Mar 27 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.1-1
- new upstream release

* Mon Mar 25 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-6
- remove verbose "Expire in" ... messages (#1690971)

* Thu Mar 21 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-5
- avoid spurious "Could not resolve host: [host name]" error messages

* Wed Feb 27 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-4
- fix NULL dereference if flushing cookies with no CookieInfo set (#1683676)

* Mon Feb 25 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-3
- prevent NetworkManager from leaking file descriptors (#1680198)

* Mon Feb 11 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-2
- make zsh completion work again

* Wed Feb 06 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2019-3823 - SMTP end-of-response out-of-bounds read
    CVE-2019-3822 - NTLMv2 type-3 header stack buffer overflow
    CVE-2018-16890 - NTLM type-2 out-of-bounds buffer read

* Mon Feb 04 2019 Kamil Dudka <kdudka@redhat.com> - 7.63.0-7
- prevent valgrind from reporting false positives on x86_64

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.63.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Kamil Dudka <kdudka@redhat.com> - 7.63.0-5
- xattr: strip credentials from any URL that is stored (CVE-2018-20483)

* Fri Jan 04 2019 Kamil Dudka <kdudka@redhat.com> - 7.63.0-4
- replace 0105-curl-7.63.0-libstubgss-ldadd.patch by upstream patch

* Wed Dec 19 2018 Kamil Dudka <kdudka@redhat.com> - 7.63.0-3
- curl -J: do not append to the destination file (#1658574)

* Fri Dec 14 2018 Kamil Dudka <kdudka@redhat.com> - 7.63.0-2
- revert an upstream commit that broke `fedpkg new-sources` (#1659329)

* Wed Dec 12 2018 Kamil Dudka <kdudka@redhat.com> - 7.63.0-1
- new upstream release

* Wed Oct 31 2018 Kamil Dudka <kdudka@redhat.com> - 7.62.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2018-16839 - SASL password overflow via integer overflow
    CVE-2018-16840 - use-after-free in handle close
    CVE-2018-16842 - warning message out-of-buffer read

* Thu Oct 11 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.1-3
- enable TLS 1.3 post-handshake auth in OpenSSL
- update the documentation of --tlsv1.0 in curl(1) man page

* Thu Oct 04 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.1-2
- enforce versioned libpsl dependency for libcurl (#1631804)
- test320: update expected output for gnutls-3.6.4
- drop 0105-curl-7.61.0-tests-ssh-keygen.patch no longer needed (#1622594)

* Wed Sep 05 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.1-1
- new upstream release, which fixes the following vulnerability
    CVE-2018-14618 - NTLM password overflow via integer overflow

* Tue Sep 04 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-8
- make the --tls13-ciphers option work

* Mon Aug 27 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-7
- tests: make ssh-keygen always produce PEM format (#1622594)

* Wed Aug 15 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-6
- scp/sftp: fix infinite connect loop on invalid private key (#1595135)

* Thu Aug 09 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-5
- ssl: set engine implicitly when a PKCS#11 URI is provided (#1219544)

* Tue Aug 07 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-4
- relax crypto policy for the test-suite to make it pass again (#1610888)

* Tue Jul 31 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-3
- disable flaky test 1900, which covers deprecated HTTP pipelining
- adapt test 323 for updated OpenSSL

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.61.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-1
- new upstream release, which fixes the following vulnerability
    CVE-2018-0500 - SMTP send heap buffer overflow

* Tue Jul 10 2018 Kamil Dudka <kdudka@redhat.com> - 7.60.0-3
- enable support for brotli compression in libcurl-full

* Wed Jul 04 2018 Kamil Dudka <kdudka@redhat.com> - 7.60.0-2
- do not hard-wire path of the Python 3 interpreter

* Wed May 16 2018 Kamil Dudka <kdudka@redhat.com> - 7.60.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2018-1000300 - FTP shutdown response buffer overflow
    CVE-2018-1000301 - RTSP bad headers buffer over-read

* Thu Mar 15 2018 Kamil Dudka <kdudka@redhat.com> - 7.59.0-3
- make the test-suite use Python 3

* Wed Mar 14 2018 Kamil Dudka <kdudka@redhat.com> - 7.59.0-2
- ftp: fix typo in recursive callback detection for seeking

* Wed Mar 14 2018 Kamil Dudka <kdudka@redhat.com> - 7.59.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2018-1000120 - FTP path trickery leads to NIL byte out of bounds write
    CVE-2018-1000121 - LDAP NULL pointer dereference
    CVE-2018-1000122 - RTSP RTP buffer over-read

* Mon Mar 12 2018 Kamil Dudka <kdudka@redhat.com> - 7.58.0-8
- http2: mark the connection for close on GOAWAY

* Mon Feb 19 2018 Paul Howarth <paul@city-fan.org> - 7.58.0-7
- Add explicity-used build requirements
- Fix libcurl soname version number in %%files list to avoid accidental soname
  bumps

* Thu Feb 15 2018 Paul Howarth <paul@city-fan.org> - 7.58.0-6
- switch to %%ldconfig_scriptlets
- drop legacy BuildRoot: and Group: tags
- enforce versioned libssh dependency for libcurl

* Tue Feb 13 2018 Kamil Dudka <kdudka@redhat.com> - 7.58.0-5
- drop temporary workaround for #1540549

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.58.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Kamil Dudka <kdudka@redhat.com> - 7.58.0-3
- temporarily work around internal compiler error on x86_64 (#1540549)
- disable brp-ldconfig to make RemovePathPostfixes work with shared libs again

* Wed Jan 24 2018 Andreas Schneider <asn@redhat.com> - 7.58.0-2
- use libssh (instead of libssh2) to implement SCP/SFTP in libcurl (#1531483)

* Wed Jan 24 2018 Kamil Dudka <kdudka@redhat.com> - 7.58.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2018-1000005 - curl: HTTP/2 trailer out-of-bounds read
    CVE-2018-1000007 - curl: HTTP authentication leak in redirects

* Wed Nov 29 2017 Kamil Dudka <kdudka@redhat.com> - 7.57.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2017-8816 - curl: NTLM buffer overflow via integer overflow
    CVE-2017-8817 - curl: FTP wildcard out of bounds read
    CVE-2017-8818 - curl: SSL out of buffer access

* Mon Oct 23 2017 Kamil Dudka <kdudka@redhat.com> - 7.56.1-1
- new upstream release (fixes CVE-2017-1000257)

* Wed Oct 04 2017 Kamil Dudka <kdudka@redhat.com> - 7.56.0-1
- new upstream release (fixes CVE-2017-1000254)

* Mon Aug 28 2017 Kamil Dudka <kdudka@redhat.com> - 7.55.1-5
- apply the patch for the previous commit and fix its name (#1485702)

* Mon Aug 28 2017 Bastien Nocera <bnocera@redhat.com> - 7.55.1-4
- Fix NetworkManager connectivity check not working (#1485702)

* Tue Aug 22 2017 Kamil Dudka <kdudka@redhat.com> 7.55.1-3
- utilize system wide crypto policies for TLS (#1483972)

* Tue Aug 15 2017 Kamil Dudka <kdudka@redhat.com> 7.55.1-2
- make zsh completion work again

* Mon Aug 14 2017 Kamil Dudka <kdudka@redhat.com> 7.55.1-1
- new upstream release

* Wed Aug 09 2017 Kamil Dudka <kdudka@redhat.com> 7.55.0-1
- drop multilib fix for libcurl header files no longer needed
- new upstream release, which fixes the following vulnerabilities
    CVE-2017-1000099 - FILE buffer read out of bounds
    CVE-2017-1000100 - TFTP sends more than buffer size
    CVE-2017-1000101 - URL globbing out of bounds read

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.54.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Fri Jul 28 2017 Florian Weimer <fweimer@redhat.com> - 7.54.1-7
- Rebuild with fixed binutils (#1475636)

* Fri Jul 28 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7.54.1-6
- Enable separate debuginfo back

* Thu Jul 27 2017 Kamil Dudka <kdudka@redhat.com> 7.54.1-5
- rebuild to fix broken linkage of cmake on ppc64le

* Wed Jul 26 2017 Kamil Dudka <kdudka@redhat.com> 7.54.1-4
- avoid build failure caused broken RPM code that produces debuginfo packages

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.54.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Kamil Dudka <kdudka@redhat.com> 7.54.1-2
- enforce versioned openssl-libs dependency for libcurl (#1462184)

* Wed Jun 14 2017 Kamil Dudka <kdudka@redhat.com> 7.54.1-1
- new upstream release

* Tue May 16 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-5
- add *-full provides for curl and libcurl to make them explicitly installable

* Thu May 04 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-4
- make curl-minimal require a new enough version of libcurl

* Thu Apr 27 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-3
- switch the TLS backend back to OpenSSL (#1445153)

* Tue Apr 25 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-2
- nss: use libnssckbi.so as the default source of trust
- nss: do not leak PKCS #11 slot while loading a key (#1444860)

* Thu Apr 20 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-1
- new upstream release (fixes CVE-2017-7468)

* Thu Apr 13 2017 Paul Howarth <paul@city-fan.org> 7.53.1-7
- add %%post and %%postun scriptlets for libcurl-minimal
- libcurl-minimal provides both libcurl and libcurl%%{?_isa}
- remove some legacy spec file cruft

* Wed Apr 12 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-6
- provide (lib)curl-minimal subpackages with lightweight build of (lib)curl

* Mon Apr 10 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-5
- disable upstream test 2033 (flaky test for HTTP/1 pipelining)

* Fri Apr 07 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-4
- fix out of bounds read in curl --write-out (CVE-2017-7407)

* Mon Mar 06 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-3
- make the dependency on nss-pem arch-specific (#1428550)

* Thu Mar 02 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-2
- re-enable valgrind on ix86 because sqlite is fixed (#1428286)

* Fri Feb 24 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-1
- new upstream release

* Wed Feb 22 2017 Kamil Dudka <kdudka@redhat.com> 7.53.0-1
- do not use valgrind on ix86 until sqlite is rebuilt by patched GCC (#1423434)
- new upstream release (fixes CVE-2017-2629)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.52.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Kamil Dudka <kdudka@redhat.com> 7.52.1-1
- new upstream release (fixes CVE-2016-9586)

* Mon Nov 21 2016 Kamil Dudka <kdudka@redhat.com> 7.51.0-3
- map CURL_SSLVERSION_DEFAULT to NSS default, add support for TLS 1.3 (#1396719)

* Tue Nov 15 2016 Kamil Dudka <kdudka@redhat.com> 7.51.0-2
- stricter host name checking for file:// URLs
- ssh: check md5 fingerprints case insensitively

* Wed Nov 02 2016 Kamil Dudka <kdudka@redhat.com> 7.51.0-1
- temporarily disable failing libidn2 test-cases
- new upstream release, which fixes the following vulnerabilities
    CVE-2016-8615 - Cookie injection for other servers
    CVE-2016-8616 - Case insensitive password comparison
    CVE-2016-8617 - Out-of-bounds write via unchecked multiplication
    CVE-2016-8618 - Double-free in curl_maprintf
    CVE-2016-8619 - Double-free in krb5 code
    CVE-2016-8620 - Glob parser write/read out of bounds
    CVE-2016-8621 - curl_getdate out-of-bounds read
    CVE-2016-8622 - URL unescape heap overflow via integer truncation
    CVE-2016-8623 - Use-after-free via shared cookies
    CVE-2016-8624 - Invalid URL parsing with '#'
    CVE-2016-8625 - IDNA 2003 makes curl use wrong host

* Thu Oct 20 2016 Kamil Dudka <kdudka@redhat.com> 7.50.3-3
- drop 0103-curl-7.50.0-stunnel.patch no longer needed

* Fri Oct 07 2016 Kamil Dudka <kdudka@redhat.com> 7.50.3-2
- use the just built version of libcurl while generating zsh completion

* Wed Sep 14 2016 Kamil Dudka <kdudka@redhat.com> 7.50.3-1
- new upstream release (fixes CVE-2016-7167)

* Wed Sep 07 2016 Kamil Dudka <kdudka@redhat.com> 7.50.2-1
- new upstream release

* Fri Aug 26 2016 Kamil Dudka <kdudka@redhat.com> 7.50.1-2
- work around race condition in PK11_FindSlotByName()
- fix incorrect use of a previously loaded certificate from file
  (related to CVE-2016-5420)

* Wed Aug 03 2016 Kamil Dudka <kdudka@redhat.com> 7.50.1-1
- new upstream release (fixes CVE-2016-5419, CVE-2016-5420, and CVE-2016-5421)

* Tue Jul 26 2016 Kamil Dudka <kdudka@redhat.com> 7.50.0-2
- run HTTP/2 tests on all architectures (#1360319 now worked around in nghttp2)

* Thu Jul 21 2016 Kamil Dudka <kdudka@redhat.com> 7.50.0-1
- run HTTP/2 tests only on Intel for now to work around #1358845
- require nss-pem because it is no longer included in the nss package (#1347336)
- fix HTTPS and FTPS tests (work around stunnel bug #1358810)
- new upstream release

* Fri Jun 17 2016 Kamil Dudka <kdudka@redhat.com> 7.49.1-3
- use multilib-rpm-config to install arch-dependent header files

* Fri Jun 03 2016 Kamil Dudka <kdudka@redhat.com> 7.49.1-2
- fix SIGSEGV of the curl tool while parsing URL with too many globs (#1340757)

* Mon May 30 2016 Kamil Dudka <kdudka@redhat.com> 7.49.1-1
- new upstream release

* Wed May 18 2016 Kamil Dudka <kdudka@redhat.com> 7.49.0-1
- new upstream release

* Wed Mar 23 2016 Kamil Dudka <kdudka@redhat.com> 7.48.0-1
- new upstream release

* Wed Mar 02 2016 Kamil Dudka <kdudka@redhat.com> 7.47.1-4
- do not refuse cookies for localhost (#1308791)

* Wed Feb 17 2016 Kamil Dudka <kdudka@redhat.com> 7.47.1-3
- make SCP and SFTP test-cases work with up2date OpenSSH

* Wed Feb 10 2016 Kamil Dudka <kdudka@redhat.com> 7.47.1-2
- enable support for Public Suffix List (#1305701)

* Mon Feb 08 2016 Kamil Dudka <kdudka@redhat.com> 7.47.1-1
- new upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.47.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Kamil Dudka <kdudka@redhat.com> 7.47.0-1
- new upstream release (fixes CVE-2016-0755)

* Fri Dec  4 2015 Kamil Dudka <kdudka@redhat.com> 7.46.0-2
- own /usr/share/zsh/site-functions instead of requiring zsh (#1288529)

* Wed Dec  2 2015 Kamil Dudka <kdudka@redhat.com> 7.46.0-1
- disable silent builds (suggested by Paul Howarth)
- use default port numbers when running the upstream test-suite
- install zsh completion script
- new upstream release

* Wed Oct  7 2015 Paul Howarth <paul@city-fan.org> 7.45.0-1
- new upstream release
- drop %%defattr, redundant since rpm 4.4

* Fri Sep 18 2015 Kamil Dudka <kdudka@redhat.com> 7.44.0-2
- prevent NSS from incorrectly re-using a session (#1104597)

* Wed Aug 12 2015 Kamil Dudka <kdudka@redhat.com> 7.44.0-1
- new upstream release

* Thu Jul 30 2015 Kamil Dudka <kdudka@redhat.com> 7.43.0-3
- prevent dnf from crashing when using both FTP and HTTP (#1248389)

* Thu Jul 16 2015 Kamil Dudka <kdudka@redhat.com> 7.43.0-2
- build support for the HTTP/2 protocol

* Wed Jun 17 2015 Kamil Dudka <kdudka@redhat.com> 7.43.0-1
- new upstream release (fixes CVE-2015-3236 and CVE-2015-3237)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.42.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Kamil Dudka <kdudka@redhat.com> 7.42.1-2
- curl-config --libs now works on x86_64 without libcurl-devel.x86_64 (#1228363)

* Wed Apr 29 2015 Kamil Dudka <kdudka@redhat.com> 7.42.1-1
- new upstream release (fixes CVE-2015-3153)

* Wed Apr 22 2015 Kamil Dudka <kdudka@redhat.com> 7.42.0-1
- new upstream release (fixes CVE-2015-3143, CVE-2015-3144, CVE-2015-3145,
  and CVE-2015-3148)
- implement public key pinning for NSS backend (#1195771)
- do not run flaky test-cases in %%check

* Wed Feb 25 2015 Kamil Dudka <kdudka@redhat.com> 7.41.0-1
- new upstream release
- include extern-scan.pl to make test1135 succeed (upstream commit 1514b718)

* Mon Feb 23 2015 Kamil Dudka <kdudka@redhat.com> 7.40.0-3
- fix a spurious connect failure on dual-stacked hosts (#1187531)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 7.40.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Jan 08 2015 Kamil Dudka <kdudka@redhat.com> 7.40.0-1
- new upstream release (fixes CVE-2014-8150)

* Wed Nov 05 2014 Kamil Dudka <kdudka@redhat.com> 7.39.0-1
- new upstream release (fixes CVE-2014-3707)

* Tue Oct 21 2014 Kamil Dudka <kdudka@redhat.com> 7.38.0-2
- fix a connection failure when FTPS handle is reused

* Wed Sep 10 2014 Kamil Dudka <kdudka@redhat.com> 7.38.0-1
- new upstream release (fixes CVE-2014-3613 and CVE-2014-3620)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.37.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.37.1-2
- include arch'd Requires/Provides

* Wed Jul 16 2014 Kamil Dudka <kdudka@redhat.com> 7.37.1-1
- new upstream release
- fix endless loop with GSSAPI proxy auth (patches by David Woodhouse, #1118751)

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> 7.37.0-4
- fix license handling

* Fri Jul 04 2014 Kamil Dudka <kdudka@redhat.com> 7.37.0-3
- various SSL-related fixes (mainly crash on connection failure)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Kamil Dudka <kdudka@redhat.com> 7.37.0-1
- new upstream release

* Fri May 09 2014 Kamil Dudka <kdudka@redhat.com> 7.36.0-4
- auth failure on duplicated 'WWW-Authenticate: Negotiate' header (#1093348)

* Fri Apr 25 2014 Kamil Dudka <kdudka@redhat.com> 7.36.0-3
- nss: implement non-blocking SSL handshake

* Wed Apr 02 2014 Kamil Dudka <kdudka@redhat.com> 7.36.0-2
- extend URL parser to support IPv6 zone identifiers (#680996)

* Wed Mar 26 2014 Kamil Dudka <kdudka@redhat.com> 7.36.0-1
- new upstream release (fixes CVE-2014-0138)

* Mon Mar 17 2014 Paul Howarth <paul@city-fan.org> 7.35.0-5
- add all perl build requirements for the test suite, in a portable way

* Mon Mar 17 2014 Kamil Dudka <kdudka@redhat.com> 7.35.0-4
- add BR for perl-Digest-MD5, which is required by the test-suite

* Wed Mar 05 2014 Kamil Dudka <kdudka@redhat.com> 7.35.0-3
- avoid spurious failure of test1086 on s390(x) koji builders (#1072273)

* Tue Feb 25 2014 Kamil Dudka <kdudka@redhat.com> 7.35.0-2
- refresh expired cookie in test172 from upstream test-suite (#1068967)

* Wed Jan 29 2014 Kamil Dudka <kdudka@redhat.com> 7.35.0-1
- new upstream release (fixes CVE-2014-0015)

* Wed Dec 18 2013 Kamil Dudka <kdudka@redhat.com> 7.34.0-1
- new upstream release

* Mon Dec 02 2013 Kamil Dudka <kdudka@redhat.com> 7.33.0-2
- allow to use TLS > 1.0 if built against recent NSS

* Mon Oct 14 2013 Kamil Dudka <kdudka@redhat.com> 7.33.0-1
- new upstream release
- fix missing initialization in NTLM code causing test 906 to fail
- fix missing initialization in SSH code causing test 619 to fail

* Fri Oct 11 2013 Kamil Dudka <kdudka@redhat.com> 7.32.0-3
- do not limit the speed of SCP upload on a fast connection

* Mon Sep 09 2013 Kamil Dudka <kdudka@redhat.com> 7.32.0-2
- avoid delay if FTP is aborted in CURLOPT_HEADERFUNCTION callback (#1005686)

* Mon Aug 12 2013 Kamil Dudka <kdudka@redhat.com> 7.32.0-1
- new upstream release
- make sure that NSS is initialized prior to calling PK11_GenerateRandom()

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.31.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Kamil Dudka <kdudka@redaht.com> 7.31.0-4
- mention all option listed in 'curl --help' in curl.1 man page

* Tue Jul 02 2013 Kamil Dudka <kdudka@redhat.com> 7.31.0-3
- restore the functionality of 'curl -u :'

* Wed Jun 26 2013 Kamil Dudka <kdudka@redhat.com> 7.31.0-2
- build the curl tool with metalink support

* Sat Jun 22 2013 Kamil Dudka <kdudka@redhat.com> 7.31.0-1
- new upstream release (fixes CVE-2013-2174)

* Fri Apr 26 2013 Kamil Dudka <kdudka@redhat.com> 7.30.0-2
- prevent an artificial timeout event due to stale speed-check data (#906031)

* Fri Apr 12 2013 Kamil Dudka <kdudka@redhat.com> 7.30.0-1
- new upstream release (fixes CVE-2013-1944)
- prevent test-suite failure due to using non-default port ranges in tests

* Tue Mar 12 2013 Kamil Dudka <kdudka@redhat.com> 7.29.0-4
- do not ignore poll() failures other than EINTR (#919127)
- curl_global_init() now accepts the CURL_GLOBAL_ACK_EINTR flag (#919127)

* Wed Mar 06 2013 Kamil Dudka <kdudka@redhat.com> 7.29.0-3
- switch SSL socket into non-blocking mode after handshake
- drop the hide_selinux.c hack no longer needed in %%check

* Fri Feb 22 2013 Kamil Dudka <kdudka@redhat.com> 7.29.0-2
- fix a SIGSEGV when closing an unused multi handle (#914411)

* Wed Feb 06 2013 Kamil Dudka <kdudka@redhat.com> 7.29.0-1
- new upstream release (fixes CVE-2013-0249)

* Tue Jan 15 2013 Kamil Dudka <kdudka@redhat.com> 7.28.1-3
- require valgrind for build only on i386 and x86_64 (#886891)

* Tue Jan 15 2013 Kamil Dudka <kdudka@redhat.com> 7.28.1-2
- prevent NSS from crashing on client auth hook failure
- clear session cache if a client cert from file is used
- fix error messages for CURLE_SSL_{CACERT,CRL}_BADFILE

* Tue Nov 20 2012 Kamil Dudka <kdudka@redhat.com> 7.28.1-1
- new upstream release

* Wed Oct 31 2012 Kamil Dudka <kdudka@redhat.com> 7.28.0-1
- new upstream release

* Mon Oct 01 2012 Kamil Dudka <kdudka@redhat.com> 7.27.0-3
- use the upstream facility to disable problematic tests
- do not crash if MD5 fingerprint is not provided by libssh2

* Wed Aug 01 2012 Kamil Dudka <kdudka@redhat.com> 7.27.0-2
- eliminate unnecessary inotify events on upload via file protocol (#844385)

* Sat Jul 28 2012 Kamil Dudka <kdudka@redhat.com> 7.27.0-1
- new upstream release

* Mon Jul 23 2012 Kamil Dudka <kdudka@redhat.com> 7.26.0-6
- print reason phrase from HTTP status line on error (#676596)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.26.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Kamil Dudka <kdudka@redhat.com> 7.26.0-4
- fix duplicated SSL handshake with multi interface and proxy (#788526)

* Wed May 30 2012 Karsten Hopp <karsten@redhat.com> 7.26.0-3
- disable test 1319 on ppc64, server times out

* Mon May 28 2012 Kamil Dudka <kdudka@redhat.com> 7.26.0-2
- use human-readable error messages provided by NSS (upstream commit 72f4b534)

* Fri May 25 2012 Kamil Dudka <kdudka@redhat.com> 7.26.0-1
- new upstream release

* Wed Apr 25 2012 Karsten Hopp <karsten@redhat.com> 7.25.0-3
- valgrind on ppc64 works fine, disable ppc32 only

* Wed Apr 25 2012 Karsten Hopp <karsten@redhat.com> 7.25.0-3
- drop BR valgrind on PPC(64) until bugzilla #810992 gets fixed

* Fri Apr 13 2012 Kamil Dudka <kdudka@redhat.com> 7.25.0-2
- use NSS_InitContext() to initialize NSS if available (#738456)
- provide human-readable names for NSS errors (upstream commit a60edcc6)

* Fri Mar 23 2012 Paul Howarth <paul@city-fan.org> 7.25.0-1
- new upstream release (#806264)
- fix character encoding of docs with a patch rather than just iconv
- update debug and multilib patches
- don't use macros for commands
- reduce size of %%prep output for readability

* Tue Jan 24 2012 Kamil Dudka <kdudka@redhat.com> 7.24.0-1
- new upstream release (fixes CVE-2012-0036)

* Thu Jan 05 2012 Paul Howarth <paul@city-fan.org> 7.23.0-6
- rebuild for gcc 4.7

* Mon Jan 02 2012 Kamil Dudka <kdudka@redhat.com> 7.23.0-5
- upstream patch that allows to run FTPS tests with nss-3.13 (#760060)

* Tue Dec 27 2011 Kamil Dudka <kdudka@redhat.com> 7.23.0-4
- allow to run FTPS tests with nss-3.13 (#760060)

* Sun Dec 25 2011 Kamil Dudka <kdudka@redhat.com> 7.23.0-3
- avoid unnecessary timeout event when waiting for 100-continue (#767490)

* Mon Nov 21 2011 Kamil Dudka <kdudka@redhat.com> 7.23.0-2
- curl -JO now uses -O name if no C-D header comes (upstream commit c532604)

* Wed Nov 16 2011 Kamil Dudka <kdudka@redhat.com> 7.23.0-1
- new upstream release (#754391)

* Mon Sep 19 2011 Kamil Dudka <kdudka@redhat.com> 7.22.0-2
- nss: select client certificates by DER (#733657)

* Tue Sep 13 2011 Kamil Dudka <kdudka@redhat.com> 7.22.0-1
- new upstream release
- curl-config now provides dummy --static-libs option (#733956)

* Sun Aug 21 2011 Paul Howarth <paul@city-fan.org> 7.21.7-4
- actually fix SIGSEGV of curl -O -J given more than one URL (#723075)

* Mon Aug 15 2011 Kamil Dudka <kdudka@redhat.com> 7.21.7-3
- fix SIGSEGV of curl -O -J given more than one URL (#723075)
- introduce the --delegation option of curl (#730444)
- initialize NSS with no database if the selected database is broken (#728562)

* Wed Aug 03 2011 Kamil Dudka <kdudka@redhat.com> 7.21.7-2
- add a new option CURLOPT_GSSAPI_DELEGATION (#719939)

* Thu Jun 23 2011 Kamil Dudka <kdudka@redhat.com> 7.21.7-1
- new upstream release (fixes CVE-2011-2192)

* Wed Jun 08 2011 Kamil Dudka <kdudka@redhat.com> 7.21.6-2
- avoid an invalid timeout event on a reused handle (#679709)

* Sat Apr 23 2011 Paul Howarth <paul@city-fan.org> 7.21.6-1
- new upstream release

* Mon Apr 18 2011 Kamil Dudka <kdudka@redhat.com> 7.21.5-2
- fix the output of curl-config --version (upstream commit 82ecc85)

* Mon Apr 18 2011 Kamil Dudka <kdudka@redhat.com> 7.21.5-1
- new upstream release

* Sat Apr 16 2011 Peter Robinson <pbrobinson@gmail.com> 7.21.4-4
- no valgrind on ARMv5 arches

* Sat Mar 05 2011 Dennis Gilmore <dennis@ausil.us> 7.21.4-3
- no valgrind on sparc arches

* Tue Feb 22 2011 Kamil Dudka <kdudka@redhat.com> 7.21.4-2
- do not ignore failure of SSL handshake (upstream commit 7aa2d10)

* Fri Feb 18 2011 Kamil Dudka <kdudka@redhat.com> 7.21.4-1
- new upstream release
- avoid memory leak on SSL connection failure (upstream commit a40f58d)
- work around valgrind bug (#678518)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.21.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Kamil Dudka <kdudka@redhat.com> 7.21.3-2
- build libcurl with --enable-hidden-symbols

* Thu Dec 16 2010 Paul Howarth <paul@city-fan.org> 7.21.3-1
- update to 7.21.3:
  - added --noconfigure switch to testcurl.pl
  - added --xattr option
  - added CURLOPT_RESOLVE and --resolve
  - added CURLAUTH_ONLY
  - added version-check.pl to the examples dir
  - check for libcurl features for some command line options
  - Curl_setopt: disallow CURLOPT_USE_SSL without SSL support
  - http_chunks: remove debug output
  - URL-parsing: consider ? a divider
  - SSH: avoid using the libssh2_ prefix
  - SSH: use libssh2_session_handshake() to work on win64
  - ftp: prevent server from hanging on closed data connection when stopping
    a transfer before the end of the full transfer (ranges)
  - LDAP: detect non-binary attributes properly
  - ftp: treat server's response 421 as CURLE_OPERATION_TIMEDOUT
  - gnutls->handshake: improved timeout handling
  - security: pass the right parameter to init
  - krb5: use GSS_ERROR to check for error
  - TFTP: resend the correct data
  - configure: fix autoconf 2.68 warning: no AC_LANG_SOURCE call detected
  - GnuTLS: now detects socket errors on Windows
  - symbols-in-versions: updated en masse
  - added a couple of examples that were missing from the tarball
  - Curl_send/recv_plain: return errno on failure
  - Curl_wait_for_resolv (for c-ares): correct timeout
  - ossl_connect_common: detect connection re-use
  - configure: prevent link errors with --librtmp
  - openldap: use remote port in URL passed to ldap_init_fd()
  - url: provide dead_connection flag in Curl_handler::disconnect
  - lots of compiler warning fixes
  - ssh: fix a download resume point calculation
  - fix getinfo CURLINFO_LOCAL* for reused connections
  - multi: the returned running handles counter could turn negative
  - multi: only ever consider pipelining for connections doing HTTP(S)
- drop upstream patches now in tarball
- update bz650255 and disable-test1112 patches to apply against new codebase
- add workaround for false-positive glibc-detected buffer overflow in tftpd
  test server with FORTIFY_SOURCE (similar to #515361)

* Fri Nov 12 2010 Kamil Dudka <kdudka@redhat.com> 7.21.2-5
- do not send QUIT to a dead FTP control connection (#650255)
- pull back glibc's implementation of str[n]casecmp(), #626470 appears fixed

* Tue Nov 09 2010 Kamil Dudka <kdudka@redhat.com> 7.21.2-4
- prevent FTP client from hanging on unrecognized ABOR response (#649347)
- return more appropriate error code in case FTP server session idle
  timeout has exceeded (#650255)

* Fri Oct 29 2010 Kamil Dudka <kdudka@redhat.com> 7.21.2-3
- prevent FTP server from hanging on closed data connection (#643656)

* Thu Oct 14 2010 Paul Howarth <paul@city-fan.org> 7.21.2-2
- enforce versioned libssh2 dependency for libcurl (#642796)

* Wed Oct 13 2010 Kamil Dudka <kdudka@redhat.com> 7.21.2-1
- new upstream release, drop applied patches
- make 0102-curl-7.21.2-debug.patch less intrusive

* Wed Sep 29 2010 jkeating - 7.21.1-6
- Rebuilt for gcc bug 634757

* Sat Sep 11 2010 Kamil Dudka <kdudka@redhat.com> 7.21.1-5
- make it possible to run SCP/SFTP tests on x86_64 (#632914)

* Tue Sep 07 2010 Kamil Dudka <kdudka@redhat.com> 7.21.1-4
- work around glibc/valgrind problem on x86_64 (#631449)

* Tue Aug 24 2010 Paul Howarth <paul@city-fan.org> 7.21.1-3
- fix up patches so there's no need to run autotools in the rpm build
- drop buildreq automake
- drop dependency on automake for devel package from F-14, where
  %%{_datadir}/aclocal is included in the filesystem package
- drop dependency on pkgconfig for devel package from F-11, where
  pkgconfig dependencies are auto-generated

* Mon Aug 23 2010 Kamil Dudka <kdudka@redhat.com> 7.21.1-2
- re-enable test575 on s390(x), already fixed (upstream commit d63bdba)
- modify system headers to work around gcc bug (#617757)
- curl -T now ignores file size of special files (#622520)
- fix kerberos proxy authentication for https (#625676)
- work around glibc/valgrind problem on x86_64 (#626470)

* Thu Aug 12 2010 Kamil Dudka <kdudka@redhat.com> 7.21.1-1
- new upstream release

* Mon Jul 12 2010 Dan Horák <dan[at]danny.cz> 7.21.0-3
- disable test 575 on s390(x)

* Mon Jun 28 2010 Kamil Dudka <kdudka@redhat.com> 7.21.0-2
- add support for NTLM authentication (#603783)

* Wed Jun 16 2010 Kamil Dudka <kdudka@redhat.com> 7.21.0-1
- new upstream release, drop applied patches
- update of %%description
- disable valgrind for certain test-cases (libssh2 problem)

* Tue May 25 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-6
- fix -J/--remote-header-name to strip CR-LF (upstream patch)

* Wed Apr 28 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-5
- CRL support now works again (#581926)
- make it possible to start a testing OpenSSH server when building with SELinux
  in the enforcing mode (#521087)

* Sat Apr 24 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-4
- upstream patch preventing failure of test536 with threaded DNS resolver
- upstream patch preventing SSL handshake timeout underflow

* Thu Apr 22 2010 Paul Howarth <paul@city-fan.org> 7.20.1-3
- replace Rawhide s390-sleep patch with a more targeted patch adding a
  delay after tests 513 and 514 rather than after all tests

* Wed Apr 21 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-2
- experimentally enabled threaded DNS lookup
- make curl-config multilib ready again (#584107)

* Mon Apr 19 2010 Kamil Dudka <kdudka@redhat.com> 7.20.1-1
- new upstream release

* Tue Mar 23 2010 Kamil Dudka <kdudka@redhat.com> 7.20.0-4
- add missing quote in libcurl.m4 (#576252)

* Fri Mar 19 2010 Kamil Dudka <kdudka@redhat.com> 7.20.0-3
- throw CURLE_SSL_CERTPROBLEM in case peer rejects a certificate (#565972)
- valgrind temporarily disabled (#574889)
- kerberos installation prefix has been changed

* Wed Feb 24 2010 Kamil Dudka <kdudka@redhat.com> 7.20.0-2
- exclude test1112 from the test suite (#565305)

* Thu Feb 11 2010 Kamil Dudka <kdudka@redhat.com> 7.20.0-1
- new upstream release - added support for IMAP(S), POP3(S), SMTP(S) and RTSP
- dropped patches applied upstream
- dropped curl-7.16.0-privlibs.patch no longer useful
- a new patch forcing -lrt when linking the curl tool and test-cases

* Fri Jan 29 2010 Kamil Dudka <kdudka@redhat.com> 7.19.7-11
- upstream patch adding a new option -J/--remote-header-name
- dropped temporary workaround for #545779

* Thu Jan 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 7.19.7-10
- bump for libssh2 rebuild

* Sun Dec 20 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-9
- temporary workaround for #548269
  (restored behavior of 7.19.7-4)

* Wed Dec 09 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-8
- replace hard wired port numbers in the test suite

* Wed Dec 09 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-7
- use different port numbers for 32bit and 64bit builds
- temporary workaround for #545779

* Tue Dec 08 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-6
- make it possible to run test241
- re-enable SCP/SFTP tests (#539444)

* Sat Dec 05 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-5
- avoid use of uninitialized value in lib/nss.c
- suppress failure of test513 on s390

* Tue Dec 01 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-4
- do not require valgrind on s390 and s390x
- temporarily disabled SCP/SFTP test-suite (#539444)

* Thu Nov 12 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-3
- fix crash on doubly closed NSPR descriptor, patch contributed
  by Kevin Baughman (#534176)
- new version of patch for broken TLS servers (#525496, #527771)

* Wed Nov 04 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-2
- increased release number (CVS problem)

* Wed Nov 04 2009 Kamil Dudka <kdudka@redhat.com> 7.19.7-1
- new upstream release, dropped applied patches
- workaround for broken TLS servers (#525496, #527771)

* Wed Oct 14 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-13
- fix timeout issues and gcc warnings within lib/nss.c

* Tue Oct 06 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-12
- upstream patch for NSS support written by Guenter Knauf

* Wed Sep 30 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-11
- build libcurl with c-ares support (#514771)

* Sun Sep 27 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-10
- require libssh2>=1.2 properly (#525002)

* Sat Sep 26 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-9
- let curl test-suite use valgrind
- require libssh2>=1.2 (#525002)

* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 7.19.6-8
- rebuild for libssh2 1.2

* Thu Sep 17 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-7
- make curl test-suite more verbose

* Wed Sep 16 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-6
- update polling patch to the latest upstream version

* Thu Sep 03 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-5
- cover ssh and stunnel support by the test-suite

* Wed Sep 02 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-4
- use pkg-config to find nss and libssh2 if possible
- better patch (not only) for SCP/SFTP polling
- improve error message for not matching common name (#516056)

* Fri Aug 21 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-3
- avoid tight loop during a sftp upload
- http://permalink.gmane.org/gmane.comp.web.curl.library/24744

* Tue Aug 18 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-2
- let curl package depend on the same version of libcurl

* Fri Aug 14 2009 Kamil Dudka <kdudka@redhat.com> 7.19.6-1
- new upstream release, dropped applied patches
- changed NSS code to not ignore the value of ssl.verifyhost and produce more
  verbose error messages (#516056)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 7.19.5-10
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-8
- do not pre-login to all PKCS11 slots, it causes problems with HW tokens
- try to select client certificate automatically when not specified, thanks
  to Claes Jakobsson

* Fri Jul 10 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-7
- fix SIGSEGV when using NSS client certificates, thanks to Claes Jakobsson

* Sun Jul 05 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-6
- force test suite to use the just built libcurl, thanks to Paul Howarth

* Thu Jul 02 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-5
- run test suite after build
- enable built-in manual

* Wed Jun 24 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-4
- fix bug introduced by the last build (#504857)

* Wed Jun 24 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-3
- exclude curlbuild.h content from spec (#504857)

* Wed Jun 10 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-2
- avoid unguarded comparison in the spec file, thanks to R P Herrold (#504857)

* Tue May 19 2009 Kamil Dudka <kdudka@redhat.com> 7.19.5-1
- update to 7.19.5, dropped applied patches

* Mon May 11 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-11
- fix infinite loop while loading a private key, thanks to Michael Cronenworth
  (#453612)

* Mon Apr 27 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-10
- fix curl/nss memory leaks while using client certificate (#453612, accepted
  by upstream)

* Wed Apr 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-9
- add missing BuildRequire for autoconf

* Wed Apr 22 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-8
- fix configure.ac to not discard -g in CFLAGS (#496778)

* Tue Apr 21 2009 Debarshi Ray <rishi@fedoraproject.org> 7.19.4-7
- Fixed configure to respect the environment's CFLAGS and CPPFLAGS settings.

* Tue Apr 14 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-6
- upstream patch fixing memory leak in lib/nss.c (#453612)
- remove redundant dependency of libcurl-devel on libssh2-devel

* Wed Mar 18 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-5
- enable 6 additional crypto algorithms by default (#436781,
  accepted by upstream)

* Thu Mar 12 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-4
- fix memory leak in src/main.c (accepted by upstream)
- avoid using %%ifarch

* Wed Mar 11 2009 Kamil Dudka <kdudka@redhat.com> 7.19.4-3
- make libcurl-devel multilib-ready (bug #488922)

* Fri Mar 06 2009 Jindrich Novy <jnovy@redhat.com> 7.19.4-2
- drop .easy-leak patch, causes problems in pycurl (#488791)
- fix libcurl-devel dependencies (#488895)

* Tue Mar 03 2009 Jindrich Novy <jnovy@redhat.com> 7.19.4-1
- update to 7.19.4 (fixes CVE-2009-0037)
- fix leak in curl_easy* functions, thanks to Kamil Dudka
- drop nss-fix patch, applied upstream

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Kamil Dudka <kdudka@redhat.com> 7.19.3-1
- update to 7.19.3, dropped applied nss patches
- add patch fixing 7.19.3 curl/nss bugs

* Mon Dec 15 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-9
- rebuild for f10/rawhide cvs tag clashes

* Sat Dec 06 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-8
- use improved NSS patch, thanks to Rob Crittenden (#472489)

* Tue Sep 09 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-7
- update the thread safety patch, thanks to Rob Crittenden (#462217)

* Wed Sep 03 2008 Warren Togami <wtogami@redhat.com> 7.18.2-6
- add thread safety to libcurl NSS cleanup() functions (#459297)

* Fri Aug 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.18.2-5
- undo mini libcurl.so.3

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 7.18.2-4
- make miniature library for libcurl.so.3

* Fri Jul  4 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-3
- enable support for libssh2 (#453958)

* Wed Jun 18 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-2
- fix curl_multi_perform() over a proxy (#450140), thanks to
  Rob Crittenden

* Wed Jun  4 2008 Jindrich Novy <jnovy@redhat.com> 7.18.2-1
- update to 7.18.2

* Wed May  7 2008 Jindrich Novy <jnovy@redhat.com> 7.18.1-2
- spec cleanup, thanks to Paul Howarth (#225671)
  - drop BR: libtool
  - convert CHANGES and README to UTF-8
  - _GNU_SOURCE in CFLAGS is no more needed
  - remove bogus rpath

* Mon Mar 31 2008 Jindrich Novy <jnovy@redhat.com> 7.18.1-1
- update to curl 7.18.1 (fixes #397911)
- add ABI docs for libcurl
- remove --static-libs from curl-config
- drop curl-config patch, obsoleted by @SSL_ENABLED@ autoconf
  substitution (#432667)

* Fri Feb 15 2008 Jindrich Novy <jnovy@redhat.com> 7.18.0-2
- define _GNU_SOURCE so that NI_MAXHOST gets defined from glibc

* Mon Jan 28 2008 Jindrich Novy <jnovy@redhat.com> 7.18.0-1
- update to curl-7.18.0
- drop sslgen patch -> applied upstream
- fix typo in description

* Tue Jan 22 2008 Jindrich Novy <jnovy@redhat.com> 7.17.1-6
- fix curl-devel obsoletes so that we don't break F8->F9 upgrade
  path (#429612)

* Tue Jan  8 2008 Jindrich Novy <jnovy@redhat.com> 7.17.1-5
- do not attempt to close a bad socket (#427966),
  thanks to Caolan McNamara

* Tue Dec  4 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-4
- rebuild because of the openldap soname bump
- remove old nsspem patch

* Fri Nov 30 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-3
- drop useless ldap library detection since curl doesn't
  dlopen()s it but links to it -> BR: openldap-devel
- enable LDAPS support (#225671), thanks to Paul Howarth
- BR: krb5-devel to reenable GSSAPI support
- simplify build process
- update description

* Wed Nov 21 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-2
- update description to contain complete supported servers list (#393861)

* Sat Nov 17 2007 Jindrich Novy <jnovy@redhat.com> 7.17.1-1
- update to curl 7.17.1
- include patch to enable SSL usage in NSS when a socket is opened
  nonblocking, thanks to Rob Crittenden (rcritten@redhat.com)

* Wed Oct 24 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-10
- correctly provide/obsolete curl-devel (#130251)

* Wed Oct 24 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-9
- create libcurl and libcurl-devel subpackages (#130251)

* Thu Oct 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-8
- list features correctly when curl is compiled against NSS (#316191)

* Mon Sep 17 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-7
- add zlib-devel BR to enable gzip compressed transfers in curl (#292211)

* Mon Sep 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-6
- provide webclient (#225671)

* Thu Sep  6 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-5
- add support for the NSS PKCS#11 pem reader so the command-line is the
  same for both OpenSSL and NSS by Rob Crittenden (rcritten@redhat.com)
- switch to NSS again

* Mon Sep  3 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-4
- revert back to use OpenSSL (#266021)

* Mon Aug 27 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-3
- don't use openssl, use nss instead

* Fri Aug 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-2
- fix anonymous ftp login (#251570), thanks to David Cantrell

* Wed Jul 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.4-1
- update to 7.16.4

* Mon Jun 25 2007 Jindrich Novy <jnovy@redhat.com> 7.16.3-1
- update to 7.16.3
- drop .print patch, applied upstream
- next series of merge review fixes by Paul Howarth
- remove aclocal stuff, no more needed
- simplify makefile arguments
- don't reference standard library paths in libcurl.pc
- include docs/CONTRIBUTE

* Mon Jun 18 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-5
- don't print like crazy (#236981), backported from upstream CVS

* Fri Jun 15 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-4
- another series of review fixes (#225671),
  thanks to Paul Howarth
- check version of ldap library automatically
- don't use %%makeinstall and preserve timestamps
- drop useless patches

* Fri May 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-3
- add automake BR to curl-devel to fix aclocal dir. ownership,
  thanks to Patrice Dumas

* Thu May 10 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-2
- package libcurl.m4 in curl-devel (#239664), thanks to Quy Tonthat

* Wed Apr 11 2007 Jindrich Novy <jnovy@redhat.com> 7.16.2-1
- update to 7.16.2

* Mon Feb 19 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-3
- don't create/ship static libraries (#225671)

* Mon Feb  5 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-2
- merge review related spec fixes (#225671)

* Mon Jan 29 2007 Jindrich Novy <jnovy@redhat.com> 7.16.1-1
- update to 7.16.1

* Tue Jan 16 2007 Jindrich Novy <jnovy@redhat.com> 7.16.0-5
- don't package generated makefiles for docs/examples to avoid
  multilib conflicts

* Mon Dec 18 2006 Jindrich Novy <jnovy@redhat.com> 7.16.0-4
- convert spec to UTF-8
- don't delete BuildRoot in %%prep phase
- rpmlint fixes

* Thu Nov 16 2006 Jindrich Novy <jnovy@redhat.com> -7.16.0-3
- prevent curl from dlopen()ing missing ldap libraries so that
  ldap:// requests work (#215928)

* Tue Oct 31 2006 Jindrich Novy <jnovy@redhat.com> - 7.16.0-2
- fix BuildRoot
- add Requires: pkgconfig for curl-devel
- move LDFLAGS and LIBS to Libs.private in libcurl.pc.in (#213278)

* Mon Oct 30 2006 Jindrich Novy <jnovy@redhat.com> - 7.16.0-1
- update to curl-7.16.0

* Thu Aug 24 2006 Jindrich Novy <jnovy@redhat.com> - 7.15.5-1.fc6
- update to curl-7.15.5
- use %%{?dist}

* Fri Jun 30 2006 Ivana Varekova <varekova@redhat.com> - 7.15.4-1
- update to 7.15.4

* Mon Mar 20 2006 Ivana Varekova <varekova@redhat.com> - 7.15.3-1
- fix multilib problem using pkg-config
- update to 7.15.3

* Thu Feb 23 2006 Ivana Varekova <varekova@redhat.com> - 7.15.1-2
- fix multilib problem - #181290 - 
  curl-devel.i386 not installable together with curl-devel.x86-64

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 7.15.1-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 7.15.1-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Ivana Varekova <varekova@redhat.com> 7.15.1-1
- update to 7.15.1 (bug 175191)

* Wed Nov 30 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-3
- fix curl-config bug 174556 - missing vernum value

* Wed Nov  9 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-2
- rebuilt

* Tue Oct 18 2005 Ivana Varekova <varekova@redhat.com> 7.15.0-1
- update to 7.15.0

* Thu Oct 13 2005 Ivana Varekova <varekova@redhat.com> 7.14.1-1
- update to 7.14.1

* Thu Jun 16 2005 Ivana Varekova <varekova@redhat.com> 7.14.0-1
- rebuild new version 

* Tue May 03 2005 Ivana Varekova <varekova@redhat.com> 7.13.1-3
- fix bug 150768 - curl-7.12.3-2 breaks basic authentication
  used Daniel Stenberg patch 

* Mon Apr 25 2005 Joe Orton <jorton@redhat.com> 7.13.1-2
- update to use ca-bundle in /etc/pki
- mark License as MIT not MPL

* Wed Mar  9 2005 Ivana Varekova <varekova@redhat.com> 7.13.1-1
- rebuilt (7.13.1)

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 7.13.0-2
- rebuild with openssl-0.9.7e

* Sun Feb 13 2005 Florian La Roche <laroche@redhat.com>
- 7.13.0

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 7.12.3-3
- don't pass /usr to --with-libidn to remove "-L/usr/lib" from
  'curl-config --libs' output on x86_64.

* Fri Jan 28 2005 Adrian Havill <havill@redhat.com> 7.12.3-1
- Upgrade to 7.12.3, which uses poll() for FDSETSIZE limit (#134794)
- require libidn-devel for devel subpkg (#141341)
- remove proftpd kludge; included upstream

* Wed Oct 06 2004 Adrian Havill <havill@redhat.com> 7.12.1-1
- upgrade to 7.12.1
- enable GSSAPI auth (#129353)
- enable I18N domain names (#134595)
- workaround for broken ProFTPD SSL auth (#134133). Thanks to
  Aleksandar Milivojevic

* Wed Sep 29 2004 Adrian Havill <havill@redhat.com> 7.12.0-4
- move new docs position so defattr gets applied

* Mon Sep 27 2004 Warren Togami <wtogami@redhat.com> 7.12.0-3
- remove INSTALL, move libcurl docs to -devel

* Mon Jul 26 2004 Jindrich Novy <jnovy@redhat.com>
- updated to 7.12.0
- updated nousr patch

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 07 2004 Adrian Havill <havill@redhat.com> 7.11.1-1
- upgraded; updated nousr patch
- added COPYING (#115956)
- 

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 31 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 7.10.8
- remove patch2, already upstream

* Wed Oct 15 2003 Adrian Havill <havill@redhat.com> 7.10.6-7
- aclocal before libtoolize
- move OpenLDAP license so it's present as a doc file, present in
  both the source and binary as per conditions

* Mon Oct 13 2003 Adrian Havill <havill@redhat.com> 7.10.6-6
- add OpenLDAP copyright notice for usage of code, add OpenLDAP
  license for this code

* Tue Oct 07 2003 Adrian Havill <havill@redhat.com> 7.10.6-5
- match serverAltName certs with SSL (#106168)

* Tue Sep 16 2003 Adrian Havill <havill@redhat.com> 7.10.6-4.1
- bump n-v-r for RHEL

* Tue Sep 16 2003 Adrian Havill <havill@redhat.com> 7.10.6-4
- restore ca cert bundle (#104400)
- require openssl, we want to use its ca-cert bundle

* Sun Sep  7 2003 Joe Orton <jorton@redhat.com> 7.10.6-3
- rebuild

* Fri Sep  5 2003 Joe Orton <jorton@redhat.com> 7.10.6-2.2
- fix to include libcurl.so

* Mon Aug 25 2003 Adrian Havill <havill@redhat.com> 7.10.6-2.1
- bump n-v-r for RHEL

* Mon Aug 25 2003 Adrian Havill <havill@redhat.com> 7.10.6-2
- devel subpkg needs openssl-devel as a Require (#102963)

* Mon Jul 28 2003 Adrian Havill <havill@redhat.com> 7.10.6-1
- bumped version

* Tue Jul 01 2003 Adrian Havill <havill@redhat.com> 7.10.5-1
- bumped version

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 7.10.4
- adapt nousr patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Joe Orton <jorton@redhat.com> 7.9.8-4
- don't add -L/usr/lib to 'curl-config --libs' output

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 7.9.8-3
- rebuild

* Wed Nov  6 2002 Joe Orton <jorton@redhat.com> 7.9.8-2
- fix `curl-config --libs` output for libdir!=/usr/lib
- remove docs/LIBCURL from docs list; remove unpackaged libcurl.la
- libtoolize and reconf

* Mon Jul 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.8-1
- 7.9.8 (# 69473)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.7-1
- 7.9.7

* Wed Apr 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.6-1
- 7.9.6

* Thu Mar 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.5-2
- Stop the curl-config script from printing -I/usr/include 
  and -L/usr/lib (#59497)

* Fri Mar  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.5-1
- 7.9.5

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.3-2
- Rebuild

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 7.9.3-1
- update to 7.9.3

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 7.9.2-2
- automated rebuild

* Wed Jan  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 7.9.2-1
- 7.9.2

* Fri Aug 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- include curl-config in curl-devel
- update to 7.8 to fix memory leak and strlcat() symbol pollution from libcurl

* Wed Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- added openssl-devel build req

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- built for the distro

* Tue Apr 24 2001 Jeff Johnson <jbj@redhat.com>
- upgrade to curl-7.7.2.
- enable IPv6.

* Fri Mar  2 2001 Tim Powers <timp@redhat.com>
- rebuilt against openssl-0.9.6-1

* Thu Jan  4 2001 Tim Powers <timp@redhat.com>
- fixed mising ldconfigs
- updated to 7.5.2, bug fixes

* Mon Dec 11 2000 Tim Powers <timp@redhat.com>
- updated to 7.5.1

* Mon Nov  6 2000 Tim Powers <timp@redhat.com>
- update to 7.4.1 to fix bug #20337, problems with curl -c
- not using patch anymore, it's included in the new source. Keeping
  for reference

* Fri Oct 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bogus req in -devel package

* Fri Oct 20 2000 Tim Powers <timp@redhat.com> 
- devel package needed defattr so that root owns the files

* Mon Oct 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 7.3
- apply vsprintf/vsnprintf patch from Colin Phipps via Debian

* Mon Aug 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable SSL support
- fix packager tag
- move buildroot to %%{_tmppath}

* Tue Aug 1 2000 Tim Powers <timp@redhat.com>
- fixed vendor tag for bug #15028

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Tue Jul 11 2000 Tim Powers <timp@redhat.com>
- workaround alpha build problems with optimizations

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jun 5 2000 Tim Powers <timp@redhat.com>
- put man pages in correct place
- use %%makeinstall

* Mon Apr 24 2000 Tim Powers <timp@redhat.com>
- updated to 6.5.2

* Wed Nov 3 1999 Tim Powers <timp@redhat.com>
- updated sources to 6.2
- gzip man page

* Mon Aug 30 1999 Tim Powers <timp@redhat.com>
- changed group

* Thu Aug 26 1999 Tim Powers <timp@redhat.com>
- changelog started
- general cleanups, changed prefix to /usr, added manpage to files section
- including in Powertools
