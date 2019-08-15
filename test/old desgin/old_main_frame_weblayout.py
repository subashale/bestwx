#!/bin/python
"""
Hello World, but with more meat.
"""
import wx

from controller import MainFrame
import event_execute
import controller
class Main_Frame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(Main_Frame, self).__init__(*args, **kw)

        panel = wx.Panel(self)

        # making object to send event
        self.event_execute = event_execute

        # vertical box sizer
        vertical_box = wx.BoxSizer(wx.VERTICAL)

        vertical_box.Add((0, 0), proportion=1, flag=wx.EXPAND)

        LOGO_PATH = "C:/Users/subash/Documents/ml/prj/bestwxpy/test_data/logo.jpg"
        self.img_logo = wx.Image(LOGO_PATH)
        self.image_ctrl = wx.StaticBitmap(panel, bitmap=wx.Bitmap(self.img_logo))
        vertical_box.Add(self.image_ctrl, 0, wx.ALIGN_CENTER)

        self.st_best_app = wx.StaticText(panel, -1, "BEST App")
        vertical_box.Add(self.st_best_app, 0, wx.ALIGN_CENTER)

        vertical_box.Add((-1, 50), proportion=1, flag=wx.EXPAND)

        self.st_load_data = wx.StaticText(panel, -1, "Load Data")
        vertical_box.Add(self.st_load_data, 0, wx.ALIGN_CENTER)

        self.btn = wx.Button(panel, -1, "Upload")
        vertical_box.Add(self.btn, 0, wx.ALIGN_CENTER)

        self.btn.Bind(wx.EVT_BUTTON, self.event_execute.MainFrame.openFileDialog)

        # horizontal box sizer
        vertical_box.Add((-1, 450), proportion=1, flag=wx.EXPAND)

        #vertical_box.Add((-1, 450))
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)

        # previous
        self.btn_previous = wx.Button(panel, -1, "Previous")
        horizontal_box.Add(self.btn_previous, 0, wx.ALIGN_CENTER)
        self.btn_previous.Bind(wx.EVT_BUTTON, self.event_execute.MainFrame.OnClicked)

        # upload
        self.btn_upload = wx.Button(panel, -1, "Upload")
        horizontal_box.Add(self.btn_upload, 0, wx.ALIGN_CENTER)
        self.btn_upload.Bind(wx.EVT_BUTTON, self.event_execute.MainFrame.OnClicked)

        # preparation
        self.btn_preparation = wx.Button(panel, -1, "Preparation")
        horizontal_box.Add(self.btn_preparation, 0, wx.ALIGN_CENTER)
        self.btn_preparation.Bind(wx.EVT_BUTTON, self.event_execute.MainFrame.OnClicked)

        # model training
        self.btn_model_training = wx.Button(panel, -1, "Model Training")
        horizontal_box.Add(self.btn_model_training, 0, wx.ALIGN_CENTER)
        self.btn_model_training.Bind(wx.EVT_BUTTON, self.event_execute.MainFrame.OnClicked)

        # report
        self.btn_report = wx.Button(panel, -1, "Report")
        horizontal_box.Add(self.btn_report, 0, wx.ALIGN_CENTER)
        self.btn_report.Bind(wx.EVT_BUTTON, self.event_execute.MainFrame.OnClicked)

        # prediction
        self.btn_prediction = wx.Button(panel, -1, "Prediction")
        horizontal_box.Add(self.btn_prediction, 0, wx.ALIGN_CENTER)
        self.btn_prediction.Bind(wx.EVT_BUTTON, self.event_execute.MainFrame.OnClicked)

        # next
        self.btn_next = wx.Button(panel, -1, "Next")
        horizontal_box.Add(self.btn_next, 0, wx.ALIGN_CENTER)
        self.btn_next.Bind(wx.EVT_BUTTON, self.event_execute.MainFrame.OnClicked)

        # setting vertical box sizer
        vertical_box.Add(horizontal_box, 1, wx.ALIGN_CENTER)
        panel.SetSizer(vertical_box)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.Centre()
        self.Show()
        self.Fit()



    def OnClickedOpenData(self, event):
        btn = event.GetEventObject().GetLabel()
        self.openFileDialog()

    def openFileDialog(self):
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
        getFileName = dlg_openFileDialog.GetFilename()
        self.st_load_data.SetLabel(getFileName)
        dlg_openFileDialog.Destroy()
        frame.Destroy()

        objMainFrame = controller.MainFrame(getFileLocation)
        print(objMainFrame.display())
        objMainFrame.creatgtable()
        self.creatgtable(getFileLocation)
        return getFileLocation, getFileName



