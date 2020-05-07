import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ehr-fhir-converter-kclconsult",
    version="0.0.1",
    author="Martin Chapman",
    author_email="martin.chapman@kcl.ac.uk",
    description="Convert arbitrary EHR extracts to FHIR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kclconsult/ehr-fhir-converter",
    packages=setuptools.find_packages(""),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['pytest'],
    setup_requires=["pytest-runner"]
)
