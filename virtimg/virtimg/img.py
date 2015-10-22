#!/usr/bin/python2

class Manager(object):
    def __init__(self):
        self.images = []

    def __iter__(self):
        for item in self.images:
            yield item

    def __getitem__(self, name):
        (x for x in self.images if x.name == name).next()

    def add(self, image):
        if isinstance(image, Image):
            self.images.append(image)

    def add(self, name, path):
        self.images.append(Image(name, path))

class Image(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
