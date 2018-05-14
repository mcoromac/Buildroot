################################################################################
#
# python-fprynt
#
################################################################################

PYTHON_FPRYNT = 1.0
PYTHON_FPRYNT_VERSION = 505af6b46404000e286352de83be96ddd2241f1b
PYTHON_FPRYNT_SITE = $(call github,hfeeki,fprynt,$(PYTHON_FPRYNT_VERSION))
PYTHON_FPRYNT_DEPENDENCIES = libfprint boost
PYTHON_FPRYNT_INSTALL_STAGING = YES

$(eval $(cmake-package))
