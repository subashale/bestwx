import wx
import wx.lib.agw.aui as aui

# common_view view
from view.common_view.common_file_dialog import open_file_dialog as ofd

# controller
from controller.training.training import Training

# loading its child views
from view.training.load_data import LoadData

class TrainingPanel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        # storing info pane to give information on each step


        self.panel_design()

    def panel_design(self):
        # create notebook
        self.nb_training = aui.AuiNotebook(self)

        #self.default_tab()
        self.main_area()
        # to display page to notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb_training, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)

        self.Fit()
        self.Center()
        self.Show()

    # wokring area for each step of model training
    def main_area(self):

        self.panel = wx.Panel(self, -1)

        self.display_panel = wx.Panel(self.panel)
        #self.display_panel.SetMaxSize((wx.EXPAND, 600))
        self.display_panel.SetBackgroundColour("red")
        self.navigation_panel = wx.Panel(self.panel)
        self.navigation_panel.SetMaxSize((wx.EXPAND, 40))
        self.navigation_panel.SetBackgroundColour("blue")

        #self.default_panel()
        self.navigation_area()

        self.basicsizer = wx.BoxSizer(wx.VERTICAL)
        self.basicsizer.Add(self.navigation_panel, 1, wx.EXPAND)
        self.basicsizer.Add(self.display_panel, 1, wx.EXPAND)
        self.panel.SetSizer(self.basicsizer)


        #main.SetSizer(vsz_top)
        self.nb_training.AddPage(self.panel, "Train Model")

    # design for top panel to work
    def default_panel(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.load_data_panel = wx.Panel(self.display_panel)
        welcome_intro = "Training Section, left side file explore, right side data description"
        wx.StaticText(self.load_data_panel, -1, welcome_intro)
        vbox.Add(self.load_data_panel, 0, wx.ALIGN_CENTER)

        self.display_panel.SetSizer(vbox)

    # after opening data from file dialog, describe it with its basic properties else directly go to next step
    # basic properties would be like dataset full name of dataset;
    # no of rows/columns
    # attributes/columns names
    # file size
    ### Select task would be classification, regression and clustering;
    # #
    # button buttons for calling each steps
    def navigation_area(self):

        # design for bottom panel
        vbz = wx.BoxSizer(wx.VERTICAL)
        hbz = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_load_data = wx.Button(self.navigation_panel, 1, 'Load Data')
        self.btn_select_task = wx.Button(self.navigation_panel, 2, 'Select Task')
        self.btn_prepare_target = wx.Button(self.navigation_panel, 3, 'Prepare Target')
        self.btn_select_input = wx.Button(self.navigation_panel, 3, 'Select Input')
        self.btn_model_type = wx.Button(self.navigation_panel, 3, 'Model Type')
        self.btn_result = wx.Button(self.navigation_panel, 3, 'Result')

        # buttons click events
        self.btn_load_data.Bind(wx.EVT_BUTTON, self.onClickedLoadData)
        self.btn_select_task.Bind(wx.EVT_BUTTON, self.onClickedSelectTask)
        self.btn_prepare_target.Bind(wx.EVT_BUTTON, self.onClickedPrepareTarget)
        self.btn_select_input.Bind(wx.EVT_BUTTON, self.onClickedSelectInput)
        self.btn_model_type.Bind(wx.EVT_BUTTON, self.onClickedModelType)
        self.btn_result.Bind(wx.EVT_BUTTON, self.onClickResult)

        # Disable buttons
        self.btn_select_task.Enable(False)
        self.btn_prepare_target.Enable(False)
        self.btn_select_input.Enable(False)
        self.btn_model_type.Enable(False)
        self.btn_result.Enable(False)

        # centering buttons
        hbz.Add(self.btn_load_data, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbz.Add(self.btn_select_task, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        hbz.Add(self.btn_prepare_target, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        hbz.Add(self.btn_select_input, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        hbz.Add(self.btn_model_type, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        hbz.Add(self.btn_result, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        vbz.Add(hbz, 1, wx.ALIGN_CENTER)
        self.navigation_panel.SetSizer(vbz)

    # action for loading data to train a model
    def onClickedLoadData(self, event):
        self.obj_LoadData = LoadData(self)
        self.getFileLocation, self.getFileName = self.obj_LoadData.open_load_data()

        print(self.getFileLocation, self.getFileName)
        if self.getFileLocation and self.getFileName != "":
            # enable next button, btn select task
            self.obj_LoadData.display_data_properties()
            self.btn_select_task.Enable(True)

        # try:
        #     self.getFileLocation, self.getFileName = ofd()
        #     if self.getFileLocation and self.getFileName != "":
        #
        #         # enable next button, btn select task
        #         self.btn_select_task.Enable(True)
        # except:
        #     print("got cancelled")

    # action for selecting task
    def onClickedSelectTask(self, event):
    #if selection is prediction then choose label as well
    # if other skip prepare target;#
        print("select task clicked")
        self.task = {}
        selected_task = "prediction"

        # condition for task selection
        if selected_task == "prediction":
            # put prediction name and label for it, default label can be last column name
            self.task["task"] = "prediction"
            self.task["label"] = "Species"
            # active next button prepare target
            self.btn_prepare_target.Enable(True)
        else:
            # we can skip prepare target for other
            self.btn_select_input.Enable(True)

    # action for prepare target class/label
    def onClickedPrepareTarget(self, event):
    # show label distribution and option to change label name;#
        ok = "ok"
        if ok == "ok":
            self.btn_select_input.Enable(True)

    # action for select input as feature
    def onClickedSelectInput(self, event):
    # select feature for training, default can be all but users can change
    # text cannot directly process there we need to handle that in this part, long text, categorical text, names, other
    # for now on iris data we select all [:-1];#
        select_input = "all"

        self.task["select_input"] = select_input
        if select_input != "":
            self.btn_model_type.Enable(True)

    #action for select types of model to train on
    def onClickedModelType(self, event):
    #give list of algorithm for particular task;#
        model = ["DecisionTreeClassifier", "LogisticRegression"]

        # check if model length not empty
        if len(model) != 0:
            self.task["model"] = model
            self.btn_result.Enable(True)
    # action for result button
    def onClickResult(self, event):
        # we are sending task object and file location but later we can separate each

        obj = Training()
        obj.read_hold(self.getFileLocation, self.task)


