# standard imports
import logging
import subprocess
import time

# third-party imports
import semver

# local imports

logg = logging.getLogger()

version = (0, 2, 0, 'alpha.3')

version_object = semver.VersionInfo(
    major=version[0],
    minor=version[1],
    patch=version[2],
    prerelease=version[3],
)

version_string = str(version_object)
