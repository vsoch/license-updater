.. _getting_started-developer-guide:

===============
Developer Guide
===============

This developer guide includes more complex interactions like contributing
modular updaters. If you haven't read :ref:`getting_started-installation`
you should do that first.

.. _getting_started-developer-guide-linting:


Linting
=======

To lint your code, you can install pre-commit and other dependencies to your environment:

.. code-block:: console

    $ pip install -r .github/dev-requirements.txt


And run:

.. code-block:: console

    $ pre-commit run --all-files


Or install as a hook:

.. code-block:: console

    $ pre-commit install


.. _getting_started-developer-guide-developing-an-updater:


Developing an Updater
=====================

Each updater is required to have one file, ``update.py`` that uses the ``UpdaterBase`` class and
has one function to ``detect``. The easiest way to get this structure is to copy another updater completely,
and use it as a template.

Updater Class
-------------

Your updater class is discovered based on the module folder name. The class should be the uppercase of that,
with ``Updater`` as a suffix. E.g.,:

- python_copyright_metadata -> PythonCopyrightMetadataUpdater

If you don't follow this convention, we won't be able to discover it and use it! You'll also get errors
and know very quickly.

.. _getting_started-developer-guide-updater-metadata:

Updater Metadata
----------------

You are required to have:

- description
- name (typically same as the folder name, but not required) must be all lowercase and only ``-`` for special characters

Here is what the header looks like of the class. Importantly, it needs a regular expression to know what files it matches:

.. code-block:: python

    class PythonCopyrightMetadataUpdater(UpdaterBase):

        name = "python-copyright-updater"
        description = "update __copyright__ in python files"
        file_regex = "[.]py$"



.. _getting_started-developer-guide-updater-detect:


Updater Detect
--------------

Your updater class has a main function ``detect`` that must exist. Any and all other classes are largely optional (and of course encouraged to have a modular design)!
The function should expect a script (``license_updater.main.script.ScriptFile``) to be provided, and to look at ``script.original`` and make updates to ``script.changed``
Note that we:

 - Keep track of self.count, setting it to 0 in the beginning, and incrementing it for each change.
 - Make changes directly to ``script.changed``. Since this is a copy of the original config, this is what will be changed (and saved to file, if desired).
 - Return a boolean to indicate if changes were detected.


.. code-block:: python

    def detect(self, script):
        """
        An example detection function
        """
        # Set the count to 0
        self.count = 0

        # No point if we don't have jobs!
        if not script.original:
            return False

        # Do some kind of detection here
        lines = []
        for line in script.original.split('\n'):

            changed_line = self.has_header_changes(line):
            if changed_line:
                self.count += 1
                lines.append(changed_line)
                continue
            lines.append(line)

        self.changed = "\n".join(lines)
        return self.count != 0


The client will handle displaying changes and otherwise saving updates, so you do not need to
The updater will also be automatically detected and registered, and included in basic testing, however you do need
to add a "before" and "after" set of files, discussed next.

.. _getting_started-developer-guide-testing:

Testing
-------

Each updater should have a ``<name>-before.<ext>`` and ``<name>-after.<ext>`` in ``license_updater/tests/data``.
The format is simple - it should be a text/code file (any of your choosing!) before and after running an update.
The easiest way to make this is to create a "before" file manually (with updates you know need to happen)
(in Python) create a client, run detect, and then write to an after file. And be sure to check that your
updater worked  as you would like! Here is an example (what I used for my test cases):

.. code-block:: python

    from license_updater.main.client import LicenseUpdater
    cli = LicenseUpdater()

    # Before and after files (assuming in present working directory)
    before_file = "python-copyright-updater-before.py"
    after_file = "python-copyright-updater-after.py"

    # Run detect *only* for the updater you care about
    updater = cli.detect(before_file, updaters=['pythoncopyrightupdater'])

    # Write changes to new file (then check it!)
    updater[before_file].write(after_file)


And then visually check it - and you should be done! These files will be used in testing,
along with testing basic output and metadata for your updater. If you have an idea for an updater but
don't have bandwidth to add? Please ping @vsoch by opening an issue!
