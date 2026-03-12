# GUI frame for the hprModel_function.py

from tkinter import *
import os
import sys
from tkinter import messagebox, filedialog

import hpsModel_function
from smstools.models import utilFunctions as UF


class HpsModel_frame:

    def __init__(self, parent):

        self.parent = parent
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sounds_dir = os.path.normpath(os.path.join(self.base_dir, "..", "sounds"))
        self.initUI()

    def initUI(self):

        # Configure columns for responsive layout
        self.parent.grid_columnconfigure(0, weight=0)
        self.parent.grid_columnconfigure(1, weight=1)
        self.parent.grid_columnconfigure(2, weight=0)
        self.parent.grid_columnconfigure(3, weight=1)

        Label(self.parent, text="Input file (.wav, mono and 44100 sampling rate):").grid(
            row=0, column=0, columnspan=4, sticky=W, padx=5, pady=(10, 2)
        )

        # TEXTBOX TO PRINT PATH OF THE SOUND FILE
        self.filelocation = Entry(self.parent)
        self.filelocation.focus_set()
        self.filelocation["width"] = 25
        self.filelocation.grid(row=1, column=0, columnspan=2, sticky=EW, padx=5, pady=(5, 5))
        self.filelocation.delete(0, END)
        self.filelocation.insert(0, os.path.join(self.sounds_dir, "sax-phrase-short.wav"))

        # BUTTON TO BROWSE SOUND FILE
        self.open_file = Button(
            self.parent, text="Browse...", command=self.browse_file
        )
        self.open_file.grid(row=1, column=2, sticky=W, padx=5, pady=(5, 5))

        # BUTTON TO PREVIEW SOUND FILE
        self.preview = Button(
            self.parent, text=">", command=lambda: UF.wavplay(self.filelocation.get())
        )
        self.preview.grid(row=1, column=3, sticky=W, padx=5, pady=(5, 5))

        ## HARMONIC MODEL PARAMETERS

        # Row 2: Window type + Window size
        Label(self.parent, text="Window type:").grid(
            row=2, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.w_type = StringVar()
        self.w_type.set("blackman")
        window_option = OptionMenu(
            self.parent,
            self.w_type,
            "rectangular",
            "hann",
            "hamming",
            "blackman",
            "blackmanharris",
        )
        window_option.grid(row=2, column=1, sticky=EW, padx=5, pady=(10, 2))

        Label(self.parent, text="M:").grid(row=2, column=2, sticky=W, padx=5, pady=(10, 2))
        self.M = Entry(self.parent, justify=CENTER)
        self.M.grid(row=2, column=3, sticky=EW, padx=5, pady=(10, 2))
        self.M.delete(0, END)
        self.M.insert(0, "601")

        # Row 3: FFT size + Magnitude threshold
        Label(self.parent, text="N:").grid(row=3, column=0, sticky=W, padx=5, pady=(5, 2))
        self.N = Entry(self.parent, justify=CENTER)
        self.N.grid(row=3, column=1, sticky=EW, padx=5, pady=(5, 2))
        self.N.delete(0, END)
        self.N.insert(0, "1024")

        Label(self.parent, text="Threshold (dB):").grid(
            row=3, column=2, sticky=W, padx=5, pady=(5, 2)
        )
        self.t = Entry(self.parent, justify=CENTER)
        self.t.grid(row=3, column=3, sticky=EW, padx=5, pady=(5, 2))
        self.t.delete(0, END)
        self.t.insert(0, "-100")

        # Row 4: Min sine duration + Max harmonics
        Label(self.parent, text="Min duration (s):").grid(
            row=4, column=0, sticky=W, padx=5, pady=(5, 2)
        )
        self.minSineDur = Entry(self.parent, justify=CENTER)
        self.minSineDur.grid(row=4, column=1, sticky=EW, padx=5, pady=(5, 2))
        self.minSineDur.delete(0, END)
        self.minSineDur.insert(0, "0.1")

        Label(self.parent, text="Max harmonics:").grid(
            row=4, column=2, sticky=W, padx=5, pady=(5, 2)
        )
        self.nH = Entry(self.parent, justify=CENTER)
        self.nH.grid(row=4, column=3, sticky=EW, padx=5, pady=(5, 2))
        self.nH.delete(0, END)
        self.nH.insert(0, "100")

        # Row 5: Min f0 + Max f0
        Label(self.parent, text="Min f0 (Hz):").grid(
            row=5, column=0, sticky=W, padx=5, pady=(5, 2)
        )
        self.minf0 = Entry(self.parent, justify=CENTER)
        self.minf0.grid(row=5, column=1, sticky=EW, padx=5, pady=(5, 2))
        self.minf0.delete(0, END)
        self.minf0.insert(0, "350")

        Label(self.parent, text="Max f0 (Hz):").grid(
            row=5, column=2, sticky=W, padx=5, pady=(5, 2)
        )
        self.maxf0 = Entry(self.parent, justify=CENTER)
        self.maxf0.grid(row=5, column=3, sticky=EW, padx=5, pady=(5, 2))
        self.maxf0.delete(0, END)
        self.maxf0.insert(0, "700")

        # Row 6: f0 error + harmonic deviation
        Label(self.parent, text="f0 error:").grid(row=6, column=0, sticky=W, padx=5, pady=(5, 2))
        self.f0et = Entry(self.parent, justify=CENTER)
        self.f0et.grid(row=6, column=1, sticky=EW, padx=5, pady=(5, 2))
        self.f0et.delete(0, END)
        self.f0et.insert(0, "5")

        Label(self.parent, text="Harmonic dev:").grid(
            row=6, column=2, sticky=W, padx=5, pady=(5, 2)
        )
        self.harmDevSlope = Entry(self.parent, justify=CENTER)
        self.harmDevSlope.grid(row=6, column=3, sticky=EW, padx=5, pady=(5, 2))
        self.harmDevSlope.delete(0, END)
        self.harmDevSlope.insert(0, "0.01")

        # Row 7: Stochastic factor
        Label(self.parent, text="Stochastic factor:").grid(
            row=7, column=0, sticky=W, padx=5, pady=(5, 2)
        )
        self.stocf = Entry(self.parent, justify=CENTER)
        self.stocf.grid(row=7, column=1, sticky=EW, padx=5, pady=(5, 2))
        self.stocf.delete(0, END)
        self.stocf.insert(0, "0.2")

        # Row 8: Compute button
        self.compute = Button(self.parent, text="Compute", command=self.compute_model)
        self.compute.grid(row=8, column=0, columnspan=4, sticky=W, padx=5, pady=(10, 5))

        # Row 9: Output buttons
        Label(self.parent, text="Outputs:").grid(
            row=9, column=0, sticky=W, padx=5, pady=(5, 5)
        )

        self.output_sine = Button(
            self.parent,
            text="> Sinusoidal",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_hpsModel_sines.wav"
            ),
        )
        self.output_sine.grid(row=9, column=1, sticky=W, padx=5, pady=(5, 5))

        self.output_stoch = Button(
            self.parent,
            text="> Stochastic",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_hpsModel_stochastic.wav"
            ),
        )
        self.output_stoch.grid(row=9, column=2, sticky=W, padx=5, pady=(5, 5))

        self.output = Button(
            self.parent,
            text="> Combined",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_hpsModel.wav"
            ),
        )
        self.output.grid(row=9, column=3, sticky=W, padx=5, pady=(5, 5))

        # define options for opening file
        self.file_opt = options = {}
        options["defaultextension"] = ".wav"
        options["filetypes"] = [("All files", ".*"), ("Wav files", ".wav")]
        options["initialdir"] = self.sounds_dir
        options["title"] = "Open a mono audio file .wav with sample frequency 44100 Hz"

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
            t = int(self.t.get())
            minSineDur = float(self.minSineDur.get())
            nH = int(self.nH.get())
            minf0 = int(self.minf0.get())
            maxf0 = int(self.maxf0.get())
            f0et = int(self.f0et.get())
            harmDevSlope = float(self.harmDevSlope.get())
            stocf = float(self.stocf.get())

            hpsModel_function.main(
                inputFile,
                window,
                M,
                N,
                t,
                minSineDur,
                nH,
                minf0,
                maxf0,
                f0et,
                harmDevSlope,
                stocf,
            )

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", str(errorMessage))
