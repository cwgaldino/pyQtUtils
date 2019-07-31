import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyQtUtils",
    version="0.0.6",
    author="Carlos Galdino",
    author_email="galdino@ifi.unicamp.br",
    description="Utility functions useful when programming and developing pyQt5 applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cwgaldino/pyQtUtils",
    packages=['pyQtUtils'],
    packages_dir={'pyQtUtils': './pyQtUtils'},
    py_modules=['pyQtUtils.pyQt_FSlider',
                'pyQtUtils.pyQt_bundles',
                ],
    package_data={'pyQtUtils': ['*.ui']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
