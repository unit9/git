import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../libs'))

from system import System
import yaml

class Project:

  @staticmethod
  def get():
    '''
    Returns a Project instance resolving the file path automatically.
    '''
    project_yaml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../project.yaml'))
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
    print 'ok'
    return