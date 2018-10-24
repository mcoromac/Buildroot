################################################################################
#
# jlibfprint
#
################################################################################

JLIBFPRINT_VERSION = 775295f08174d11d39da9e327120b128ef270fc4
JLIBFPRINT_SITE = $(call github,eduardobogoni,jlibfprint,$(JLIBFPRINT_VERSION))
JLIBFPRINT_AUTORECONF = YES
JLIBFPRINT_SUBDIR = JlibFprint_jni
#JLIBFPRINT_CONF_OPTS = --enable-debug-log --enable-udev-rules=no --disable-debug-log
JLIBFPRINT_DEPENDENCIES = libfprint
JLIBFPRINT_INSTALL_STAGING = YES

define PREPARE_FILES_AND_FIX_DIRECTORY
	cd $(@D)/JlibFprint_jni && \
	libtoolize
endef

JLIBFPRINT_PRE_CONFIGURE_HOOKS += PREPARE_FILES_AND_FIX_DIRECTORY

$(eval $(autotools-package))
