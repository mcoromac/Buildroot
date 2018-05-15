################################################################################
#
# python-pyfprint
#
################################################################################

PYTHON_PYFPRINT = 1.0
PYTHON_PYFPRINT_VERSION = tab6
PYTHON_PYFPRINT_SITE = $(call github,mcoromac,pyfprint-cffi,$(PYTHON_PYFPRINT_VERSION))
PYTHON_PYFPRINT_DEPENDENCIES = libfprint python-cffi python-pillow
PYTHON_PYFPRINT_SETUP_TYPE = distutils

$(eval $(python-package))
