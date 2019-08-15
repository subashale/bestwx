# new_process_panel.py
# file dialog click handler
#     def on_clicked_open_data(self, event):
#         self.getFileLocation, self.getFileName = common_view.open_file_dialog()
#         self.dataframe_list = common_view.make_df(self.getFileLocation)
#
#         # send grid to processs pane; notebook object and data frame list and name
#         #self.nb_process.AddPage(self.grid_design(self.nb_process, self.dataframe_list), self.getFileName)
#         grid = common_view.grid_design(self.nb_process,self.dataframe_list)
#         self.nb_process.AddPage(grid, self.getFileName)

        # update in insight pane, add page on nb_result
        #self.design_result_notebook()

        # call by reference but got error while closing from one notebook to another;
        # for example if I close from process notebook then it will raise error to insight notebook;
        # handel try using exception handle and if else condition;
        # or do this later 31 of aug#

        # self.grid = self.grid_design(dataframe_list)
        #
        # self.nb_process.AddPage(self.grid, getFileName)
        # self.nb_result.AddPage(self.grid, getFileName)


# wx libraries
import wx
import wx.lib.agw.aui as aui
import wx.grid as gridlib

# common_view functions
from controller.common_view import common_pandas_function

# events
import event_execute
from event_execute.main_frame.MainFrame import MainFrame

# other view part import
from view.new_process.new_process_panel import NewProcessPanel
from view.insight.insight_panel import InsightPanel
from view.training.training_panel import TrainingPanel
from view.common_view.common_gridview import CommonGridView

# 3rd party libraries
import pandas as pd

class Main_Frame(wx.Frame):

    # constructor auto load
    def __init__(self, *args, **kw):
        super(Main_Frame, self).__init__(*args, **kw)
        self.menu_bar_design()
        self.aui_panes_design()
        self.Centre()
        self.Show()
        self.Fit()

    # design of menu bar
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

    # main design layout
    def aui_panes_design(self):
        self.mgr = aui.AuiManager(self)
        self.mgr.SetManagedWindow(self)

        # desing of each panes
        self.mgr.AddPane(self.toolbar_buttons(), aui.AuiPaneInfo().Top().CloseButton(False))
        self.mgr.AddPane(self.recent_activities(), aui.AuiPaneInfo().Left().Caption("Recent activities").CloseButton(False).MinimizeButton(True))
        #self._center_panel = aui.AuiPaneInfo().CenterPane().CloseButton(False).MinimizeButton(True)
        self.mgr.AddPane(self.working_area_process(),
                         aui.AuiPaneInfo().Name("process_pane").CenterPane().CloseButton(False).MinimizeButton(True))
        self.mgr.AddPane(self.working_area_result(),
                         aui.AuiPaneInfo().Name("result_pane").CenterPane().CloseButton(False).MinimizeButton(True).Hide())
        self.mgr.AddPane(self.working_area_training(),
                         aui.AuiPaneInfo().Name("training_pane").CenterPane().CloseButton(False).MinimizeButton(
                             True).Hide())
        self.mgr.AddPane(self.information_area(), aui.AuiPaneInfo().Bottom().Caption("Information area").CloseButton(False).MinimizeButton(True))
        self.mgr.Update()

    # for top pane as toolbar
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

        self.btn_train = wx.Button(toolbar_panel, -1, "Training")
        self.btn_train.Bind(wx.EVT_BUTTON, self.onTrainingClicked)
        hbox.Add(self.btn_train, 0, wx.ALIGN_CENTER)

        # self.btn_stat = wx.Button(toolbar_panel, -1, "Statistics")
        # hbox.Add(self.btn_stat, 0, wx.ALIGN_CENTER)

        # self.btn_report= wx.Button(toolbar_panel, -1, "Report")
        # hbox.Add(self.btn_report, 0, wx.ALIGN_CENTER)
        #
        # self.btn_apis = wx.Button(toolbar_panel, -1, "APIs")
        # hbox.Add(self.btn_apis, 0, wx.ALIGN_CENTER)

        vbox.Add(hbox, 1, wx.ALIGN_CENTER)
        toolbar_panel.SetSizer(vbox)

        return toolbar_panel

    # for left pane as history/recent activity
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

    # for bottom pane as information area
    def information_area(self):
        information_area_panel = wx.Panel(self, -1, size=(300, 150))
        wx.StaticText(information_area_panel, -1, "Information area Panel - sample text")
        return information_area_panel

    ## main pane area for all buttons working area
    # for new process working area
    def working_area_process(self):
        self.obj_NewProcess = NewProcessPanel(self)
        return self.obj_NewProcess

    # for insight working area
    def working_area_result(self):
        self.working_area_result_panel = wx.Panel(self)
        self.nb_result = aui.AuiNotebook(self.working_area_result_panel)

        try:
            if self.getFileName is None:
                print("no filename")
        except:
            print("got exception call frist tab")
            self.result_first_tab()
        else:
            print("insight")
            self.result_first_tab()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb_result, 1, wx.EXPAND)

        self.working_area_result_panel.SetSizer(sizer)
        self.working_area_result_panel.Fit()
        self.working_area_result_panel.Show()

        return self.working_area_result_panel

    def working_area_training(self):
        self.working_area_training_panel = wx.Panel(self)
        self.nb_training = aui.AuiNotebook(self.working_area_training_panel)

        self.trainingObj = TrainingPanel(self, self.nb_training)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb_training, 1, wx.EXPAND)

        self.working_area_training_panel.SetSizer(sizer)
        self.working_area_training_panel.Fit()
        self.working_area_training_panel.Show()
        return self.working_area_training_panel

    # file dialog click handler
    def on_clicked_open_data(self, event):
        if common_pandas_function.open_file_dialog() != False:
            self.getFileLocation, self.getFileName = common_pandas_function.open_file_dialog()
            self.dataframe_list = common_pandas_function.make_df_list(self.getFileLocation)
            self.obj_NewProcess.grid_design(self.dataframe_list, self.getFileName)
        #pass

    # action when new process button is clicked, it will show process_pane
    def onClickNewProcess(self, event):
        btn = event.GetEventObject().GetLabel()
        print("Label of pressed button = ", btn)
        self.obj_NewProcess.panel_design()
        self.Layout()
        self.Show()

        # if self.obj_NewProcess.check_nb_obj() == None:
        #     print("none")
        #     #del self.obj_NewProcess
        #     self.working_area_process()
        # else:
        #     self.obj_NewProcess.panel_design()
        #     self.Layout()
        #     self.Fit()
        #     self.Show()


    # action when insight button is clicked, it will show result_pane
    def onResultClicked(self, event):
        print("insight is clicked")
        self.mgr.GetPaneByName("process_pane").Hide()
        self.mgr.GetPaneByName("training_pane").Hide()
        self.mgr.GetPaneByName("result_pane").Show()
        self.mgr.Update()

    # action when training button is clicked, it will show train_pane
    def onTrainingClicked(self, event):
        print("training clicked")
        self.mgr.GetPaneByName("process_pane").Hide()
        self.mgr.GetPaneByName("result_pane").Hide()
        self.mgr.GetPaneByName("training_pane").Show()
        self.mgr.Update()

    # test desing for insight button as in rapidminer
    def design_result_notebook(self):
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
        btn_data = wx.Button(left_panel, label="Data")
        btn_data.Bind(wx.EVT_BUTTON, self.result_left_button_data)

        btn_statistics = wx.Button(left_panel, label="Statistics")
        btn_statistics.Bind(wx.EVT_BUTTON, self.result_left_button_statistics)

        btn_visualization = wx.Button(left_panel, label="Visualization")
        btn_visualization.Bind(wx.EVT_BUTTON, self.result_left_button_visualization)
        btn_annotation = wx.Button(left_panel, label="Annotation")

        bs_lp.Add(btn_data, 0, wx.ALL)
        bs_lp.Add(btn_statistics, 1, wx.ALL)
        bs_lp.Add(btn_visualization, 2, wx.ALL)
        bs_lp.Add(btn_annotation, 3, wx.ALL)
        left_panel.SetSizer(bs_lp)

        # right panel desing
        self.right_panel = wx.Panel(main, -1, size=(1100, 400))
        self.right_panel.SetMinSize((1100, 400))
        #self.right_panel.SetBackgroundColour(wx.BLUE)

        #sizer = wx.BoxSizer(wx.HORIZONTAL)
        #grid = gridlib.Grid(self.right_panel)
        #grid.CreateGrid(35, 25)
        #sizer.Add(grid, 1, wx.EXPAND)
        #self.right_panel.SetSizer(sizer)

        sz = wx.BoxSizer(wx.VERTICAL)
        hsz.Add(left_panel, 1, wx.EXPAND)
        hsz.Add(self.right_panel, 1, wx.EXPAND)

        sz.Add(top_panel, 0, wx.EXPAND)
        sz.Add(hsz, 1, wx.EXPAND)

        # initilized all panels for button
        self.data_panel = wx.Panel(self.right_panel)

        # show grid as default

        #sizer = wx.BoxSizer(wx.HORIZONTAL)
        #grid = self.grid_design(self.right_panel, self.dataframe_list)
        #sizer.Add(grid, 1, wx.EXPAND)
        #self.right_panel.SetSizer(sizer)

        self.statistics_panel = wx.Panel(self.right_panel)
        self.statistics_panel.Hide()
        self.visualization_panel = wx.Panel(self.right_panel)
        self.visualization_panel.Hide()

        main.SetSizer(sz)
        self.nb_result.AddPage(main, self.getFileName)

    # insight pane left side panel; data button desing
    def result_left_button_data(self, event):
        # hide other buttons panels, cannot call unexists object, uff
        self.statistics_panel.Hide()
        self.visualization_panel.Hide()

        try:
            if self.grid is None:
                print("no filename")
        except:
            print("got exception call frist tab")
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.grid = self.grid_design(self.right_panel, self.dataframe_list)

            sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL)
            self.right_panel.SetSizer(sizer)
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

    # notify if there is no data uploaded/display recent insight
    def result_first_tab(self):
        result_panel = wx.Panel(self.nb_result)
        vbox = wx.BoxSizer(wx.VERTICAL)

        welcome_intro_result = "Please select process first."

        welcome_page = wx.StaticText(result_panel, -1, welcome_intro_result)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        result_panel.SetSizer(vbox)

        self.nb_result.AddPage(result_panel, "Result Tab")

    # testing on grid layout unsuccess
    def test_grid_layout_result_pane(self):
        panel = wx.Panel(self, -1)

        sizer = wx.GridBagSizer(0,0)

        btn_data = wx.Button(panel, label="Data")
        btn_statistics = wx.Button(panel, label="Statistics")
        btn_visualization = wx.Button(panel, label="Visualization")
        btn_annotation = wx.Button(panel, label="Annotation")

        sizer.Add(btn_data, pos=(0,0), flag=wx.ALL, border=5)
        sizer.Add(btn_statistics, pos=(1, 0), flag=wx.ALL, border=5)
        sizer.Add(btn_visualization, pos=(2, 0), flag=wx.ALL, border=5)
        sizer.Add(btn_annotation, pos=(3, 0), flag=wx.ALL, border=5)

        #sizer.Add(self.grid_design(), pos=(4, 1), flag=wx.EXPAND) grid desing
        grid = gridlib.Grid(panel)
        grid.CreateGrid(35, 25)

        grid.GetScrollPos(wx.SB_VERTICAL)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(grid, 0, wx.EXPAND)
        sizer.Add(vbox, pos=(1,5), flag=wx.EXPAND)

        panel.SetSizerAndFit(sizer)

        panel.Show()
        self.nb_result.AddPage(panel, "Result")

    # for displaying grid in notebook only
    def grid_design(self, notebook, dataframe_list):
        grid = CommonGridView(notebook)

        return grid.grid_generate(dataframe_list)


    # tomorrow task is to add buttons in each panels
        # discuss about design; I realized we cannot separate event_handler with layout because
        # for example button.Bind doesn't take any return as we expected
        # the layout will be v->c->m->c->v ->: return only not callable
        # I event cannot separate design in each files
        # insight_panel.py; try in auimanger Resutl.working_area_panel not displayed correctly
        # try separating with main toolbar button in individual files

        # how to return/store data location file for other operation like in insight

        # prepare centerpane for all buttons at once then use hide/show method : done
            # create view part for insight where exact same thing will be there as in rapid minor

        # or create open new process for insight and  then take dataframe from them
