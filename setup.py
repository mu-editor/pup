import io
import os
import re

import setuptools



###############################################################################

NAME = "pup"
META_PATH = os.path.join("src", "pup", "__init__.py")
KEYWORDS = ["packaging", "gui", "applications"]
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Installation/Setup",
    "Topic :: System :: Software Distribution",
]
INSTALL_REQUIRES = [
    "importlib-metadata==6.8.0;python_version<'3.8'",
    "click==8.1.6",
    "httpx==0.24.1",
    "wheel==0.40.0",
    "pkginfo==1.9.6",
    "importlib-resources==6.0.0;python_version<'3.9'",
    "cookiecutter==2.2.3",
    "zstandard==0.21.0",
    "dmgbuild==1.6.1;sys_platform=='darwin'",
    "Pillow==10.0.0",
    "requirements-parser==0.5.0",
]
EXTRAS_REQUIRE = {
    "docs": [
        "sphinx",
        "towncrier",
    ],
    "tests": [
        "coverage",
    ],
    "release": [
        "twine",
    ],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["docs"]



###############################################################################

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with io.open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read()



META_FILE = read(META_PATH)

def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))



if __name__ == "__main__":
    setuptools.setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("uri"),
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=read("README.rst"),
        long_description_content_type='text/x-rst',
        packages=setuptools.find_packages(where="src"),
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        entry_points={                                                                    
            'console_scripts': [
                'pup=pup.__main__:main',
            ],
            'pup.plugins': [
                'pup.metadata=pup.plugins.metadata:Step',
                'pup.download=pup.plugins.download:Step',
                'pup.python_runtime=pup.plugins.python_runtime:Step',
                'pup.pip_install=pup.plugins.pip_install:Step',
                'pup.install_cleanup=pup.plugins.install_cleanup:Step',
                'mac.dirs=pup.plugins.mac.dirs:Directories',
                'mac.steps=pup.plugins.mac.steps:Steps',
                'mac.icon_from_png=pup.plugins.mac.icon_from_png:Step',
                'mac.app_bundle_template=pup.plugins.mac.app_bundle:Step',
                'mac.launcher=pup.plugins.mac.launcher:Step',
                'mac.sign_app_bundle=pup.plugins.mac.sign:Step',
                'mac.notarize_app_bundle=pup.plugins.mac.notarize:Step',
                'mac.create_dmg=pup.plugins.mac.create_dmg:Step',
                'win.dirs=pup.plugins.win.dirs:Directories',
                'win.steps=pup.plugins.win.steps:Steps',
                'win.icon_from_png=pup.plugins.win.icon_from_png:Step',
                'win.distribution_layout=pup.plugins.win.dist_layout:Step',
                'win.create_msi=pup.plugins.win.create_msi:Step',
                'win.sign_binaries=pup.plugins.win.signer:SignBinaries',
                'win.sign_msi=pup.plugins.win.signer:SignMSI',
                'linux.dirs=pup.plugins.linux.dirs:Directories',
                'linux.steps=pup.plugins.linux.steps:Steps',
                'linux.appdir_layout=pup.plugins.linux.appdir_layout:Step',
                'linux.appdir_create=pup.plugins.linux.appdir_create:Step',
            ],
        },
        include_package_data=True,
    )

