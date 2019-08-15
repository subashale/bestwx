# for result button tab
import wx.lib.agw.aui as aui
import wx

# common_view view
from view.common_view.common_gridview import CommonGridView, TestFrame, Test

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
        self.data_frame_list = data_frame_list
        # main panel
        self.main_panel = wx.Panel(self)

        # left panel init
        self.left_panel = wx.Panel(self.main_panel)
        self.left_panel.SetMaxSize((100, wx.EXPAND))
        self.left_panel.SetBackgroundColour("white")

        # left panel design
        self.left_panel_desing()

        # right panel init
        self.right_panel = wx.Panel(self.main_panel)
        self.right_panel.SetMaxSize((wx.EXPAND, wx.EXPAND))

        # right panels, which are hidden except data_panel which is default
        self.data_panel = wx.Panel(self.right_panel)
        self.data_panel.SetBackgroundColour("white")
        self.statistics_panel = wx.Panel(self.right_panel)
        self.visualization_panel = wx.Panel(self.right_panel)

        # call right data panel
        self.data_panel_desing()

        # positioning left and right panel(vz_right_panel)
        hs_main_panel = wx.BoxSizer(wx.HORIZONTAL)
        hs_main_panel.Add(self.left_panel, 1, wx.ALL | wx.EXPAND)
        hs_main_panel.Add(self.right_panel, 1, wx.ALL | wx.EXPAND)
        self.main_panel.SetSizer(hs_main_panel)

        # main.SetSizer(vsz_top)
        self.nb_result.AddPage(self.main_panel, getFileName, wx.ALL | wx.EXPAND)


    # left panel desing
    def left_panel_desing(self):

        # buttons for left panel
        btn_data = wx.Button(self.left_panel, label="Data", size=(wx.EXPAND, 50))
        btn_statistics = wx.Button(self.left_panel, label="Statistics", size=(wx.EXPAND, 50))
        btn_visualization = wx.Button(self.left_panel, label="Visualization", size=(wx.EXPAND, 50))

        # left panel button click handler
        btn_data.Bind(wx.EVT_BUTTON, self.show_data)
        btn_statistics.Bind(wx.EVT_BUTTON, self.show_statistics)
        btn_visualization.Bind(wx.EVT_BUTTON, self.show_visualization)

        # # button positioning for left panel
        vs_left_panel = wx.BoxSizer(wx.VERTICAL)
        vs_left_panel.Add((-1, 180), proportion=1, flag=wx.EXPAND)
        vs_left_panel.Add(btn_data, 0, wx.ALL, 5)
        vs_left_panel.Add(btn_statistics, 1, wx.ALL, 5)
        vs_left_panel.Add(btn_visualization, 2, wx.ALL, 5)
        vs_left_panel.Add((-1, 180), proportion=1, flag=wx.EXPAND)

        self.left_panel.SetSizer(vs_left_panel)

    # data panel desing
    def data_panel_desing(self):

        # to send data directly for preprocessing and model training
        btn_preprocess = wx.Button(self.data_panel, label="Pre-Process")
        btn_train_model = wx.Button(self.data_panel, label="Train Model")

        # designing filter buttons for gird
        btn_filter = wx.Button(self.data_panel, label="filter")
        btn_optOne = wx.Button(self.data_panel, label="option one")

        # positioning filter buttons for grid
        hz_data_option = wx.BoxSizer(wx.HORIZONTAL)
        hz_data_option.Add(btn_preprocess, 0, wx.ALL, 5)
        hz_data_option.Add(btn_train_model, 0,wx.ALL, 5)
        hz_data_option.Add(btn_filter, 0, wx.ALL, 5)
        hz_data_option.Add(btn_optOne, 0, wx.ALL, 5)
        #self.data_panel.SetSizer(hz_data_option)

        vz_data_panel = wx.BoxSizer(wx.VERTICAL)
        vz_data_panel.Add(hz_data_option, wx.CENTER)
        #vz_data_panel.Add(self.grid_design(self.data_panel), wx.ALL | wx.EXPAND)
        vz_data_panel.Add(self.grid_design_huge(self.data_panel), wx.ALL | wx.EXPAND)
        self.data_panel.SetSizer(vz_data_panel)

        # positioning to right main panel but if I use this it will create problem while clicking other buttons stat, viz
        hz_right_panel = wx.BoxSizer(wx.HORIZONTAL)
        hz_right_panel.Add(self.data_panel, wx.ALL | wx.EXPAND)
        self.right_panel.SetSizer(hz_right_panel)

    # statistics panel design
    def statistics_panel_design(self):
        # statistics content
        vz_statistics_panel = wx.BoxSizer(wx.VERTICAL)
        welcome_intro_result = "Satistics merge desing from friends"
        welcome_page = wx.StaticText(self.statistics_panel, -1, welcome_intro_result)
        vz_statistics_panel.Add(welcome_page, 0, wx.ALIGN_CENTER)
        self.statistics_panel.SetSizer(vz_statistics_panel)

        # self.statistics_panel.Layout()
        # self.statistics_panel.Fit()
        # self.statistics_panel.Show()

        hz_right_panel = wx.BoxSizer(wx.HORIZONTAL)
        hz_right_panel.Add(self.statistics_panel, wx.ALL | wx.EXPAND)
        self.right_panel.SetSizer(hz_right_panel)

    # visualization panel design
    def visualization_panel_design(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        welcome_intro_result = "Validation panel merge design from friends"

        welcome_page = wx.StaticText(self.visualization_panel, -1, welcome_intro_result)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        self.visualization_panel.SetSizer(vbox)
        self.visualization_panel.Layout()
        self.visualization_panel.Fit()
        self.visualization_panel.Show()

    # result pane left side panel; data button desing
    def show_data(self, event):
        # hide other buttons panels, cannot call unexists object, uff
        self.statistics_panel.Hide()
        self.visualization_panel.Hide()
        self.data_panel.Show()
        self.data_panel_desing()

        # this condition doesnot work if multiple data is imported
        # because the self.grid is already exist for another page, dataset
        # so check for each possible condition like make different object for each notepad's grid;#

    # result pane left side statistics button desing
    def show_statistics(self, event):
        self.data_panel.Hide()
        self.visualization_panel.Hide()
        self.statistics_panel.Show()
        self.statistics_panel_design()


    def show_visualization(self, event):
        self.data_panel.Hide()
        self.statistics_panel.Hide()
        #self.visualization_panel.Show()
        self.visualization_panel_design()

    # for displaying grid in notebook only, it will disply in page; we need to send nb object
    def grid_design(self, panel):
        # it will take grid object from CommonPanelView and send to grid
        # send grid to process pane; notebook object and data frame list and name
        grid = CommonGridView(self, panel)
        return grid.grid_generate(self.data_frame_list)

        # for huge data
    def grid_design_huge(self, panel):
        # it will take grid object from CommonPanelView and send to grid
        # send grid to processs pane; notebook object and data frame list and name
        # grid = Test(self)
        # self.nb_process.AddPage(grid.grid_generate(dataframe_list), getFileName, wx.ALL | wx.EXPAND)

        # huge
        grid = Test(self, panel)
        return grid.grid_generate(self.data_frame_list)