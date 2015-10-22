#!/bin/python2

import os, sys, imp
import logging

class ModulesManager(object):
    def __init__(self):
        self.logger = logging.getLogger('virtimg')
        self.modules=dict()

    def __iter__(self):
        return iter(self.modules.items())

    def __getitem__(self, value):
        return self.modules[value]

    def loadModules(self):
        import pkgutil
        path = os.path.join(os.path.dirname(__file__), "modules")
        sys.path.append(path);
        modules = pkgutil.iter_modules(path=[path])
        for loader, mod_name, ispkg in modules:
            if mod_name not in sys.modules and mod_name not in self.modules:
                fp, pathname, description = imp.find_module(mod_name)
                module = None
                try:
                    module=imp.load_module(mod_name, fp, pathname, description)
                finally:
                    if fp:
                        fp.close()
                try:
                    if ( module 
                         and callable(getattr(module,'parser'))
                         and callable(getattr(module,'run')) ):
                        self.modules[mod_name] = module
                    else:
                        raise AttributeError
                except AttributeError:
                    self.logger.warn("Module %s is missing mandatory functions: requires, parser, run: ignoring" % (mod_name))



