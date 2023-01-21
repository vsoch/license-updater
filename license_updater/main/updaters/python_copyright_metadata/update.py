__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022-2023, Vanessa Sochat"
__license__ = "MPL 2.0"

import re
from datetime import datetime

from license_updater.main.updater import UpdaterBase


class PythonCopyrightMetadataUpdater(UpdaterBase):

    name = "python-copyright-updater"
    description = "update __copyright__ in python files"
    file_regex = "[.]py$"

    def detect(self, script):
        """
        Detect changes in an action, old set-state.
        """
        # Set the count to 0
        self.count = 0

        # No point if we don't have jobs!
        if not script.original:
            return False

        # For each line, look for copyright regular expression
        lines = []
        for line in script.original.split("\n"):
            if "__copyright__" in line:

                if self.is_up_to_date(line):
                    lines.append(line)
                    continue

                updated_line = self.match_date_range(line)
                if updated_line:
                    self.count += 1
                    lines.append(updated_line)
                    continue

                updated_line = self.match_date(line)
                if updated_line:
                    self.count += 1
                    lines.append(updated_line)
                    continue

            # Appent original line, no updates
            lines.append(line)

        script.changes = "\n".join(lines)
        return self.count != 0

    def match_date(self, line):
        """
        Match Case 2: a single year
        """
        # Get the current year
        year = str(datetime.now().year)

        match = re.search(
            "(?P<start>Copyright\s+)(?P<fromyear>[0-9]{4})", line, re.IGNORECASE  # noqa
        )
        if not match:
            return

        group = match.groupdict()

        # The year was already updated!
        if group["fromyear"] == year:
            return

        start = line[: match.start()]
        end = line[match.end() :]
        middle = f"{group['fromyear']}-{year}"
        return f"{start}{group['start']}{middle}{end}"

    def is_up_to_date(self, line):
        """
        An up to date line has a date range that is correct!
        """
        # Get the current year
        year = str(datetime.now().year)

        match = re.search(
            "(?P<start>Copyright\s+)(?P<fromyear>[0-9]{4})-(?P<toyear>[0-9]{4})",  # noqa
            line,
            re.IGNORECASE,
        )
        if not match:
            return False
        group = match.groupdict()

        # Already updated
        if group["toyear"] == year:
            return True
        return False

    def match_date_range(self, line):
        """
        Match Case 2: a range of years (2022-2023)
        """
        # Get the current year
        year = str(datetime.now().year)

        match = re.search(
            "(?P<start>Copyright\s+)(?P<fromyear>[0-9]{4})-(?P<toyear>[0-9]{4})",  # noqa
            line,
            re.IGNORECASE,
        )
        if not match:
            return
        group = match.groupdict()

        # Already updated
        if group["toyear"] == year:
            return

        start = line[: match.start()]
        end = line[match.end() :]
        middle = f"{group['start']}{group['fromyear']}-{year}"
        return f"{start}{middle}{end}"
