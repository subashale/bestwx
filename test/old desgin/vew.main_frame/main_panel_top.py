"""
This panel contents recent activity, process information, available solution features and other information
# Recent activities:
    - List of recently happened process
    - Shortcut of quick check for each recent process
# Process information:
    - As help it will show how process can be done
# Available solution:
    - All the available feature that it provides for example,
        Sentiment analysis, outlier detection, statistical analysis, statistical testing,
# Other information:
    - Quick help information area, with search feature
    - Available libraries information
"""

import wx


class MainPanelTop(wx.Panel):

    def __init__(self, parent):
        self.panel = wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.panel_design()

    def panel_design(self):
        wx.TextCtrl(self, -1, "Pane 1 - sample text")

