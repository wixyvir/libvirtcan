#!/bin/python2

import logging



def parser(subparser):
    subparser.add_argument('--image', help='Image to download from glance', required=True)

def run(mgr, namespace):
    from sh import glance
    logger = logging.getLogger('virtimg')
    if namespace.image in mgr:
        logger.warn("[Glance Download] Image %s already exists, overwriting..." % (namespace.image))
    glance('image-download', '--file', "%s/%s" % (namespace.workdir, namespace.image), namespace.image)
    mgr.add(namespace.image, "%s/%s" % (namespace.workdir, namespace.image))
    

    


