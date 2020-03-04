import pip._internal as pip

package_names=['matplotlib'] #packages to install
pip.main(['install'] + package_names + ['--upgrade']) 
# --upgrade to install or update existing packages
