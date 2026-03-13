# GUI frame for the stochasticModel_function.py

from tkinter import *
import sys, os
from tkinter import filedialog, messagebox

from gui_layout import apply_responsive_grid, make_entry
import stochasticModel_function
from smstools.models import utilFunctions as UF


class StochasticModel_frame:

    def __init__(self, parent):

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
        self.filelocation.insert(0, os.path.join(self.sounds_dir, "ocean.wav"))

        # BUTTON TO BROWSE SOUND FILE
        self.open_file = Button(
            self.parent, text="Browse...", command=self.browse_file
        )  # see: def browse_file(self)
        self.open_file.grid(
            row=1, column=0, sticky=W, padx=(220, 6)
        )  # put it beside the filelocation textbox

        # BUTTON TO PREVIEW SOUND FILE
        self.preview = Button(
            self.parent, text=">", command=lambda: UF.wavplay(self.filelocation.get())
        )
        self.preview.grid(row=1, column=0, sticky=W, padx=(306, 6))

        ## STOCHASTIC MODEL

        # HOP SIZE
        Label(self.parent, text="Hop size (H):").grid(
            row=2, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.H = make_entry(self.parent)
        self.H.grid(row=2, column=0, sticky=W, padx=(90, 5), pady=(10, 2))
        self.H.delete(0, END)
        self.H.insert(0, "256")

        # FFT size
        Label(self.parent, text="FFT size (N):").grid(
            row=3, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.N = make_entry(self.parent)
        self.N.grid(row=3, column=0, sticky=W, padx=(90, 5), pady=(10, 2))
        self.N.delete(0, END)
        self.N.insert(0, "512")

        # DECIMATION FACTOR
        Label(self.parent, text="Decimation factor (bigger than 0, max of 1):").grid(
            row=4, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.stocf = make_entry(self.parent)
        self.stocf.grid(row=4, column=0, sticky=W, padx=(285, 5), pady=(10, 2))
        self.stocf.delete(0, END)
        self.stocf.insert(0, "0.1")

        # MEl SCALE
        Label(self.parent, text="Approximation scale (0: linear, 1: mel):").grid(
            row=5, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.melScale = make_entry(self.parent)
        self.melScale.grid(row=5, column=0, sticky=W, padx=(285, 5), pady=(10, 2))
        self.melScale.delete(0, END)
        self.melScale.insert(0, "1")

        # NORMALIZATION
        Label(self.parent, text="Amplitude normalization (0: no, 1: yes):").grid(
            row=6, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.normalization = make_entry(self.parent)
        self.normalization.grid(row=6, column=0, sticky=W, padx=(285, 5), pady=(10, 2))
        self.normalization.delete(0, END)
        self.normalization.insert(0, "1")

        # BUTTON TO COMPUTE EVERYTHING
        self.compute = Button(self.parent, text="Compute", command=self.compute_model, font=("TkDefaultFont", 11, "bold"), padx=10, pady=4)
        self.compute.grid(row=7, column=0, padx=5, pady=(10, 2), sticky=W)

        # BUTTON TO PLAY OUTPUT
        Label(self.parent, text="Stochastic:").grid(
            row=8, column=0, sticky=W, padx=5, pady=(10, 15)
        )
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds", os.path.basename(self.filelocation.get())[:-4] + "_stochasticModel.wav")),
        )
        self.output.grid(row=8, column=0, padx=(80, 5), pady=(10, 15), sticky=W)

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
            H = int(self.H.get())
            N = int(self.N.get())
            stocf = float(self.stocf.get())
            melScale = int(self.melScale.get())
            normalization = int(self.normalization.get())

            stochasticModel_function.main(
                inputFile, H, N, stocf, melScale, normalization
            )

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", errorMessage)
