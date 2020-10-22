# wx libraries
import wx
import wx.lib.agw.aui as aui
import wx.grid as gridlib

# common_view functions
from controller.common_view import common_pandas_function

# common_view view
from view.common_view.common_file_dialog import open_file_dialog as ofd

# events

# other view part import working area panels
from view.new_process.new_process_panel import NewProcessPanel
from view.insight.insight_panel import InsightPanel
from view.preprocess.preprocess import Preprocess
from view.training.training_panel import TrainingPanel

# common_view panels


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

        self.mgr.AddPane(self.toolbar_buttons(), aui.AuiPaneInfo().CaptionVisible(False).Name("toolbar_pane").MinSize(0, 30).Fixed().Top().CloseButton(False))
        self.mgr.AddPane(self.recent_activities(),
                         aui.AuiPaneInfo().Name("recent_pane").BestSize(180, 0).MinSize(180, 0).Left().Caption("Recent activities").CloseButton(False).MinimizeButton(True))
        #self._center_panel = aui.AuiPaneInfo().CenterPane().CloseButton(False).MinimizeButton(True)
        self.mgr.AddPane(self.working_area_process(),
                         aui.AuiPaneInfo().Name("process_pane").CenterPane().CloseButton(False).MinimizeButton(True))
        self.mgr.AddPane(self.working_area_result(),
                         aui.AuiPaneInfo().Name("insight_pane").CenterPane().CloseButton(False).MinimizeButton(True).Hide())
        self.mgr.AddPane(self.working_area_preprocess(),
                         aui.AuiPaneInfo().Name("preprocess_pane").CenterPane().CloseButton(False).MinimizeButton(
                             True).Hide())
        self.mgr.AddPane(self.working_area_training(),
                         aui.AuiPaneInfo().Name("training_pane").CenterPane().CloseButton(False).MinimizeButton(
                             True).Hide())
        self.mgr.AddPane(self.information_area(), aui.AuiPaneInfo().Name("information_pane").Bottom().Caption("Information area").CloseButton(False).MinimizeButton(True))
        self.mgr.Update()

    # for top pane as toolbar
    def toolbar_buttons(self):
        toolbar_panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_new = wx.Button(toolbar_panel, -1, "New Process")
        self.btn_new.Bind(wx.EVT_BUTTON, self.onClickNewProcess)
        hbox.Add(self.btn_new, 0, wx.ALIGN_CENTER)

        self.btn_insight = wx.Button(toolbar_panel, -1, "Insight")
        self.btn_insight.Bind(wx.EVT_BUTTON, self.onInsightClicked)
        hbox.Add(self.btn_insight, 0, wx.ALIGN_CENTER)

        self.btn_pre_process = wx.Button(toolbar_panel, -1, "Pre-Processing")
        self.btn_pre_process.Bind(wx.EVT_BUTTON, self.onPreProcessingClicked)
        hbox.Add(self.btn_pre_process, 0, wx.ALIGN_CENTER)

        self.btn_train = wx.Button(toolbar_panel, -1, "Training")
        self.btn_train.Bind(wx.EVT_BUTTON, self.onTrainingClicked)
        hbox.Add(self.btn_train, 0, wx.ALIGN_CENTER)

        vbox.Add(hbox, 1, wx.ALIGN_CENTER)
        toolbar_panel.SetSizer(vbox)

        return toolbar_panel

    # for left pane as history/recent activity
    def recent_activities(self):
        self.recent_activities_panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        b2 = wx.Button(self.recent_activities_panel, label="Import Data")
        b2.Bind(wx.EVT_BUTTON, self.on_clicked_open_data)
        vbox.Add(b2, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL)

        self.tree = wx.TreeCtrl(self.recent_activities_panel, -1, wx.Point(0, 0), wx.Size(wx.EXPAND, wx.EXPAND),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemSelected)

        self.root = self.tree.AddRoot("Repository")
        self.items_tree_recent = []

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
        self.tree.AssignImageList(imglist)

        self.items_tree_recent.append(self.tree.AppendItem(self.root, "Active Data", 121))
        self.items_tree_recent.append(self.tree.AppendItem(self.root, "Recent-Today", 122))
        self.items_tree_recent.append(self.tree.AppendItem(self.root, "History", 123))

        self.tree.Expand(self.root)

        vbox.Add(self.tree, 0, wx.ALIGN_CENTER_VERTICAL)
        self.recent_activities_panel.SetSizer(vbox)

        return self.recent_activities_panel

    # tree event handler
    def OnItemSelected(self, event):
        print(self.tree.GetItemText(event.GetItem()))
        dataObj = self.tree.GetItemData(event.GetItem())
        if hasattr(dataObj, 'getData'):
            self.showData(dataObj)


    # after opening data set also update here for recent active dataset
    def recent_tree_active_data(self, dataObj):
        self.tree.AppendItem(self.items_tree_recent[0], text=dataObj.getData()[1], data=dataObj)
        self.tree.Expand(self.items_tree_recent[0])



    # after closing dataset form both side or exit of app also update for history;
    # we can make a log file and from there we can update this tree
    # this can be also applied in recent today#
    def recent_tree_history_data(self):

        pass

    # we can make a log file and from there we can update this tree
    def recent_tree_today_data(self):
        pass

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
        self.obj_insight = InsightPanel(self)

        return self.obj_insight

    # for preprocess working area
    def working_area_preprocess(self):
        self.obj_Preprocess = Preprocess(self)
        return self.obj_Preprocess

    # for training working area
    def working_area_training(self):
        self.obj_Training = TrainingPanel(self)
        return self.obj_Training

    # file dialog click handler
    def on_clicked_open_data(self, event):

        fileLocation, fileName = ofd()
        obj_dataHistory = DataHistory(fileLocation, fileName)
        self.showData(obj_dataHistory)
        self.recent_tree_active_data(obj_dataHistory)

    def showData(self, obj_dataHistory):
        # find separator of data, for optional argument, tsv data;#
        # also update in recent active data

        dataframe = common_pandas_function.read_data(obj_dataHistory.getData()[0])

        # for new process pane
        # self.obj_NewProcess.grid_design(dataframe, fileName)
        self.obj_NewProcess.working_area(dataframe, obj_dataHistory)
        # mainInsight(self, dataframe, fileName)

        # direct to open also in insight pane as tab, for now only show tab from file name

        self.obj_insight.working_area(self.mgr, self.obj_Training, dataframe, obj_dataHistory)

        # self.obj_Training.recent_data(obj_dataHistory)

    # action when new process button is clicked, it will show process_pane
    def onClickNewProcess(self, event):
        print("insight is clicked")
        self.mgr.GetPaneByName("process_pane").Show()
        self.mgr.GetPaneByName("recent_pane").Show()
        self.mgr.GetPaneByName("information_pane").Show()
        self.mgr.GetPaneByName("training_pane").Hide()
        self.mgr.GetPaneByName("insight_pane").Hide()
        self.mgr.GetPaneByName("preprocess_pane").Hide()
        self.mgr.Update()

        if self.obj_NewProcess.nb_process.GetPageCount() == 0:
            self.obj_NewProcess.default_tab()

        self.Layout()
    # action when insight button is clicked, it will show result_pane
    def onInsightClicked(self, event):

        print("insight is clicked")
        # self.mgr.GetPaneByName("recent_pane").Hide()
        # self.mgr.GetPaneByName("information_pane").Hide()
        self.mgr.GetPaneByName("process_pane").Hide()
        self.mgr.GetPaneByName("training_pane").Hide()
        self.mgr.GetPaneByName("preprocess_pane").Hide()
        self.mgr.GetPaneByName("recent_pane").Show()
        self.mgr.GetPaneByName("information_pane").Show()
        self.mgr.GetPaneByName("insight_pane").Show()
        self.mgr.Update()

        if self.obj_insight.nb_result.GetPageCount() == 0:
            self.obj_insight.default_tab()

        self.Layout()
    # action when pre processing button is clicked, it will show pre processing pane
    # able to do basic preprocessing, feature extraction, statistical visualization;#
    def onPreProcessingClicked(self, event):
        self.mgr.GetPaneByName("process_pane").Hide()
        self.mgr.GetPaneByName("insight_pane").Hide()
        self.mgr.GetPaneByName("recent_pane").Show()
        self.mgr.GetPaneByName("training_pane").Hide()
        self.mgr.GetPaneByName("preprocess_pane").Show()
        self.mgr.Update()

        if self.obj_Preprocess.nb_preprocess.GetPageCount() == 0:
            self.obj_Preprocess.default_tab()

    # action when training button is clicked, it will show train_pane
    def onTrainingClicked(self, event):
        # hide every other panel except its own.
        self.mgr.GetPaneByName("process_pane").Hide()
        self.mgr.GetPaneByName("insight_pane").Hide()
        self.mgr.GetPaneByName("preprocess_pane").Hide()
        self.mgr.GetPaneByName("recent_pane").Show()
        self.mgr.GetPaneByName("training_pane").Show()
        self.mgr.Update()

        if self.obj_Training.nb_training.GetPageCount() == 0:
            self.obj_Training.main_area()


class DataHistory:
    def __init__(self, fileLocation, fileName):
        self.fileLocation = fileLocation
        self.fileName = fileName


    def getData(self):
        return self.fileLocation, self.fileName



