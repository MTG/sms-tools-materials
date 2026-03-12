import sys
import matplotlib
import tkinter as tk

matplotlib.use("Agg")
matplotlib.rcParams["toolbar"] = "toolbar2"
matplotlib.rcParams["interactive"] = False

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import BOTH, Frame, Tk, TOP, Toplevel
from notebook import notebook  # window with tabs
from stftMorph_GUI_frame import *
from sineTransformations_GUI_frame import *
from harmonicTransformations_GUI_frame import *
from stochasticTransformations_GUI_frame import *
from hpsTransformations_GUI_frame import *
from hpsMorph_GUI_frame import *


def fit_window_to_screen(root, margin_x=80, margin_y=120):
    root.update_idletasks()
    width = min(root.winfo_reqwidth(), root.winfo_screenwidth() - margin_x)
    height = min(root.winfo_reqheight(), root.winfo_screenheight() - margin_y)
    root.geometry(f"{width}x{height}+0+0")
    root.minsize(640, 480)
    root.resizable(True, True)


def install_embedded_plot_viewer(root):
    def embedded_show(*args, **kwargs):
        block = kwargs.pop("block", True)
        figures = [plt.figure(num) for num in plt.get_fignums()]
        last_window = None

        for fig in figures:
            manager = getattr(getattr(fig, "canvas", None), "manager", None)
            native_window = getattr(manager, "window", None)
            if native_window is not None:
                try:
                    native_window.withdraw()
                except Exception:
                    pass

            existing_window = getattr(fig, "_sms_plot_window", None)
            if existing_window is not None and existing_window.winfo_exists():
                existing_window.deiconify()
                existing_window.lift()
                canvas = getattr(fig, "_sms_plot_canvas", None)
                if canvas is not None:
                    canvas.draw_idle()
                last_window = existing_window
                continue

            window = Toplevel(root)
            window.title(fig._suptitle.get_text() if fig._suptitle else f"Plot {fig.number}")
            window.minsize(640, 480)

            container = Frame(window)
            container.pack(fill=BOTH, expand=1)

            canvas = FigureCanvasTkAgg(fig, master=container)
            toolbar = NavigationToolbar2Tk(canvas, container, pack_toolbar=False)
            toolbar.update()
            toolbar.pack(fill="x")
            canvas.get_tk_widget().pack(fill=BOTH, expand=1)
            canvas.draw()

            fig._sms_plot_window = window
            fig._sms_plot_canvas = canvas

            def close_window(current_fig=fig, current_window=window):
                current_fig._sms_plot_window = None
                current_fig._sms_plot_canvas = None
                plt.close(current_fig)
                current_window.destroy()

            window.protocol("WM_DELETE_WINDOW", close_window)
            last_window = window

        if block and last_window is not None:
            last_window.wait_visibility()

    plt.show = embedded_show
    plt.ioff()


def install_audio_button_style():
    if getattr(tk.Button, "_sms_audio_style_installed", False):
        return

    original_init = tk.Button.__init__

    def styled_init(self, master=None, cnf=None, **kw):
        cnf = {} if cnf is None else dict(cnf)
        text = kw.get("text", cnf.get("text"))

        if isinstance(text, str) and (text == ">" or text.startswith("> ")):
            styled_text = "▶ Play" if text == ">" else f"▶{text[1:]}"

            if "text" in kw:
                kw["text"] = styled_text
                kw.setdefault("width", max(10, len(styled_text)))
                kw.setdefault("font", ("TkDefaultFont", 11, "bold"))
                kw.setdefault("padx", 6)
                kw.setdefault("pady", 2)
            else:
                cnf["text"] = styled_text
                cnf.setdefault("width", max(10, len(styled_text)))
                cnf.setdefault("font", ("TkDefaultFont", 11, "bold"))
                cnf.setdefault("padx", 6)
                cnf.setdefault("pady", 2)

        original_init(self, master, cnf, **kw)

    tk.Button.__init__ = styled_init
    tk.Button._sms_audio_style_installed = True


root = Tk()
root.title("sms-tools transformations GUI")
install_audio_button_style()
install_embedded_plot_viewer(root)
nb = notebook(
    root, TOP
)  # make a few diverse frames (panels), each using the NB as 'master':

# Frames are built lazily: only when the tab is first selected.
f1 = Frame(nb()); nb.add_screen(f1, "STFT Morph",  build_func=lambda f: StftMorph_frame(f))
f2 = Frame(nb()); nb.add_screen(f2, "Sine",         build_func=lambda f: SineTransformations_frame(f))
f3 = Frame(nb()); nb.add_screen(f3, "Harmonic",     build_func=lambda f: HarmonicTransformations_frame(f))
f4 = Frame(nb()); nb.add_screen(f4, "Stochastic",   build_func=lambda f: StochasticTransformations_frame(f))
f5 = Frame(nb()); nb.add_screen(f5, "HPS",          build_func=lambda f: HpsTransformations_frame(f))
f6 = Frame(nb()); nb.add_screen(f6, "HPS Morph",    build_func=lambda f: HpsMorph_frame(f))

nb.display(f1)

fit_window_to_screen(root)
root.mainloop()
