################################################################################
#
# python-passport-eye
#
################################################################################

PYTHON_PASSPORT_EYE_VERSION = 1.2.0
PYTHON_PASSPORT_EYE_SOURCE = PassportEye-$(PYTHON_PASSPORT_EYE_VERSION).tar.gz
PYTHON_PASSPORT_EYE_SITE = https://files.pythonhosted.org/packages/73/bb/e74c3ce256a2b7c5c0262348d3b8ed8e49416531715a8c33fc452c2004d9
PYTHON_PASSPORT_EYE_SETUP_TYPE = setuptools
PYTHON_PASSPORT_EYE_DEPENDENCIES = tesseract-ocr

$(eval $(python-package))
