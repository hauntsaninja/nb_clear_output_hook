from setuptools import setup

setup(
    name="nb_clear_output",
    version="0.2.0",
    py_modules=["nb_clear_output"],
    install_requires=["nbformat"],
    entry_points={"console_scripts": ["nb_clear_output=nb_clear_output:main"]},
)
