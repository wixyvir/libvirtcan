# libvirtcan docker image

This Dockerfile builds a docker image for OpenStack/libvirt images management.

It uses `virtimg` a python project, see the according subfolder.

## Build and push the image

First, build `virtimg` pip package, see `virtimg` subfolder.

* `docker build -t registry.srv-docker/manage-virt-img .`

* `docker push registry.srv-docker/manage-virt-img `

