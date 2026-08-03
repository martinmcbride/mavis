# Mavis project
#
# Created by Martin McBride 30-Aug-2026
# MIT licence
import dataclasses

import wx
from wx import GraphicsContext

# Main document view

@dataclasses.dataclass
class Page:
    width: float = 100.0
    height: float = 100.0
    color: wx.Colour = dataclasses.field(default_factory=lambda: wx.WHITE)

    def paint(self, gc: GraphicsContext):
        gc.DrawRectangle(0, 0, self.width, self.height, self.color)
