#!/usr/bin/python

# Copyright (C) 2022 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil

from license_updater.main.client import LicenseUpdater

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)


def init_client():
    """
    Get a common client for some container technology and module system
    """
    return LicenseUpdater(quiet=False)

def get_updaters():
    client = init_client()
    return client.updaters
