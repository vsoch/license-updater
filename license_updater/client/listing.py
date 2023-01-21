__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022-2023, Vanessa Sochat"
__license__ = "MPL 2.0"

import license_updater.main.client as client
from license_updater.logger import Table


def list_updaters(args, parser, extra, subparser):
    cli = client.LicenseUpdater(quiet=args.quiet)

    items = [
        {"title": x.title, "identifier": name, "description": x.description}
        for name, x in cli.updaters.items()
    ]
    table = Table(items)
    table.show()
