#!/bin/python2

import logging

def parser(subparser):
    subparser.add_argument('--flavour', help='Flavour name', required=True)


def getFlavourDiskSize(flavour):
    from sh import nova, tail, grep, awk
    return int(awk(grep(nova("flavor-show", flavour), '| disk'), '{ print $4 }'))

def populateImageParts(img):
    import sh, re
    from sh import tail
    logger = logging.getLogger('virtimg')
    df = sh.Command('virt-df')
    out = str(tail(df('-a', img.path), '-n+2'))
    logger.debug('%s: df-h: %s', img.name, out)
    regex = re.compile('^[\w.\-]+:/dev/sda(?P<partid>\d+)\s+(?P<size>\d+)\s+\d+\s+(?P<free>\d+)', re.M)
    res = re.findall(regex, out)
    img.parts = dict()
    for part in res:
        img.parts[part[0]] = dict()
        img.parts[part[0]]["size"] = part[1]
        img.parts[part[0]]["free"] = part[2]
    img.lastpart = max(img.parts.keys())

def populateImageDiskInfos(mgr):
    import sh, re
    qemu = sh.Command('qemu-img')
    regexFormat = re.compile(r"^file format: (\w+)$", re.M)
    regexDiskSize = re.compile(r"^disk size: (\d+)G", re.M)
    regexVDiskSize = re.compile(r"^virtual size: (\d+)G", re.M)
    logger = logging.getLogger('virtimg')
    for img in mgr:
        info = str(qemu('info', img.path))
        logger.debug('%s: qemu-img info: %s', img.name, info)
        frmtR = re.search(regexFormat, info)
        diskSizeR = re.search(regexDiskSize, info)
        vDiskSizeR = re.search(regexVDiskSize, info)
        if frmtR:
            img.format = frmtR.group(1)
        if diskSizeR:
            img.diskSize = diskSizeR.group(1)
        if vDiskSizeR:
            img.vDiskSize = vDiskSizeR.group(1)
        logger.debug("format: %s, size: %s, vsize: %s", img.format, img.diskSize, img.vDiskSize)

def checkPartition(img, partid):
    from sh import guestfish
    logger = logging.getLogger('virtimg')
    str = """add %s
             run
             e2fsck-f /dev/sda%s
          """ % (img.path, partid)
    for line in guestfish(_in=str, _iter=True):
        logger.debug('%s: guestfish e2fsck-f: %s', img.name, line)

def convertRaw(img):
    import sh, os
    qemu = sh.Command('qemu-img')
    qemu('convert', '-O', 'raw', img.path, "%s.raw" % (img.path))
    img.format='raw'
    os.remove(img.path)
    img.path = "%s.raw" % (img.path)

def resizeFsImage(img, partid, size):
    from sh import guestfish
    logger = logging.getLogger('virtimg')
    str = """add %s
             run
             resize2fs-size /dev/sda%s %dK
          """ % (img.path, partid, size)
    for line in guestfish(_in=str, _iter=True):
        logger.debug('%s: guestfish resize2fs-size: %s', line)

def resizeImage(img, sizeToDrop):
    import sh
    qemu = sh.Command('qemu-img')
    qemu('resize', img.path, '-%sK' % (sizeToDrop))

def convertQcow2(img):
    import sh
    import os
    qemu = sh.Command('qemu-img')
    qemu('convert', '-O', 'qcow2', '-c', '-o', 'compat=0.10', img.path, '%s.qcow2' % (img.path))
    os.remove(img.path)
    img.path = "%s.qcow2" % (img.path)

def resizePartImage(img, partid, size):
    import sh
    from sh import truncate
    import os
    logger = logging.getLogger('virtimg')
    resize = sh.Command('virt-resize')
    truncate('-r', img.path, "%s.resized" % (img.path))
    for line in resize('--no-extra-partition', '--resize-force', "/dev/sda%s=%dK" % (partid, size), img.path, "%s.resized" % (img.path), _iter=True):
        logger.debug('%s: resizeFS: %s', img.name, line)
    os.remove(img.path)
    img.path = "%s.resized" % (img.path)

def run(mgr, namespace):
    logger = logging.getLogger('virtimg')
    flavourDiskSize = getFlavourDiskSize(namespace.flavour)
    populateImageDiskInfos(mgr)
    for img in mgr:
        img.toFlavour = False
        logger.info("%s: Checking image requirements", img.name)
        if int(img.vDiskSize) <= flavourDiskSize:
            logger.warn("%s: virtual disk size small enough: toFlavour ignored", img.name)
            continue
        if int(img.diskSize) >= flavourDiskSize:
            logger.warn("%s: disk size too big: toFlavour ignored", img.name)
            continue
        img.spaceToRemove = (int(img.vDiskSize) - flavourDiskSize)*1024*1024
        populateImageParts(img)
        if int(img.parts[img.lastpart]["free"]) < img.spaceToRemove:
            logger.warn("%s: not enough space on /dev/sda%s: toFlavour ignored", img.name, str(img.lastpart))
            continue
        img.toFlavour = True
        for img in mgr:
            if not img.toFlavour:
                continue
            logger.info("%s: Checking image filesystems", img.name)
            for key,val in img.parts.iteritems():
                logger.info("%s: checking /dev/sda%s", img.name, key)
                checkPartition(img, key)
            if img.format != 'raw':
                logger.info("%s: Image is not in RAW format, converting", img.name)
                convertRaw(img)
            newsize = int(img.parts[img.lastpart]["size"]) - img.spaceToRemove
            logger.info("%s: Resizing filesystem /dev/sda%s to %sK", img.name, img.lastpart, str(newsize))
            resizeFsImage(img, img.lastpart, newsize)
            logger.info("%s: checking /dev/sda%s", img.name, img.lastpart)
            checkPartition(img, img.lastpart)
            logger.info("%s: Resizing partition /dev/sda%s to %sK", img.name, img.lastpart, str(newsize))
            resizePartImage(img, img.lastpart, newsize)
            logger.info("%s: Resizing image from %sG to %sG", img.name, img.vDiskSize, str(flavourDiskSize))
            resizeImage(img, img.spaceToRemove)
            logger.info("%s: Converting back to qcow2", img.name)
            convertQcow2(img)
    populateImageDiskInfos(mgr)
