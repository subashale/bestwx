from view.main_frame.main_frame import Main_Frame
import wx.lib.mixins.inspection


class Main(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        self.Init()  # initialize the inspection tool
        frame = Main_Frame(None, 1, title='Best Application')
        frame.SetMinSize(size=(900, 700))
        # frame.SetMaxSize(size=(1366, 768))
        # self.SetTopWindow(frame)
        frame.Show()
        frame.Center()
        return True


# old method
# def loadMain():
#     # When this module is run (not imported) then create the app, the
#     # frame, show it, and start the event loop.
#
#     app = wx.App()
#     frame = Main_Frame(None, 1, title='Best Application')
#     frame.SetMinSize(size=(900, 700))
#     frame.SetMaxSize(size=(1366, 768))
#     frame.Show()
#     frame.Center()
#     app.MainLoop()
