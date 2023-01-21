__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022-2023, Vanessa Sochat"
__license__ = "MPL 2.0"

import license_updater.main.client as client
from license_updater.logger import logger

from .helpers import parse_updaters


def main(args, parser, extra, subparser):
    cli = client.LicenseUpdater(quiet=args.quiet)
    cli.detect(
        paths=args.paths,
        details=not args.no_details,
        updaters=parse_updaters(args),
        ignore_patterns=args.ignore_patterns,
    )
    if cli.has_changes:
        logger.exit("Found changes, exiting with non-zero code.")
