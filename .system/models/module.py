import os, sys

class Module:

  modules_by_name = {}
  modules_by_full_name = {}

  @staticmethod
  def get_by_name(name):
    '''
    Returns an array of modules of a given name.
    Null if no module with a given name exists.
    '''
    if not name:
      return None
    if name in Module.modules_by_name:
      return Module.modules_by_name[name]
    elif name in Module.modules_by_full_name:
      return [Module.modules_by_full_name[name]]
    return None

  def __init__(self, name, parent_full_name, path, submodules):
    self.name = name
    self.full_name = name
    if parent_full_name:
        self.full_name = parent_full_name + '/' + name
    self.path = path
    self.submodules = []
    self.add_submodules(submodules)
    self.register()
    return

  def register(self):
    if not self.name in Module.modules_by_name:
      Module.modules_by_name[self.name] = []
    if self.full_name in Module.modules_by_full_name:
      raise Exception('Duplicate module full name %s' % self.full_name)
    Module.modules_by_name[self.name].append(self)
    Module.modules_by_full_name[self.full_name] = self
    return

  def add_submodules(self, submodules):
    if not submodules:
        return
    for submodule in submodules:
      sub_submodules = None
      if 'modules' in submodule:
        sub_submodules = submodule['modules']
      self.submodules.append(Module(submodule['name'], self.full_name, self.path + '/' + submodule['path'], sub_submodules))
    pass

  def perform_action(self, action, args):
    if hasattr(self, action):
      getattr(self, action)(args)
    else:
     raise Exception('unknown action \'%s\'' % action)
    for module in self.submodules:
      module.perform_action(action, args)
    pass

  def bootstrap(self, args):
    pass

  def develop(self, args):
    pass

  def test(self, args):
    pass

  def run(self, args):
    self.run_script('run', args);
    pass

  def deploy(self, args):
    pass

  def get_path_to_script(self, script):
    return os.path.join(self.path, script)

  def run_script(self, script_name, args):
    script_path = self.get_path_to_script(script_name)
    if os.path.isfile(script_path):
      os.system(script_path + ' %s' % (' '.join(args)))
    return