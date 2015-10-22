#!/bin/python2

def parser(subparser):
    pass

def run(mgr, namespace):
    import sh, re
    fs = sh.Command('virt-filesystems')
    for img in mgr:
        info = fs('-l', '--all', '-a', img.path)
        print "Image Filesystems Infos for %s" % (img.name)
        print info


