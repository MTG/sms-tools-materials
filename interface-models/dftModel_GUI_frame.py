# GUI frame for the dftModel_function.py
import os
from tkinter import filedialog, messagebox

import dftModel_function
from gui_layout import apply_responsive_grid, add_window_size_label, make_entry
from smstools.models import utilFunctions as UF
from tkinter import *


class DftModel_frame:

    def __init__(self, parent):

        self.preview = None
        self.parent = parent
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sounds_dir = os.path.normpath(os.path.join(self.base_dir, "..", "sounds"))
        self.initUI()

    def initUI(self):

        Label(self.parent, text="Input file (.wav, mono and 44100 sampling rate):").grid(
            row=0, column=0, sticky=W, padx=5, pady=(10, 2)
        )

        # TEXTBOX TO PRINT PATH OF THE SOUND FILE
        self.filelocation = Entry(self.parent)
        self.filelocation.focus_set()
        self.filelocation["width"] = 25
        self.filelocation.grid(row=1, column=0, sticky=W, padx=10)
        self.filelocation.delete(0, END)
        self.filelocation.insert(0, os.path.join(self.sounds_dir, "piano.wav"))

        # BUTTON TO BROWSE SOUND FILE
        self.open_file = Button(
            self.parent, text="Browse...", command=self.browse_file
        )  # see: def browse_file(self)
        self.open_file.grid(
            row=1, column=0, sticky=W, padx=(220, 6)
        )  # put it beside the filelocation textbox

        # BUTTON TO PREVIEW SOUND FILE
        # self.preview = Button(self.parent, text='>', command=lambda: UF.wavplay(self.filelocation.get()), bg="gray30", fg="white")
        self.preview = Button(
            self.parent, text=">", command=lambda: UF.wavplay(self.filelocation.get())
        )
        self.preview.grid(row=1, column=0, sticky=W, padx=(306, 6))

        ## DFT MODEL

        # ANALYSIS WINDOW TYPE
        Label(self.parent, text="Window type:").grid(
            row=2, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.w_type = StringVar()
        self.w_type.set("blackman")  # initial value
        window_option = OptionMenu(
            self.parent,
            self.w_type,
            "rectangular",
            "hann",
            "hamming",
            "blackman",
            "blackmanharris",
        )
        window_option.grid(row=2, column=0, sticky=W, padx=(95, 5), pady=(10, 2))

        # WINDOW SIZE
        add_window_size_label(self.parent)
        self.M = make_entry(self.parent)
        self.M.grid(row=3, column=0, sticky=W, padx=(115, 5), pady=(10, 2))
        self.M.delete(0, END)
        self.M.insert(0, "511")

        # FFT SIZE
        Label(self.parent, text="FFT size (N) (power of two bigger than M):").grid(
            row=4, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.N = make_entry(self.parent)
        self.N.grid(row=4, column=0, sticky=W, padx=(270, 5), pady=(10, 2))
        self.N.delete(0, END)
        self.N.insert(0, "1024")

        # TIME TO START ANALYSIS
        Label(self.parent, text="Time in sound (in seconds):").grid(
            row=5, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.time = make_entry(self.parent)
        self.time.grid(row=5, column=0, sticky=W, padx=(180, 5), pady=(10, 2))
        self.time.delete(0, END)
        self.time.insert(0, ".2")

        # BUTTON TO COMPUTE EVERYTHING
        self.compute = Button(self.parent, text="Compute", command=self.compute_model)
        self.compute.grid(row=6, column=0, padx=5, pady=(10, 15), sticky=W)

        # define options for opening file
        self.file_opt = options = {}
        options["defaultextension"] = ".wav"
        options["filetypes"] = [("All files", ".*"), ("Wav files", ".wav")]
        options["initialdir"] = self.sounds_dir
        options["title"] = "Open a mono audio file .wav with sample frequency 44100 Hz"

        apply_responsive_grid(self.parent)

    def browse_file(self):

        self.filename = filedialog.askopenfilename(**self.file_opt)

        # set the text of the self.filelocation
        self.filelocation.delete(0, END)
        self.filelocation.insert(0, self.filename)

    def compute_model(self):

        try:
            inputFile = self.filelocation.get()
            window = self.w_type.get()
            M = int(self.M.get())
            N = int(self.N.get())
            time = float(self.time.get())

            dftModel_function.main(inputFile, window, M, N, time)

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", str(errorMessage))
