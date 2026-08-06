# Mavis project
#
# Document and all the items that form part of the document content
#
# Created by Martin McBride 04-Aug-2026
# MIT licence

import dataclasses
from typing import List

import wx
from wx import GraphicsContext

# Main document view

@dataclasses.dataclass
class Page:
    width: float = 500.0
    height: float = 400.0
    color: wx.Colour = dataclasses.field(default_factory=lambda: wx.WHITE)

    def paint(self, gc: GraphicsContext):
        gc.SetBrush(wx.Brush(self.color))
        gc.DrawRectangle(0, 0, self.width, self.height)

@dataclasses.dataclass
class Item:

    def paint(self, gc: GraphicsContext):
        pass


@dataclasses.dataclass
class Rectangle(Item):
    x: float = 0.0
    y: float = 0.0
    width: float = 100.0
    height: float = 100.0
    fill_color: wx.Colour = dataclasses.field(default_factory=lambda: wx.WHITE)
    stroke_color: wx.Colour = dataclasses.field(default_factory=lambda: wx.BLACK)
    stroke_width: float = 4

    def paint(self, gc: GraphicsContext):
        gc.SetBrush(wx.Brush(self.fill_color))
        gc.SetPen(wx.Pen(self.stroke_color, self.stroke_width))
        gc.DrawRectangle(0, 0, self.width, self.height)


@dataclasses.dataclass
class Document:
    page: Page = dataclasses.field(default_factory=lambda: Page())
    items: List[Item] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.items.append(Rectangle())
