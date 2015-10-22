#!/bin/python2

def parser(subparser):
    subparser.add_argument('location', help='Output folder location')

def run(mgr, namespace):
    import shutil

    for img in mgr:
        print "Copying %s in %s" % (img.name, namespace.location)
        shutil.copyfile(img.path, "%s/%s" % (namespace.location, img.name))



