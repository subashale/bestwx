# for result button tab
import wx.lib.agw.aui as aui
import wx
import wx.lib.scrolledpanel
# common_view view
from view.common_view.common_gridview import Test, MegaGrid
from controller.common_view.common_pandas_function import *
from controller.helper.StatisticInfo import StatisticInfo as si
## use multi thread concept to handle each functionaliy for each page
# useful when clicking data, statistics.. buttons for each opened dataset
# task assign: ashish ;#
from view.training.training_panel import TrainingPanel

class InsightPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.panel_design()

    def panel_design(self):
        # create notebook
        self.nb_result = aui.AuiNotebook(self)

        self.default_tab()

        # self.new_demo_tab()
        # to display page to notebook
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.nb_result, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Fit()
        self.Center()
        self.Show()

    def default_tab(self):
        welcome_panel = wx.Panel(self.nb_result, 0)

        vbox = wx.BoxSizer(wx.VERTICAL)
        welcome_intro = "Result Section"
        welcome_page = wx.StaticText(welcome_panel, -1, welcome_intro)
        vbox.Add(welcome_page, 0, wx.ALIGN_CENTER)

        welcome_panel.SetSizer(vbox)
        self.nb_result.AddPage(welcome_panel, "Recent")

    def working_area(self, mgr, objTrain, data_frame_list, objDataHistory):
        self.newPage = PageDesign(self, self.nb_result, mgr, objTrain)
        # self.nb_result.AddPage(self.newPage.design(data_frame_list, objDataHistory.getData()[0]), objDataHistory.getData()[1])
        self.newPage.design(data_frame_list, objDataHistory.getData()[0], objDataHistory.getData()[1])
        # self.nb_result.Layout()


# Every new panel opeartion
class PageDesign(wx.Panel):

    def __init__(self, parent, nb_panel, mgr, objTrain):
        wx.Panel.__init__(self, parent=parent)
        self.nb_panel = nb_panel
        self.mgr = mgr
        self.obj_Training = objTrain

    def design(self, data_frame_list, fileLocation, fileName):
        self.fileLocation = fileLocation
        self.data_frame_list = data_frame_list
        self.fileName = fileName
        self.new_page_panel = wx.Panel(self.nb_panel)

        self.data_panel = wx.Panel(self.new_page_panel, wx.ID_ANY)
        self.statistics_panel = wx.Panel(self.new_page_panel, wx.ID_ANY)

        self.new_page_sizer = wx.BoxSizer(wx.VERTICAL)

        dataBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Data")
        statisticsBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Statistics")
        visualizationBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Visualization")

        staticLine = wx.StaticLine(self.new_page_panel, 2, pos=(50, 0), size=(1, 25), style=wx.LI_VERTICAL)
        preprocessBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Preprocess")
        trainingBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Training")
        trainingBtn.Bind(wx.EVT_BUTTON, self.showInTraining)

        # button click events
        dataBtn.Bind(wx.EVT_BUTTON, self.data_dispaly)
        statisticsBtn.Bind(wx.EVT_BUTTON, self.stat_dispaly)

        self.bottom_sizer = wx.BoxSizer(wx.VERTICAL)
        bottom_left_sizer = wx.BoxSizer(wx.HORIZONTAL)

        bottom_left_sizer.Add(dataBtn, 0, 0, 0)
        bottom_left_sizer.Add(statisticsBtn, 0, 0, 0)
        bottom_left_sizer.Add(visualizationBtn, 0, 0, 0)

        bottom_left_sizer.Add(staticLine, flag=wx.ALIGN_RIGHT | wx.RIGHT|wx.LEFT, border=15)
        bottom_left_sizer.Add(preprocessBtn, 0, 0, 0)
        bottom_left_sizer.Add(trainingBtn, 0, 0, 0)

        self.bottom_sizer.Add(bottom_left_sizer, 0, 0)
        self.new_page_sizer.Add(self.bottom_sizer, 0, wx.EXPAND, 0)

        self.data_panel_design()
        self.statistics_panel_desing()
        self.statistics_panel.Hide()
        self.new_page_panel.SetSizer(self.new_page_sizer)
        self.new_page_panel.Layout()

        self.nb_panel.AddPage(self.new_page_panel, self.fileName, wx.ALL | wx.EXPAND)

    def data_panel_design(self):
        # data grid and options

        self.data_panel.SetMaxSize((-1, -1))
        options = ['All', 'Missing rows', 'Not missing rows']
        self.grid_filter_cmb = wx.ComboBox(self.data_panel, choices=options, pos=(50, 50))
        self.grid_filter_cmb.SetStringSelection("All")
        self.grid_filter_cmb.SetEditable(False)
        self.grid_filter_cmb.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        self.resultOfSelectionSt = wx.StaticText(self.data_panel, -1, "")

        # self.data_grid = wx.grid.Grid(self.data_panel, wx.ID_ANY, size=(1, 1))

        # show = 10
        # self.data_grid, resultTxt = self.grid_generate(self.data_panel, self.data_frame_list.head(show))

        resultTxt = (str(len(self.data_frame_list)) + "/" + str(len(self.data_frame_list)))
        grid = Test(self, self.data_panel)
        self.data_grid = grid.grid_generate(self.data_frame_list)

        self.resultOfSelectionSt.SetLabel(resultTxt)
        self.missingMeans = wx.TextCtrl(self.data_panel)
        self.missingMeans.SetLabelText("',' sep without space")

        # put button, combo selection and text in one sizer
        sizer_grid_plus_btn_cmb = wx.BoxSizer(wx.HORIZONTAL)
        sizer_grid_plus_btn_cmb.Add(self.missingMeans, 1, wx.TOP, 10)
        sizer_grid_plus_btn_cmb.Add(self.grid_filter_cmb, 1, wx.LEFT | wx.TOP, 10)
        sizer_grid_plus_btn_cmb.Add(self.resultOfSelectionSt, 1, wx.LEFT | wx.TOP, 15)

        self.bottm_right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.bottm_right_sizer.Add(sizer_grid_plus_btn_cmb, wx.ALIGN_RIGHT)

        self.grid_position = 0
        if len(self.data_frame_list) > 20:
            self.grid_position = 1
        else:
            self.grid_position = 0

        self.gridOnlySz = wx.BoxSizer(wx.HORIZONTAL)

        self.gridOnlySz.Add(self.data_grid, self.grid_position, wx.EXPAND, 0)

        self.bottm_right_sizer.Add(self.gridOnlySz, self.grid_position, wx.EXPAND, 0)

        self.data_panel.SetSizer(self.bottm_right_sizer)

        self.bottom_sizer.Add(self.data_panel, 1, wx.ALL | wx.EXPAND, 0)

        self.nb_panel.Layout()

    def statistics_panel_desing(self):

        self.statistics_panel.Show()

        # check desktop/stat.jpg
        # each attribute becomes panel and check phonix to for minize option
        #     python run.py PyCollapsiblePane
        #     python CollapisblePane
        #
        # 1. write class to get information regarding each attributes


        statpanel = StatisticPanel(self, self.statistics_panel, self.data_frame_list)
        statpanel.design()
        self.bottom_sizer.Add(self.statistics_panel, 0, wx.ALL | wx.EXPAND, 0)

        self.nb_panel.Layout()

    def OnCombo(self, event):
        if self.data_grid:
            self.bottm_right_sizer.Detach(self.gridOnlySz)
            self.gridOnlySz.Detach(self.data_grid)
            self.data_grid.Destroy()
            self.gridOnlySz.Destroy()


        filterSelected = self.grid_filter_cmb.GetValue()
        resultTxt = ""
        data = self.data_frame_list

        missingList = self.missingMeans.GetValue()
        if missingList == "',' sep without space":
            missingList = ""

        grid = Test(self, self.data_panel)

        if filterSelected == "All":
            # if all then get all data and informaiton of len in text and re
            resultTxt = (str(len(self.data_frame_list)) + "/" + str(len(self.data_frame_list)))
            self.data_grid = grid.grid_generate(self.data_frame_list)

            # self.data_grid, resultTxt = self.grid_generate(self.data_panel, data)
            print(filterSelected)
        elif filterSelected == "Missing rows":
            data = missing_df(self.fileLocation, missingList)
            resultTxt = (str(len(data)) + "/" + str(len(self.data_frame_list)))
            self.data_grid = grid.grid_generate(data)
            # self.data_grid, resultTxt = self.grid_generate(self.data_panel, data)
            print(filterSelected)
        elif filterSelected == "Not missing rows":
            data = not_missing_df(self.fileLocation, missingList)
            resultTxt = (str(len(data)) + "/" + str(len(self.data_frame_list)))
            self.data_grid = grid.grid_generate(data)
            # self.data_grid, resultTxt = self.grid_generate(self.data_panel, data)
            print(filterSelected)
        print("len data:", len(data))
        if len(data) > 20:
            self.grid_position = 1
        else:
            self.grid_position = 0

        self.resultOfSelectionSt.SetLabel(resultTxt)
        print("pos", self.grid_position)
        self.gridOnlySz = wx.BoxSizer(wx.HORIZONTAL)
        self.gridOnlySz.Add(self.data_grid, self.grid_position, wx.EXPAND, 0)
        self.bottm_right_sizer.Add(self.gridOnlySz, self.grid_position, wx.EXPAND, 0)
        self.new_page_panel.Layout()
        return self.new_page_panel

    def showInTraining(self, event):
        self.mgr.GetPaneByName("process_pane").Hide()
        self.mgr.GetPaneByName("insight_pane").Hide()
        self.mgr.GetPaneByName("preprocess_pane").Hide()
        self.mgr.GetPaneByName("recent_pane").Show()
        self.mgr.GetPaneByName("training_pane").Show()

        self.obj_Training.trainingDesing(self.data_frame_list, self.fileName)

        self.mgr.Update()

    def data_dispaly(self, event):
        # targeting each widgets by
        # keep single panels
        if self.statistics_panel:
            self.statistics_panel.Hide()

        # self.data_panel_design()
        self.data_panel.Show()

        self.new_page_panel.Layout()

    def stat_dispaly(self, event):
        # self.grid_options.Hide()
        if self.data_panel:
            self.data_panel.Hide()

        # self.statistics_panel_desing()
        self.statistics_panel.Show()
        self.statistics_panel.Layout()
        self.new_page_panel.Layout()

class showData(wx.Panel):

    def __init__(self, parent, panel):
        wx.Panel.__init__(self, parent=parent)
        self.panel = panel
        self.dataGridPanl = wx.Panel(self.panel, wx.ID_ANY)
        self.grid_1 = wx.grid.Grid(self.dataGridPanl, wx.ID_ANY)
        self.InfoPnl = wx.Panel(self.panel, wx.ID_ANY)

        self.dataGridPanl.SetMaxSize((750,-1))

    def OnChecked(self,event):
        clicked = event.GetEventObject()
        print(clicked.GetName())
        print(event.IsChecked())

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

        self.panel.Layout()
        return self.panel

class StatisticPanel(wx.Panel):

    def __init__(self, parent, panel, df):
        wx.Panel.__init__(self, parent=parent)
        self.panel = panel
        self.df = df

    def design(self):
        # calling for statistic information
        self.si = si(self.df)
        mainhbox = wx.BoxSizer(wx.VERTICAL)
        screenSize = wx.DisplaySize()
        self.mainStatPnl = wx.lib.scrolledpanel.ScrolledPanel(self.panel, 1, size=(wx.EXPAND, screenSize[1]),
                                                              style=wx.SIMPLE_BORDER)

        self.mainStatPnl.SetupScrolling()
        self.mainStatPnl.SetBackgroundColour('#FFFFFF')

        # self.mainStatPnl.SetMinSize((wx.ALL, screenSize[0]))

        attributes = self.df.keys()
        main = wx.GridBagSizer(0, 0) # wx.BoxSizer(wx.VERTICAL)

        headerPnl = wx.Panel(self.panel, wx.ID_ANY)
        headerPnl.SetMaxSize((wx.EXPAND, 20))

        hbox = wx.GridBagSizer(0,0)
        attributeName = wx.StaticText(headerPnl, 0, "Name")
        attributeName.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        attributeType = wx.StaticText(headerPnl, 0, "Type")
        attributeType.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        attributeMissing = wx.StaticText(headerPnl, 0, "Missing")
        attributeMissing.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        attributeStat = wx.StaticText(headerPnl, 0, "Statistics")
        attributeStat.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        hbox.Add(attributeName, pos=(0, 0), span=(0, 27), flag=wx.LEFT, border=15)
        hbox.Add(attributeType, pos=(0, 28), flag=wx.LEFT, border=15)
        hbox.Add(attributeMissing, pos=(0, 33), flag=wx.LEFT, border=15)
        hbox.Add(attributeStat, pos=(0, 36), flag=wx.LEFT, border=15)

        headerPnl.SetSizer(hbox)

        mainhbox.Add(headerPnl, 0,0,0)
        # main.Add(headerPnl, pos=(0, 0), flag=wx.EXPAND, border=-1) #main.Add(headerPnl, 0, wx.EXPAND, wx.BOTTOM | wx.TOP, 15)

        color = "#e8e9eb"
        maxNameChar = 25
        for i, att in enumerate(attributes):
            attName = att
            remove = 0
            if len(attName) > maxNameChar:
                remove = len(attName) - maxNameChar
                attName = attName[:-remove] + "..."

            att = wx.Panel(self.mainStatPnl, wx.ID_ANY, size=(wx.EXPAND, 120))
            att.SetMaxSize((wx.EXPAND, 150))
            att.SetBackgroundColour(color)

            name = wx.StaticText(att, wx.ID_ANY, attName)
            name.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            name.SetForegroundColour("black")

            dataType = wx.StaticText(att, wx.ID_ANY, str(self.si.showType(attributes[i])), size=((65, 20)))
            missing = wx.StaticText(att, wx.ID_ANY, str(self.si.getMissing(attributes[i])), size=((65, 20)))

            statData = self.si.getStatistics(attributes[i])
            lMMMAVLabel = list(statData.keys())
            lMMMAVValue = list(statData.values())

            leastOrMin = wx.StaticText(att, wx.ID_ANY, lMMMAVLabel[0], size=((50, 20)))
            leastOrMinVal = wx.StaticText(att, wx.ID_ANY, str(lMMMAVValue[0]), size=((150, 120)))

            fixSizer1 = wx.BoxSizer(wx.HORIZONTAL)
            fixSizer1.Add(leastOrMinVal, 0, wx.EXPAND, 0)

            mostOrMax = wx.StaticText(att, wx.ID_ANY, lMMMAVLabel[1], size=((50, 20)))
            mostOrMaxVal = wx.StaticText(att, wx.ID_ANY, str(lMMMAVValue[1]), size=((150, 120)))

            fixSizer2 = wx.BoxSizer(wx.HORIZONTAL)
            fixSizer2.Add(mostOrMaxVal, 0, wx.EXPAND, 0)

            avgOrValues = wx.StaticText(att, wx.ID_ANY, lMMMAVLabel[2], size=((50, 20)))
            if isinstance(lMMMAVValue[2],float) or isinstance(lMMMAVValue[2], int):
                avgOrValuesVal = wx.StaticText(att, wx.ID_ANY, str(lMMMAVValue[2]), size=((-1, 12)))
                print(attributes[i], lMMMAVValue[0])
            elif isinstance(lMMMAVValue[2], dict):
                print(lMMMAVValue[2])
                label = ""
                for key, count in lMMMAVValue[2].items():

                    if list(lMMMAVValue[2].keys())[-1] == key:
                        label = label+str(key)+"("+str(count)+")"
                    else:
                        label = label + str(key) + "(" + str(count) + ")\n, "
                avgOrValuesVal = wx.TextCtrl(att, wx.ID_ANY, value=label, pos=wx.DefaultPosition,
                                  size=(-1, 120),
                                  style=wx.TE_MULTILINE | wx.SUNKEN_BORDER)
                avgOrValuesVal.SetEditable(False)
            else:
                print(lMMMAVValue[2], type(lMMMAVValue[2]))
                avgOrValuesVal = wx.StaticText(att, wx.ID_ANY, str(lMMMAVValue[2]), size=((200, 100)))

            fixSizer3 = wx.BoxSizer(wx.HORIZONTAL)
            fixSizer3.Add(avgOrValuesVal, 0, wx.EXPAND, 0)

            sizer = wx.GridBagSizer(0,0)

            sizer.Add(name, pos=(0, 0), span=(0, 27), flag=wx.LEFT|wx.TOP, border=15)
            sizer.Add(dataType, pos=(0, 28), flag=wx.LEFT|wx.TOP, border=15)
            sizer.Add(missing, pos=(0, 31), flag=wx.ALIGN_LEFT|wx.LEFT|wx.TOP, border=15)

            sizer.Add(leastOrMin, pos=(0, 33), flag=wx.ALIGN_RIGHT|wx.LEFT|wx.TOP, border=15)
            sizer.Add(fixSizer1, pos=(0, 34), flag=wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, border=15)
            sizer.Add(mostOrMax, pos=(0, 35), flag=wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, border=15)
            sizer.Add(fixSizer2, pos=(0, 36), flag=wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, border=15)
            sizer.Add(avgOrValues, pos=(0, 37), flag=wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, border=15)
            sizer.Add(fixSizer3, pos=(0, 38), flag=wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, border=15)

            att.SetSizer(sizer)

            main.Add(att, pos=(i+1, 0), flag=wx.EXPAND| wx.TOP, border=3)

            # if len(attributes) == i+1:
            #     continue
            # stl = wx.StaticLine(self.mainStatPnl, -1)
            # main.Add(stl, pos=(i+2,0), flag=wx.ALL, border=5)
            #main.Add(wx.StaticLine(self.mainStatPnl, -1), 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        self.mainStatPnl.SetSizer(main)
        # self.mainStatPnl.Layout()
        mainhbox.Add(self.mainStatPnl)
        self.panel.SetSizer(mainhbox)
        self.panel.Layout()