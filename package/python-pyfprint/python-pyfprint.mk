################################################################################
#
# python-pyfprint
#
################################################################################

PYTHON_PYFPRINT = 1.0
PYTHON_PYFPRINT_VERSION = b9f67b8531989d7d861687e037ba1b73a84f9067
PYTHON_PYFPRINT_SITE = $(call github,luksan,pyfprint,$(PYTHON_PYFPRINT_VERSION))
PYTHON_PYFPRINT_DEPENDENCIES = libfprint
PYTHON_PYFPRINT_SETUP_TYPE = distutils

$(eval $(python-package))
