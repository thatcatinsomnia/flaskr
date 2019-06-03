from setuptools import find_packages, setup

# this file describes your project and the files that belong to it.
setup(
    name='flaskr',
    version='1.0.0',
    packages = find_packages(), 
    include_package_data = True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

# packages tells Python what package directories to include
# find_packages() finds these directories automatically
# include_package_data to include other data, such as static and templates directories

# the file MANIFEST.in tell python what are the other datas
# content of MANIFEST is to tell Pythonto copy everything in the static and templates directories, 
# and the schema.sql file
# exclude all bytecode files.
