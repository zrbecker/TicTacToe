
import wx

from TicTacToeWindow import *

class TicTacToe(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self._arrange_widgets()
        self._event_handlers()

    def _arrange_widgets(self):
        sizer = wx.GridBagSizer(hgap=10, vgap=10)
        self.ttt_window = TicTacToeWindow(self)
        _, btn_h = wx.Button.GetDefaultSize()
        self.btn_new = wx.Button(self, label='2 Players', size=(125, btn_h))
        self.btn_new_x = wx.Button(self, label='Computer is X',
            size=(125, btn_h))
        self.btn_new_o = wx.Button(self, label='Computer is O',
            size=(125, btn_h))
        sizer.Add(self.ttt_window, pos=(1, 1), span=(4, 1), flag=wx.EXPAND)
        sizer.Add(self.btn_new, pos=(1, 2))
        sizer.Add(self.btn_new_x, pos=(2, 2))
        sizer.Add(self.btn_new_o, pos=(3, 2))
        sizer.AddSpacer(pos=(0, 0), item=(0.5, 0.5))
        sizer.AddSpacer(pos=(5, 3), item=(0.5, 0.5))
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(4)
        self.SetSizer(sizer)
        self.Fit()

    def _event_handlers(self):
        self.Bind(wx.EVT_BUTTON, self.new_game, self.btn_new)
        self.Bind(wx.EVT_BUTTON, self.new_game_ai_x, self.btn_new_x)
        self.Bind(wx.EVT_BUTTON, self.new_game_ai_o, self.btn_new_o)

    def new_game(self, event):
        self.ttt_window.reset_game()

    def new_game_ai_x(self, event):
        self.ttt_window.reset_game('X')

    def new_game_ai_o(self, event):
        self.ttt_window.reset_game('O')

    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TicTacToe(None)
    frame.Show()
    app.MainLoop()
