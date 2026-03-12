# GUI frame for the hprModel_function.py

from tkinter import *
import sys, os
from tkinter import filedialog, messagebox

from gui_layout import apply_responsive_grid, add_window_size_label, make_entry
import hprModel_function
from smstools.models import utilFunctions as UF


class HprModel_frame:

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
        self.filelocation.insert(0, os.path.join(self.sounds_dir, "sax-phrase-short.wav"))

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

        ## HARMONIC MODEL

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
        self.M.insert(0, "601")

        # FFT SIZE
        Label(self.parent, text="FFT size (N) (power of two bigger than M):").grid(
            row=4, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.N = make_entry(self.parent)
        self.N.grid(row=4, column=0, sticky=W, padx=(270, 5), pady=(10, 2))
        self.N.delete(0, END)
        self.N.insert(0, "1024")

        # THRESHOLD MAGNITUDE
        Label(self.parent, text="Magnitude threshold (t) (in dB):").grid(
            row=5, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.t = make_entry(self.parent)
        self.t.grid(row=5, column=0, sticky=W, padx=(205, 5), pady=(10, 2))
        self.t.delete(0, END)
        self.t.insert(0, "-100")

        # MIN DURATION SINUSOIDAL TRACKS
        Label(self.parent, text="Minimum duration of harmonic tracks:").grid(
            row=6, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.minSineDur = make_entry(self.parent)
        self.minSineDur.grid(row=6, column=0, sticky=W, padx=(250, 5), pady=(10, 2))
        self.minSineDur.delete(0, END)
        self.minSineDur.insert(0, "0.1")

        # MAX NUMBER OF HARMONICS
        Label(self.parent, text="Maximum number of harmonics:").grid(
            row=7, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.nH = make_entry(self.parent)
        self.nH.grid(row=7, column=0, sticky=W, padx=(215, 5), pady=(10, 2))
        self.nH.delete(0, END)
        self.nH.insert(0, "100")

        # MIN FUNDAMENTAL FREQUENCY
        Label(self.parent, text="Minimum fundamental frequency:").grid(
            row=8, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.minf0 = make_entry(self.parent)
        self.minf0.grid(row=8, column=0, sticky=W, padx=(220, 5), pady=(10, 2))
        self.minf0.delete(0, END)
        self.minf0.insert(0, "350")

        # MAX FUNDAMENTAL FREQUENCY
        Label(self.parent, text="Maximum fundamental frequency:").grid(
            row=9, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.maxf0 = make_entry(self.parent)
        self.maxf0.grid(row=9, column=0, sticky=W, padx=(220, 5), pady=(10, 2))
        self.maxf0.delete(0, END)
        self.maxf0.insert(0, "700")

        # MAX ERROR ACCEPTED
        Label(self.parent, text="Maximum error in f0 detection algorithm:").grid(
            row=10, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.f0et = make_entry(self.parent)
        self.f0et.grid(row=10, column=0, sticky=W, padx=(265, 5), pady=(10, 2))
        self.f0et.delete(0, END)
        self.f0et.insert(0, "5")

        # ALLOWED DEVIATION OF HARMONIC TRACKS
        Label(self.parent, text="Max frequency deviation in harmonic tracks:").grid(
            row=11, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.harmDevSlope = make_entry(self.parent)
        self.harmDevSlope.grid(row=11, column=0, sticky=W, padx=(285, 5), pady=(10, 2))
        self.harmDevSlope.delete(0, END)
        self.harmDevSlope.insert(0, "0.01")

        # BUTTON TO COMPUTE EVERYTHING
        self.compute = Button(self.parent, text="Compute", command=self.compute_model)
        self.compute.grid(row=12, column=0, padx=5, pady=(10, 2), sticky=W)

        # BUTTON TO PLAY SINE OUTPUT
        Label(self.parent, text="Sinusoidal:").grid(
            row=13, column=0, sticky=W, padx=5, pady=(10, 0)
        )
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_hprModel_sines.wav"
            ),
        )
        self.output.grid(row=13, column=0, padx=(80, 5), pady=(10, 0), sticky=W)

        # BUTTON TO PLAY RESIDUAL OUTPUT
        Label(self.parent, text="Residual:").grid(
            row=14, column=0, sticky=W, padx=5, pady=(5, 0)
        )
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_hprModel_residual.wav"
            ),
        )
        self.output.grid(row=14, column=0, padx=(80, 5), pady=(5, 0), sticky=W)

        # BUTTON TO PLAY OUTPUT
        Label(self.parent, text="Output:").grid(
            row=15, column=0, sticky=W, padx=5, pady=(5, 15)
        )
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_hprModel.wav"
            ),
        )
        self.output.grid(row=15, column=0, padx=(80, 5), pady=(5, 15), sticky=W)

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
            nH = int(self.nH.get())
            minf0 = int(self.minf0.get())
            maxf0 = int(self.maxf0.get())
            f0et = int(self.f0et.get())
            harmDevSlope = float(self.harmDevSlope.get())

            hprModel_function.main(
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

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", str(errorMessage))
