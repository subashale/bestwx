import controller
import wx
from view.new_process.new_process_panel import NewProcessPanel

class MainFrame():
    def __init__(self):
        """Constructor"""
        pass

    def tool_clicked(self, event):
        btn = event.GetEventObject().GetLabel()
        print("Label of pressed button = ", btn)

    def new_process_panel(self, event):
        self.new_process_panel = NewProcessPanel(self.parent)
        #self.callPanel = callPanel(self.parent)

    # file dialog click handler
    def on_clicked_open_data(self, event, nb_process):
        getFileLocation, getFileName = self.open_file_dialog()
        dataframe_list = self.make_df(getFileLocation)

        # notebook object and data frame list
        self.grid_design(nb_process, dataframe_list, getFileName)

    # open file dialog
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
        return getFileLocation, getFileName

        dlg_openFileDialog.Destroy()
        frame.Destroy()

    # make dataframe to read csv file and convert to list
    def make_df(self, getFileLocation):
        df = pd.read_csv(getFileLocation)
        df_list = [df.columns.values.tolist()] + df.values.tolist()
        return df_list

