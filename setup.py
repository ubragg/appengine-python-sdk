import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appengine-python-protobuf",
    version="0.0.1",
    author="Google LLC",
    description="legacy Google App Engine services SDK for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ubragg/appengine-python-sdk",
    packages=setuptools.find_packages(),
    namespace_packages=["google"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6, <4",
)
