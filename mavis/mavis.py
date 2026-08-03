# Mavis project
#
# Created by Martin McBride 30-Aug-2026
# MIT licence

import wx

class DrawingPanel(wx.Panel):
    """A panel that allows freehand drawing with the mouse."""

    def __init__(self, parent):
        super().__init__(parent, style=wx.FULL_REPAINT_ON_RESIZE)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetBackgroundColour(wx.WHITE)

        self.lines = []          # list of completed strokes: [(points, colour, width), ...]
        self.current_line = []   # points of the stroke currently being drawn
        self.pen_colour = wx.BLACK
        self.pen_width = 2
        self.drawing = False

        # Bind events
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)

    # ---------- Mouse handlers ----------

    def on_left_down(self, event):
        self.drawing = True
        self.current_line = [event.GetPosition()]
        self.CaptureMouse()

    def on_left_up(self, event):
        if self.drawing:
            self.drawing = False
            if self.HasCapture():
                self.ReleaseMouse()
            if len(self.current_line) > 1:
                self.lines.append(
                    (self.current_line, self.pen_colour, self.pen_width)
                )
            self.current_line = []
            self.Refresh()

    def on_leave(self, event):
        if self.drawing and self.HasCapture():
            self.ReleaseMouse()
            self.drawing = False
            if len(self.current_line) > 1:
                self.lines.append(
                    (self.current_line, self.pen_colour, self.pen_width)
                )
            self.current_line = []
            self.Refresh()

    def on_motion(self, event):
        # Update the status bar with the current mouse coordinates
        frame = self.GetTopLevelParent()
        pos = event.GetPosition()
        frame.SetStatusText(f"X: {pos.x}   Y: {pos.y}", 1)

        if self.drawing and event.Dragging() and event.LeftIsDown():
            self.current_line.append(pos)
            self.Refresh()

    # ---------- Painting ----------

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        if gc is None:
            return

        # Draw completed strokes
        for points, colour, width in self.lines:
            self._draw_stroke(gc, points, colour, width)

        # Draw the stroke currently in progress
        if self.current_line:
            self._draw_stroke(gc, self.current_line, self.pen_colour, self.pen_width)

    @staticmethod
    def _draw_stroke(gc, points, colour, width):
        if len(points) < 2:
            return
        pen = wx.Pen(colour, width)
        gc.SetPen(pen)
        path = gc.CreatePath()
        path.MoveToPoint(points[0].x, points[0].y)
        for pt in points[1:]:
            path.AddLineToPoint(pt.x, pt.y)
        gc.StrokePath(path)

    # ---------- Public API used by the menu ----------

    def clear_canvas(self):
        self.lines = []
        self.current_line = []
        self.Refresh()

    def set_pen_colour(self, colour):
        self.pen_colour = colour

    def set_pen_width(self, width):
        self.pen_width = width


class MainFrame(wx.Frame):
    """Main application window."""

    def __init__(self):
        super().__init__(parent=None, title="wxPython Drawing App", size=(800, 600))

        self.drawing_panel = DrawingPanel(self)

        self._create_menu_bar()
        self._create_status_bar()

        self.Centre()

    # ---------- Menu bar ----------

    def _create_menu_bar(self):
        menu_bar = wx.MenuBar()

        # --- File menu ---
        file_menu = wx.Menu()
        clear_item = file_menu.Append(wx.ID_ANY, "&Clear Canvas\tCtrl+N",
                                       "Clear the drawing area")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q",
                                      "Exit the application")
        menu_bar.Append(file_menu, "&File")

        # --- Edit menu (pen options) ---
        edit_menu = wx.Menu()
        colour_item = edit_menu.Append(wx.ID_ANY, "Choose Pen &Colour...\tCtrl+K",
                                        "Choose the pen colour")
        width_item = edit_menu.Append(wx.ID_ANY, "Choose Pen &Width...\tCtrl+W",
                                       "Choose the pen width")
        menu_bar.Append(edit_menu, "&Edit")

        # --- Help menu ---
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "&About",
                                       "About this application")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

        # Bind menu events
        self.Bind(wx.EVT_MENU, self.on_clear, clear_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_choose_colour, colour_item)
        self.Bind(wx.EVT_MENU, self.on_choose_width, width_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    # ---------- Status bar ----------

    def _create_status_bar(self):
        # Two fields: general status message, and mouse coordinates
        self.status_bar = self.CreateStatusBar(2)
        self.status_bar.SetStatusWidths([-3, -1])
        self.SetStatusText("Ready", 0)
        self.SetStatusText("X: 0   Y: 0", 1)

    # ---------- Menu event handlers ----------

    def on_clear(self, event):
        self.drawing_panel.clear_canvas()
        self.SetStatusText("Canvas cleared", 0)

    def on_exit(self, event):
        self.Close()

    def on_choose_colour(self, event):
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            colour = dlg.GetColourData().GetColour()
            self.drawing_panel.set_pen_colour(colour)
            self.SetStatusText(f"Pen colour set to {colour.GetAsString(wx.C2S_HTML_SYNTAX)}", 0)
        dlg.Destroy()

    def on_choose_width(self, event):
        dlg = wx.TextEntryDialog(self, "Enter pen width (1-20):", "Pen Width",
                                  value=str(self.drawing_panel.pen_width))
        if dlg.ShowModal() == wx.ID_OK:
            try:
                width = max(1, min(20, int(dlg.GetValue())))
                self.drawing_panel.set_pen_width(width)
                self.SetStatusText(f"Pen width set to {width}", 0)
            except ValueError:
                wx.MessageBox("Please enter a valid integer.", "Invalid Input",
                              wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def on_about(self, event):
        wx.MessageBox(
            "wxPython Drawing App\n\n"
            "A simple demonstration of a menu bar, status bar,\n"
            "and a freehand drawing canvas.",
            "About",
            wx.OK | wx.ICON_INFORMATION,
        )


class DrawingApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show()
        return True


if __name__ == "__main__":
    app = DrawingApp()
    app.MainLoop()