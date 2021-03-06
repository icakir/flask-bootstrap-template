import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='flask_blog',
    description='Personal Blog',
    author='Martin C Drohmann',
    author_email='mdrohmann@gmail.com',
    version='3.0',
    scripts=[
        'scripts/mk_booklet.py'],
    install_requires=[
        'py-bcrypt',
        'passlib',
        'markdown',
        'translitcodec',
        'Flask',
        'Flask-Login',
        'Flask-DebugToolbar',
        'Flask-Mail',
        'Flask-WTF',
        'flup',
        'PyYAML'],
    test_suite='tests',
    tests_require=['pytest', 'pytest-cov'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='LICENSE',
    cmdclass={'test': PyTest},
    url='http://tallygist.com',
    )
