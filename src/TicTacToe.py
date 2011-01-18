
import wx

from TicTacToeWindow import *

class TicTacToe(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.ttt_window = TicTacToeWindow(self)
        self.Fit()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TicTacToe(None)
    frame.Show()
    app.MainLoop()
