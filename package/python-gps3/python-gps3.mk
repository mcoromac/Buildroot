################################################################################
#
# python-gps3
#
################################################################################

PYTHON_GPS3 = 0.33.3
PYTHON_GPS3_VERSION = 91adcd7073b891b135b2a46d039ce2125cf09a09
PYTHON_GPS3_SITE = $(call github,wadda,gps3,$(PYTHON_GPS3_VERSION))
PYTHON_GPS3_DEPENDENCIES = gpsd
PYTHON_GPS3_SETUP_TYPE = setuptools

$(eval $(python-package))
