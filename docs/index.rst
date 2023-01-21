.. _manual-main:

===============
License Updater
===============

.. image:: https://img.shields.io/github/stars/vsoch/license-updater?style=social
    :alt: GitHub stars
    :target: https://github.com/vsoch/license-updater/stargazers

The license updater will make it easy to update license headers:

 - 🥑 Python `__copyright__` years
 - 🥑 Copyright statements in headers
 - 🥑 preview, write to new file, or write in place!

To see the code, head over to the `repository <https://github.com/vsoch/license-updater/>`_.

.. _main-getting-started:

----------------------------------------
Getting started with the License Updater
----------------------------------------

There are two primary functions - to ``detect`` and ``update``!
The first previews changes to a set of files (or directory) and the
second writes the changes to file.

.. code-block:: console

    $ license-updater detect mypackage
    $ license-updater update mypackage

And that's it! The action comes with several :ref:`getting_started_updaters` that will look
for particular aspects to lint or update. If you have a request for a new updater, please
`open an issue <https://github.com/vsoch/license-updater/issues>`_,

The License Updater can be installed from pypi or directly from the repository. See :ref:`getting_started-installation` for
installation, and then the :ref:`getting-started` section for using the client.

.. _main-support:

-------
Support
-------

* For **bugs and feature requests**, please use the `issue tracker <https://github.com/vsoch/license-updater/issues>`_.
* For **contributions**, visit Caliper on `Github <https://github.com/vsoch/license-updater>`_.

---------
Resources
---------

`GitHub Repository <https://github.com/vsoch/license-updater>`_
    The code on GitHub.

.. toctree::
   :caption: Getting started
   :name: getting_started
   :hidden:
   :maxdepth: 2

   getting_started/index
   getting_started/user-guide
   getting_started/developer-guide

.. toctree::
    :caption: API Reference
    :name: api-reference
    :hidden:
    :maxdepth: 4

    source/modules
