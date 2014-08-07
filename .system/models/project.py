import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../libs'))

import yaml
from system import System
from models.module import Module

class Project:

  root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

  @staticmethod
  def get_root_path():
    return Project.root_path

  @staticmethod
  def get():
    '''
    Returns a Project instance resolving the file path automatically.
    '''
    project_yaml_path = os.path.join(Project.get_root_path(), 'project.yaml')
    return Project.from_file(project_yaml_path)

  @staticmethod
  def from_file(path):
    '''
    Returns a Project instance by reading a file at a given path.
    '''
    project = Project()
    project.read_yaml(path)
    return project

  def __init__(self):
    '''
    Constructor.
    '''
    self.modules = []
    self.modules_by_name = {}
    return

  def read_yaml(self, path):
    '''
    Reads a YAML file and applies its data to this instance.
    '''
    # Read the data.
    stream = open(path, 'r')
    data = yaml.load(stream)
    # Validate the API version.
    if data['api_version'] != System.API_VERSION:
      raise Exception(('Your project.yaml api_version: %d does not match the current infrastructure\'s API version: %d. '
        'Please consult your sysadmin or documentation in order to upgrade your config file.') % (data['api_version'], System.API_VERSION))
    # Apply the data.
    for module in data['modules']:
      self.add_module(module)
    return

  def add_module(self, module):
    module_instance = Module(module['name'], None, os.path.join(Project.root_path, module['path']), module['modules'])
    self.modules.append(module_instance)
    self.modules_by_name[module['name']] = module_instance
    return

  def perform_action(self, action, module_name, module_args):
    modules = None
    if module_name:
      modules = Module.get_by_name(module_name)
      if not modules:
        print 'Could not find any module named \'%s\'' % module_name
        return
    else:
      modules = self.modules
    for module in modules:
      module.perform_action(action, module_args)
    return