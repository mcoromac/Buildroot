################################################################################
#
# libfprint
#
################################################################################

LIBFPRINT_VERSION = 0.6.0
LIBFPRINT_SOURCE = libfprint-$(LIBFPRINT_VERSION).tar.xz
LIBFPRINT_SITE = https://people.freedesktop.org/~anarsoul
LIBFPRINT_CONF_OPTS = --enable-debug-log --enable-udev-rules=no --enable-static=yes --enable-examples-build=yes
LIBFPRINT_INSTALL_STAGING = YES

LIBFPRINT_DEPENDENCIES = pixman libglib2 libnss libusb libopenssl 

$(eval $(autotools-package))
