import wx
import wx.grid as gridlib
import pandas as pd
import numpy as np

# auto grid makes loading data extremly slow find other ways to use autosize functionality


class CommonGridView(wx.Panel):
    """"""

    def __init__(self, parent, notebook):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        #self.parent = parent
        self.notebook = notebook


    def grid_generate(self, data_frame):
        data_frame = [data_frame.columns.values.tolist()] + data_frame.values.tolist()

        grid = gridlib.Grid(self.notebook)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        grid.CreateGrid(len(data_frame)-1, len(data_frame[0]))

        for index, value in enumerate(data_frame[0]):
            grid.SetColLabelValue(index, value)

        for row, j in enumerate(data_frame[1:]):
            for col, value in enumerate(j):
                grid.SetCellValue(row, col, str(value))

        sizer.Add(grid, 1, wx.ALL | wx.EXPAND)
        grid.AutoSize()
        self.SetSizer(sizer)

        return grid

# for huge data
class GridData(wx.grid.GridTableBase):

    def set_values(self, cols, data):
        self._cols = cols
        self._data = data
        self._highlighted = set()

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



class Test(wx.Panel):

    def __init__(self, parent, panel):

        wx.Panel.__init__(self, parent=parent)
        self.panel = panel


    def grid_generate(self, dataframe):
        # dataframe = pd.concat([dataframe, dataframe, dataframe, dataframe, dataframe, dataframe, dataframe, dataframe])
        # dataframe = pd.concat([dataframe, dataframe])
        # dataframe = pd.concat([dataframe, dataframe, dataframe, dataframe, dataframe])

        cols = dataframe.columns.values.tolist()
        data = dataframe.values.tolist()

        self.data = GridData()

        self.data.set_values(cols, data)

        grid = wx.grid.Grid(self.panel)

        grid.SetTable(self.data)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(grid, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(sizer)

        return grid

### huge grid
class HugeTable(gridlib.GridTableBase):

    def __init__(self):
        gridlib.GridTableBase.__init__(self)

        self.odd = gridlib.GridCellAttr()
        self.odd.SetBackgroundColour("sky blue")
        self.even = gridlib.GridCellAttr()
        self.even.SetBackgroundColour("sea green")

    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr

    # This is all it takes to make a custom data table to plug into a
    # wxGrid.  There are many more methods that can be overridden, but
    # the ones shown below are the required ones.  This table simply
    # provides strings containing the row and column values.
    def set_values(self, cols, data):
        self._cols = cols
        self._data = data
        self._highlighted = set()

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


# ---------------------------------------------------------------------------


class HugeTableGrid(gridlib.Grid):
    def __init__(self, parent, cols, data):
        gridlib.Grid.__init__(self, parent, -1)

        table = HugeTable()
        table.set_values(cols, data)
        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(table, True)

        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightDown)

    def OnRightDown(self, event):
        print("hello")
        print(self.GetSelectedRows())


# ---------------------------------------------------------------------------

class TestFrame(wx.Panel):
    def __init__(self, parent, panel):
        #wx.Frame.__init__(self, parent, -1, "Huge (virtual) Table Demo", size=(640, 480))

        wx.Panel.__init__(self, parent)
        self.panel = panel
    def grid_generate(self, dataframe):
        #dataframe = pd.concat([dataframe, dataframe, dataframe, dataframe, dataframe, dataframe, dataframe, dataframe])
        #dataframe = pd.concat([dataframe, dataframe])
        #dataframe = pd.concat([dataframe, dataframe, dataframe, dataframe, dataframe])

        cols = dataframe.columns.values.tolist()
        data = dataframe.values.tolist()

        grid = HugeTableGrid(self.panel, cols, data)
        grid.SetReadOnly(5, 5, True)

        #grid.AutoSize() # this take longer process so use in event handler
        print("this is caled")
        return grid