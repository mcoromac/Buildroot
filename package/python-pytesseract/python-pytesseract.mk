################################################################################
#
# python-pytesseract
#
################################################################################

PYTHON_PYTESSERACT_VERSION = 0.2.2
PYTHON_PYTESSERACT_SOURCE = pytesseract-$(PYTHON_PYTESSERACT_VERSION).tar.gz
PYTHON_PYTESSERACT_SITE = https://files.pythonhosted.org/packages/c8/bb/62ac168973155ee3277971594b8739ef9873d07fdb0835ab3da43d43541a
PYTHON_PYTESSERACT_SETUP_TYPE = setuptools
PYTHON_PYTESSERACT_DEPENDENCIES = tesseract-ocr

$(eval $(python-package))
