import wx, wx.grid
#from data import musicdata

import pandas as pd

class GridData(wx.grid.GridTableBase):
    # _cols = "a b c".split()
    #
    # _data = [
    #     "1 2 3".split(),
    #     "4 5 6".split(),
    #     "7 8 9".split()
    # ]
    # _data = musicdata

    # pandas
    dataframe = pd.read_csv("C:/Users/subash/Documents/ml/prj/bestwxpy/test/test_data/10mb.csv", encoding='utf-8')
    dataframe = pd.concat([dataframe, dataframe, dataframe, dataframe, dataframe, dataframe, dataframe, dataframe])
    dataframe = pd.concat([dataframe, dataframe])
    dataframe = pd.concat([dataframe, dataframe, dataframe, dataframe, dataframe])

    _cols = dataframe.columns.values.tolist()
    _data = dataframe.values.tolist()

    _highlighted = set()

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetValue(self, row, col, val):
        self._data[row][col] = val

    def GetAttr(self, row, col, kind):
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(wx.GREEN if row in self._highlighted else wx.WHITE)
        return attr

    def set_value(self, row, col, val):
        self._highlighted.add(row)
        self.SetValue(row, col, val)

class Test(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)

        self.data = GridData()
        self.grid = wx.grid.Grid(self)
        self.grid.SetTable(self.data)

        btn = wx.Button(self, label="set a2 to x")
        btn.Bind(wx.EVT_BUTTON, self.OnTest)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.grid, 1, wx.EXPAND)
        self.Sizer.Add(btn, 0, wx.EXPAND)

    def OnTest(self, event):
        self.data.set_value(1, 0, "x")
        self.grid.Refresh()


app = wx.App()
app.TopWindow = Test()
app.TopWindow.Show()
app.MainLoop()