from setuptools import find_packages, setup

setup(
    name="bazy_danych",
    version="0.0.1",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
