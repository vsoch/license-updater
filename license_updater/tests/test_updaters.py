#!/usr/bin/python

# Copyright (C) 2022 Vanessa Sochat.

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import string

import pytest

from license_updater.main.script import ScriptFile 
from license_updater.tests.helpers import get_updaters, here, init_client


@pytest.mark.parametrize("updater_name", get_updaters())
def test_updaters(updater_name):
    """
    Test each updater.
    """
    client = init_client()
    updater = client.updaters[updater_name]

    # The updater must have a description and title
    assert updater.description
    assert updater.title

    # The name must be all lowercase, no special characters except for -
    letters = string.ascii_letters + "-"
    for letter in updater.name:
        assert letter in letters

    # A test (before and after) must be defined for each
    before_file = os.path.join(here, "data", f"{updater.name}-before.py")
    after_file = os.path.join(here, "data", f"{updater.name}-after.py")
    for filename in before_file, after_file:
        assert os.path.exists(filename)

    # Count is 0 before run, and we find changes
    assert updater.count == 0

    # Read into GitHub action
    script = ScriptFile(before_file)

    # Run the whole thing with detect (to print to console)
    result = client.detect(before_file, updaters=[updater.slug])
    result[before_file].original == script.changes

    result = updater.detect(script)
    assert result is True
    assert script.has_changes

    # Count is 0 before run, and we find changes
    assert updater.count != 0

    # Now for the after file (shouldn't change until GitHub updates versions, slowly)
    script = ScriptFile(after_file)
    result = updater.detect(script)
    assert result is False
