
import wx
import wx.lib.agw.aui as aui
import wx.lib.layoutf as layoutf
import controller
import wx.grid as gridlib
import event_execute
from view.main_frame.main_panel_top import MainPanelTop
from view.main_frame.main_panel_bottom import MainPanelBottom
from view.main_frame.test_mini_frame_left import TestMiniFrameLeft
from view.main_frame.test_mini_frame_right import TestMiniFrameRight

from view.new_process.new_process_panel import NewProcessPanel

import pandas as pd

class Main_Frame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(Main_Frame, self).__init__(*args, **kw)
        self.menu_bar_design()
        #self.panel_design()
        #self.auigui()
        self.aui_panes_design()
        #self.tool_bar_design()

        self.Centre()
        self.Show()
        self.Fit()

        #self.newProcess = NewProcessPanel(self)

    def menu_bar_design(self):
        menu_bar = wx.MenuBar()

        # create for file menu
        file_menu = wx.Menu()
        exit_menu_item = file_menu.Append(wx.NewId(), "Exit", "Exit the application")
        menu_bar.Append(file_menu, "&File")

        # create for view menu
        view_menu = wx.Menu()
        view_menu_item = view_menu.Append(wx.NewId(), "Toolbar", "Setting view option")
        menu_bar.Append(view_menu, "&View")

        # create for help menu
        help_menu = wx.Menu()
        about_menu_item = help_menu.Append(wx.NewId(), "About", "Describe Application")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

    def panel_design(self):
        splitter = wx.SplitterWindow(self)
        top = MainPanelTop(splitter)
        bottom = MainPanelBottom(splitter)

        splitter.SplitVertically(top, bottom)
        #splitter.SetMinimumPaneSize(200)

    def tool_bar_design(self):
        self.event_main_frame = event_execute.MainFrame(self)

        tb = self.CreateToolBar(wx.TB_BOTTOM | wx.BORDER)

        self.ToolBar = tb
        tb.SetToolBitmapSize((21, 21))  # this required for non-standard size buttons on MSW

        # New Process, it is using default panel in main frame
        tb.AddControl(wx.Button(tb, 201, "New Process", wx.DefaultPosition, wx.DefaultSize))
        self.Bind(wx.EVT_BUTTON, self.event_main_frame.new_process_panel, id=201)

        # Statistics
        tb.AddControl(wx.Button(tb, 202, "Statistics", wx.DefaultPosition, wx.DefaultSize))
        self.Bind(wx.EVT_BUTTON, self.event_main_frame.tool_clicked, id=202)

        # Preprocessing
        tb.AddControl(wx.Button(tb, 203, "Result", wx.DefaultPosition, wx.DefaultSize))
        self.Bind(wx.EVT_BUTTON, self.event_main_frame.tool_clicked, id=203)

        # Training
        tb.AddControl(wx.Button(tb, 204, "Training", wx.DefaultPosition, wx.DefaultSize))
        self.Bind(wx.EVT_BUTTON, self.event_main_frame.tool_clicked, id=204)

        # Report
        tb.AddControl(wx.Button(tb, 205, "Report", wx.DefaultPosition, wx.DefaultSize))
        self.Bind(wx.EVT_BUTTON, self.event_main_frame.tool_clicked, id=205)

        # APIs
        tb.AddControl(wx.Button(tb, 206, "APIs", wx.DefaultPosition, wx.DefaultSize))
        self.Bind(wx.EVT_BUTTON, self.event_main_frame.tool_clicked, id=206)

        tb.Realize()

    def aui_panes_design(self):
        self.mgr = aui.AuiManager(self)
        self.mgr.SetManagedWindow(self)

        self.mgr.AddPane(self.toolbar_buttons(), aui.AuiPaneInfo().Top().CloseButton(False))
        self.mgr.AddPane(self.recent_activities(), aui.AuiPaneInfo().Left().Caption("Recent activities").CloseButton(False).MinimizeButton(True))

        self._center_panel = aui.AuiPaneInfo().CenterPane().CloseButton(False).MinimizeButton(True)
        #self.mgr.AddPane(self.working_area(), aui.AuiPaneInfo().CenterPane().CloseButton(False).MinimizeButton(True))
        self.mgr.AddPane(self.information_area(), aui.AuiPaneInfo().Bottom().Caption("Information area").CloseButton(False).MinimizeButton(True))
        self.mgr.Update()

    def toolbar_buttons(self):
        toolbar_panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_new = wx.Button(toolbar_panel, -1, "New Process")
        self.btn_new.Bind(wx.EVT_BUTTON, self.onClickNewProcess)
        hbox.Add(self.btn_new, 0, wx.ALIGN_CENTER)

        self.btn_pre = wx.Button(toolbar_panel, -1, "Result ")
        self.btn_pre.Bind(wx.EVT_BUTTON, self.onResultClicked)
        hbox.Add(self.btn_pre, 0, wx.ALIGN_CENTER)

        self.btn_stat = wx.Button(toolbar_panel, -1, "Statistics")
        hbox.Add(self.btn_stat, 0, wx.ALIGN_CENTER)

        self.btn_train = wx.Button(toolbar_panel, -1, "Training")
        hbox.Add(self.btn_train, 0, wx.ALIGN_CENTER)

        self.btn_report= wx.Button(toolbar_panel, -1, "Report")
        hbox.Add(self.btn_report, 0, wx.ALIGN_CENTER)

        self.btn_apis = wx.Button(toolbar_panel, -1, "APIs")
        hbox.Add(self.btn_apis, 0, wx.ALIGN_CENTER)

        vbox.Add(hbox, 1, wx.ALIGN_CENTER)
        toolbar_panel.SetSizer(vbox)

        return toolbar_panel

    def recent_activities(self):
        self.recent_activities_panel = wx.Panel(self, -1, size=(200, wx.EXPAND))

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((0, 150), proportion=1, flag=wx.EXPAND)
        b2 = wx.Button(self.recent_activities_panel, label="Import Data", size=(200, 25))
        #self.event_new_process_panel = event_execute.NewProcessPanel(self)
        b2.Bind(wx.EVT_BUTTON, self.on_clicked_open_data)

        vbox.Add(b2, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)

        st_l = wx.StaticLine(self.recent_activities_panel, -1, style=wx.LI_HORIZONTAL)
        vbox.Add(st_l, 1, wx.ALIGN_CENTER_VERTICAL)

        vbox.Add((300, 300), proportion=2, flag=wx.EXPAND)

        tree = wx.TreeCtrl(self.recent_activities_panel, -1, wx.Point(0, 0), wx.Size(wx.EXPAND, wx.EXPAND),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)

        root = tree.AddRoot("AUI Project")
        items = []

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
        tree.AssignImageList(imglist)

        items.append(tree.AppendItem(root, "Item 1", 0))
        items.append(tree.AppendItem(root, "Item 2", 0))
        items.append(tree.AppendItem(root, "Item 3", 0))
        items.append(tree.AppendItem(root, "Item 4", 0))
        items.append(tree.AppendItem(root, "Item 5", 0))

        for ii in range(len(items)):
            id = items[ii]
            tree.AppendItem(id, "Subitem 1", 1)
            tree.AppendItem(id, "Subitem 2", 1)
            tree.AppendItem(id, "Subitem 3", 1)
            tree.AppendItem(id, "Subitem 4", 1)
            tree.AppendItem(id, "Subitem 5", 1)

        tree.Expand(root)

        vbox.Add(tree, 0, wx.ALIGN_CENTER_VERTICAL)
        self.recent_activities_panel.SetSizer(vbox)

        return self.recent_activities_panel

    def information_area(self):
        information_area_panel = wx.Panel(self, -1, size=(300, 150))
        wx.StaticText(information_area_panel, -1, "Information area Panel - sample text")
        return information_area_panel

    def on_clicked_open_data(self, event):
        self.event = event
        file_loc = self.open_file_dialog()

    def open_file_dialog(self):
        # Create open file dialog
        frame = wx.Frame(None, -1, 'win.py')
        frame.SetSize(0, 0, 100, 25)

        wildcard = "CSV (*.csv)|*.csv|" \
                   "JSON (*.json)|*.json|" \
                   "All files (*.*)|*.*"

        dlg_openFileDialog = wx.FileDialog(frame,
                                           message="Open",
                                           defaultDir="",
                                           defaultFile="",
                                           wildcard=wildcard,
                                           # "Data(*.csv)|*.csv",
                                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dlg_openFileDialog.ShowModal() == wx.ID_CANCEL:
            dlg_openFileDialog.Destroy()
            frame.Destroy()
            return

        getFileLocation = dlg_openFileDialog.GetPath()
        print(getFileLocation)

        dlg_openFileDialog.Destroy()
        frame.Destroy()
        self.df = self.make_df(getFileLocation)
        self.grid_design()
        #self.objMainFrame = controller.MainFrame(getFileLocation)

    def make_df(self, getFileLocation):
        df = pd.read_csv(getFileLocation)

        df_list = [df.columns.values.tolist()] + df.values.tolist()
        return df_list

    def onClickNewProcess(self, event):
        #print("clicked here")
        btn = event.GetEventObject().GetLabel()
        print("Label of pressed button = ", btn)
        #self.define_aui_manager()
        # do if statement for checking availabelity of welcome page
        self.working_area()

    def onResultClicked(self, event):
        print("insight is clicked")
        self.define_aui_manager()
        #self.result_design()

    def define_aui_manager(self):
        self.test_panel = wx.Panel(self)
        text3 = wx.TextCtrl(self.test_panel, -1, "Main content window",
                            wx.DefaultPosition, wx.Size(200, 150),
                            wx.NO_BORDER | wx.TE_MULTILINE)
        self.mgr.AddPane(self.test_panel, self._center_panel)
        self.mgr.Update()

    def working_area(self):
        self.working_area_panel = wx.Panel(self)
        self.nb = aui.AuiNotebook(self.working_area_panel)
        self.default_tab()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.working_area_panel.SetSizer(sizer)
        self.working_area_panel.Fit()
        self.Show()
        self.mgr.AddPane(self.working_area_panel, self._center_panel)
        self.mgr.Update()
        #return self.working_area_panel

    def default_tab(self):
        welcome_panel = wx.Panel(self.nb, -1)
        print("asdfa")
        vbox = wx.BoxSizer(wx.VERTICAL)
        b2 = wx.Button(welcome_panel, label="Import Data", size=(200, 25))
        b2.Bind(wx.EVT_BUTTON, self.on_clicked_open_data)

        vbox.Add(b2, 0, wx.ALIGN_CENTER)
        welcome_intro = " Hello, Welcome to ....., Test beta version"

        welcome_page = wx.StaticText(welcome_panel, -1, welcome_intro)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        welcome_panel.SetSizer(vbox)

        self.nb.AddPage(welcome_panel, "Welcome")

    def result_design(self):
        panel = wx.Panel(self, -1)

        sizer = wx.GridBagSizer(0,0)

        btn_data = wx.Button(panel, label="Data")
        btn_statistics = wx.Button(panel, label="Statistics")
        btn_visualization = wx.Button(panel, label="Visualization")
        btn_annotation = wx.Button(panel, label="Annotation")

        sizer.Add(btn_data, pos=(0,0), flag=wx.ALL, border=5)
        sizer.Add(btn_statistics, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_visualization, pos=(2, 0), flag=wx.ALL, border=5)
        sizer.Add(btn_annotation, pos=(3, 0), flag=wx.EXPAND | wx.ALL, border=5)

        #sizer.Add(self.grid_design(), pos=(4, 1), flag=wx.EXPAND)

        buttonOk = wx.Button(panel, label="Ok")
        buttonClose = wx.Button(panel, label="Close")

        sizer.Add(buttonOk, pos=(4, 2), flag=wx.ALL, border=5)
        sizer.Add(buttonClose, pos=(4, 3), flag=wx.ALL, border=5)

        panel.SetSizerAndFit(sizer)

        self.nb.AddPage(panel, "Result")

    def grid_design(self):
        #self.grid_desing_panel = wx.Panel(self)

        grid = NewProcessPanel(self.nb, self.df)

        # sizer = wx.GridBagSizer(4, 4)
        #
        # btn_data = wx.Button(self.grid_desing_panel, label="Data")
        # btn_statistics = wx.Button(self.grid_desing_panel, label="Statistics")
        # btn_visualization = wx.Button(self.grid_desing_panel, label="Visualization")
        # btn_annotation = wx.Button(self.grid_desing_panel, label="Annotation")
        #
        # btn_hor = wx.Button(self.grid_desing_panel, label="btn_hor")
        #
        # sizer.Add(btn_data, pos=(0, 0), flag=wx.ALL)
        # sizer.Add(btn_statistics, pos=(1, 0), flag=wx.ALL)
        # sizer.Add(btn_visualization, pos=(2, 0), flag=wx.ALL)
        # sizer.Add(btn_annotation, pos=(3, 0), flag=wx.ALL)
        #
        # sizer.Add(btn_hor, pos=(0, 4), span=(0, 5), flag=wx.TOP | wx.RIGHT | wx.ALIGN_RIGHT)
        #
        # sizer.Add(grid, pos=(1, 1), span=(5, 5), flag=wx.ALIGN_CENTER_HORIZONTAL)
        #
        # self.grid_desing_panel.SetSizerAndFit(sizer)

        self.nb.AddPage(grid, "New Process")


    # prepare centerpane for all buttons at once then use hide/show method
    # or create open new process for insight and then take dataframe from them
# def auigui(self):
    #
    #     self._mgr = aui.AuiManager()
    #
    #     # notify AUI which frame to use
    #     self._mgr.SetManagedWindow(self)
    #     # create several text controls
    #     text1 = wx.TextCtrl(self, -1, "Pane 1 - sample text",
    #                         wx.DefaultPosition, wx.Size(200, 150),
    #                         wx.NO_BORDER | wx.TE_MULTILINE)
    #
    #     text2 = wx.TextCtrl(self, -1, "Pane 2 - sample text",
    #                         wx.DefaultPosition, wx.Size(200, 150),
    #                         wx.NO_BORDER | wx.TE_MULTILINE)
    #
    #     text3 = wx.TextCtrl(self, -1, "Main content window",
    #                         wx.DefaultPosition, wx.Size(200, 150),
    #                         wx.NO_BORDER | wx.TE_MULTILINE)
    #     text4 = wx.TextCtrl(self, -1, "Left Pane",
    #                         wx.DefaultPosition, wx.Size(200, 150),
    #                         wx.NO_BORDER | wx.TE_MULTILINE)
    #
    #     # text5 = wx.TextCtrl(self, -1, "Main content window",
    #     #                     wx.DefaultPosition, wx.Size(200, 150),
    #     #                     wx.NO_BORDER | wx.TE_MULTILINE)
    #
    #
    #
    #     # add the panes to the manager
    #     self._mgr.AddPane(text3, aui.AuiPaneInfo().Center().Caption("Working Pane"))
    #     #self._mgr.AddPane(text5, aui.AuiPaneInfo().Top().Caption("Top Pane"))
    #     self._mgr.AddPane(text4, aui.AuiPaneInfo().Right().Caption("Right Pane"))
    #     self._mgr.AddPane(text2, aui.AuiPaneInfo().Bottom().Caption("Bottom Pane"))
    #     self._mgr.AddPane(text1, aui.AuiPaneInfo().Left().Caption("Left Pane"))
    #
    #     # tell the manager to "commit" all the changes just made
    #     self._mgr.Update()
