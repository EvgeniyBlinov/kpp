#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,getopt,re
import pprint,inspect
import urllib,urlparse
from subprocess import call


########################################################################
#                        KernelCMDParser
########################################################################
class KernelCMDParser(object):
    PARAM_DELIMITER = ';'
    PARAM_EVAL      = ':'
    KPP_RE_PATTERN  = '^kpp='
    def __init__(self):
        self.cmd = self.getCMDParams()
        self.params = self.getKPPParams()

    def getCMDParams(self):
        with open('/proc/cmdline') as f:
            lines = f.readlines()
        return ' '.join(lines).split(' ')

    def getKPPParams(self):
        kppre = re.compile(self.KPP_RE_PATTERN)
        params = {}
        for paramstr in self.cmd:
            if kppre.search(paramstr):
                paramstr = paramstr.rstrip()[4:]
                params = dict(urlparse.parse_qsl(paramstr))
        return params

    def doExec(self, command='all'):
        if command == 'all':
            pprint.pprint(self.params)
        else:
            param = self.params.get(command)
            if param:
                print param

    def doConfig(self, config):
        #print '#!/bin/sh'
        #print '. /etc/grub.d/10_linux > /dev/null 2>&1'
        print """#!/bin/sh
. /etc/grub.d/10_linux > /dev/null 2>&1
########################################################################
# grub-common:2.02~beta2-36ubuntu3.11 - fixes
########################################################################
for path in / /boot/;do test -f "${path}vmlinuz-$(uname -r)" && export rel_dirname=${path%%/};done
export version="$(uname -r)"
export basename="$version"
export dirname="$rel_dirname"
initrd=
for i in "initrd.img-${version}" "initrd-${version}.img" "initrd-${version}.gz" \
    "initrd-${version}" "initramfs-${version}.img" \
    "initrd.img-${alt_version}" "initrd-${alt_version}.img" \
    "initrd-${alt_version}" "initramfs-${alt_version}.img" \
    "initramfs-genkernel-${version}" \
    "initramfs-genkernel-${alt_version}" \
    "initramfs-genkernel-${GENKERNEL_ARCH}-${version}" \
    "initramfs-genkernel-${GENKERNEL_ARCH}-${alt_version}"; do
if test -e "${dirname}/${i}" ; then
    initrd="$i"
    break
fi
done
########################################################################
"""
        for cmd in config.split(';'):
            print "linux_entry \"${OS} %(cmd)s\" \"$(uname -r)\" kpp \"${GRUB_CMDLINE_LINUX} ${GRUB_CMDLINE_LINUX_DEFAULT} 'kpp=%(cmd)s'\"" % {'cmd': cmd}

########################################################################

# settings
verbose = False

# usage
def usage(status = 0):
  global verbose
  print 'Usage: ' + os.path.basename(sys.argv[0]) + ' -[hv]'
  sys.exit(status)

# main
def main():
    global verbose
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvae:c:",
            ["help", "verbose", "all", "exec"]
        )
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage(2)
    verbose = False
    parser = KernelCMDParser()
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
        elif o in ("-e", "--exec"):
            parser.doExec(a)
        elif o in ("-c", "--config"):
            parser.doConfig(a)
        elif o in ("-a", "--all"):
            parser.doExec()
        else:
            assert False, "unhandled option"
            usage()

if __name__ == "__main__":
    main()
