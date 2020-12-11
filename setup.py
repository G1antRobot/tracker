from setuptools import setup, find_packages

setup(name="ETCCTracker",
      version="1.0.0",
      py_modules=find_packages("app"),
      entry_points={
          'console_scripts': ["trackit=main:main"]
      },
      url='https://github.com/G1antRobot/tracker',
      classifiers=[
          'Programming Language :: Python :: 3.7'
      ]
      )