import wx
import re


class PositiveNumberCtrl(wx.TextCtrl):
    """
    A TextCtrl that only accepts positive numbers.

    Parameters
    ----------
    allow_decimal : bool
        If True, allows a single decimal point (e.g. "12.5").
        If False, only whole positive integers are allowed.
    allow_zero : bool
        If True, "0" is a valid value. If False, "0" is rejected
        (still allows the user to type "0" temporarily while typing
        e.g. "0.5", but flags empty/zero as invalid on blur if
        allow_zero=False).
    max_value : float or None
        Optional upper bound. Values above this are rejected as
        keystrokes are entered (best-effort; full validation should
        also be done on IsValid()/GetValue()).
    """

    def __init__(self, parent, value="", allow_decimal=True,
                 allow_zero=True, max_value=None, **kwargs):
        super().__init__(parent, value=value, **kwargs)

        self.allow_decimal = allow_decimal
        self.allow_zero = allow_zero
        self.max_value = max_value

        # Normal / error background colours for visual feedback
        self._normal_bg = self.GetBackgroundColour()
        self._error_bg = wx.Colour(128, 32, 32)

        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_TEXT, self.on_text)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)

        if value:
            self._validate_and_flag(value)

    # ---------- Keystroke filtering ----------

    def on_char(self, event):
        keycode = event.GetKeyCode()

        # Always allow control keys: backspace, delete, arrows, tab,
        # and standard shortcuts (Ctrl+C/V/X/A) so editing still works.
        if keycode in (wx.WXK_BACK, wx.WXK_DELETE, wx.WXK_LEFT, wx.WXK_RIGHT,
                       wx.WXK_UP, wx.WXK_DOWN, wx.WXK_HOME, wx.WXK_END,
                       wx.WXK_TAB, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            event.Skip()
            return

        if event.CmdDown() or event.ControlDown():
            # Allow Ctrl+A/C/V/X/Z etc. through to default handling
            event.Skip()
            return

        char = chr(keycode) if 0 <= keycode < 256 else ""

        # Reject anything that isn't a digit or (optionally) a decimal point
        if char.isdigit():
            event.Skip()
            return

        if self.allow_decimal and char == "." and "." not in self.GetValue():
            event.Skip()
            return

        # Explicitly reject '-', '+', 'e', letters, symbols, and a second '.'
        # by simply not calling event.Skip() -> the keystroke is discarded.

    # ---------- Catch paste / programmatic changes ----------

    def on_text(self, event):
        """
        EVT_CHAR doesn't catch pasted text (Ctrl+V) or SetValue() calls,
        so we re-validate the whole field on every text-change event and
        strip out anything invalid.
        """
        value = self.GetValue()
        cleaned = self._sanitize(value)

        if cleaned != value:
            insertion_point = self.GetInsertionPoint()
            self.ChangeValue(cleaned)  # ChangeValue avoids re-firing EVT_TEXT
            # Try to keep the cursor roughly where the user left it
            new_pos = min(insertion_point, len(cleaned))
            self.SetInsertionPoint(new_pos)

        self._validate_and_flag(cleaned)
        event.Skip()

    def _sanitize(self, text):
        """Strip characters that shouldn't be there (handles paste)."""
        if self.allow_decimal:
            # Keep digits and at most one decimal point
            text = re.sub(r"[^0-9.]", "", text)
            parts = text.split(".")
            if len(parts) > 2:
                text = parts[0] + "." + "".join(parts[1:])
        else:
            text = re.sub(r"[^0-9]", "", text)
        return text

    # ---------- Validation / visual feedback ----------

    def _validate_and_flag(self, text):
        valid = self._is_text_valid(text)
        self.SetBackgroundColour(self._normal_bg if valid else self._error_bg)
        self.Refresh()
        return valid

    def _is_text_valid(self, text):
        if text in ("", "."):
            return False  # empty or just a lone "." isn't a complete number
        try:
            num = float(text)
        except ValueError:
            return False

        if num < 0:
            return False
        if not self.allow_zero and num == 0:
            return False
        if self.max_value is not None and num > self.max_value:
            return False
        return True

    def on_kill_focus(self, event):
        # Re-check validity when the user leaves the field
        self._validate_and_flag(self.GetValue())
        event.Skip()

    # ---------- Public API ----------

    def IsValid(self):
        """Return True if the current contents are a valid positive number."""
        return self._is_text_valid(self.GetValue())

    def GetNumericValue(self, default=0):
        """Return the value as int/float, or `default` if invalid/empty."""
        text = self.GetValue()
        if not self._is_text_valid(text):
            return default
        num = float(text)
        return int(num) if not self.allow_decimal else num


