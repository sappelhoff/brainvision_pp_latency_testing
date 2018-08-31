"""Setup the package."""
from setuptools import setup, find_packages


setup(name='brainvision_pp_latency_testing',
      version='0.0.0',
      description='Latency testing of parallel port (pp) versus Trigger Box '
                  'for BrainVision',
      url='http://github.com/sappelhoff/brainvision_pp_latency_testing',
      author='Stefan Appelhoff',
      author_email='stefan.appelhoff@mailbox.org',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
