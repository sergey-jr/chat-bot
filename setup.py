from setuptools import setup
import setuptools

setup(name='scheduler',
      version='1',
      description='Scheduler bot for VSUET',
      url='https://github.com/sergey-jr/chat-bot',
      author='Sergey Bakaleynik',
      author_email='bilaserg@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=[
          'kutana', 'pytz'
      ],
      python_requires='>=3.5')
