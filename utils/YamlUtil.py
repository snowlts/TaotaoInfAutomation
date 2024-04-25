import yaml
import os

from yaml.composer import ComposerError


class YamlLoader:
    def __init__(self,yml_file):
        self._data = None
        if os.path.exists(yml_file):
            self.yml_file = yml_file
        else:
            raise FileNotFoundError("File %s not found" % yml_file)

    def get_data(self):
        if not self._data:
            with open(self.yml_file,'rb') as f:
                self._data = yaml.safe_load(f)
        return self._data

    def get_data_all(self):
        if not self._data:
            with open(self.yml_file,'rb') as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data

    @property
    def data(self):
        try:
            return self.get_data()
        except ComposerError as e:
            return self.get_data_all()
