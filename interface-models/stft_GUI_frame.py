# GUI frame for the stft_function.py

from tkinter import *
import sys, os
from tkinter import messagebox, filedialog

from gui_layout import apply_responsive_grid, add_window_size_label, place_entry
import stft_function
from smstools.models import utilFunctions as UF


class Stft_frame:
    def __init__(self, parent):
        self.compute = None
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
        self.preview = Button(
            self.parent, text=">", command=lambda: UF.wavplay(self.filelocation.get())
        )
        self.preview.grid(row=1, column=0, sticky=W, padx=(306, 6))

        ## STFT

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
        add_window_size_label(self.parent)
        self.M = place_entry(self.parent, row=3, padx=(115, 5), default="1024")

        # FFT SIZE
        Label(self.parent, text="FFT size (N) (power of two bigger than M):").grid(
            row=4, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.N = place_entry(self.parent, row=4, padx=(270, 5), default="1024")

        # HOP SIZE
        Label(self.parent, text="Hop size (H):").grid(
            row=5, column=0, sticky=W, padx=5, pady=(10, 2)
        )
        self.H = place_entry(self.parent, row=5, padx=(95, 5), default="512")

        # BUTTON TO COMPUTE EVERYTHING
        self.compute = Button(self.parent, text="Compute", command=self.compute_model)
        self.compute.grid(row=6, column=0, padx=5, pady=(10, 2), sticky=W)

        # BUTTON TO PLAY OUTPUT
        Label(self.parent, text="Output:").grid(
            row=7, column=0, sticky=W, padx=5, pady=(10, 15)
        )
        self.output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(
                "output_sounds/"
                + os.path.basename(self.filelocation.get())[:-4]
                + "_stft.wav"
            ),
        )
        self.output.grid(row=7, column=0, padx=(60, 5), pady=(10, 15), sticky=W)

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
            H = int(self.H.get())

            stft_function.main(inputFile, window, M, N, H)

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", str(errorMessage))
