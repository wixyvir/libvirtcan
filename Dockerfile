FROM ubuntu:latest

#
# manage-virt-img
# Cyprien DIOT <wixyvir@gmail.com>
# Manage Qcow2/Raw disk images
#

MAINTAINER  Cyprien DIOT <cyprien.diot@pmsipilot.com>
RUN DEBIAN_FRONTEND=noninteractive apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libguestfs-tools libvirt-bin wget 
RUN update-guestfs-appliance
RUN wget http://libguestfs.org/download/binaries/appliance/appliance-`dpkg -s libguestfs0  | grep Version | awk '{ split($2,a,":"); split(a[2], b, "-"); print b[1] }'`.tar.xz && tar -xf appliance-*.tar.xz -C /
ENV LIBGUESTFS_PATH /appliance
RUN apt-get update && apt-get install -y python-glanceclient python-pip python-novaclient
COPY virtimg/dist/virtimg-*.tar.gz /root/
RUN pip install /root/virtimg-*.tar.gz
ENTRYPOINT [ "/usr/local/bin/virtimg" ]




