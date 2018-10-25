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

define CREATE_JAR
	cd $(@D)/JlibFprint && \
	mvn install
endef
JLIBFPRINT_PRE_CONFIGURE_HOOKS += PREPARE_FILES_AND_FIX_DIRECTORY
JLIBFPRINT_POST_BUILD_HOOKS += CREATE_JAR
$(eval $(autotools-package))
