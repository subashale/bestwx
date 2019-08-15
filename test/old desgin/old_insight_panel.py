# for result button tab
import wx.lib.agw.aui as aui
import wx

# common_view view
from view.common_view.common_gridview import CommonGridView

## use multi thread concept to handle each functionaliy for each page
# useful when clicking data, statistics.. buttons for each opened dataset
# task assign: ashish ;#

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

    def working_area(self, data_frame_list, getFileName):
        # main panel
        self.main_panel = wx.Panel(self, -1)

        # left panel design
        self.left_panel_desing()

        # right panel design
        self.right_panel_desing(data_frame_list)

        # positioning right panel and navigation panel
        vz_right_panel = wx.BoxSizer(wx.VERTICAL)
        vz_right_panel.Add(self.navigation_panel, 1, wx.ALL | wx.EXPAND)
        vz_right_panel.Add(self.right_panel, 1, wx.ALL | wx.EXPAND)

        # positioning left and right panel(vz_right_panel)
        hs_main_panel = wx.BoxSizer(wx.HORIZONTAL)
        hs_main_panel.Add(self.left_panel, 1, wx.ALL | wx.EXPAND)
        hs_main_panel.Add(vz_right_panel, 1, wx.ALL | wx.EXPAND)

        self.main_panel.SetSizer(hs_main_panel)

        # main.SetSizer(vsz_top)
        self.nb_result.AddPage(self.main_panel, getFileName, wx.ALL | wx.EXPAND)

    # left panel desing
    def left_panel_desing(self):
        # left panel init
        self.left_panel = wx.Panel(self.main_panel)
        self.left_panel.SetMaxSize((100, wx.EXPAND))
        self.left_panel.SetBackgroundColour("white")

        # buttons for left panel
        btn_data = wx.Button(self.left_panel, label="Data", size=(wx.EXPAND, 50))
        btn_statistics = wx.Button(self.left_panel, label="Statistics", size=(wx.EXPAND, 50))
        btn_visualization = wx.Button(self.left_panel, label="Visualization", size=(wx.EXPAND, 50))
        btn_annotation = wx.Button(self.left_panel, label="Annotation", size=(wx.EXPAND, 50))

        # left panel button click handler
        btn_data.Bind(wx.EVT_BUTTON, self.result_left_button_data)
        btn_statistics.Bind(wx.EVT_BUTTON, self.result_left_button_statistics)
        btn_visualization.Bind(wx.EVT_BUTTON, self.result_left_button_visualization)

        # # button positioning for left panel
        vs_left_panel = wx.BoxSizer(wx.VERTICAL)
        vs_left_panel.Add((-1, 150), proportion=1, flag=wx.EXPAND)
        vs_left_panel.Add(btn_data, 0, wx.ALL, 5)
        vs_left_panel.Add(btn_statistics, 1, wx.ALL, 5)
        vs_left_panel.Add(btn_visualization, 2, wx.ALL, 5)
        vs_left_panel.Add(btn_annotation, 3, wx.ALL, 5)
        vs_left_panel.Add((-1, 160), proportion=1, flag=wx.EXPAND)

        self.left_panel.SetSizer(vs_left_panel)

    # data panel desing
    def right_panel_desing(self, data_frame_list):

        # right panel init
        self.right_panel = wx.Panel(self.main_panel)
        self.right_panel.SetMaxSize((wx.EXPAND, wx.EXPAND))

        # right top nav design
        self.navigation_panel = wx.Panel(self.main_panel)
        self.navigation_panel.SetMaxSize((wx.EXPAND, 40))
        self.navigation_panel.SetBackgroundColour("white")


        ## navigation panel design
        btn_filter = wx.Button(self.navigation_panel, label="filter")
        btn_optOne = wx.Button(self.navigation_panel, label="option one")
        btn_optTwo = wx.Button(self.navigation_panel, label="option two")

        # centering buttons for navigation panel
        vz_navigation_panel = wx.BoxSizer(wx.VERTICAL)
        hz_navigation_panel = wx.BoxSizer(wx.HORIZONTAL)
        hz_navigation_panel.Add(btn_filter, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hz_navigation_panel.Add(btn_optOne, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hz_navigation_panel.Add(btn_optTwo, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        vz_navigation_panel.Add(hz_navigation_panel, 1, wx.ALIGN_CENTER)
        self.navigation_panel.SetSizer(vz_navigation_panel)

        # make data button active for first time
        hz_right_panel = wx.BoxSizer(wx.VERTICAL)

        b2 = wx.Button(self.right_panel, label="Btn2")
        hz_right_panel.Add(b2, wx.ALL | wx.EXPAND,  5)

        self.grid = self.grid_design(self.right_panel, data_frame_list)
        hz_right_panel.Add(self.grid, wx.ALL | wx.EXPAND)
        self.right_panel.SetSizer(hz_right_panel)

        # right panels, which are hidden except data_panel which is default
        self.data_panel = wx.Panel(self.right_panel)
        self.statistics_panel = wx.Panel(self.right_panel)
        self.statistics_panel.Hide()
        self.visualization_panel = wx.Panel(self.right_panel)
        self.visualization_panel.Hide()


    # result pane left side panel; data button desing
    def result_left_button_data(self, event):
        # hide other buttons panels, cannot call unexists object, uff
        print("button data clicked")
        self.statistics_panel.Hide()
        self.visualization_panel.Hide()

        # this condition doesnot work if multiple data is imported
        # because the self.grid is already exist for another page, dataset
        # so check for each possible condition like make different object for each notepad's grid;#
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

    # result pane left side statistics button desing
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
        # result pane left side visualization button desing

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
    def grid_design(self, panel, data_frame_list):
        # it will take grid object from CommonPanelView and send to grid
        # send grid to process pane; notebook object and data frame list and name
        grid = CommonGridView(self, panel)
        return grid.grid_generate(data_frame_list)