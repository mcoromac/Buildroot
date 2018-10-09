################################################################################
#
# c-periphery
#
################################################################################

C_PERIPHERY_VERSION = v1.1.1
C_PERIPHERY_SITE = $(call github,vsergeev,c-periphery,$(C_PERIPHERY_VERSION))
C_PERIPHERY_INSTALL_STAGING = YES
# only a static library
C_PERIPHERY_INSTALL_TARGET = YES
C_PERIPHERY_LICENSE = MIT
C_PERIPHERY_LICENSE_FILES = LICENSE

define C_PERIPHERY_BUILD_CMDS
	$(TARGET_MAKE_ENV) $(TARGET_CONFIGURE_OPTS) $(MAKE) -C $(@D)
endef

# There is no 'install' rule in the Makefile, so we handle things
# manually.
define C_PERIPHERY_INSTALL_STAGING_CMDS
	$(INSTALL) -D -m 0644 $(@D)/periphery.a $(STAGING_DIR)/usr/lib/libc-periphery.a
	mkdir -p $(STAGING_DIR)/usr/include/c-periphery/
	cp -dpfr $(@D)/src/*.h $(STAGING_DIR)/usr/include/c-periphery/
endef

define SAVE_OBJ_AS_SHARED_LIBRARY
	$(HOST_DIR)/bin/arm-linux-gnueabihf-ld -shared $(@D)/obj/i2c.o -o $(@D)/libperipheryi2c.so
	$(HOST_DIR)/bin/arm-linux-gnueabihf-ld -shared $(@D)/obj/spi.o -o $(@D)/libperipheryspi.so
	$(HOST_DIR)/bin/arm-linux-gnueabihf-ld -shared $(@D)/obj/serial.o -o $(@D)/libperipheryserial.so
	$(HOST_DIR)/bin/arm-linux-gnueabihf-ld -shared $(@D)/obj/mmio.o -o $(@D)/libperipherymmio.so
endef
 
C_PERIPHERY_POST_INSTALL_TARGET_HOOKS += SAVE_OBJ_AS_SHARED_LIBRARY
$(eval $(generic-package))
