import wx

# controller
from view.common_view.common_file_dialog import open_file_dialog as ofd


class LoadData(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent


    def panel_design(self):
        pass

    def open_load_data(self):
        try:
            self.getFileLocation, self.getFileName = ofd()
            return self.getFileLocation, self.getFileName
        except:
            print("got cancelled")

    def display_data_properties(self):
        panel = wx.Panel(self, size=(wx.EXPAND, wx.EXPAND))
        panel.SetBackgroundColour("white")
        vbox = wx.BoxSizer(wx.HORIZONTAL)
        fileName = wx.StaticText(panel, -1, self.getFileName)
        vbox.Add(fileName, 0, wx.EXPAND)
        panel.SetSizer(vbox)
        panel.Show()