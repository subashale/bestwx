import wx
import wx.lib.agw.aui as aui

# comment controllers/functions
from controller.common_view import common_pandas_function

# common_view view
from view.common_view.common_file_dialog import open_file_dialog as ofd
from view.common_view.common_gridview import CommonGridView
from view.common_view.common_gridview import Test, TestFrame


class NewProcessPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.panel_design()
        self.pageDict = {}

    def panel_design(self):
        # create notebook
        self.nb_process = aui.AuiNotebook(self)

        self.default_tab()

        #self.grid_design_huge("daf", "dd100")

        # to display page to notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb_process, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)

        self.Fit()
        self.Center()
        self.Show()

    def default_tab(self):
        welcome_panel = wx.Panel(self.nb_process, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        ### unable to display in insight pane page so its hidden ;
        # now only way to importing data is from recent activities pane;
        # b2 = wx.Button(welcome_panel, label="Import Data", size=(200, 25))
        #b2.Bind(wx.EVT_BUTTON, self.on_clicked_open_data)
        #vbox.Add(b2, 0, wx.ALIGN_CENTER)

        welcome_intro = " Hello, Welcome to ....., Test beta version"

        welcome_page = wx.StaticText(welcome_panel, -1, welcome_intro)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        welcome_panel.SetSizer(vbox)

        self.nb_process.AddPage(welcome_panel, "Welcome")

    # file dialog click handler
    def on_clicked_open_data(self, event):
        try:
            getFileLocation, getFileName = ofd()
            data_frame = common_pandas_function.read_data(getFileLocation)
            # to display grid here
            self.grid_design(data_frame, getFileName)

            ### Unable to open for insight pane object is not need but no way to pass it here.

        except:
            print("got canceled")

    # for displaying grid in notebook only, it will disply in page; we need to send nb object
    def grid_design(self, dataframe_list, getFileName):
        # it will take grid object from CommonPanelView and send to grid
        # send grid to processs pane; notebook object and data frame list and name
        grid = CommonGridView(self, self.nb_process)

        self.nb_process.AddPage(grid.grid_generate(dataframe_list), getFileName, wx.ALL | wx.EXPAND)

    def a(self): return 2

    def working_area(self, dataFrame, objDataHistory):
        #
        # no use
        # for i, j in self.pageDict.items():
        #     print(i, j)
        #
        # if objDataHistory.getData()[1] in self.pageDict:
        #     print(self.pageDict[objDataHistory.getData()[1]], type(self.pageDict[objDataHistory.getData()[1]]))
        #     # self.nb_process.EnableTab(2, True)
        #     # self.nb_process.AdvanceSelection(forward=False)
        #
        # else:
        #     self.grid_design_huge(dataframe_list=dataFrame, getFileName=objDataHistory.getData()[1])
        #     self.pageDict[objDataHistory.getData()[1]] = self.nb_process.GetPageCount()

        self.grid_design_huge(dataframe_list=dataFrame, getFileName=objDataHistory.getData()[1])
    # for huge data

    def grid_design_huge(self, dataframe_list, getFileName):
        # it will take grid object from CommonPanelView and send to grid
        # send grid to processs pane; notebook object and data frame list and name
        #grid = Test(self)
        #self.nb_process.AddPage(grid.grid_generate(dataframe_list), getFileName, wx.ALL | wx.EXPAND)

        #huge
        grid = Test(self, self.nb_process)
        self.nb_process.AddPage(grid.grid_generate(dataframe_list.head(100)), getFileName, wx.ALL | wx.EXPAND)
