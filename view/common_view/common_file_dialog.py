###for common_view function

import wx

# for opening file dialog
def open_file_dialog():
    # It will return name of file and full location
    frame = wx.Frame(None, -1, 'win.py')
    frame.SetSize(0, 0, 100, 25)

    wildcard = "Data Set (*.csv; *.json)|*.csv;*.json|" \
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

    else:
        getFileLocation = dlg_openFileDialog.GetPath()
        getFileName = dlg_openFileDialog.GetFilename()
        dlg_openFileDialog.Destroy()
        frame.Destroy()
        return getFileLocation, getFileName

