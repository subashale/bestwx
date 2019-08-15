import wx
import controller


#from view.main_frame.main_frame import Main_Frame
class NewProcessPanel():
    def __init__(self, parent):
        self.parent = parent

    def on_clicked_open_data(self, event):
        self.event = event
        #btn = event.GetEventObject().GetLabel()

        #fileLocation, fileName  = self.open_file_dialog()
        file_loc = self.open_file_dialog()
        #self.st_load_data.SetLabel(fileName)
        # print("fileName:", fileName)
        # print("Label of pressed button = ", fileLocation, fileName)
        return file_loc

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
        getFileName = dlg_openFileDialog.GetFilename()

        #self.st_load_data.SetLabel(getFileName)

        dlg_openFileDialog.Destroy()
        frame.Destroy()

        objMainFrame = controller.MainFrame(getFileLocation)

        #print(objMainFrame.display())
        # destroy current panel

        # call another panel to display in grid
        #obj = TempDataDisplay(self.parent, objMainFrame.make_data())
        Main_Frame.working_area_process(objMainFrame)
        #return obj
        #return objMainFrame
        # return obj  getFileLocation, getFileName

