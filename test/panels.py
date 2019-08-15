import wx


class Panel1(wx.Panel):
    """create a panel with a label and button on it"""

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        str1 = "War is Hell!"
        self.label1 = wx.StaticText(self, -1, str1, pos=(20, 30))
        self.button1 = wx.Button(self, id=-1, label='Destroy',
                                 pos=(20, 60), size=(175, 28))
        self.button1.Bind(wx.EVT_BUTTON, self.button1Click)

    def button1Click(self, event):
        # this will just destroy the label
        # self.label1.Destroy()
        # this will destroy the whole panel and the components on it
        self.Destroy()


app = wx.PySimpleApp()
# create a window/frame, no parent, -1 is default ID
frame1 = wx.Frame(None, -1, "A label on a panel", size=(300, 150))
# call the derived class, parent is frame and id is -1
Panel1(frame1, -1)
frame1.Show(1)
app.MainLoop()