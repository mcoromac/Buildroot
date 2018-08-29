################################################################################
#
# jlibfprint
#
################################################################################

JLIBFPRINT_VERSION = 775295f08174d11d39da9e327120b128ef270fc4
JLIBFPRINT_SITE = $(call github,eduardobogoni,jlibfprint,$(JLIBFPRINT_VERSION))
#JLIBFPRINT_CONF_OPTS = --enable-debug-log --enable-udev-rules=no --disable-debug-log

JLIBFPRINT_INSTALL_STAGING = YES

define PREPARE_FILES_AND_FIX_DIRECTORY
	cd $(@D)/JlibFprint_jni && \
	libtoolize && \
	./autogen.sh
endef

define JLIBFPRINT_CONFIGURE_CMDS
	cd /home/mariano/buildroot/output/build/jlibfprint-775295f08174d11d39da9e327120b128ef270fc4/JlibFprint_jni/build && rm -rf \
	config.cache && \
	PATH="/home/mariano/buildroot/output/host/bin:/home/mariano/buildroot/output/host/sbin:/home/mariano/bin:/home/mariano/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
	AR="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-ar" \
	AS="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-as" \
	LD="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-ld" \
	NM="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-nm" \
	CC="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-gcc" \
	GCC="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-gcc" \
	CPP="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-cpp" \
	CXX="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-g++" \
	FC="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-gfortran" \
	F77="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-gfortran" \
	RANLIB="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-ranlib" \
	READELF="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-readelf" \
	STRIP="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-strip" \
	OBJCOPY="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-objcopy" \
	OBJDUMP="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-objdump" \
	AR_FOR_BUILD="/usr/bin/ar" AS_FOR_BUILD="/usr/bin/as" CC_FOR_BUILD="/usr/bin/gcc" \
	GCC_FOR_BUILD="/usr/bin/gcc" CXX_FOR_BUILD="/usr/bin/g++" LD_FOR_BUILD="/usr/bin/ld" \
	CPPFLAGS_FOR_BUILD="-I/home/mariano/buildroot/output/host/include" CFLAGS_FOR_BUILD="-O2 \
	-I/home/mariano/buildroot/output/host/include" CXXFLAGS_FOR_BUILD="-O2 -I/home/mariano/buildroot/output/host/include" \
	LDFLAGS_FOR_BUILD="-L/home/mariano/buildroot/output/host/lib -Wl,-rpath,/home/mariano/buildroot/output/host/lib" \
	FCFLAGS_FOR_BUILD="" DEFAULT_ASSEMBLER="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-as" \
	DEFAULT_LINKER="/home/mariano/buildroot/output/host/bin/arm-linux-gnueabihf-ld" CPPFLAGS="-D_LARGEFILE_SOURCE \
	-D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64" CFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  \
	-Os " CXXFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64  -Os " LDFLAGS="" FCFLAGS=" -Os " \
	FFLAGS=" -Os " PKG_CONFIG="/home/mariano/buildroot/output/host/bin/pkg-config" \
	STAGING_DIR="/home/mariano/buildroot/output/host/arm-buildroot-linux-gnueabihf/sysroot" \
	INTLTOOL_PERL=/usr/bin/perl ac_cv_lbl_unaligned_fail=yes ac_cv_func_mmap_fixed_mapped=yes \
	ac_cv_func_memcmp_working=yes ac_cv_have_decl_malloc=yes gl_cv_func_malloc_0_nonnull=yes \
	ac_cv_func_malloc_0_nonnull=yes ac_cv_func_calloc_0_nonnull=yes ac_cv_func_realloc_0_nonnull=yes \
	lt_cv_sys_lib_search_path_spec="" ac_cv_c_bigendian=no   CONFIG_SITE=/dev/null \
	../configure \
	--target=arm-buildroot-linux-gnueabihf --host=arm-buildroot-linux-gnueabihf --build=x86_64-pc-linux-gnu --prefix=/usr \
	--exec-prefix=/usr --sysconfdir=/etc --localstatedir=/var --program-prefix="" --disable-gtk-doc --disable-gtk-doc-html \
	--disable-doc --disable-docs --disable-documentation --with-xmlto=no --with-fop=no --disable-dependency-tracking --enable-ipv6 \
	--disable-nls --disable-static --enable-shared
endef

#define JLIBFPRINT_BUILD_CMDS
#	cd $(@D)/JlibFprint_jni/build && \
#	make
#endef
JLIBFPRINT_PRE_CONFIGURE_HOOKS += PREPARE_FILES_AND_FIX_DIRECTORY

$(eval $(autotools-package))
