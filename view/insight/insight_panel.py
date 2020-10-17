# for result button tab
import wx.lib.agw.aui as aui
import wx

# common_view view
from view.common_view.common_gridview import Test, MegaGrid
from controller.common_view.common_pandas_function import *
## use multi thread concept to handle each functionaliy for each page
# useful when clicking data, statistics.. buttons for each opened dataset
# task assign: ashish ;#

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

    def working_area(self, data_frame_list, objDataHistory):
        # new panel to work with
        self.newPage = PageDesign(self, self.nb_result)

        self.nb_result.AddPage(self.newPage.design(data_frame_list, objDataHistory.getData()[0]), objDataHistory.getData()[1])

        self.nb_result.Layout()


# Every new panel opeartion
class PageDesign(wx.Panel):

    def __init__(self, parent, panel):
        wx.Panel.__init__(self, parent=parent)
        self.panel = panel

    def design(self, data_frame_list, fileLocation):
        self.fileLocation = fileLocation
        self.data_frame_list = data_frame_list

        self.new_page_panel = wx.Panel(self.panel)
        self.new_page_sizer = wx.BoxSizer(wx.VERTICAL)

        # top desing
        button_16 = wx.Button(self.new_page_panel, wx.ID_ANY, "Top button 1: GO TO -->")
        preprocessBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Preprocess")
        trainingBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Training")

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(button_16, 0, 0, 0)
        top_sizer.Add(preprocessBtn, 0, 0, 0)
        top_sizer.Add(trainingBtn, 0, 0, 0)

        self.new_page_sizer.Add(top_sizer, 0, wx.EXPAND, 0)
        # end top desing

        # left desing
        dataBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Data")
        statisticsBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Statistics")
        visualizationBtn = wx.Button(self.new_page_panel, wx.ID_ANY, "Visualization")

        # button click events
        dataBtn.Bind(wx.EVT_BUTTON, self.data_dispaly)
        statisticsBtn.Bind(wx.EVT_BUTTON, self.stat_dispaly)

        self.bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_left_sizer = wx.BoxSizer(wx.VERTICAL)

        bottom_left_sizer.Add(dataBtn, 0, 0, 0)
        bottom_left_sizer.Add(statisticsBtn, 0, 0, 0)
        bottom_left_sizer.Add(visualizationBtn, 0, 0, 0)

        self.bottom_sizer.Add(bottom_left_sizer, 0, wx.ALIGN_CENTER_VERTICAL, 10)

        self.new_page_sizer.Add(self.bottom_sizer, 0, wx.EXPAND, 0)

        self.data_panel_design()

        # self.statistics_panel_desing()

        # end left desing

        # # data grid and options
        # self.data_panel = wx.Panel(self.new_page_panel, wx.ID_ANY)
        # options = ['All', 'Missing rows', 'Not missing rows']
        # self.grid_filter_cmb = wx.ComboBox(self.data_panel, choices=options, pos=(50, 50))
        # self.grid_filter_cmb.SetStringSelection("All")
        # self.grid_filter_cmb.SetEditable(False)
        # self.grid_filter_cmb.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        # self.resultOfSelectionSt = wx.StaticText(self.data_panel, -1, "")
        # self.data_grid = wx.grid.Grid(self.data_panel, wx.ID_ANY, size=(1, 1))
        # show = 10
        # self.data_grid, resultTxt = self.grid_generate(self.data_panel, data_frame_list.head(show))
        # self.resultOfSelectionSt.SetLabel(resultTxt)
        # self.missingMeans = wx.TextCtrl(self.data_panel)
        # self.missingMeans.SetLabelText("',' sep without space")
        #
        # # put button, combo selection and text in one sizer
        # sizer_grid_plus_btn_cmb = wx.BoxSizer(wx.HORIZONTAL)
        # sizer_grid_plus_btn_cmb.Add(self.missingMeans, 1, wx.LEFT | wx.TOP, 10)
        # sizer_grid_plus_btn_cmb.Add(self.grid_filter_cmb, 1, wx.LEFT | wx.TOP, 10)
        # sizer_grid_plus_btn_cmb.Add(self.resultOfSelectionSt, 1, wx.LEFT | wx.TOP, 15)
        #
        # self.bottm_right_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.bottm_right_sizer.Add(sizer_grid_plus_btn_cmb, wx.ALIGN_RIGHT, wx.TOP, 10)
        #
        # self.grid_position = 0
        # if len(data_frame_list.head(show)) < 20:
        #     self.grid_position = 0
        # else:
        #     self.data_panel = 1
        #
        # self.bottm_right_sizer.Add(self.data_grid, self.grid_position, wx.ALL | wx.EXPAND | wx.LEFT | wx.TOP, 10)
        # self.data_grid.AutoSize()
        # self.data_panel.SetSizer(self.bottm_right_sizer)

        # end working area

        self.new_page_panel.SetSizer(self.new_page_sizer)
        self.new_page_panel.Layout()

        return self.new_page_panel

    def data_panel_design(self):
        # data grid and options
        self.data_panel = wx.Panel(self.new_page_panel, wx.ID_ANY)
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
        sizer_grid_plus_btn_cmb.Add(self.missingMeans, 1, wx.LEFT | wx.TOP, 10)
        sizer_grid_plus_btn_cmb.Add(self.grid_filter_cmb, 1, wx.LEFT | wx.TOP, 10)
        sizer_grid_plus_btn_cmb.Add(self.resultOfSelectionSt, 1, wx.LEFT | wx.TOP, 15)

        self.bottm_right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.bottm_right_sizer.Add(sizer_grid_plus_btn_cmb, wx.ALIGN_RIGHT, wx.TOP, 10)

        self.grid_position = 0
        if len(self.data_frame_list) > 20:
            self.grid_position = 1
        else:
            self.grid_position = 0

        self.gridOnlySz = wx.BoxSizer(wx.HORIZONTAL)
        self.gridOnlySz.Add(self.data_grid, self.grid_position, wx.ALL | wx.EXPAND | wx.LEFT | wx.TOP, 10)

        self.bottm_right_sizer.Add(self.gridOnlySz, self.grid_position, wx.ALL | wx.EXPAND | wx.LEFT | wx.TOP, 10)

        self.data_panel.SetSizer(self.bottm_right_sizer)

        self.bottom_sizer.Add(self.data_panel, 0, wx.ALL | wx.EXPAND | wx.LEFT | wx.TOP, 10)

    def statistics_panel_desing(self):
        self.statistics_panel = wx.Panel(self.new_page_panel, wx.ID_ANY)

        self.welcome = wx.StaticText(self.statistics_panel, -1, "asdfadf")
        # put button, combo selection and text in one sizer
        sizer_grid_plus_btn_cmb = wx.BoxSizer(wx.HORIZONTAL)
        sizer_grid_plus_btn_cmb.Add(self.welcome, 1, wx.LEFT | wx.TOP, 15)

        self.statistics_panel.SetSizer(sizer_grid_plus_btn_cmb)

        self.bottom_sizer.Add(self.statistics_panel, 0, wx.ALL | wx.EXPAND | wx.LEFT | wx.TOP, 10)

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
        self.gridOnlySz.Add(self.data_grid, self.grid_position, wx.ALL | wx.EXPAND | wx.LEFT | wx.TOP, 10)
        self.bottm_right_sizer.Add(self.gridOnlySz, self.grid_position, wx.ALL | wx.EXPAND | wx.LEFT | wx.TOP, 10)

        self.new_page_panel.Layout()
        return self.new_page_panel

    def data_dispaly(self, event):
        # targeting each widgets by
        # keep single panels
        if self.statistics_panel:
            self.statistics_panel.Hide()

        self.data_panel_design()
        self.data_panel.Show()

        self.new_page_panel.Layout()
        # while creating individual panels
        # if self.grid_options.Show() == False:
        #     self.grid_options.Show()

    def stat_dispaly(self, event):
        # self.grid_options.Hide()
        if self.data_panel:
            self.data_panel.Hide()


        self.statistics_panel_desing()
        self.statistics_panel.Show()
        self.new_page_panel.Layout()
        # self.statistics_panel.Show()
        # self.grid_1.Destroy() # deletes the widiges
        # self.data_grid.Hide()


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

