# GUI frame for the harmonicTransformations_function.py

from tkinter import *
import sys, os
from tkinter import messagebox

import numpy as np
from gui_layout import apply_responsive_grid, make_entry, place_entry
import harmonicTransformations_function as hT
from smstools.models import utilFunctions as UF


class HarmonicTransformations_frame:

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
        self.filelocation.insert(0, os.path.join(self.sounds_dir, "vignesh.wav"))

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

        ## HARMONIC TRANSFORMATIONS ANALYSIS

        # ANALYSIS WINDOW TYPE
        Label(self.parent, text="window:").grid(
            row=1, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.w_type = StringVar()
        self.w_type.set("blackman")  # initial value
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
        self.M.insert(0, "1201")

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
        self.minSineDur.insert(0, "0.1")

        # MAX NUMBER OF HARMONICS
        Label(self.parent, text="nH:").grid(
            row=2, column=0, sticky=W, padx=(145, 5), pady=(10, 2)
        )
        self.nH = make_entry(self.parent)
        self.nH.grid(row=2, column=0, sticky=W, padx=(172, 5), pady=(10, 2))
        self.nH.delete(0, END)
        self.nH.insert(0, "100")

        # MIN FUNDAMENTAL FREQUENCY
        Label(self.parent, text="minf0:").grid(
            row=2, column=0, sticky=W, padx=(227, 5), pady=(10, 2)
        )
        self.minf0 = make_entry(self.parent)
        self.minf0.grid(row=2, column=0, sticky=W, padx=(275, 5), pady=(10, 2))
        self.minf0.delete(0, END)
        self.minf0.insert(0, "130")

        # MAX FUNDAMENTAL FREQUENCY
        Label(self.parent, text="maxf0:").grid(
            row=2, column=0, sticky=W, padx=(330, 5), pady=(10, 2)
        )
        self.maxf0 = make_entry(self.parent)
        self.maxf0.grid(row=2, column=0, sticky=W, padx=(380, 5), pady=(10, 2))
        self.maxf0.delete(0, END)
        self.maxf0.insert(0, "300")

        # MAX ERROR ACCEPTED
        Label(self.parent, text="f0et:").grid(
            row=3, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.f0et = make_entry(self.parent, 3)
        self.f0et.grid(row=3, column=0, sticky=W, padx=(42, 5), pady=(10, 2))
        self.f0et.delete(0, END)
        self.f0et.insert(0, "7")

        # ALLOWED DEVIATION OF HARMONIC TRACKS
        Label(self.parent, text="harmDevSlope:").grid(
            row=3, column=0, sticky=W, padx=(90, 5), pady=(10, 2)
        )
        self.harmDevSlope = make_entry(self.parent)
        self.harmDevSlope.grid(row=3, column=0, sticky=W, padx=(190, 5), pady=(10, 2))
        self.harmDevSlope.delete(0, END)
        self.harmDevSlope.insert(0, "0.01")

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
                + "_harmonicModel.wav"
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
        self.freqScaling = place_entry(self.parent, row=7, padx=5, default="[0, 2.0, 1, 0.3]", width=35, sticky="we", pady=(0, 2))

        # FREQUENCY STRETCHING FACTORSharmonicModelTransformation
        Label(self.parent, text="Frequency stretching factors (time, value pairs):").grid(
            row=8, column=0, sticky=W, padx=5, pady=(5, 2)
        )
        self.freqStretching = place_entry(self.parent, row=9, padx=5, default="[0, 1, 1, 1.5]", width=35, sticky="we", pady=(0, 2))

        # TIMBRE PRESERVATION
        Label(
            self.parent,
            text="Timbre preservation (1 preserves original timbre, 0 it does not):",
        ).grid(
            row=10, column=0, sticky=W, padx=5, pady=(5, 2)
        )
        self.timbrePreservation = make_entry(self.parent, 2)
        self.timbrePreservation.grid(
            row=10, column=0, sticky=W + E, padx=(395, 5), pady=(5, 2)
        )
        self.timbrePreservation.delete(0, END)
        self.timbrePreservation.insert(0, "1")

        # TIME SCALING FACTORS
        Label(self.parent, text="Time scaling factors (time, value pairs):").grid(
            row=11, column=0, sticky=W, padx=5, pady=(5, 2)
        )
        self.timeScaling = place_entry(self.parent, row=12, padx=5, default="[0, 0, 0.671, 0.671, 1.978, 1.978+1.0]", width=35, sticky="we", pady=(0, 2))

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
                + "_harmonicModelTransformation.wav"
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

    def browse_file(self, tkFileDialog=None):

        self.filename = tkFileDialog.askopenfilename(**self.file_opt)

        # set the text of the self.filelocation
        self.filelocation.delete(0, END)
        self.filelocation.insert(0, self.filename)

    def analysis(self, tkMessageBox=None):

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

            self.inputFile, self.fs, self.hfreq, self.hmag = hT.analysis(
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
            )

        except ValueError:
            tkMessageBox.showerror(
                "Input values error", "Some parameters are incorrect"
            )

    def transformation_synthesis(self):

        try:
            inputFile = self.inputFile
            fs = self.fs
            hfreq = self.hfreq
            hmag = self.hmag
            freqScaling = np.array(eval(self.freqScaling.get()))
            freqStretching = np.array(eval(self.freqStretching.get()))
            timbrePreservation = int(self.timbrePreservation.get())
            timeScaling = np.array(eval(self.timeScaling.get()))

            hT.transformation_synthesis(
                inputFile,
                fs,
                hfreq,
                hmag,
                freqScaling,
                freqStretching,
                timbrePreservation,
                timeScaling,
            )

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", errorMessage)

        except AttributeError:
            messagebox.showerror(
                "Analysis not computed", "First you must analyse the sound!"
            )
