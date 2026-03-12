# GUI frame for the sineTransformations_function.py

from tkinter import *
import sys, os
from tkinter import filedialog, messagebox

import numpy as np
from gui_layout import apply_responsive_grid, make_entry, place_entry
import sineTransformations_function as sT
from smstools.models import utilFunctions as UF


class SineTransformations_frame:

    def __init__(self, parent):

        self.parent = parent
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sounds_dir = os.path.normpath(os.path.join(self.base_dir, "..", "sounds"))
        self.initUI()

    def initUI(self):

        Label(self.parent, text="inputFile:").grid(
            row=0, column=0, sticky=W, padx=5, pady=(10, 2)
        )

        # TEXTBOX TO PRINT PATH OF THE SOUND FILE
        self.filelocation = Entry(self.parent)
        self.filelocation.focus_set()
        self.filelocation["width"] = 32
        self.filelocation.grid(row=0, column=0, sticky=W, padx=(70, 5), pady=(10, 2))
        self.filelocation.delete(0, END)
        self.filelocation.insert(0, os.path.join(self.sounds_dir, "mridangam.wav"))

        # BUTTON TO BROWSE SOUND FILE
        open_file = Button(
            self.parent, text="...", command=self.browse_file
        )  # see: def browse_file(self)
        open_file.grid(
            row=0, column=0, sticky=W, padx=(340, 6), pady=(10, 2)
        )  # put it beside the filelocation textbox

        # BUTTON TO PREVIEW SOUND FILE
        preview = Button(
            self.parent, text=">", command=lambda: UF.wavplay(self.filelocation.get())
        )
        preview.grid(row=0, column=0, sticky=W, padx=(385, 6), pady=(10, 2))

        ## SINE TRANSFORMATIONS ANALYSIS

        # ANALYSIS WINDOW TYPE
        Label(self.parent, text="window:").grid(
            row=1, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.w_type = StringVar()
        self.w_type.set("hamming")  # initial value
        window_option = OptionMenu(
            self.parent,
            self.w_type,
            "rectangular",
            "hanning",
            "hamming",
            "blackman",
            "blackmanharris",
        )
        window_option.grid(row=1, column=0, sticky=W, padx=(65, 5), pady=(10, 2))

        # WINDOW SIZE
        Label(self.parent, text="M:").grid(
            row=1, column=0, sticky=W, padx=(180, 5), pady=(10, 2)
        )
        self.M = make_entry(self.parent)
        self.M.grid(row=1, column=0, sticky=W, padx=(200, 5), pady=(10, 2))
        self.M.delete(0, END)
        self.M.insert(0, "801")

        # FFT SIZE
        Label(self.parent, text="N:").grid(
            row=1, column=0, sticky=W, padx=(255, 5), pady=(10, 2)
        )
        self.N = make_entry(self.parent)
        self.N.grid(row=1, column=0, sticky=W, padx=(275, 5), pady=(10, 2))
        self.N.delete(0, END)
        self.N.insert(0, "2048")

        # THRESHOLD MAGNITUDE
        Label(self.parent, text="t:").grid(
            row=1, column=0, sticky=W, padx=(330, 5), pady=(10, 2)
        )
        self.t = make_entry(self.parent)
        self.t.grid(row=1, column=0, sticky=W, padx=(348, 5), pady=(10, 2))
        self.t.delete(0, END)
        self.t.insert(0, "-90")

        # MIN DURATION SINUSOIDAL TRACKS
        Label(self.parent, text="minSineDur:").grid(
            row=2, column=0, sticky=W, padx=(5, 5), pady=(10, 2)
        )
        self.minSineDur = make_entry(self.parent)
        self.minSineDur.grid(row=2, column=0, sticky=W, padx=(87, 5), pady=(10, 2))
        self.minSineDur.delete(0, END)
        self.minSineDur.insert(0, "0.01")

        # MAX NUMBER OF SINES
        Label(self.parent, text="maxnSines:").grid(
            row=2, column=0, sticky=W, padx=(145, 5), pady=(10, 2)
        )
        self.maxnSines = make_entry(self.parent)
        self.maxnSines.grid(row=2, column=0, sticky=W, padx=(220, 5), pady=(10, 2))
        self.maxnSines.delete(0, END)
        self.maxnSines.insert(0, "150")

        # FREQUENCY DEVIATION ALLOWED
        Label(self.parent, text="freqDevOffset:").grid(
            row=2, column=0, sticky=W, padx=(280, 5), pady=(10, 2)
        )
        self.freqDevOffset = make_entry(self.parent)
        self.freqDevOffset.grid(row=2, column=0, sticky=W, padx=(372, 5), pady=(10, 2))
        self.freqDevOffset.delete(0, END)
        self.freqDevOffset.insert(0, "20")

        # SLOPE OF THE FREQUENCY DEVIATION
        Label(self.parent, text="freqDevSlope:").grid(
            row=3, column=0, sticky=W, padx=(5, 5), pady=(10, 2)
        )
        self.freqDevSlope = make_entry(self.parent)
        self.freqDevSlope.grid(row=3, column=0, sticky=W, padx=(98, 5), pady=(10, 2))
        self.freqDevSlope.delete(0, END)
        self.freqDevSlope.insert(0, "0.02")

        # BUTTON TO DO THE ANALYSIS OF THE SOUND
        self.compute = Button(
            self.parent, text="Analysis/Synthesis", command=self.analysis
        )
        self.compute.grid(row=4, column=0, padx=5, pady=(10, 5), sticky=W)

        # BUTTON TO PLAY ANALYSIS/SYNTHESIS OUTPUT
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_sineModel.wav"
            ),
        )
        self.output.grid(row=4, column=0, padx=(145, 5), pady=(10, 5), sticky=W)

        ###
        # SEPARATION LINE
        Frame(self.parent, height=1, width=50, bg="black").grid(
            row=5, pady=5, sticky=W + E
        )
        ###

        # FREQUENCY SCALING FACTORS
        Label(self.parent, text="Frequency scaling factors (time, value pairs):").grid(
            row=6, column=0, sticky=W, padx=5, pady=(5, 2)
        )
        self.freqScaling = place_entry(self.parent, row=7, padx=5, default="[0, 2.0, 1, .3]", width=35, sticky="we", pady=(0, 2))

        # TIME SCALING FACTORS
        Label(self.parent, text="Time scaling factors (in time, value pairs):").grid(
            row=8, column=0, sticky=W, padx=5, pady=(5, 2)
        )
        self.timeScaling = place_entry(self.parent, row=9, padx=5, default="[0, .0, .671, .671, 1.978, 1.978+1.0]", width=35, sticky="we", pady=(0, 2))

        # BUTTON TO DO THE SYNTHESIS
        self.compute = Button(
            self.parent,
            text="Apply Transformation",
            command=self.transformation_synthesis,
        )
        self.compute.grid(row=13, column=0, padx=5, pady=(10, 15), sticky=W)

        # BUTTON TO PLAY TRANSFORMATION SYNTHESIS OUTPUT
        self.transf_output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_sineModelTransformation.wav"
            ),
        )
        self.transf_output.grid(
            row=13, column=0, padx=(165, 5), pady=(10, 15), sticky=W
        )

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
            inputFile = self.inputFile
            fs = self.fs
            tfreq = self.tfreq
            tmag = self.tmag
            freqScaling = np.array(eval(self.freqScaling.get()))
            timeScaling = np.array(eval(self.timeScaling.get()))

            sT.transformation_synthesis(
                inputFile, fs, tfreq, tmag, freqScaling, timeScaling
            )

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", errorMessage)

        except AttributeError:
            messagebox.showerror(
                "Analysis not computed", "First you must analyse the sound!"
            )
