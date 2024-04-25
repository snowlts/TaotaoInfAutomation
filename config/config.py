import os

from utils.YamlUtil import YamlLoader


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# def yml_file():
#     return os.path.join(basedir,'config','config.yml')
def get_path(file_name):
    if file_name =="yaml_conf":
        return os.path.join(basedir,'config','config.yml')
    elif file_name =="logs":
        return os.path.join(basedir,'logs')
    elif file_name =='testcases':
        return os.path.join(basedir, 'data', 'testcases.yml')
    else:
        raise FileNotFoundError("File %s not found!" % file_name)


class ConfigLoader:
    def __init__(self,yml_file=get_path("yaml_conf")):
        self._data =YamlLoader(yml_file).data

    @property
    def config(self):
        return self._data

    @property
    def url(self):
        return self._data['BASE']['test']['url']
    @property
    def log(self):
        return self._data['BASE']['test']['log']

    @property
    def db(self):
        return self._data['BASE']['test']['db']

config = ConfigLoader()




