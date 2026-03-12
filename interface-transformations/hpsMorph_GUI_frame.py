# GUI frame for the hpsMorph_function.py

from tkinter import *
import sys, os
from tkinter import messagebox

import numpy as np
import hpsMorph_function as hM
from smstools.models import utilFunctions as UF


class HpsMorph_frame:

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

        row_num = 0

        # INPUT FILE 1
        Label(self.parent, text="Sound 1:").grid(
            row=row_num, column=0, sticky=W, padx=5, pady=(10, 2)
        )

        self.filelocation1 = Entry(self.parent)
        self.filelocation1.focus_set()
        self.filelocation1.grid(row=row_num, column=1, columnspan=2, sticky=EW, padx=5, pady=(10, 2))
        self.filelocation1.delete(0, END)
        self.filelocation1.insert(0, os.path.join(self.sounds_dir, "violin-B3.wav"))

        open_file1 = Button(self.parent, text="...", command=self.browse_file1)
        open_file1.grid(row=row_num, column=3, sticky=W, padx=5, pady=(10, 2))

        preview1 = Button(self.parent, text=">", command=lambda: UF.wavplay(self.filelocation1.get()))
        preview1.grid(row=row_num, column=3, sticky=E, padx=(0, 5), pady=(10, 2))

        row_num += 1

        # Sound 1 analysis parameters
        Label(self.parent, text="Window:").grid(row=row_num, column=0, sticky=W, padx=5, pady=(5, 2))
        self.w1_type = StringVar()
        self.w1_type.set("blackman")
        window1_option = OptionMenu(self.parent, self.w1_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris")
        window1_option.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(5, 2))

        Label(self.parent, text="M:").grid(row=row_num, column=2, sticky=W, padx=5, pady=(5, 2))
        self.M1 = Entry(self.parent, justify=CENTER)
        self.M1.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(5, 2))
        self.M1.delete(0, END)
        self.M1.insert(0, "1001")

        row_num += 1

        Label(self.parent, text="N:").grid(row=row_num, column=0, sticky=W, padx=5, pady=(2, 2))
        self.N1 = Entry(self.parent, justify=CENTER)
        self.N1.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(2, 2))
        self.N1.delete(0, END)
        self.N1.insert(0, "1024")

        Label(self.parent, text="Threshold (dB):").grid(row=row_num, column=2, sticky=W, padx=5, pady=(2, 2))
        self.t1 = Entry(self.parent, justify=CENTER)
        self.t1.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(2, 2))
        self.t1.delete(0, END)
        self.t1.insert(0, "-100")

        row_num += 1

        Label(self.parent, text="Min dur (s):").grid(row=row_num, column=0, sticky=W, padx=5, pady=(2, 2))
        self.minSineDur1 = Entry(self.parent, justify=CENTER)
        self.minSineDur1.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(2, 2))
        self.minSineDur1.delete(0, END)
        self.minSineDur1.insert(0, "0.05")

        Label(self.parent, text="Min f0 (Hz):").grid(row=row_num, column=2, sticky=W, padx=5, pady=(2, 2))
        self.minf01 = Entry(self.parent, justify=CENTER)
        self.minf01.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(2, 2))
        self.minf01.delete(0, END)
        self.minf01.insert(0, "200")

        row_num += 1

        Label(self.parent, text="Max f0 (Hz):").grid(row=row_num, column=0, sticky=W, padx=5, pady=(2, 2))
        self.maxf01 = Entry(self.parent, justify=CENTER)
        self.maxf01.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(2, 2))
        self.maxf01.delete(0, END)
        self.maxf01.insert(0, "300")

        Label(self.parent, text="f0 error:").grid(row=row_num, column=2, sticky=W, padx=5, pady=(2, 2))
        self.f0et1 = Entry(self.parent, justify=CENTER)
        self.f0et1.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(2, 2))
        self.f0et1.delete(0, END)
        self.f0et1.insert(0, "10")

        row_num += 1

        Label(self.parent, text="Harmonic dev:").grid(row=row_num, column=0, sticky=W, padx=5, pady=(2, 5))
        self.harmDevSlope1 = Entry(self.parent, justify=CENTER)
        self.harmDevSlope1.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(2, 5))
        self.harmDevSlope1.delete(0, END)
        self.harmDevSlope1.insert(0, "0.01")

        Frame(self.parent, height=1, bg="black").grid(
            row=row_num, column=2, columnspan=2, sticky=EW, padx=5, pady=(2, 5)
        )

        row_num += 1

        # INPUT FILE 2
        Label(self.parent, text="Sound 2:").grid(
            row=row_num, column=0, sticky=W, padx=5, pady=(10, 2)
        )

        self.filelocation2 = Entry(self.parent)
        self.filelocation2.focus_set()
        self.filelocation2.grid(row=row_num, column=1, columnspan=2, sticky=EW, padx=5, pady=(10, 2))
        self.filelocation2.delete(0, END)
        self.filelocation2.insert(0, os.path.join(self.sounds_dir, "soprano-E4.wav"))

        open_file2 = Button(self.parent, text="...", command=self.browse_file2)
        open_file2.grid(row=row_num, column=3, sticky=W, padx=5, pady=(10, 2))

        preview2 = Button(self.parent, text=">", command=lambda: UF.wavplay(self.filelocation2.get()))
        preview2.grid(row=row_num, column=3, sticky=E, padx=(0, 5), pady=(10, 2))

        row_num += 1

        # Sound 2 analysis parameters
        Label(self.parent, text="Window:").grid(row=row_num, column=0, sticky=W, padx=5, pady=(5, 2))
        self.w2_type = StringVar()
        self.w2_type.set("hamming")
        window2_option = OptionMenu(self.parent, self.w2_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris")
        window2_option.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(5, 2))

        Label(self.parent, text="M:").grid(row=row_num, column=2, sticky=W, padx=5, pady=(5, 2))
        self.M2 = Entry(self.parent, justify=CENTER)
        self.M2.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(5, 2))
        self.M2.delete(0, END)
        self.M2.insert(0, "901")

        row_num += 1

        Label(self.parent, text="N:").grid(row=row_num, column=0, sticky=W, padx=5, pady=(2, 2))
        self.N2 = Entry(self.parent, justify=CENTER)
        self.N2.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(2, 2))
        self.N2.delete(0, END)
        self.N2.insert(0, "1024")

        Label(self.parent, text="Threshold (dB):").grid(row=row_num, column=2, sticky=W, padx=5, pady=(2, 2))
        self.t2 = Entry(self.parent, justify=CENTER)
        self.t2.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(2, 2))
        self.t2.delete(0, END)
        self.t2.insert(0, "-100")

        row_num += 1

        Label(self.parent, text="Min dur (s):").grid(row=row_num, column=0, sticky=W, padx=5, pady=(2, 2))
        self.minSineDur2 = Entry(self.parent, justify=CENTER)
        self.minSineDur2.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(2, 2))
        self.minSineDur2.delete(0, END)
        self.minSineDur2.insert(0, "0.05")

        Label(self.parent, text="Min f0 (Hz):").grid(row=row_num, column=2, sticky=W, padx=5, pady=(2, 2))
        self.minf02 = Entry(self.parent, justify=CENTER)
        self.minf02.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(2, 2))
        self.minf02.delete(0, END)
        self.minf02.insert(0, "250")

        row_num += 1

        Label(self.parent, text="Max f0 (Hz):").grid(row=row_num, column=0, sticky=W, padx=5, pady=(2, 2))
        self.maxf02 = Entry(self.parent, justify=CENTER)
        self.maxf02.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(2, 2))
        self.maxf02.delete(0, END)
        self.maxf02.insert(0, "500")

        Label(self.parent, text="f0 error:").grid(row=row_num, column=2, sticky=W, padx=5, pady=(2, 2))
        self.f0et2 = Entry(self.parent, justify=CENTER)
        self.f0et2.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(2, 2))
        self.f0et2.delete(0, END)
        self.f0et2.insert(0, "10")

        row_num += 1

        Label(self.parent, text="Harmonic dev:").grid(row=row_num, column=0, sticky=W, padx=5, pady=(2, 5))
        self.harmDevSlope2 = Entry(self.parent, justify=CENTER)
        self.harmDevSlope2.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(2, 5))
        self.harmDevSlope2.delete(0, END)
        self.harmDevSlope2.insert(0, "0.01")

        Frame(self.parent, height=1, bg="black").grid(
            row=row_num, column=2, columnspan=2, sticky=EW, padx=5, pady=(2, 5)
        )

        row_num += 1

        # Common parameters
        Label(self.parent, text="Max harmonics:").grid(row=row_num, column=0, sticky=W, padx=5, pady=(5, 2))
        self.nH = Entry(self.parent, justify=CENTER)
        self.nH.grid(row=row_num, column=1, sticky=EW, padx=5, pady=(5, 2))
        self.nH.delete(0, END)
        self.nH.insert(0, "60")

        Label(self.parent, text="Stochastic factor:").grid(row=row_num, column=2, sticky=W, padx=5, pady=(5, 2))
        self.stocf = Entry(self.parent, justify=CENTER)
        self.stocf.grid(row=row_num, column=3, sticky=EW, padx=5, pady=(5, 2))
        self.stocf.delete(0, END)
        self.stocf.insert(0, "0.1")

        row_num += 1

        # Interpolation factors
        Label(self.parent, text="Harmonic freq interp:").grid(row=row_num, column=0, columnspan=4, sticky=W, padx=5, pady=(5, 2))
        row_num += 1

        self.hfreqIntp = Entry(self.parent, justify=CENTER)
        self.hfreqIntp.grid(row=row_num, column=0, columnspan=4, sticky=EW, padx=5, pady=(0, 5))
        self.hfreqIntp.delete(0, END)
        self.hfreqIntp.insert(0, "[0, 0, .1, 0, .9, 1, 1, 1]")

        row_num += 1

        Label(self.parent, text="Harmonic mag interp:").grid(row=row_num, column=0, columnspan=4, sticky=W, padx=5, pady=(5, 2))
        row_num += 1

        self.hmagIntp = Entry(self.parent, justify=CENTER)
        self.hmagIntp.grid(row=row_num, column=0, columnspan=4, sticky=EW, padx=5, pady=(0, 5))
        self.hmagIntp.delete(0, END)
        self.hmagIntp.insert(0, "[0, 0, .1, 0, .9, 1, 1, 1]")

        row_num += 1

        Label(self.parent, text="Stochastic interp:").grid(row=row_num, column=0, columnspan=4, sticky=W, padx=5, pady=(5, 2))
        row_num += 1

        self.stocIntp = Entry(self.parent, justify=CENTER)
        self.stocIntp.grid(row=row_num, column=0, columnspan=4, sticky=EW, padx=5, pady=(0, 5))
        self.stocIntp.delete(0, END)
        self.stocIntp.insert(0, "[0, 0, .1, 0, .9, 1, 1, 1]")

        row_num += 1

        # Buttons
        self.compute = Button(self.parent, text="Analysis", command=self.analysis)
        self.compute.grid(row=row_num, column=0, columnspan=2, sticky=W, padx=5, pady=(10, 5))

        self.compute_synth = Button(self.parent, text="Apply Transformation", command=self.transformation_synthesis)
        self.compute_synth.grid(row=row_num, column=2, columnspan=2, sticky=W, padx=5, pady=(10, 5))

        row_num += 1

        self.transf_output = Button(
            self.parent,
            text="> Play Output",
            command=lambda: UF.wavplay("output_sounds/" + os.path.basename(self.filelocation1.get())[:-4] + "_hpsMorph.wav"),
        )
        self.transf_output.grid(row=row_num, column=0, columnspan=4, sticky=W, padx=5, pady=(0, 10))

        # define options for opening file
        self.file_opt = options = {}
        options["defaultextension"] = ".wav"
        options["filetypes"] = [("All files", ".*"), ("Wav files", ".wav")]
        options["initialdir"] = self.sounds_dir
        options["title"] = "Open a mono audio file .wav with sample frequency 44100 Hz"

    def browse_file1(self, tkFileDialog=None):

        self.filename1 = tkFileDialog.askopenfilename(**self.file_opt)

        # set the text of the self.filelocation
        self.filelocation1.delete(0, END)
        self.filelocation1.insert(0, self.filename1)

    def browse_file2(self, tkFileDialog=None):

        self.filename2 = tkFileDialog.askopenfilename(**self.file_opt)

        # set the text of the self.filelocation
        self.filelocation2.delete(0, END)
        self.filelocation2.insert(0, self.filename2)

    def analysis(self, tkMessageBox=None):

        try:
            inputFile1 = self.filelocation1.get()
            window1 = self.w1_type.get()
            M1 = int(self.M1.get())
            N1 = int(self.N1.get())
            t1 = int(self.t1.get())
            minSineDur1 = float(self.minSineDur1.get())
            minf01 = int(self.minf01.get())
            maxf01 = int(self.maxf01.get())
            f0et1 = int(self.f0et1.get())
            harmDevSlope1 = float(self.harmDevSlope1.get())

            nH = int(self.nH.get())
            stocf = float(self.stocf.get())

            inputFile2 = self.filelocation2.get()
            window2 = self.w2_type.get()
            M2 = int(self.M2.get())
            N2 = int(self.N2.get())
            t2 = int(self.t2.get())
            minSineDur2 = float(self.minSineDur2.get())
            minf02 = int(self.minf02.get())
            maxf02 = int(self.maxf02.get())
            f0et2 = int(self.f0et2.get())
            harmDevSlope2 = float(self.harmDevSlope2.get())

            (
                self.inputFile1,
                self.fs1,
                self.hfreq1,
                self.hmag1,
                self.stocEnv1,
                self.inputFile2,
                self.hfreq2,
                self.hmag2,
                self.stocEnv2,
            ) = hM.analysis(
                inputFile1,
                window1,
                M1,
                N1,
                t1,
                minSineDur1,
                nH,
                minf01,
                maxf01,
                f0et1,
                harmDevSlope1,
                stocf,
                inputFile2,
                window2,
                M2,
                N2,
                t2,
                minSineDur2,
                minf02,
                maxf02,
                f0et2,
                harmDevSlope2,
            )

        except ValueError as errorMessage:
            tkMessageBox.showerror("Input values error", errorMessage)

    def transformation_synthesis(self):

        try:
            inputFile1 = self.inputFile1
            fs = self.fs1
            hfreq1 = self.hfreq1
            hmag1 = self.hmag1
            stocEnv1 = self.stocEnv1
            inputFile2 = self.inputFile2
            hfreq2 = self.hfreq2
            hmag2 = self.hmag2
            stocEnv2 = self.stocEnv2
            hfreqIntp = np.array(eval(self.hfreqIntp.get()))
            hmagIntp = np.array(eval(self.hmagIntp.get()))
            stocIntp = np.array(eval(self.stocIntp.get()))

            hM.transformation_synthesis(
                inputFile1,
                fs,
                hfreq1,
                hmag1,
                stocEnv1,
                inputFile2,
                hfreq2,
                hmag2,
                stocEnv2,
                hfreqIntp,
                hmagIntp,
                stocIntp,
            )

        except ValueError as errorMessage:
            messagebox.showerror("Input values error", errorMessage)

        except AttributeError:
            messagebox.showerror(
                "Analysis not computed", "First you must analyse the sound!"
            )
