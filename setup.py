from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='hybrid_cc',
    url='https://github.com/ChipMcCallahan/HybridCC',
    author='Chip McCallahan',
    author_email='thisischipmccallahan@gmail.com',
    # Needed to actually package something
    packages=['hybrid_cc'],
    package_dir={'hybrid_cc': 'src'},
    # Needed for dependencies
    install_requires=[
    ],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='LICENSE',
    description='Hybrid ruleset for playing CC1 DAT files.',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)