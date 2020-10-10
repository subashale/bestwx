# import wx
# import wx.lib.agw.aui as aui
# import wx.py as py
#
# class RunApp(wx.App):
#     def __init__(self):
#         wx.App.__init__(self, redirect=False)
#
#     def OnInit(self):
#         frame = MainFrame()
#         frame.Show(True)
#         self.SetTopWindow(frame)
#         self.frame = frame
#         return True
#
# class MainFrame(wx.Frame):
#     ID_SHOW_PANE1 = wx.NewId()
#     ID_SHOW_PANE2 = wx.NewId()
#     ID_SHOW_PANE3 = wx.NewId()
#     ID_LOAD_PERSPECTIVE = wx.NewId()
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1, 'aui demo', size=(600, 400))
#         self._mgr = aui.AuiManager()
#
#         self._mgr.SetManagedWindow(self)
#
#         ns = {}
#         ns['wx'] = wx
#         ns['app'] = wx.GetApp()
#         ns['frame'] = self
#         self.shell = py.shell.Shell(self, -1, locals=ns)
#         auiinfo = aui.AuiPaneInfo().Caption('shell').BestSize((300, 300))\
#                    .DestroyOnClose(False).CenterPane()
#         self._mgr.AddPane(self.shell, auiinfo)
#
#         self.panel1 = wx.Panel(self)
#         auiinfo1 = aui.AuiPaneInfo().Caption('panel1').BestSize((300, 300)).\
#                     DestroyOnClose(False).Top().Snappable().Dockable().\
#                     MinimizeButton(True).MaximizeButton(True)
#
#         self._mgr.Update()
#         self._mgr.AddPane(self.panel1, auiinfo1)
#         self.panel2 = wx.Panel(self)
#         auiinfo2 = aui.AuiPaneInfo().Caption('panel2').BestSize((300, 300)).\
#                     DestroyOnClose(False).Top().Dockable().\
#                     MinimizeButton(True).MaximizeButton(True)
#
#         self._mgr.AddPane(self.panel2, auiinfo2,target=auiinfo1)
#
#         self.panel3 = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#         auiinfo3 = aui.AuiPaneInfo().Caption('panel3').BestSize((300, 300)).\
#                     DestroyOnClose(False).Top().Dockable().\
#                     MinimizeButton(True).MaximizeButton(True)
#
#         self._mgr.AddPane(self.panel3, auiinfo3, target=auiinfo1)
#
#         self.perspective = self._mgr.SavePerspective()
#         self._mgr.Update()
#
#         menubar = wx.MenuBar()
#         viewMenu = wx.Menu()
#         item = wx.MenuItem(viewMenu, self.ID_SHOW_PANE1,
#                            text="Show Panel1",kind = wx.ITEM_NORMAL)
#         viewMenu.Append(item)
#         item = wx.MenuItem(viewMenu, self.ID_SHOW_PANE2,
#                            text="Show Panel2",kind = wx.ITEM_NORMAL)
#         viewMenu.Append(item)
#         item = wx.MenuItem(viewMenu, self.ID_SHOW_PANE3,
#                            text="Show Panel3",kind = wx.ITEM_NORMAL)
#         viewMenu.Append(item)
#         viewMenu.AppendSeparator()
#         item = wx.MenuItem(viewMenu, self.ID_LOAD_PERSPECTIVE,
#                            text="Load Default Perspective",kind = wx.ITEM_NORMAL)
#         viewMenu.Append(item)
#         menubar.Append(viewMenu, '&View')
#         self.SetMenuBar(menubar)
#
#         self.Bind(wx.EVT_TOOL, self.OnProcessTool)
#
#     def OnProcessTool(self, event):
#         eid = event.GetId()
#         if eid == self.ID_SHOW_PANE1:
#             self._mgr.ShowPane(self.panel1, True)
#         elif eid == self.ID_SHOW_PANE2:
#             self._mgr.ShowPane(self.panel2, True)
#         elif eid == self.ID_SHOW_PANE3:
#             self._mgr.ShowPane(self.panel3, True)
#         elif eid == self.ID_LOAD_PERSPECTIVE:
#             self._mgr.LoadPerspective(self.perspective)
#         else:
#             event.Skip()
#
# def main():
#     app = RunApp()
#     app.MainLoop()
#
# if __name__ == '__main__':
#     main()

# !/usr/bin/env python

import wx
import wx.lib.agw.aui.auibook as aui

text = """\
Hello!
Welcome to this little demo of draggable tabs using the aui module.
To try it out, drag a tab from the top of the window all the way to the bottom.  After releasing the mouse, the tab will dock at the hinted position.  Then try it again with the remaining tabs in various other positions.  Finally, try dragging a tab to an existing tab ctrl.  You'll soon see that very complex tab layouts may be achieved.
"""


# ----------------------------------------------------------------------


class TestPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.nb = aui.AuiNotebook(self)
        page = wx.TextCtrl(self.nb, -1, text, style=wx.TE_MULTILINE)
        self.nb.AddPage(page, "Welcome")

        for num in range(1, 5):
            page = wx.TextCtrl(self.nb, -1, "This is page %d" % num,
                               style=wx.TE_MULTILINE)
            self.nb.AddPage(page, "Tab Number %d" % num)

        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.nb.SendSizeEvent)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnPageClose)

    def OnPageClose(self, event):
        print('OnPageClose')
        self.nb.DeletePage(0)

    def OnPageChanged(self, event):
        if self:
            old = event.GetOldSelection()
            new = event.GetSelection()
            sel = self.GetSelection()
            print('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
        if self:
            old = event.GetOldSelection()
            new = event.GetSelection()
            sel = self.GetSelection()
            print('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()


########################################################################
class DemoFrame(wx.Frame):
    """
    wx.Frame class
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "AGW AUI Notebook Tutorial",
                          size=(600, 400))
        self.testPanel = TestPanel(self)


# ----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App()
    frame = DemoFrame()
    frame.Show()
    app.MainLoop()