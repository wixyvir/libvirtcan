#!/bin/bash
#
# Cyprien DIOT <wixyvir@gmail.com>
# Basic run script for manage-virt-img 


 docker run -e 'OS_USERNAME' -e 'OS_AUTH_URL' -e 'OS_TENANT_ID' -e 'OS_TENANT_NAME' -e 'OS_PASSWORD' -it registry.srv-docker/manage-virt-img bash
