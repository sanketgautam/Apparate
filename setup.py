from setuptools import setup, find_packages

setup(
    name='apparate',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click==6.7",
        "PyGithub==1.39",
        "selenium==3.12.0"
    ],
    entry_points='''
        [console_scripts]
        apparate=scripts.apparate:apparate
    ''',
)
