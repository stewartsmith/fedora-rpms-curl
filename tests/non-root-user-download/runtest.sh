#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/curl/Sanity/non-root-user-download
#   Description: various download methods with non-root user
#   Author: Karel Srot <ksrot@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2013 Red Hat, Inc. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include Beaker environment
. /usr/bin/rhts-environment.sh || exit 1
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="curl"

FTP_URL=ftp://ftp.scientificlinux.org/linux/fedora/releases/18/Live/x86_64/Fedora-18-x86_64-Live-CHECKSUM
HTTP_URL=https://archives.fedoraproject.org/pub/archive/fedora/linux/releases/18/Live/x86_64/Fedora-18-x86_64-Live-CHECKSUM
CONTENT=a276e06d244e04b765f0a35532d9036ad84f340b0bdcc32e0233a8fbc31d5bed
PASSWORD=pAssw0rd
OPTIONS=""
rlIsRHEL 7 && OPTIONS="--insecure"

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlRun "pushd $TmpDir"
        rlRun "useradd -m curltester" 0 "Adding the test user"
        rlRun "echo $PASSWORD | passwd --stdin curltester" 0 "Setting the password for the test user"
        rlRun "su - curltester -c 'echo $CONTENT > ~/testfile'" 0 "Creating ~curltester/testfile"
        [ -d $HOME/.ssh ] || ( mkdir $HOME/.ssh && restorecon HOME/.ssh )
        rlFileBackup $HOME/.ssh/known_hosts /etc/hosts
        ssh-keygen -F localhost -f $HOME/.ssh/known_hosts || rlRun "ssh-keyscan localhost >> $HOME/.ssh/known_hosts"
    rlPhaseEnd

    rlPhaseStartTest "http download"
        rlRun "su - curltester -c 'curl $HTTP_URL' &> http.log"
        cat http.log
        rlAssertGrep "$CONTENT" http.log
    rlPhaseEnd

    rlPhaseStartTest "ftp download"
        rlRun "su - curltester -c 'curl $FTP_URL' &> ftp.log"
        cat ftp.log
        rlAssertGrep "$CONTENT" ftp.log
    rlPhaseEnd

if ! rlIsRHEL 5; then
# scp sftp not supported on RHEL5

    rlPhaseStartTest "scp download"
        rlRun "curl -u curltester:$PASSWORD $OPTIONS scp://localhost/home/curltester/testfile &> scp.log"
        cat scp.log
        rlAssertGrep "$CONTENT" scp.log
    rlPhaseEnd

    rlPhaseStartTest "sftp download"
        rlRun "curl -u curltester:$PASSWORD $OPTIONS sftp://localhost/home/curltester/testfile &> sftp.log"
        cat sftp.log
        rlAssertGrep "$CONTENT" sftp.log
    rlPhaseEnd

fi

    rlPhaseStartCleanup
        rlRun "rm -f $HOME/.ssh/known_hosts"
        rlFileRestore
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
        rlRun "userdel -r --force curltester"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
