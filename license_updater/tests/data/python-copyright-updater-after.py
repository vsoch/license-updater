__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022-2023, Vanessa Sochat"
__license__ = "MPL 2.0"

__version__ = "0.0.0"
AUTHOR = "Vanessa Sochat"
EMAIL = "vsoch@users.noreply.github.com"
NAME = "license-updater"
PACKAGE_URL = "https://github.com/vsoch/license-updater"
KEYWORDS = "github, license, docstring, header, updater"
DESCRIPTION = "Update license years"
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = (
    ("ruamel.yaml", {"min_version": None}),
    ("rich", {"min_version": None}),
)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)

################################################################################
# Submodule Requirements (versions that include database)

INSTALL_REQUIRES_ALL = INSTALL_REQUIRES + TESTS_REQUIRES
