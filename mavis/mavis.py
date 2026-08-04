# Mavis project
#
# Created by Martin McBride 04-Aug-2026
# MIT licence

import wx

from document import Document
from view import MavisDrawingPanel
import ui

class MainFrame(wx.Frame):
    """Main application window."""

    def __init__(self):
        super().__init__(parent=None, title="wxPython Drawing App", size=(800, 600))

        self.document = Document()

        self.drawing_panel = MavisDrawingPanel(self)

        self._create_menu_bar()
        self._create_status_bar()

        self.Centre()

    # ---------- Menu bar ----------

    def _create_menu_bar(self):
        menu_bar = wx.MenuBar()

        # --- File menu ---
        file_menu = wx.Menu()
        # clear_item = file_menu.Append(wx.ID_ANY, "&Clear Canvas\tCtrl+N",
        #                                "Clear the drawing area")
        # file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q",
                                       "Exit the application")
        menu_bar.Append(file_menu, "&File")

        # --- Edit menu (pen options) ---
        edit_menu = wx.Menu()
        page_settings_item = edit_menu.Append(wx.ID_ANY, "Page settings...\tCtrl+K",
                                        "Set up the page")
        menu_bar.Append(edit_menu, "&Edit")

        # --- Help menu ---
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "&About",
                                       "About this application")
        menu_bar.Append(help_menu, "&Help")

        self.SetMenuBar(menu_bar)

        # Bind menu events
        self.Bind(wx.EVT_MENU, self.on_page_settings, page_settings_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        # self.Bind(wx.EVT_MENU, self.on_choose_colour, colour_item)
        # self.Bind(wx.EVT_MENU, self.on_choose_width, width_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

    # ---------- Status bar ----------

    def _create_status_bar(self):
        # Two fields: general status message, and mouse coordinates
        self.status_bar = self.CreateStatusBar(2)
        self.status_bar.SetStatusWidths([-3, -1])
        self.SetStatusText("Ready", 0)
        self.SetStatusText("X: 0   Y: 0", 1)

    # ---------- Menu event handlers ----------

    def on_page_settings(self, event):
        dlg = ui.PageSettingsDialog(self, self.document.page)
        if dlg.ShowModal() == wx.ID_OK:
            width, height, color = dlg.get_values()
            self.drawing_panel.page.color = color
        dlg.Destroy()

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