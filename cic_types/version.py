# standard imports
import os
import subprocess
import time

# third-party imports
import semver

# local imports


def git_hash():
    build_value = None
    try:
        g_hash = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True)
        build_value = g_hash.stdout.decode('utf-8')[:8]
        return f'build.{build_value}'
    except FileNotFoundError:
        time_string_pair = str(time.time()).split('.')
        build_value += '+build.{}{:<09d}'.format(
            time_string_pair[0],
            int(time_string_pair[1])
        )
        return build_value


version = (0, 1, 0, 'alpha.1', git_hash())

version_string = semver.VersionInfo(
    major=version[0],
    minor=version[1],
    patch=version[2],
    prerelease=version[3],
    build=version[4]
)


def generate_version_file():
    root_directory = os.path.dirname(os.path.dirname(__file__))
    file_name = 'VERSION'
    file_path = os.path.join(root_directory, file_name)
    version_file = open(file_path, 'w+')
    __version__ = str(version_string)
    version_file.write(__version__)
    version_file.close()


if __name__ == '__main__':
    generate_version_file()