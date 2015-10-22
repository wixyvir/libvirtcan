#!/bin/python2

def parser(subparser):
    pass

def run(mgr, namespace):
    import sh, re
    qemu = sh.Command('qemu-img')
    regex = re.compile(r"^file format: (\w+)$", re.M)
    for img in mgr:
        info = qemu('info', img.path)
        frmt = re.search(regex, str(info))
        if frmt:
            img.type = frmt.group(1)
        print "Image Infos for %s" % (img.name)
        print info


