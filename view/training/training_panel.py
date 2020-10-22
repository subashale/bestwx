import wx
import wx.lib.agw.aui as aui
import wx.lib.scrolledpanel
import pandas as pd

# common_view view
from view.common_view.common_file_dialog import open_file_dialog as ofd

# controller
from controller.training.training import Training

# loading its child views
from view.common_view.common_gridview import Test, MegaGrid
from view.training.load_data import LoadData

class TrainingPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        # storing info pane to give information on each step
        width, height = wx.GetDisplaySize()

        self.panel_design()

    def panel_design(self):
        # create notebook
        self.nb_training = aui.AuiNotebook(self)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.close, self.nb_training)

        #self.default_tab()
        self.main_area()
        # to display page to notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb_training, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer)

        self.Fit()
        self.Center()
        self.Show()

    def close(self, evt):
        print("close clicked")

        if self.nb_training.GetPageCount() == 0:
            self.main_area()
            self.panel.Layout()
            self.nb_training.Update()
            self.nb_training.Layout()

    # wokring area for each step of model training
    def main_area(self):

        self.panel = wx.Panel(self.nb_training, -1)
        self.display_panel = wx.Panel(self.panel)
        #self.display_panel.SetMaxSize((wx.EXPAND, 600))
        self.display_panel.SetBackgroundColour("#707772")
        self.navigation_panel = wx.Panel(self.panel)
        self.navigation_panel.SetMaxSize((wx.EXPAND, 40))
        self.navigation_panel.SetBackgroundColour("#518962")

        self.navigation_area(self.navigation_panel)
        self.obj_showData = showData(self, self.display_panel)
        self.obj_showData.design()

        self.basicsizer = wx.BoxSizer(wx.VERTICAL)
        self.basicsizer.Add(self.navigation_panel, 1, wx.EXPAND)
        self.basicsizer.Add(self.display_panel, 1, wx.EXPAND)
        self.panel.SetSizer(self.basicsizer)


        # #main.SetSizer(vsz_top)
        self.nb_training.AddPage(self.panel, "Train Model", wx.ALL | wx.EXPAND)

    # after opening data from file dialog, describe it with its basic properties else directly go to next step
    # basic properties would be like dataset full name of dataset;
    # no of rows/columns
    # attributes/columns names
    # file size
    ### Select task would be classification, regression and clustering;
    # #
    # button buttons for calling each steps
    def navigation_area(self, navigation_panel):

        # design for bottom panel
        vbz = wx.BoxSizer(wx.VERTICAL)
        hbz = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_load_data = wx.Button(navigation_panel, 1, 'Load Data')
        self.btn_select_task = wx.Button(navigation_panel, 2, 'Select Task')
        # self.btn_prepare_target = wx.Button(self.navigation_panel, 3, 'Prepare Target')
        # self.btn_select_input = wx.Button(self.navigation_panel, 3, 'Select Input')
        # self.btn_model_type = wx.Button(self.navigation_panel, 3, 'Model Type')
        self.btn_result = wx.Button(navigation_panel, 3, 'Training')

        # buttons click events
        self.btn_load_data.Bind(wx.EVT_BUTTON, self.onClickedLoadData)
        self.btn_select_task.Bind(wx.EVT_BUTTON, self.onClickedSelectTask)
        # self.btn_prepare_target.Bind(wx.EVT_BUTTON, self.onClickedPrepareTarget)
        # self.btn_select_input.Bind(wx.EVT_BUTTON, self.onClickedSelectInput)
        # self.btn_model_type.Bind(wx.EVT_BUTTON, self.onClickedModelType)
        self.btn_result.Bind(wx.EVT_BUTTON, self.onClickTraining)

        # Disable buttons
        self.btn_select_task.Enable(False)
        # self.btn_prepare_target.Enable(False)
        # self.btn_select_input.Enable(False)
        # self.btn_model_type.Enable(False)
        self.btn_result.Enable(False)

        # centering buttons
        hbz.Add(self.btn_load_data, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbz.Add(self.btn_select_task, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        # hbz.Add(self.btn_prepare_target, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        # hbz.Add(self.btn_select_input, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        # hbz.Add(self.btn_model_type, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        hbz.Add(self.btn_result, 1, wx.ALIGN_CENTER | wx.ALL, 5)

        vbz.Add(hbz, 1, wx.ALIGN_CENTER)
        navigation_panel.SetSizer(vbz)

    # action for loading data to train a model
    def onClickedLoadData(self, event):
        obj_LoadData = LoadData(self)
        self.getFileLocation, self.getFileName = obj_LoadData.open_load_data()

        if self.getFileLocation and self.getFileName != "":
            # enable next button, btn select task
            # self.obj_LoadData.display_data_properties()
            self.btn_select_task.Enable(True)


        df = pd.read_csv(self.getFileLocation)
        self.trainingDesing(df, self.getFileName)

    def trainingDesing(self, df, name):
        self.btn_result.Enable(False)
        self.obj_showData.grid_design_huge(df)
        self.nb_training.SetPageText(page_idx=self.nb_training.GetSelection(), text=name)

    # for multiple trainig process
    def getFrom(self, df, name):
        panel = wx.Panel(self.nb_training, -1)
        display_panel = wx.Panel(panel)
        #self.display_panel.SetMaxSize((wx.EXPAND, 600))
        display_panel.SetBackgroundColour("#707772")
        navigation_panel = wx.Panel(panel)
        navigation_panel.SetMaxSize((wx.EXPAND, 40))
        navigation_panel.SetBackgroundColour("#518962")

        self.navigation_area(navigation_panel)
        self.btn_select_task.Enable(True)
        obj_showData = showData(self, display_panel)
        obj_showData.design()
        obj_showData.grid_design_huge(df)


        basicsizer = wx.BoxSizer(wx.VERTICAL)
        basicsizer.Add(navigation_panel, 1, wx.EXPAND)
        basicsizer.Add(display_panel, 1, wx.EXPAND)
        panel.SetSizer(basicsizer)
        self.nb_training.AddPage(panel, name, wx.ALL | wx.EXPAND)

    # action for selecting task
    def onClickedSelectTask(self, event):
        self.processInfo = self.obj_showData.getInformation()

        if self.processInfo:
            self.btn_result.Enable(True)
        else:
            self.btn_result.Enable(False)

    def onClickTraining(self, event):
        # we are sending task object and file location but later we can separate each

        obj = Training()
        obj.read_hold(self.processInfo)

    # new codes

# getters and setters for store process information
class ProcessInformation:
    def __init__(self):
        pass
    def setTask(self, task):
        self.task = task
    def getTask(self):
        return self.task
    def setAlgos(self, algos):
        self.algos = algos
    def getAlgos(self):
        return self.algos
    def setInputFeatures(self, inputFeatures):
        self.inputFeatures = inputFeatures
    def getInputFeatures(self):
        return self.inputFeatures
    def setOutputFeature(self, outputFeature):
        self.outputFeature = outputFeature
    def getOutputFeature(self):
        return self.outputFeature
    def setHeaders(self, headers):
        self.headers = headers
    def getHeaders(self):
        return self.headers
    def setRows(self, rows):
        self.rows = rows
    def getRows(self):
        return self.rows

# Every new panel opeartion
class selectTask(wx.Panel):

    def __init__(self, parent, panel):
        wx.Panel.__init__(self, parent=parent)
        self.panel = panel
        # self.default_panel()

    def desingPanel(self):
        pass


# Every new panel opeartion
class showData(wx.Panel):

    def __init__(self, parent, panel):
        wx.Panel.__init__(self, parent=parent)
        self.panel = panel
        self.dataGridPanl = wx.Panel(self.panel, wx.ID_ANY)
        self.grid_1 = wx.grid.Grid(self.dataGridPanl, wx.ID_ANY)
        self.InfoPnl = wx.Panel(self.panel, wx.ID_ANY)

        self.dataGridPanl.SetMaxSize((750,-1))

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.grid_1.CreateGrid(10, 9)

        # end wxGlade

    def design(self):
        # begin wxGlade: MyFrame.__do_layout
        self.main_sz = wx.BoxSizer(wx.HORIZONTAL)
        self.rightInfosz = wx.BoxSizer(wx.VERTICAL)
        self.leftGridsz = wx.BoxSizer(wx.VERTICAL)
        self.leftGridsz.Add(self.grid_1, 1, wx.EXPAND, 0)
        self.dataGridPanl.SetSizer(self.leftGridsz)
        self.main_sz.Add(self.dataGridPanl, 1, wx.ALL | wx.EXPAND, 0)
        # self.rightInfosz.Add(self.combo_box_1, 0, 0, 0)
        self.rightInfosz.Add((0, 0), 0, 0, 0)
        self.rightInfosz.Add((0, 0), 0, 0, 0)
        self.InfoPnl.SetSizer(self.rightInfosz)

        self.main_sz.Add(self.InfoPnl, 1, wx.EXPAND, 0)
        self.panel.SetSizer(self.main_sz)
        self.panel.Layout()
        return self.panel
        # end wxGlade


    def inputOutputDesing(self, df):
        self.InfoPnlMainsz = wx.BoxSizer(wx.VERTICAL)

        self.taskAlgo = wx.BoxSizer(wx.HORIZONTAL)
        taskSt = wx.StaticText(self.InfoPnl, wx.ID_ANY, "Task")
        self.taskList = ["Classification", "Regression"]
        self.taskCombo = wx.ComboBox(self.InfoPnl, wx.ID_ANY, choices=self.taskList, style=wx.CB_DROPDOWN)
        self.taskCombo.SetValue(self.taskList[0])
        algoSt = wx.StaticText(self.InfoPnl, 0, "Select Algorithm(s)")
        self.listAlgo = ["Decision Tree", "Logistic Regression", "SVM"]
        self.taskAlgo.Add(taskSt)
        self.taskAlgo.Add(self.taskCombo)
        self.taskAlgo.Add(algoSt)

        self.algosCb = []
        for i in self.listAlgo:
            i = wx.CheckBox(self.InfoPnl, wx.ID_ANY, name=i, label=i)
            i.SetValue(True)
            self.taskAlgo.Add(i)
            self.algosCb.append(i)


        self.InfoPnlMainsz.Add(self.taskAlgo, 0)

        self.inputOutputSz = wx.BoxSizer(wx.HORIZONTAL)
        self.inputSz = wx.BoxSizer(wx.VERTICAL)
        self.outputSz = wx.BoxSizer(wx.VERTICAL)

        screenSize = wx.DisplaySize()
        # screenWidth = screenSize[0]
        self.columns = df.columns.tolist()
        maxLen = max([len(c) for c in self.columns])+150
        panel2 = wx.lib.scrolledpanel.ScrolledPanel(self.InfoPnl, -1, size=(maxLen, screenSize[1]),
                                                    style=wx.SIMPLE_BORDER)
        panel2.SetupScrolling()
        panel2.SetBackgroundColour('#FFFFFF')

        self.inputFeaturesCh = []
        for i in self.columns:
            i = wx.CheckBox(panel2, wx.ID_ANY, name=i, label=i)
            if i.GetName() != self.columns[-1]:
                i.SetValue(True)

            self.inputSz.Add(i)
            self.inputFeaturesCh.append(i)
        panel2.SetSizer(self.inputSz)

        self.Bind(wx.EVT_CHECKBOX, self.OnChecked)
        # self.Bind(wx.EVT_BUTTON, self.OnGetData)

        self.output = wx.ComboBox(self.InfoPnl, wx.ID_ANY, choices=self.columns, style=wx.CB_DROPDOWN)

        self.outputSz.Add(self.output)

        inputsSt = wx.StaticText(self.InfoPnl, 0, "Select inputs")
        outputSt = wx.StaticText(self.InfoPnl, 0, "Select output")
        self.inputOutputSz.Add(inputsSt, 0, wx.TOP, 30)
        self.inputOutputSz.Add(panel2, 0, wx.TOP, 30)
        self.inputOutputSz.Add(outputSt, 0, wx.TOP, 30)
        self.inputOutputSz.Add(self.outputSz, 0, wx.TOP, 30)

        self.InfoPnlMainsz.Add(self.inputOutputSz, 0)
        # self.InfoPnl.SetSizer(self.inputOutputSz)
        self.InfoPnl.SetSizer(self.InfoPnlMainsz)

    def OnChecked(self,event):
        clicked = event.GetEventObject()
        print(clicked.GetName())
        print(event.IsChecked())

    def getInformation(self):
        task = self.taskCombo.GetValue()
        output = self.output.GetValue()

        selectedAlgos = []
        for i in self.algosCb:
            if i.IsChecked():
                selectedAlgos.append(i.GetName())

        inputFeatures = []

        for i in self.inputFeaturesCh:
            if i.IsChecked():
                inputFeatures.append(i.GetName())

        if task == "" or len(selectedAlgos) < 1 or len(inputFeatures) < 1 or output== "":
            wx.MessageBox('Fields must not be empty', 'Empty values',
                          wx.OK | wx.ICON_INFORMATION)
            return False

        if output in inputFeatures:
            wx.MessageBox('Output must not present in input checkboxes \n ' +
                          output + ' is in Input Feature', 'Input output problem',
                          wx.OK | wx.ICON_INFORMATION)
            return False
        if task not in self.taskList or output not in self.columns:
            wx.MessageBox('Please select given values only \n Select Task and Output value', 'Selection error',
                          wx.OK | wx.ICON_INFORMATION)
            return False

        # get current data from grid
        headers, rows = self.getCurrentGridData()

        # if everything okey store process information in one object
        processInfo = ProcessInformation()
        processInfo.setTask(task)
        processInfo.setAlgos(selectedAlgos)
        processInfo.setInputFeatures(inputFeatures)
        processInfo.setOutputFeature(output)
        processInfo.setHeaders(headers)
        processInfo.setRows(rows)

        return processInfo

    def getCurrentGridData(self):
        columsData = []

        for index in range(self.grid_1.GetNumberCols()):
            header = self.grid_1.GetColLabelValue(index)
            columsData.append(header)


        rowsData = []
        for rowIdx in range(self.grid_1.GetNumberRows()):
            row = []
            for colIdx in range(self.grid_1.GetNumberCols()):
                # grid.SetCellValue(row, col, str(value))
                value = self.grid_1.GetCellValue(rowIdx, colIdx)
                row.append(value)
            rowsData.append(row)

        return columsData, rowsData

    def girdData(self, dataframe):
        columns = dataframe.columns.values.tolist()
        rows = dataframe.values.tolist()
        data = []
        for i in range(len(rows)):
            d = {}
            for row, col in zip(rows[i], columns):
        #         print(col, row)
                d[col] = row
            data.append((str(i), d))

        return data, columns

    def grid_design_huge(self, dataFrame):
        self.panel.Show()
        self.panel.Layout()
        self.dataFrame = dataFrame
        if self.grid_1:
            self.leftGridsz.Detach(self.grid_1)
            self.grid_1.Destroy()
            self.InfoPnl.Destroy()


        self.InfoPnl = wx.Panel(self.panel, wx.ID_ANY)
        self.main_sz.Add(self.InfoPnl, 1, wx.EXPAND, 0)

        # huge data grid with additional properties
        data, columns = self.girdData(dataFrame)
        self.grid_1 = MegaGrid(self.dataGridPanl, data, columns)
        # self.grid_1.Reset()

        # simple huge data grid
        # grid = Test(self, self.dataGridPanl)
        # self.grid_1 = grid.grid_generate(self.dataFrame)

        self.leftGridsz.Add(self.grid_1, 1, wx.EXPAND, 0)
        self.inputOutputDesing(self.dataFrame)

        # self.grid_1.AutoSize()
        self.panel.Layout()
        return self.panel