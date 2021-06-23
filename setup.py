# standard imports
from html.parser import HTMLParser
from setuptools import setup
from setuptools.dist import Distribution
from urllib import request

# third-party imports

# local imports
from cic_types.error import VersionBumpError
from cic_types.version import version_string


requirements = []
requirements_file = open('requirements.txt', 'r')
while True:
    requirement = requirements_file.readline()
    if requirement == '':
        break
    requirements.append(requirement.rstrip())
requirements_file.close()

test_requirements = []
test_requirements_file = open('test_requirements.txt', 'r')
while True:
    test_requirement = test_requirements_file.readline()
    if test_requirement == '':
        break
    test_requirements.append(test_requirement.rstrip())
test_requirements_file.close()


def wheel_name(**kwargs):
    # create a fake distribution from arguments
    dist = Distribution(attrs=kwargs)

    # finalize bdist_wheel command
    bdist_wheel_cmd = dist.get_command_obj('bdist_wheel')
    bdist_wheel_cmd.ensure_finalized()

    # assemble wheel file name
    dist_name = bdist_wheel_cmd.wheel_dist_name
    tag = '-'.join(bdist_wheel_cmd.get_tag())

    return f'{dist_name}-{tag}.whl'


class IndexParser(HTMLParser):

    def __init__(self, canonical_package_name: str):
        """
        :param canonical_package_name:
        :type canonical_package_name:
        """
        super().__init__()
        self.canonical_package_name = canonical_package_name

    def handle_data(self, data):
        if self.canonical_package_name in data:
            raise VersionBumpError(f'A similar version was found in the the registry: {data}.')
        pass


def check_index_version(package_name: str, registry_host: str = "https://pip.grassrootseconomics.net:8433"):
    """ This function checks a self hosted registry for the existence of a package with a finalized version format
    matching the one being built.
    :param package_name: The name of the package being built.
    :type package_name: str
    :param registry_host: The url pointing to self-hosted registry in which packages are stored
    :type registry_host: str
    :raises VersionBumpError: If the package version at build time matches one already in the registry.
    """
    package_url = f'{registry_host}/{package_name}'

    # get packages in registry host
    req = request.urlopen(package_url)
    page_data = req.read().decode()

    # define finalized canonical package name
    canonical_package_name = wheel_name(name=package_name, version=version_string)
    canonical_package_name = canonical_package_name.split('+')[0]

    # check remote registry
    parser = IndexParser(canonical_package_name)
    parser.feed(page_data)


check_index_version('cic-types')

setup(
    install_requires=requirements,
    tests_require=test_requirements,
)
