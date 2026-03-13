# GUI frame for the stftMorph_function.py

import os
import sys
from tkinter import *
from tkinter import filedialog, messagebox

from gui_layout import apply_responsive_grid, make_entry
import stftMorph_function as sT
from smstools.models import utilFunctions as UF


class StftMorph_frame:

    def __init__(self, parent):

        self.parent = parent
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sounds_dir = os.path.normpath(os.path.join(self.base_dir, "..", "sounds"))
        self.initUI()

    def initUI(self):

        ## INPUT FILE 1
        Label(self.parent, text="inputFile1:").grid(
            row=0, column=0, sticky=W, padx=5, pady=(10, 2)
        )

        # TEXTBOX TO PRINT PATH OF THE SOUND FILE
        self.filelocation1 = Entry(self.parent)
        self.filelocation1.focus_set()
        self.filelocation1["width"] = 30
        self.filelocation1.grid(row=0, column=0, sticky=W, padx=(75, 5), pady=(10, 2))
        self.filelocation1.delete(0, END)
        self.filelocation1.insert(0, os.path.join(self.sounds_dir, "ocean.wav"))

        # BUTTON TO BROWSE SOUND FILE 1
        open_file1 = Button(
            self.parent, text="...", command=self.browse_file1
        )  # see: def browse_file(self)
        open_file1.grid(
            row=0, column=0, sticky=W, padx=(330, 6), pady=(10, 2)
        )  # put it beside the filelocation textbox

        # BUTTON TO PREVIEW SOUND FILE 1
        preview1 = Button(
            self.parent, text=">", command=lambda: UF.wavplay(self.filelocation1.get())
        )
        preview1.grid(row=0, column=0, sticky=W, padx=(375, 6), pady=(10, 2))

        # ANALYSIS WINDOW TYPE SOUND 1
        Label(self.parent, text="window1:").grid(
            row=1, column=0, sticky=W, padx=5, pady=(4, 2)
        )
        self.w1_type = StringVar()
        self.w1_type.set("hamming")  # initial value
        window1_option = OptionMenu(
            self.parent,
            self.w1_type,
            "rectangular",
            "hanning",
            "hamming",
            "blackman",
            "blackmanharris",
        )
        window1_option.grid(row=1, column=0, sticky=W, padx=(68, 5), pady=(4, 2))

        # WINDOW SIZE SOUND 1
        Label(self.parent, text="M1:").grid(
            row=1, column=0, sticky=W, padx=(180, 5), pady=(4, 2)
        )
        self.M1 = make_entry(self.parent)
        self.M1.grid(row=1, column=0, sticky=W, padx=(208, 5), pady=(4, 2))
        self.M1.delete(0, END)
        self.M1.insert(0, "1024")

        # FFT SIZE SOUND 1
        Label(self.parent, text="N1:").grid(
            row=1, column=0, sticky=W, padx=(265, 5), pady=(4, 2)
        )
        self.N1 = make_entry(self.parent)
        self.N1.grid(row=1, column=0, sticky=W, padx=(290, 5), pady=(4, 2))
        self.N1.delete(0, END)
        self.N1.insert(0, "1024")

        # HOP SIZE SOUND 1
        Label(self.parent, text="H1:").grid(
            row=1, column=0, sticky=W, padx=(343, 5), pady=(4, 2)
        )
        self.H1 = make_entry(self.parent)
        self.H1.grid(row=1, column=0, sticky=W, padx=(370, 5), pady=(4, 2))
        self.H1.delete(0, END)
        self.H1.insert(0, "256")

        ###
        # SEPARATION LINE
        Frame(self.parent, height=1, width=50, bg="black").grid(
            row=2, pady=15, sticky=W + E
        )
        ###

        ## INPUT FILE 2
        Label(self.parent, text="inputFile2:").grid(
            row=3, column=0, sticky=W, padx=5, pady=(2, 2)
        )

        # TEXTBOX TO PRINT PATH OF THE SOUND FILE
        self.filelocation2 = Entry(self.parent)
        self.filelocation2.focus_set()
        self.filelocation2["width"] = 30
        self.filelocation2.grid(row=3, column=0, sticky=W, padx=(75, 5), pady=(2, 2))
        self.filelocation2.delete(0, END)
        self.filelocation2.insert(0, os.path.join(self.sounds_dir, "speech-male.wav"))

        # BUTTON TO BROWSE SOUND FILE 2
        open_file2 = Button(
            self.parent, text="...", command=self.browse_file2
        )  # see: def browse_file(self)
        open_file2.grid(
            row=3, column=0, sticky=W, padx=(330, 6), pady=(2, 2)
        )  # put it beside the filelocation textbox

        # BUTTON TO PREVIEW SOUND FILE 2
        preview2 = Button(
            self.parent, text=">", command=lambda: UF.wavplay(self.filelocation2.get())
        )
        preview2.grid(row=3, column=0, sticky=W, padx=(375, 6), pady=(2, 2))

        # ANALYSIS WINDOW TYPE SOUND 2
        Label(self.parent, text="window2:").grid(
            row=4, column=0, sticky=W, padx=5, pady=(4, 2)
        )
        self.w2_type = StringVar()
        self.w2_type.set("hamming")  # initial value
        window2_option = OptionMenu(
            self.parent,
            self.w2_type,
            "rectangular",
            "hanning",
            "hamming",
            "blackman",
            "blackmanharris",
        )
        window2_option.grid(row=4, column=0, sticky=W, padx=(68, 5), pady=(4, 2))

        # WINDOW SIZE SOUND 2
        Label(self.parent, text="M2:").grid(
            row=4, column=0, sticky=W, padx=(180, 5), pady=(4, 2)
        )
        self.M2 = make_entry(self.parent)
        self.M2.grid(row=4, column=0, sticky=W, padx=(208, 5), pady=(4, 2))
        self.M2.delete(0, END)
        self.M2.insert(0, "1024")

        # FFT SIZE SOUND 2
        Label(self.parent, text="N2:").grid(
            row=4, column=0, sticky=W, padx=(265, 5), pady=(4, 2)
        )
        self.N2 = make_entry(self.parent)
        self.N2.grid(row=4, column=0, sticky=W, padx=(290, 5), pady=(4, 2))
        self.N2.delete(0, END)
        self.N2.insert(0, "1024")

        ###
        # SEPARATION LINE
        Frame(self.parent, height=1, width=50, bg="black").grid(
            row=5, pady=15, sticky=W + E
        )
        ###

        # SMOOTHING FACTOR
        Label(
            self.parent,
            text="Smooth factor of sound 2 (bigger than 0 to max of 1, where 1 is no",
        ).grid(
            row=6, column=0, sticky=W, padx=(5, 5), pady=(2, 2)
        )
        Label(self.parent, text="smothing):").grid(
            row=7, column=0, sticky=W, padx=(5, 5), pady=(0, 2)
        )
        self.smoothf = make_entry(self.parent)
        self.smoothf.grid(row=8, column=0, sticky=W, padx=(5, 5), pady=(2, 2))
        self.smoothf.delete(0, END)
        self.smoothf.insert(0, "0.5")

        # BALANCE FACTOR
        Label(
            self.parent,
            text="Balance factor (from 0 to 1, where 0 is sound 1 and 1 is sound 2):",
        ).grid(
            row=9, column=0, sticky=W, padx=(5, 5), pady=(10, 2)
        )
        self.balancef = make_entry(self.parent)
        self.balancef.grid(row=10, column=0, sticky=W, padx=(5, 5), pady=(2, 2))
        self.balancef.delete(0, END)
        self.balancef.insert(0, "0.2")

        # BUTTON TO DO THE SYNTHESIS
        self.compute = Button(
            self.parent,
            text="Apply Transformation",
            command=self.transformation_synthesis,
            font=("TkDefaultFont", 11, "bold"),
            padx=10,
            pady=4,
        )
        self.compute.grid(row=11, column=0, padx=5, pady=(10, 15), sticky=W)

        # BUTTON TO PLAY TRANSFORMATION SYNTHESIS OUTPUT
        self.transf_output = Button(
            self.parent,
            text=">",
            command=lambda: UF.wavplay(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds", os.path.basename(self.filelocation1.get())[:-4] + "_stftMorph.wav")),
        )
        self.transf_output.grid(
            row=11, column=0, padx=(165, 5), pady=(10, 15), sticky=W
        )

        # define options for opening file
        self.file_opt = options = {}
        options["defaultextension"] = ".wav"
        options["filetypes"] = [("All files", ".*"), ("Wav files", ".wav")]
        options["initialdir"] = self.sounds_dir
        options["title"] = "Open a mono audio file .wav with sample frequency 44100 Hz"

        apply_responsive_grid(self.parent)

    def browse_file1(self):

        self.filename1 = filedialog.askopenfilename(**self.file_opt)

        # set the text of the self.filelocation
        self.filelocation1.delete(0, END)
        self.filelocation1.insert(0, self.filename1)

    def browse_file2(self):

        self.filename2 = filedialog.askopenfilename(**self.file_opt)

        # set the text of the self.filelocation
        self.filelocation2.delete(0, END)
        self.filelocation2.insert(0, self.filename2)

    def transformation_synthesis(self):

        try:
            inputFile1 = self.filelocation1.get()
            inputFile2 = self.filelocation2.get()
            window1 = self.w1_type.get()
            window2 = self.w2_type.get()
            M1 = int(self.M1.get())
            M2 = int(self.M2.get())
            N1 = int(self.N1.get())
            N2 = int(self.N2.get())
            H1 = int(self.H1.get())
            smoothf = float(self.smoothf.get())
            balancef = float(self.balancef.get())

            sT.main(
                inputFile1,
                inputFile2,
                window1,
                window2,
                M1,
                M2,
                N1,
                N2,
                H1,
                smoothf,
                balancef,
            )

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", errorMessage)
