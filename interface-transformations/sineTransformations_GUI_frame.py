# GUI frame for the sineTransformations_function.py

from tkinter import *
import sys, os
from tkinter import filedialog, messagebox

import numpy as np
from gui_layout import apply_responsive_grid, make_entry, place_entry
import sineTransformations_function as sT
from smstools.models import utilFunctions as UF


class SineTransformations_frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))
        self.initUI()

    def initUI(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Input file
        Label(self, text="Input file (.wav, mono, 44100 Hz):").grid(row=0, column=0, sticky=W, padx=5, pady=(10, 2))
        self.filelocation = Entry(self, width=32)
        self.filelocation.grid(row=0, column=1, sticky=W, padx=10, pady=(10, 2))
        self.filelocation.insert(0, os.path.join(self.sounds_dir, "mridangam.wav"))
        Button(self, text="Browse...", command=self.browse_file).grid(row=0, column=2, sticky=W, padx=(10, 6))
        Button(self, text=">", command=lambda: UF.wavplay(self.filelocation.get())).grid(row=0, column=3, sticky=W, padx=(6, 6))

        # Window type
        Label(self, text="Window type:").grid(row=1, column=0, sticky=W, padx=5, pady=(10, 2))
        self.w_type = StringVar(value="hamming")
        OptionMenu(self, self.w_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris").grid(row=1, column=1, sticky=W, padx=(10, 5), pady=(10, 2))

        # Window size
        Label(self, text="Window size (M):").grid(row=2, column=0, sticky=W, padx=5, pady=(10, 2))
        self.M = Entry(self, width=8)
        self.M.grid(row=2, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.M.insert(0, "801")

        # FFT size
        Label(self, text="FFT size (N):").grid(row=3, column=0, sticky=W, padx=5, pady=(10, 2))
        self.N = Entry(self, width=8)
        self.N.grid(row=3, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.N.insert(0, "2048")

        # Threshold magnitude
        Label(self, text="Threshold (t):").grid(row=4, column=0, sticky=W, padx=5, pady=(10, 2))
        self.t = Entry(self, width=8)
        self.t.grid(row=4, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.t.insert(0, "-90")

        # Min duration of sinusoidal tracks
        Label(self, text="Min sine duration:").grid(row=5, column=0, sticky=W, padx=5, pady=(10, 2))
        self.minSineDur = Entry(self, width=8)
        self.minSineDur.grid(row=5, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.minSineDur.insert(0, "0.01")

        # Max number of sines
        Label(self, text="Max number of sines:").grid(row=6, column=0, sticky=W, padx=5, pady=(10, 2))
        self.maxnSines = Entry(self, width=8)
        self.maxnSines.grid(row=6, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.maxnSines.insert(0, "150")

        # Frequency deviation allowed
        Label(self, text="Freq dev offset:").grid(row=7, column=0, sticky=W, padx=5, pady=(10, 2))
        self.freqDevOffset = Entry(self, width=8)
        self.freqDevOffset.grid(row=7, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.freqDevOffset.insert(0, "20")

        # Slope of the frequency deviation
        Label(self, text="Freq dev slope:").grid(row=8, column=0, sticky=W, padx=5, pady=(10, 2))
        self.freqDevSlope = Entry(self, width=8)
        self.freqDevSlope.grid(row=8, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.freqDevSlope.insert(0, "0.02")

        # Analysis/Synthesis button
        Button(self, text="Analysis/Synthesis", command=self.analysis).grid(row=9, column=1, padx=5, pady=(10, 5), sticky=W)
        Button(self, text="▶", font=("TkDefaultFont", 18, "bold"), width=2, height=1, command=lambda: UF.wavplay(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds", f"{os.path.basename(self.filelocation.get())[:-4]}_sineModel.wav"))).grid(row=9, column=2, padx=(6, 5), pady=(10, 5), sticky=W)

        # Separation line
        Frame(self, height=1, width=50, bg="black").grid(row=10, column=0, columnspan=3, pady=10, sticky=W + E)

        # Frequency scaling factors
        Label(self, text="Frequency scaling factors (time, value pairs):").grid(row=11, column=0, sticky=W, padx=5, pady=(5, 2))
        self.freqScaling = Entry(self, width=35)
        self.freqScaling.grid(row=11, column=1, columnspan=2, sticky=W, padx=5, pady=(0, 2))
        self.freqScaling.insert(0, "[0, 2.0, 1, .3]")

        # Time scaling factors
        Label(self, text="Time scaling factors (in time, value pairs):").grid(row=12, column=0, sticky=W, padx=5, pady=(5, 2))
        self.timeScaling = Entry(self, width=35)
        self.timeScaling.grid(row=12, column=1, columnspan=2, sticky=W, padx=5, pady=(0, 2))
        self.timeScaling.insert(0, "[0, .0, .671, .671, 1.978, 1.978+1.0]")

        # Apply Transformation button
        Button(self, text="Apply Transformation", command=self.transformation_synthesis, font=("TkDefaultFont", 11, "bold"), padx=10, pady=4).grid(row=13, column=1, padx=5, pady=(10, 15), sticky=W)
        Button(self, text="▶", font=("TkDefaultFont", 18, "bold"), width=2, height=1, command=lambda: UF.wavplay(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds", f"{os.path.basename(self.filelocation.get())[:-4]}_sineModelTransformation.wav"))).grid(row=13, column=2, padx=(6, 5), pady=(10, 15), sticky=W)

        # File dialog options
        self.file_opt = options = {}
        options["defaultextension"] = ".wav"
        options["filetypes"] = [("All files", ".*"), ("Wav files", ".wav")]
        options["initialdir"] = self.sounds_dir
        options["title"] = "Open a mono audio file .wav with sample frequency 44100 Hz"

        apply_responsive_grid(self)

    def browse_file(self):

        self.filename = filedialog.askopenfilename(**self.file_opt)

        # set the text of the self.filelocation
        self.filelocation.delete(0, END)
        self.filelocation.insert(0, self.filename)

    def analysis(self):

        try:
            inputFile = self.filelocation.get()
            window = self.w_type.get()
            M = int(self.M.get())
            N = int(self.N.get())
            t = int(self.t.get())
            minSineDur = float(self.minSineDur.get())
            maxnSines = int(self.maxnSines.get())
            freqDevOffset = int(self.freqDevOffset.get())
            freqDevSlope = float(self.freqDevSlope.get())

            self.inputFile, self.fs, self.tfreq, self.tmag = sT.analysis(
                inputFile,
                window,
                M,
                N,
                t,
                minSineDur,
                maxnSines,
                freqDevOffset,
                freqDevSlope,
            )

        except ValueError:
            messagebox.showerror("Input values error", "Some parameters are incorrect")

    def transformation_synthesis(self):

        try:
            # Check if analysis has been computed
            if not hasattr(self, "inputFile") or not hasattr(self, "fs") or not hasattr(self, "tfreq") or not hasattr(self, "tmag"):
                messagebox.showerror("Analysis not computed", "First you must analyse the sound!")
                return
            inputFile = self.inputFile
            fs = self.fs
            tfreq = self.tfreq
            tmag = self.tmag
            freqScaling = np.array(eval(self.freqScaling.get()))
            timeScaling = np.array(eval(self.timeScaling.get()))
            import os
            if not os.path.exists(inputFile):
                messagebox.showerror("Input file error", "Input file does not exist. Make sure you computed the analysis/synthesis.")
                return
            sT.transformation_synthesis(
                inputFile, fs, tfreq, tmag, freqScaling, timeScaling
            )
        except ValueError as errorMessage:
            messagebox.showerror("Input values error", errorMessage)
        except Exception as e:
            messagebox.showerror("Error", str(e))
