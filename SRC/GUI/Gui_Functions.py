import tkinter as tk

C = {
    "bg":        "#0a0e1a",                 #   Main background, night blue
    "panel":     "#111827",                 #   Inner panels
    "card":      "#1a2235",                 #   Cards and listboxes
    "border":    "#1e3a5f",                 #   Steel blue borders
    "accent":    "#f59e0b",                 #   Amber, like real FIDS boards
    "accent2":   "#38bdf8",                 #   Sky blue for Schengen highlight
    "text":      "#e2e8f0",                 #   Primary text
    "text_dim":  "#64748b",                 #   Secondary / dim text
    "green":     "#22c55e",                 #   Free gate indicator
    "red":       "#ef4444",                 #   Occupied gate indicator
    "btn":       "#1e3a5f",                 #   Default button background
    "btn_hover": "#2d5a8e",                 #   Default button hover
    "btn_acc":   "#b45309",                 #   Accent button background
    "btn_acc_h": "#d97706",                 #   Accent button hover
    "hdr":       "#0f172a",                 #   Header / status bar background
}

                                            #   Font Definitions  #

F_TITLE  = ("Courier New", 22, "bold")     #   Main header title
F_BODY   = ("Courier New", 10)             #   Form entries
F_SMALL  = ("Courier New",  9)             #   General labels and buttons
F_SEC    = ("Courier New",  8, "bold")     #   Section heading labels
F_MONO   = ("Courier New", 10)             #   Listbox rows (monospaced)

class FidsButton(tk.Frame):


# Custom styled button with hover effect  #
    def __init__(self, parent, text, command, accent=False, icon="", **kw):
        self._bg = C["btn_acc"] if accent else C["btn"]  # Pick color based on accent flag
        self._hov = C["btn_acc_h"] if accent else C["btn_hover"]  # Pick hover color
        self._cmd = command  # Store callback
        super().__init__(parent, bg=self._bg, cursor="hand2", **kw)

        inner = tk.Frame(self, bg=self._bg, padx=10, pady=5)  # Inner padding frame
        inner.pack(fill=tk.BOTH, expand=True)
        self._inner = inner

        label_text = f"{icon}  {text}" if icon else text  # Prepend icon if given
        self._lbl = tk.Label(inner, text=label_text, bg=self._bg,
                             fg=C["text"], font=F_SMALL,
                             cursor="hand2", anchor=tk.W)
        self._lbl.pack(fill=tk.X)

        for w in (self, inner, self._lbl):  # Bind events to all layers
            w.bind("<Button-1>", lambda e: self._cmd())
            w.bind("<Enter>", self._enter)
            w.bind("<Leave>", self._leave)

            #   Hover enter: lighten background  #


    def _enter(self, _):
        for w in (self, self._inner, self._lbl):
            w.config(bg=self._hov)

            #   Hover leave: restore background  #


    def _leave(self, _):
        for w in (self, self._inner, self._lbl):
            w.config(bg=self._bg)

