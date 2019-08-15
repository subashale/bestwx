import wx.lib.agw.aui as aui
import wx

class Preprocess(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.panel_design()

    def panel_design(self):
        # create notebook
        self.nb_preprocess = aui.AuiNotebook(self)

        self.default_tab()

        # to display page to notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb_preprocess, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)

        self.Fit()
        self.Center()
        self.Show()

    def default_tab(self):
        welcome_panel = wx.Panel(self.nb_preprocess, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        welcome_intro = "Preprocess section"
        welcome_page = wx.StaticText(welcome_panel, -1, welcome_intro)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        welcome_panel.SetSizer(vbox)
        self.nb_preprocess.AddPage(welcome_panel, "Recent")
