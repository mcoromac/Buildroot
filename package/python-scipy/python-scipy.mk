################################################################################
#
# python-scipy
#
################################################################################

PYTHON_SCIPY_VERSION = 1.1.0
PYTHON_SCIPY_SOURCE = scipy-$(PYTHON_SCIPY_VERSION).tar.gz
PYTHON_SCIPY_SITE = https://files.pythonhosted.org/packages/07/76/7e844757b9f3bf5ab9f951ccd3e4a8eed91ab8720b0aac8c2adcc2fdae9f
PYTHON_SCIPY_DEPENDENCIES = python-numpy
PYTHON_SCIPY_SETUP_TYPE = setuptools

$(eval $(python-package))
