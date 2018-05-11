################################################################################
#
# fingerprint
#
################################################################################

FINGERPRINT_VERSION = 1.0.0
FINGERPRINT_SITE = $(TOPDIR)/board/startrack/tab6/Scripts
FINGERPRINT_SITE_METHOD = local
FINGERPRINT_INSTALL_STAGING = YES
FINGERPRINT_DEPENDENCIES = libfprint

#Tells what steps should be performed to build the package, @D is the build directory
#TARGET_CONFIGURE_OPTS tells to cross compile for my target

define FINGERPRINT_BUILD_CMDS
	$(MAKE) $(TARGET_CONFIGURE_OPTS) -C $(@D) all
endef

#This just takes the cross compiled program and places it in the target files system
define FINGERPRINT_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/fingerprint $(TARGET_DIR)/home/Startrack/fingerprint

endef

$(eval $(generic-package))
