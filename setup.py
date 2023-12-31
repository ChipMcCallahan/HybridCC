from setuptools import setup, find_packages

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='hybrid_cc',
    url='https://github.com/ChipMcCallahan/HybridCC',
    author='Chip McCallahan',
    author_email='thisischipmccallahan@gmail.com',
    # Needed to actually package something
    packages=find_packages(where="src"),
    package_data={
        'hybrid_cc': [
            'art/*/*',  # 2 levels deep
            'sets/*/*',  # 2 levels deep
            'replays/*'  # 1 level deep
        ]
    },
    package_dir={"": "src"},
    # Needed for dependencies
    install_requires=[
    ],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='LICENSE',
    description='Hybrid ruleset for playing certain tile-based games.',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
