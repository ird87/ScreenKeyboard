import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="screen-keyboard-pkg-ird87", # Replace with your own username
    version="0.1.51",
    author="ird87",
    author_email="ird87.post.ru@gmail.com",
    description="customizable on-screen keyboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ird87/ScreenKeyboard",
    packages=setuptools.find_packages(),
    use_scm_version={'write_to': 'my-package/version.py'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=["evdev>=1.4.0","lxml>=4.6.2","Pillow>=7.2.0","python-xlib>=0.29","six>=1.15.0]"],
    python_requires='>=3.5',
)




    
    