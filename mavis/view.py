# Mavis project
#
# Created by Martin McBride 30-Aug-2026
# MIT licence
import dataclasses
from typing import Tuple

import wx

from document import Page

# Main document view

@dataclasses.dataclass
class ViewSettings:
    scale: float = 100.0
    origin: Tuple[float, float] = (0., 0.)
    color: wx.Colour = dataclasses.field(default_factory=lambda: wx.Colour(128, 128, 128))


class MavisDrawingPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)

        self.parent = parent
        self.viewSettings = ViewSettings()
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetBackgroundColour(self.viewSettings.color)

        # Bind events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)

    # ---------- Mouse handlers ----------

    def on_left_down(self, event):
        pass

    def on_left_up(self, event):
        pass

    def on_leave(self, event):
        pass

    def on_motion(self, event):
        pass

    # ---------- Painting ----------

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        if gc is None:
            return

        doc = self.parent.document
        doc.page.paint(gc)

        # gc.SetBrush(wx.Brush(doc.page.color))
        # gc.DrawRectangle(0, 0, doc.page.width, doc.page.height)

        # # Draw completed strokes
        # for points, colour, width in self.lines:
        #     self._draw_stroke(gc, points, colour, width)
        #
        # # Draw the stroke currently in progress
        # if self.current_line:
        #     self._draw_stroke(gc, self.current_line, self.pen_colour, self.pen_width)

