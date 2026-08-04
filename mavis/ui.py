# Mavis project
#
# Created by Martin McBride 30-Aug-2026
# MIT licence

import wx

from document import Page

class PageSettingsDialog(wx.Dialog):
    """
    A dialog that lets the user configure a page's width, height, and colour.

    Usage:
        dlg = PageSettingsDialog(parent, width=800, height=600, colour=wx.WHITE)
        if dlg.ShowModal() == wx.ID_OK:
            width, height, colour = dlg.get_values()
        dlg.Destroy()
    """

    def __init__(self, parent, page: Page,
                 title="Page Setup"):
        super().__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE)

        self.colour = page.color
        self.width = page.width
        self.height = page.height

        self._build_ui()
        self._bind_events()

        self.Fit()
        self.SetMinSize(self.GetSize())
        self.CentreOnParent()

    # ---------- UI construction ----------

    def _build_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # --- Dimensions group ---
        dims_box = wx.StaticBox(self, label="Page Dimensions")
        dims_sizer = wx.StaticBoxSizer(dims_box, wx.VERTICAL)
        grid = wx.FlexGridSizer(rows=2, cols=2, hgap=10, vgap=8)
        grid.AddGrowableCol(1, 1)

        grid.Add(wx.StaticText(self, label="Width (px):"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        self.width_ctrl = wx.TextCtrl(self, value=str(self.width))
        grid.Add(self.width_ctrl, 0, wx.EXPAND)

        grid.Add(wx.StaticText(self, label="Height (px):"),
                  0, wx.ALIGN_CENTER_VERTICAL)
        self.height_ctrl = wx.TextCtrl(self, value=str(self.height))
        grid.Add(self.height_ctrl, 0, wx.EXPAND)

        dims_sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 8)
        main_sizer.Add(dims_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # --- Colour group ---
        colour_box = wx.StaticBox(self, label="Page Colour")
        colour_sizer = wx.StaticBoxSizer(colour_box, wx.HORIZONTAL)

        self.colour_picker = wx.ColourPickerCtrl(colour_box, colour=self.colour)
        colour_sizer.Add(self.colour_picker, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.ALL, 8)

        main_sizer.Add(colour_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # --- OK / Cancel buttons ---
        btn_sizer = wx.StdDialogButtonSizer()
        ok_btn = wx.Button(self, wx.ID_OK)
        ok_btn.SetDefault()
        cancel_btn = wx.Button(self, wx.ID_CANCEL)
        btn_sizer.AddButton(ok_btn)
        btn_sizer.AddButton(cancel_btn)
        btn_sizer.Realize()

        main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(main_sizer)

    def _bind_events(self):
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=wx.ID_OK)

    # ---------- Event handlers ----------

    def on_ok(self, event):
        # Basic validation before accepting
        width = self.width_ctrl.GetValue()
        height = self.height_ctrl.GetValue()

        if width <= 0 or height <= 0:
            wx.MessageBox("Width and height must be positive numbers.",
                          "Invalid Input", wx.OK | wx.ICON_ERROR, self)
            return  # don't close the dialog

        event.Skip()  # allow default EVT_BUTTON handling to close with ID_OK

    # ---------- Public API ----------

    def get_values(self):
        """Return the (width, height, colour) chosen by the user."""
        return (
            self.width_ctrl.GetValue(),
            self.height_ctrl.GetValue(),
            self.colour_picker.GetColour(),
        )


