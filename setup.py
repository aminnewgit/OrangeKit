from distutils.core import setup

from setuptools import find_packages

setup(
  name = 'orange_utils',         # How you named your package folder (MyLib)

  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'orange utils',   # Give a short description about your library
  author = 'junjun',                   # Type in your name
  author_email = '289584104@qq.com',      # Type in your E-Mail
  url = 'https://github.com/aminnewgit/OrangeKit',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/aminnewgit/OrangeKit/dist/orange_utils-0.1.tar.gz',    # I explain this later on
  keywords = ['orange', 'data class', ''],   # Keywords that define your package best
  install_requires =[],

  # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
  packages = find_packages(),

  # 指定包名，即你需要打包的包名称，要实际在你本地存在哟，它会将指定包名下的所有"*.py"文件进行打包哟，但不会递归去拷贝所有的子包内容。
  # 综上所述，我们如果想要把一个包的所有"*.py"文件进行打包，应该在packages列表写下所有包的层级关系哟~这样就开源将指定包路径的所有".py"文件进行打包!
  # packages = ['devops', "devops.dev", "devops.ops"],

  classifiers=[
    #  发展时期,常见的如下
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    # 开发的目标用户
    'Intended Audience :: Developers',      # Define that your audience are developers
    # 属于什么类型
    'Topic :: Software Development :: Build Tools',

    'License :: OSI Approved :: MIT License',   # Again, pick a license
    # 目标 Python 版本
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
  # https://blog.csdn.net/calvinpaean/article/details/113580458
)


