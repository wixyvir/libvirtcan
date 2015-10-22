#!/usr/bin/python2

import argparse
import logging
import mod
import sys
import img
import shutil
import os

def cli_entrypoint(argv = sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Process libvirt Qcow2/Raw disk images')
    parser.add_argument("--workdir", default='/var/tmp/', help='Images working directory (need disk space)')
    parser.add_argument("--nocleanup", action="store_true", help='Do not clean up working directory')
    parser_subparsers = parser.add_subparsers(dest='command')
    modMgr = mod.ModulesManager()
    modMgr.loadModules()
    for moduleName, module in modMgr:
        sub = parser_subparsers.add_parser(moduleName)
        module.parser(sub)
    args = argparse.Namespace()
    commands = list()
    while argv:
        args,argv =  parser.parse_known_args(argv)
        commands.append(args)
    logger = logging.getLogger('virtimg')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("Virtimg: starting")
    imgMgr = img.Manager()
    for command in commands:
        logger.debug("Running module %s" % (command.command))
        modMgr[command.command].run(imgMgr, command)
    if len(commands) > 0 and not commands[0].nocleanup:
        for oimg in imgMgr:
            os.remove(oimg.path)

if __name__ == "__main__":
    cli_entrypoint()
