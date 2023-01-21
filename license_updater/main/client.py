__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022-2023, Vanessa Sochat"
__license__ = "MPL 2.0"

import os
import re

from rich.console import Console
from rich.markdown import Markdown

import license_updater.defaults as defaults
import license_updater.utils as utils

from .script import ScriptFile
from .updater import UpdaterFinder


class LicenseUpdater:
    """
    Create a License Updater
    """

    def __init__(self, quiet=False, code_theme="vim", **kwargs):
        self._updaters = {}
        self.quiet = quiet
        self.code_theme = code_theme
        self.c = Console()

        # Keep a summary of updates
        self.summary = {}

        # If using for a GitHub action, a global flag that indicates changes
        self.has_changes = False

    @property
    def updaters(self):
        """
        Get a list of updaters available
        """
        if not self._updaters:

            # All updaters can be provided with the GitHub token
            self.finder = UpdaterFinder()
            self._updaters = {}
            for name, updaterClass in self.finder.items():

                # Instantiate an updater for the path, provide settings
                self._updaters[name] = updaterClass()

        return self._updaters

    def iter_paths(self, paths):
        """
        Helper function to flexibly handle parsing paths.
        """
        # Ensure we start from a list
        if not isinstance(paths, list):
            paths = [paths]

        final = set()

        # Run each updater on each path
        for path in paths:
            if path == ".":
                path = os.getcwd()
            if os.path.exists(path) and os.path.isfile(path):
                final.add(path)
                continue
            for filename in utils.recursive_find(path, defaults.supported_filetypes):
                final.add(filename)
        return list(final)

    def detect(self, paths, details=True, updaters=None, ignore_patterns=None):
        """
        Look for changes in files according to updaters
        """
        ignore_patterns = ignore_patterns or []
        if ignore_patterns:
            ignore_patterns = "(%s)" % "|".join(ignore_patterns)
        scripts = {}

        # Reset out summary
        self.summary = {}

        for path in self.iter_paths(paths):

            # Ignore patterns that match a user provided pattern!
            if ignore_patterns and re.search(ignore_patterns, path):
                continue

            # Load into script
            script = ScriptFile(path)

            showed_script = False

            # Todo convert this into an iter function (shared between detect and update)
            for _, updater in self.updaters.items():

                # Skip updaters per request of the user
                if updaters and updater.slug not in updaters:
                    continue

                # Don't print anything if no match
                if not updater.matches(path):
                    continue

                # The count reflects the last run
                if updater.detect(script):
                    if not showed_script:
                        self.c.print(f"⭐️ [yellow]{path}[/yellow]")
                        showed_script = True
                    self.c.print(f"[red]✖️ {updater.title} Updater: {updater.count} updates[/red]")
                    self.has_changes = True
                else:
                    if not showed_script:
                        self.c.print(f"⭐️ [yellow]{path}[/yellow]")
                        showed_script = True
                    self.c.print(f"[green]✔ {updater.title}: No updates[/green]")

            # If we want to show summary details:
            if details and script.has_changes:
                self.collect_summary(script)
            scripts[path] = script

        if details:
            self.show_summary()
        return scripts

    def show_summary(self):
        """
        Show summary of changes
        """
        if not self.summary:
            md = Markdown("""\n# No changes\n""", code_theme=self.code_theme)
            self.c.print(md)
            return

        # Sort by counts
        self.summary = {k: v for k, v in sorted(self.summary.items(), key=lambda item: item[1])}
        md = Markdown("""\n# Summary of changes\n""", code_theme=self.code_theme)
        self.c.print(md)
        total = 0

        for diff, count in self.summary.items():
            md = Markdown(
                f"""\n```diff\n{diff}\n```\n- count: {count}\n""", code_theme=self.code_theme
            )
            self.c.print(md)
            total += count

        # Show total count!
        md = Markdown(f"""## Total count: {total}\n""", code_theme=self.code_theme)
        self.c.print(md)

    def collect_summary(self, script):
        """
        Collect a summary of the changes
        """
        summary = script.diff(self.code_theme, return_result=True)
        if not summary:
            return
        if summary not in self.summary:
            self.summary[summary] = 0
        self.summary[summary] += 1

    def update(self, paths, details=True, updaters=None, ignore_patterns=None):
        """
        Update files.
        """
        updates = self.detect(
            paths, details=details, updaters=updaters, ignore_patterns=ignore_patterns
        )
        for path, script in updates.items():
            if script.has_changes:
                self.c.print(f"[purple]❇ Writing updated {path}[/purple]")
                script.write(path)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "[license-updater]"
