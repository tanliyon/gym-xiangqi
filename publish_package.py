"""
Helper script to publish package to PyPI.
Dependencies are:
- Wheel
- Twine
- Python
"""

import os


def main():
    # Remove any existing build files.
    os.system("rm -rf build/* dist/*")
    # Build and check files.
    os.system("python -m setup.py bdist_wheel sdist")
    os.system("twine check dist/*")
    # Choose to upload to PyPI or test PyPI
    site = input("Uploading to PyPI or test-PyPI? ")
    if site.lower() == "pypi":
        os.system("twine upload dist/*")
    elif site.lower() == "test-pypi":
        os.system("twine upload "
                  "--repository-url https://test.pypi.org/legacy/ dist/*")
    else:
        print("Invalid option! Please choose either pypi or test-pypi!")


if __name__ == "__main__":
    main()
