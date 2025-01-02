from setuptools import setup

APP = ["app/paint_app.py"]
DATA_FILES = ['./app/assets']
OPTIONS = {'includes': ['PyQt6', 'app'], 'excludes': ['setuptools']}

setup(
    name="Paint App",
    version="1.0.0",
    description="A useful application for paint",
    author="Vaman",
    author_email="vamanrajagopal@gmail.com",
    license="MIT",
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)