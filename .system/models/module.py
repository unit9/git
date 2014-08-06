import os, sys

class Module:

  @staticmethod
  def get():
    module_yaml_path = os.path.join(sys.argv[1], 'module.yaml')
    print 'module yaml path: %s' % module_yaml_path