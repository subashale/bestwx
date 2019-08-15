# for insight button tab
import wx.lib.agw.aui as aui
import wx

# common_view view
from view.common_view.common_gridview import CommonGridView

class InsightPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self.panel_design()

    def panel_design(self):
        # create notebook
        self.nb_result = aui.AuiNotebook(self)

        self.default_tab()

        # to display page to notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb_result, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)

        self.Fit()
        self.Center()
        self.Show()

    def default_tab(self):
        welcome_panel = wx.Panel(self.nb_result, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        welcome_intro = "Result Section"
        welcome_page = wx.StaticText(welcome_panel, -1, welcome_intro)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        welcome_panel.SetSizer(vbox)
        self.nb_result.AddPage(welcome_panel, "Recent")

    # test desing for insight button as in rapidminer
    def working_area(self, dataframe_list, getFileName):
        self.dataframe_list = dataframe_list
        self.getFileName = getFileName

        main = wx.Panel(self)
        top_panel = wx.Panel(main, -1, size=(80, 80))
        top_panel.SetMinSize((80, 80))
        top_panel.SetBackgroundColour(wx.GREEN)

        bs_top = wx.BoxSizer(wx.HORIZONTAL)
        btn_filter = wx.Button(top_panel, label="filter")
        btn_optOne = wx.Button(top_panel, label="option one")
        btn_optTwo = wx.Button(top_panel, label="option two")

        bs_top.Add(btn_optOne, 0, wx.ALL)
        bs_top.Add(btn_optTwo, 1, wx.ALL)
        bs_top.Add(btn_filter, 2, wx.ALL)

        top_panel.SetSizer(bs_top)

        hsz = wx.BoxSizer(wx.HORIZONTAL)

        # left panel desing
        left_panel = wx.Panel(main, -1, size=(100, 1000))
        left_panel.SetMinSize((100, 1000))
        left_panel.SetBackgroundColour(wx.RED)

        bs_lp = wx.BoxSizer(wx.VERTICAL)
        self.btn_data = wx.Button(left_panel, label="Data")
        self.btn_data.Bind(wx.EVT_BUTTON, self.result_left_button_data)

        btn_statistics = wx.Button(left_panel, label="Statistics")
        btn_statistics.Bind(wx.EVT_BUTTON, self.result_left_button_statistics)

        btn_visualization = wx.Button(left_panel, label="Visualization")
        btn_visualization.Bind(wx.EVT_BUTTON, self.result_left_button_visualization)
        btn_annotation = wx.Button(left_panel, label="Annotation")

        bs_lp.Add(self.btn_data, 0, wx.ALL)
        bs_lp.Add(btn_statistics, 1, wx.ALL)
        bs_lp.Add(btn_visualization, 2, wx.ALL)
        bs_lp.Add(btn_annotation, 3, wx.ALL)
        left_panel.SetSizer(bs_lp)

        # right panel desing
        self.right_panel = wx.Panel(main, -1, size=(1100, 400))
        self.right_panel.SetMinSize((1100, 400))
        #self.right_panel.SetBackgroundColour(wx.BLUE)

        sz = wx.BoxSizer(wx.VERTICAL)
        hsz.Add(left_panel, 1, wx.EXPAND)
        hsz.Add(self.right_panel, 1, wx.EXPAND)

        sz.Add(top_panel, 0, wx.EXPAND)
        sz.Add(hsz, 1, wx.EXPAND)

        # initilized all panels for button
        self.data_panel = wx.Panel(self.right_panel)

        # make data button active for first time
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.grid = self.grid_design()
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.right_panel.SetSizer(sizer)
        self.btn_data.SetFocus()

        self.statistics_panel = wx.Panel(self.right_panel)
        self.statistics_panel.Hide()
        self.visualization_panel = wx.Panel(self.right_panel)
        self.visualization_panel.Hide()

        main.SetSizer(sz)
        self.nb_result.AddPage(main, getFileName)

    def working_area_copy(self, data_list, getFileName):
        self.panel = wx.Panel(self, -1)

        self.display_panel = wx.Panel(self.panel, 1, size=(wx.EXPAND, 560))
        self.display_panel.SetBackgroundColour("red")
        self.navigation_panel = wx.Panel(self.panel, 1, size=(wx.EXPAND, 40))
        #self.navigation_panel.SetBackgroundColour("blue")

        self.left = wx.Panel(self.panel, 1, size=(80, wx.EXPAND))

        self.basicsizer = wx.BoxSizer(wx.VERTICAL)
        self.basicsizer.Add(self.navigation_panel, 1, wx.EXPAND)
        self.basicsizer.Add(self.display_panel, 1, wx.EXPAND)

        hz = wx.BoxSizer(wx.HORIZONTAL)
        hz.Add(self.left, 1, wx.EXPAND)
        hz.Add(self.basicsizer, 1, wx.EXPAND)

        self.panel.SetSizer(hz)

        # main.SetSizer(vsz_top)
        self.nb_result.AddPage(self.panel, getFileName)


    # insight pane left side panel; data button desing
    def result_left_button_data(self, event):
        # hide other buttons panels, cannot call unexists object, uff
        print("button data clicked")
        self.statistics_panel.Hide()
        self.visualization_panel.Hide()

        try:
            if self.grid is None:
                print("no filename")
        except:
            print("got exception call frist tab")
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.grid = self.grid_design()
            sizer.Add(self.grid, 1, wx.EXPAND)
            self.right_panel.SetSizer(sizer)
            self.right_panel.Layout()
            self.right_panel.Show()

        else:
            print("already exists, self.grid")
            self.grid.Show()
            self.data_panel.Show()
            self.right_panel.Show()

    # insight pane left side statistics button desing
    def result_left_button_statistics(self, event):
        self.grid.Hide()
        self.data_panel.Hide()
        self.visualization_panel.Hide()
    #
        vbox = wx.BoxSizer(wx.VERTICAL)
        welcome_intro_result = "Satistics merge desing from friends"

        welcome_page = wx.StaticText(self.statistics_panel, -1, welcome_intro_result)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        self.statistics_panel.SetSizer(vbox)
        self.statistics_panel.Layout()
        self.statistics_panel.Fit()
        self.statistics_panel.Show()
        # insight pane left side visualization button desing

    def result_left_button_visualization(self, event):
        self.grid.Hide()
        self.data_panel.Hide()
        self.statistics_panel.Hide()
        #
        vbox = wx.BoxSizer(wx.VERTICAL)
        welcome_intro_result = "Validation panel merge design from friends"

        welcome_page = wx.StaticText(self.visualization_panel, -1, welcome_intro_result)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        self.visualization_panel.SetSizer(vbox)
        self.visualization_panel.Layout()
        self.visualization_panel.Fit()
        self.visualization_panel.Show()

    # for displaying grid in notebook only, it will disply in page; we need to send nb object
    def grid_design(self):
        # it will take grid object from CommonPanelView and send to grid
        # send grid to process pane; notebook object and data frame list and name
        grid = CommonGridView(self, self.right_panel)
        return grid.grid_generate(self.dataframe_list)