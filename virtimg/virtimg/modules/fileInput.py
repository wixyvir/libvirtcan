#!/bin/python2

import logging



def parser(subparser):
    subparser.add_argument('--location', help='Image location', required=True)
    subparser.add_argument('--name', help='Image name', required=True)

def run(mgr, namespace):
    import shutil
    logger = logging.getLogger('virtimg')
    if namespace.name in mgr:
        logger.warn("[File Input] Image %s already exists, overwriting..." % (namespace.name))
    shutil.copyfile(namespace.location, "%s/%s" % (namespace.workdir, namespace.name))
    mgr.add(namespace.name, "%s/%s" % (namespace.workdir, namespace.name))
    

    


