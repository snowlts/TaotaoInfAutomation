import xlrd,xlwt
from collections import defaultdict

from utils.LogUtil import logger_init

logger = logger_init('Excel')
class Excel:
    def __init__(self,file):
        self._data = dict()
        book = xlrd.open_workbook(file)
        logger.info("The number of worksheets is {0}".format(book.nsheets))
        logger.info("Worksheet name(s): {0}".format(book.sheet_names()))
        #遍历所有的sheet
        for i in range(book.nsheets):
            sh = book.sheet_by_index(i)
            logger.info("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
            #获取列名
            field_row = [i.value for i in sh.row(0)]
            #从第二行开始遍历所有行
            for rx in range(1,sh.nrows):
                #把每一行用dict存放
                row = [i.value for i in sh.row(rx)]
                row_map = dict()
                for j in range(sh.ncols):
                    row_map[field_row[j]] = row[j]
                if row_map['是否运行'] =='yes':
                    self._data[row_map['用例编号']]=row_map

            # logger.info("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=3)))
    @property
    def data(self):
        return self._data

    def get_inf(self,case_id):
        return case_id.split("_")[0]




excel = Excel(r"H:/codes/python/automation/TaotaoInfAutomation/data/testcases.xlsx")
