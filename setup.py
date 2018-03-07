import nltk
from pip.req import parse_requirements
from setuptools import setup, find_packages
from setuptools.command.install import install

package = 'bsdetector'
version = '0.1'


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        nltk.download('punkt')
        install.run(self)


install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

print(find_packages('bsdetector'))
setup(name=package,
      version=version,
      # packages=['bsdetector', 'lexicons', 'additional_resources'],
      packages=['nltk', 'bsdetector', 'lexicons'],
      install_requires=reqs,
      package_dir={'bsdetector': 'bsdetector'},
      package_data={'bsdetector': ['*.json']},
      description="Detects biased statements in online media documents",
      url='url',
      cmdclass={
          'install': PostInstallCommand,
      }
      )
