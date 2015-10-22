#!/bin/python2

def parser(subparser):
    subparser.add_argument('format', help='Output format')
    subparser.add_argument('--compress', action='store_true', help='Compress output file')

def run(mgr, namespace):
    import sh
    import shutil

    qemu = sh.Command('qemu-img')
    for img in mgr:
        print "Converting %s" % (img.name)
        if namespace.compress:
            info = qemu('convert', '-c', '-O', namespace.format, img.path, "%s.new" % (img.path))
        else:
            info = qemu('convert', '-O', namespace.format, img.path, "%s.new" % (img.path))
        shutil.rmtree(img.path, True)
        shutil.move("%s.new" % (img.path), img.path)
        img.type=namespace.format



