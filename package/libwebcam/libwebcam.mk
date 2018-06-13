################################################################################
#
# libwebcam
#
################################################################################

LIBWEBCAM_VERSION = 0.2.5
LIBWEBCAM_SOURCE = libwebcam-src-$(LIBWEBCAM_VERSION).tar.gz
LIBWEBCAM_SITE = https://sourceforge.net/projects/libwebcam/files
LIBWEBCAM_INSTALL_STAGING = YES
LIBWEBCAM_INSTALL_TARGET = YES
LIBWEBCAM_DEPENDENCIES = libxml2 

$(eval $(cmake-package))
