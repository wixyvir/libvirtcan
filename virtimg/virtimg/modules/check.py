#!/bin/python2

def parser(subparser):
    pass

def run(mgr, namespace):
    import sh
    qemu = sh.Command('qemu-img')
    for img in mgr:
        info = qemu('check', img.path)
        print "Image Check for %s" % (img.name)
        print info


