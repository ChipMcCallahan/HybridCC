from setuptools import setup, find_packages

setup(
    name='hybrid_cc',
    url='https://github.com/ChipMcCallahan/HybridCC',
    author='Chip McCallahan',
    author_email='thisischipmccallahan@gmail.com',
    packages=find_packages(where="src"),
    package_data={
        'hybrid_cc': [
            'art/*/*',  # 2 levels deep
            'sets/*/*',  # 2 levels deep
            'solutions/json/*',  # 1 level deep
            'sfx/*/*'  # 2 levels deep
        ]
    },
    package_dir={"": "src"},
    install_requires=[
        'setuptools==69.0.3',
        'cc-tools @ git+https://github.com/ChipMcCallahan/CCTools.git@main',
        'pygame==2.5.2'
    ],
    version='0.1',
    license='LICENSE',
    description='Hybrid ruleset for playing certain tile-based games.',
    # long_description=open('README.txt').read(),
)
