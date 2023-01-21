__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022-2023, Vanessa Sochat"
__license__ = "MPL 2.0"


import copy
import difflib

from rich.console import Console
from rich.markdown import Markdown

import license_updater.utils as utils


class ScriptFile:
    """
    Parse a script and/or file into the updater.

    We always present the changes (copy of original) and then can
    easily compare the two. The overall structure should not change.
    """

    def __init__(self, filename):
        self.original = utils.read_file(filename)
        self.changes = copy.deepcopy(self.original)
        self.path = filename

    def write(self, path):
        """
        Save the action to file.
        """
        utils.write_file(self.changes, path)

    @property
    def has_changes(self):
        """
        Determine if before != after (the action has changed)
        """
        return self.changes != self.original

    def diff(self, code_theme="vim", return_result=False):
        """
        Show diff between original (cfg) and changed!
        """
        before = self.original
        after = self.changes

        # No changes
        if before == after:
            print()
            return

        diff = "\n".join(
            list(
                difflib.unified_diff(
                    before.split("\n"),
                    after.split("\n"),
                    "original",
                    "updated",
                    n=1,
                )
            )
        )

        if return_result:
            return diff
        c = Console()
        md = Markdown(f"""\n```diff\n{diff}\n```\n""", code_theme=code_theme)
        c.print(md)
