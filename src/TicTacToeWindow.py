
import wx

from TicTacToeState import *

class TicTacToeWindow(wx.Window):
    def __init__(self, parent, size=(300, 300)):
        wx.Window.__init__(self, parent, size=size)
        self._mouseover = None
        self._linewidth = 4
        self._init_game()
        self._init_buffer()
        self._event_handlers()

    def _init_game(self):
        self.game = TicTacToeState()

    def _init_buffer(self):
        self._buffer = wx.EmptyBitmap(*self.GetClientSize())
        dc = wx.BufferedDC(None, self._buffer)
        dc.SetBackground(wx.Brush('White'))
        dc.Clear()
        self._draw_scene(dc)
        self._reinit_buffer = False

    def _piece_size(self):
        window_w, window_h = self.GetClientSize()
        piece_w = (window_w - 2 * self._linewidth) / 3
        piece_h = (window_h - 2 * self._linewidth) / 3
        return (piece_w, piece_h)

    def _piece_position(self, row, column):
        piece_w, piece_h = self._piece_size()
        x = row * (piece_w + self._linewidth)
        y = column * (piece_h + self._linewidth)
        return (x, y)

    def _draw_scene(self, dc):
        self._draw_board(dc)
        for index, piece in enumerate(self.game.board):
            row = index // 3
            col = index % 3
            if piece == 'X':
                self._draw_x(dc, row, col)
            elif piece == 'O':
                self._draw_o(dc, row, col)
        if self._mouseover:
            row, col = self._mouseover
            if self.game.turn == 'X':
                self._draw_x(dc, row, col, True)
            else:
                self._draw_o(dc, row, col, True)
        if self.game.is_finished():
            self._draw_end_message(dc)

    def _draw_board(self, dc):
        win_w, win_h = self.GetClientSize()
        piece_w, piece_h = self._piece_size()
        if self._linewidth % 2:
            offset = self._linewidth / 2
        else:
            offset = self._linewidth / 2 - 1
        lines = [
            (piece_w + self._linewidth - offset, 0,
                piece_w + self._linewidth - offset, win_h),
            (2 * (piece_w + self._linewidth) - offset, 0,
                2 * (piece_w + self._linewidth) - offset, win_h),
            (0, piece_h + self._linewidth - offset,
                win_w, piece_h + self._linewidth - offset),
            (0, 2 * (piece_h + self._linewidth) - offset,
                win_w, 2 * (piece_h + self._linewidth) - offset)
        ]
        dc.SetPen(wx.Pen('Black', self._linewidth))
        dc.DrawLineList(lines)

    def _draw_x(self, dc, row, col, faded=False):
        tr_x, tr_y = self._piece_position(row, col)
        piece_w, piece_h = self._piece_size()
        pad = 10
        tr = (tr_x + pad, tr_y + pad)
        tl = (tr_x + piece_w - pad, tr_y + pad)
        br = (tr_x + pad, tr_y + piece_h - pad)
        bl = (tr_x + piece_w - pad, tr_y + piece_h - pad)
        if faded:
            color = '#FF7777'
        else:
            color = '#FF0000'
        dc.SetPen(wx.Pen(color, 10))
        dc.DrawLine(*(tr + bl))
        dc.DrawLine(*(tl + br))

    def _draw_o(self, dc, row, col, faded=False):
        tr_x, tr_y = self._piece_position(row, col)
        piece_w, piece_h = self._piece_size()
        if faded:
            color = '#7777FF'
        else:
            color = '#0000FF'
        dc.SetPen(wx.Pen(color, 10))
        dc.DrawEllipse(tr_x + 10, tr_y + 10, piece_w - 20, piece_h - 20)

    def _end_message_box(self):
        win_w, win_h = self.GetClientSize()
        w, h = int(win_w / 1.5), int(win_h / 2.5)
        x = (win_w - w) / 2
        y = (win_h - h) / 2
        return (x, y, w, h)


    def _draw_end_message(self, dc):
        if self.game.winner:
            message = 'Congrats! %s wins!\nClick to play again.' \
                % (self.game.winner)
        else:
            message = "Cat's game.\nClick to play again."
        dc.SetPen(wx.Pen('Black', 5))
        dc.SetBrush(wx.Brush('#99FFFF'))
        dc.DrawRectangle(*self._end_message_box())
        dc.DrawLabel(message, self._end_message_box(), wx.ALIGN_CENTER)

    def _event_handlers(self):
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_IDLE, self._on_idle)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_click)
        self.Bind(wx.EVT_MOTION, self._on_motion)

    def _on_size(self, event):
        self._reinit_buffer = True

    def _on_paint(self, event):
        wx.BufferedPaintDC(self, self._buffer)

    def _on_idle(self, event):
        if self._reinit_buffer == True:
            self._init_buffer()
            self.Refresh(False)

    def _pos_to_row_col(self, x, y):
        piece_w, piece_h = self._piece_size()
        row = int(x // (piece_w + self._linewidth))
        col = int(y // (piece_h + self._linewidth))
        return (row, col)

    def _on_click(self, event):
        if not self.game.is_finished():
            row, col = self._pos_to_row_col(*event.GetPositionTuple())
            if (row, col) in self.game.valid_moves():
                self.game.do_action(row, col)
                if self._mouseover == (row, col):
                    self._mouseover = None
                self._reinit_buffer = True
        else:
            x, y, w, h = self._end_message_box()
            mouse_x, mouse_y = event.GetPositionTuple()
            if x <= mouse_x < x + w and y <= mouse_y < y + h:
                self._init_game()
                self._reinit_buffer = True

    def _on_motion(self, event):
        if not self.game.is_finished():
            row, col = self._pos_to_row_col(*event.GetPositionTuple())
            if self._mouseover != (row, col):
                if (row, col) in self.game.valid_moves():
                    self._mouseover = (row, col)
                else:
                    self._mouseover = None
                self._reinit_buffer = True

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None)
    tictactoe = TicTacToeWindow(frame)
    frame.Fit()
    frame.Show()
    app.MainLoop()
