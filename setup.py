from setuptools import setup, find_packages

setup(name='clean_folder',
      python_requires='>=3.9',
      version='0.1',
      description='package of file sorting hw7',
      url='http://github.com/dummy_user/useful',
      author='Alex Sin',
      author_email='deroy193@gmail.com',
      license='',
      packages=find_packages(),
      install_requires=['EasyProcess==1.1', 'entrypoint2==1.1', 'patool==1.12', 'pyunpack==0.3'],
      entry_points={'console_scripts': ['clean-folder = clean_folder:sort_process']})
