# GUI frame for the sineModel_function.py

from tkinter import *
import sys, os
from tkinter import messagebox, filedialog

from gui_layout import apply_responsive_grid, make_entry
import sprModel_function
from smstools.models import utilFunctions as UF


class SprModel_frame:

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
        self.filelocation.insert(0, os.path.join(self.sounds_dir, "bendir.wav"))

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

        ## SPR MODEL

        # ANALYSIS WINDOW TYPE
        Label(self.parent, text="Window type:").grid(
            row=2, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.w_type = StringVar()
        self.w_type.set("hamming")  # initial value
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
        Label(self.parent, text="Window size (M):").grid(
            row=3, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.M = make_entry(self.parent)
        self.M.grid(row=3, column=0, sticky=W, padx=(115, 5), pady=(10, 2))
        self.M.delete(0, END)
        self.M.insert(0, "2001")

        # FFT SIZE
        Label(self.parent, text="FFT size (N) (power of two bigger than M):").grid(
            row=4, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.N = make_entry(self.parent)
        self.N.grid(row=4, column=0, sticky=W, padx=(270, 5), pady=(10, 2))
        self.N.delete(0, END)
        self.N.insert(0, "2048")

        # THRESHOLD MAGNITUDE
        Label(self.parent, text="Magnitude threshold (t) (in dB):").grid(
            row=5, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.t = make_entry(self.parent)
        self.t.grid(row=5, column=0, sticky=W, padx=(205, 5), pady=(10, 2))
        self.t.delete(0, END)
        self.t.insert(0, "-80")

        # MIN DURATION SINUSOIDAL TRACKS
        Label(self.parent, text="Minimum duration of sinusoidal tracks:").grid(
            row=6, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.minSineDur = make_entry(self.parent)
        self.minSineDur.grid(row=6, column=0, sticky=W, padx=(250, 5), pady=(10, 2))
        self.minSineDur.delete(0, END)
        self.minSineDur.insert(0, "0.02")

        # MAX NUMBER PARALLEL SINUSOIDS
        Label(self.parent, text="Maximum number of parallel sinusoids:").grid(
            row=7, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.maxnSines = make_entry(self.parent)
        self.maxnSines.grid(row=7, column=0, sticky=W, padx=(250, 5), pady=(10, 2))
        self.maxnSines.delete(0, END)
        self.maxnSines.insert(0, "150")

        # FREQUENCY DEVIATION ALLOWED
        Label(self.parent, text="Max frequency deviation in sinusoidal tracks (at freq 0):").grid(
            row=8, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.freqDevOffset = make_entry(self.parent)
        self.freqDevOffset.grid(row=8, column=0, sticky=W, padx=(350, 5), pady=(10, 2))
        self.freqDevOffset.delete(0, END)
        self.freqDevOffset.insert(0, "10")

        # SLOPE OF THE FREQ DEVIATION
        Label(self.parent, text="Slope of the frequency deviation (as function of freq):").grid(
            row=9, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.freqDevSlope = make_entry(self.parent)
        self.freqDevSlope.grid(row=9, column=0, sticky=W, padx=(340, 5), pady=(10, 2))
        self.freqDevSlope.delete(0, END)
        self.freqDevSlope.insert(0, "0.001")

        # BUTTON TO COMPUTE EVERYTHING
        self.compute = Button(self.parent, text="Compute", command=self.compute_model)
        self.compute.grid(row=10, column=0, padx=5, pady=(10, 2), sticky=W)

        # BUTTON TO PLAY SINE OUTPUT
        Label(self.parent, text="Sinusoidal:").grid(
            row=11, column=0, sticky=W, padx=5, pady=(10, 0)
        )
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_sprModel_sines.wav"
            ),
        )
        self.output.grid(row=11, column=0, padx=(80, 5), pady=(10, 0), sticky=W)

        # BUTTON TO PLAY RESIDUAL OUTPUT
        Label(self.parent, text="Residual:").grid(
            row=12, column=0, sticky=W, padx=5, pady=(5, 0)
        )
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_sprModel_residual.wav"
            ),
        )
        self.output.grid(row=12, column=0, padx=(80, 5), pady=(5, 0), sticky=W)

        # BUTTON TO PLAY OUTPUT
        Label(self.parent, text="Output:").grid(
            row=13, column=0, sticky=W, padx=5, pady=(5, 15)
        )
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_sprModel.wav"
            ),
        )
        self.output.grid(row=13, column=0, padx=(80, 5), pady=(5, 15), sticky=W)

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
            t = int(self.t.get())
            minSineDur = float(self.minSineDur.get())
            maxnSines = int(self.maxnSines.get())
            freqDevOffset = int(self.freqDevOffset.get())
            freqDevSlope = float(self.freqDevSlope.get())

            sprModel_function.main(
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

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", str(errorMessage))
