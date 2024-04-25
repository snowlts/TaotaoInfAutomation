import os

from utils.YamlUtil import YamlLoader
from utils.ExcelUtil import Excel

basedir = os.path.abspath(os.path.dirname(__file__))

def testcase_path(filetype):
    if filetype =='yml':
        return os.path.join(basedir, 'testcases.yml')
    elif filetype == 'xlsx':
        return os.path.join(basedir, 'testcases.xlsx')
    else:
        raise FileNotFoundError("File %s not found!" % filetype)


class DataLoader:
    def __init__(self,filetype ='xlsx'):
        file = testcase_path(filetype)
        if filetype == 'xlsx':
            self._data = Excel(file).data
        elif filetype =='yml':
            self._data =YamlLoader(file).data
        else:
            raise FileNotFoundError("File %s not found!" % filetype)

    @property
    def data(self):
        return self._data


testcases_yml = DataLoader(filetype='yml')
testcases = DataLoader(filetype='xlsx')



