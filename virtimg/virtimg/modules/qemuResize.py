#!/bin/python2

def typeParser(value):
    return value

def parser(subparser):
    subparser.add_argument('--size', required=True, nargs=1, help='new size [+|-] sizeG', type=typeParser)

def run(mgr, namespace):
    import sh
    import shutil

    qemu = sh.Command('qemu-img')
    for img in mgr:
        print "Resizing %s" % (img.name)
        info = qemu('resize', img.path, namespace.size)
        print info




