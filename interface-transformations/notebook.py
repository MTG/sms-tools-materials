from tkinter import *


class notebook(object):
    def __init__(self, master, side=LEFT):
        self.active_fr = None
        self.count = 0
        self.choice = IntVar()
        self._pending = {}  # fr -> build_func, called on first display
        self.side = LEFT if side in (TOP, BOTTOM) else TOP
        self.rb_fr = Frame(master, borderwidth=2, relief=GROOVE)
        self.rb_fr.pack(side=side, fill=BOTH)

        self.screen_container = Frame(master, borderwidth=2, relief=FLAT)
        self.screen_container.pack(fill=BOTH, expand=1)

        self.v_scrollbar = Scrollbar(self.screen_container, orient=VERTICAL)
        self.v_scrollbar.pack(side=RIGHT, fill=Y)

        self.h_scrollbar = Scrollbar(self.screen_container, orient=HORIZONTAL)
        self.h_scrollbar.pack(side=BOTTOM, fill=X)

        self.canvas = Canvas(
            self.screen_container,
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set,
        )
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.v_scrollbar.config(command=self.canvas.yview)
        self.h_scrollbar.config(command=self.canvas.xview)

        self.screen_fr = Frame(self.canvas, borderwidth=2, relief=FLAT)
        self.screen_window = self.canvas.create_window(
            (0, 0), window=self.screen_fr, anchor="nw"
        )

        self.screen_fr.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._resize_canvas_window)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def __call__(self):
        return self.screen_fr

    def _update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_canvas_window(self, event):
        req_width = self.screen_fr.winfo_reqwidth()
        req_height = self.screen_fr.winfo_reqheight()
        self.canvas.itemconfigure(
            self.screen_window,
            width=max(event.width, req_width),
            height=max(event.height, req_height),
        )
        self._update_scroll_region()

    def _bind_mousewheel(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

    def _unbind_mousewheel(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Shift-MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_screen(self, fr, title, build_func=None):
        if build_func is not None:
            self._pending[fr] = build_func
        b = Radiobutton(
            self.rb_fr,
            text=title,
            indicatoron=0,
            variable=self.choice,
            value=self.count,
            command=lambda: self.display(fr),
        )
        b.pack(fill=BOTH, side=self.side)
        if not self.active_fr:
            fr.pack(fill=BOTH, expand=1)
        self.active_fr = fr
        self.count += 1

    def display(self, fr):
        self.active_fr.forget()
        if fr in self._pending:
            self._pending.pop(fr)(fr)
        fr.pack(fill=BOTH, expand=1)
        self.active_fr = fr
        self.canvas.update_idletasks()
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self._update_scroll_region()
