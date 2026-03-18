import os
from tkinter import *
from tkinter import filedialog, messagebox
from smstools.models import utilFunctions as UF
import stftMorph_function as sT

class StftMorph_frame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.sounds_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sounds"))
        self.initUI()

    def initUI(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Input file 1
        Label(self, text="Input file 1 (.wav, mono, 44100 Hz):").grid(row=0, column=0, sticky=W, padx=5, pady=(10, 2))
        self.filelocation1 = Entry(self, width=25)
        self.filelocation1.grid(row=0, column=1, sticky=W, padx=10, pady=(10, 2))
        self.filelocation1.insert(0, os.path.join(self.sounds_dir, "ocean.wav"))
        Button(self, text="Browse...", command=self.browse_file1).grid(row=0, column=2, sticky=W, padx=(10, 6))
        Button(self, text=">", command=lambda: UF.wavplay(self.filelocation1.get())).grid(row=0, column=3, sticky=W, padx=(6, 6))

        # Window type and size for file 1
        Label(self, text="Window type 1:").grid(row=1, column=0, sticky=W, padx=5, pady=(10, 2))
        self.w1_type = StringVar(value="hamming")
        OptionMenu(self, self.w1_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris").grid(row=1, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        Label(self, text="Window size 1 (M1):").grid(row=2, column=0, sticky=W, padx=5, pady=(10, 2))
        self.M1 = Entry(self, width=8)
        self.M1.grid(row=2, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.M1.insert(0, "1024")
        Label(self, text="FFT size 1 (N1):").grid(row=3, column=0, sticky=W, padx=5, pady=(10, 2))
        self.N1 = Entry(self, width=8)
        self.N1.grid(row=3, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.N1.insert(0, "1024")
        Label(self, text="Hop size 1 (H1):").grid(row=4, column=0, sticky=W, padx=5, pady=(10, 2))
        self.H1 = Entry(self, width=8)
        self.H1.grid(row=4, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.H1.insert(0, "256")

        # Input file 2
        Label(self, text="Input file 2 (.wav, mono, 44100 Hz):").grid(row=5, column=0, sticky=W, padx=5, pady=(10, 2))
        self.filelocation2 = Entry(self, width=25)
        self.filelocation2.grid(row=5, column=1, sticky=W, padx=10, pady=(10, 2))
        self.filelocation2.insert(0, os.path.join(self.sounds_dir, "speech-male.wav"))
        Button(self, text="Browse...", command=self.browse_file2).grid(row=5, column=2, sticky=W, padx=(10, 6))
        Button(self, text=">", command=lambda: UF.wavplay(self.filelocation2.get())).grid(row=5, column=3, sticky=W, padx=(6, 6))

        # Window type and size for file 2
        Label(self, text="Window type 2:").grid(row=6, column=0, sticky=W, padx=5, pady=(10, 2))
        self.w2_type = StringVar(value="hamming")
        OptionMenu(self, self.w2_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris").grid(row=6, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        Label(self, text="Window size 2 (M2):").grid(row=7, column=0, sticky=W, padx=5, pady=(10, 2))
        self.M2 = Entry(self, width=8)
        self.M2.grid(row=7, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.M2.insert(0, "1024")
        Label(self, text="FFT size 2 (N2):").grid(row=8, column=0, sticky=W, padx=5, pady=(10, 2))
        self.N2 = Entry(self, width=8)
        self.N2.grid(row=8, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.N2.insert(0, "1024")

        # Smoothing factor
        Label(self, text="Smooth factor (0-1):").grid(row=9, column=0, sticky=W, padx=5, pady=(10, 2))
        self.smoothf = Entry(self, width=8)
        self.smoothf.grid(row=9, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.smoothf.insert(0, "0.5")

        # Balance factor
        Label(self, text="Balance factor (0-1):").grid(row=10, column=0, sticky=W, padx=5, pady=(10, 2))
        self.balancef = Entry(self, width=8)
        self.balancef.grid(row=10, column=1, sticky=W, padx=(10, 5), pady=(10, 2))
        self.balancef.insert(0, "0.2")

        # Apply transformation button
        Button(self, text="Apply Transformation", command=self.apply_transformation, font=("TkDefaultFont", 11, "bold"), padx=10, pady=4).grid(row=11, column=1, padx=5, pady=(10, 15), sticky=W)

        # Output play button
        Label(self, text="Output:").grid(row=12, column=0, sticky=W, padx=5, pady=(10, 15))
        self.transf_output = Button(self, text="▶", font=("TkDefaultFont", 18, "bold"), width=2, height=1, command=self.play_output)
        self.transf_output.grid(row=12, column=1, sticky=W, padx=(60, 5), pady=(10, 15))

    def browse_file1(self):
        filename = filedialog.askopenfilename(defaultextension=".wav", filetypes=[("Wav files", ".wav"), ("All files", ".*")], initialdir=self.sounds_dir, title="Open a mono audio file .wav with sample frequency 44100 Hz")
        if filename:
            self.filelocation1.delete(0, END)
            self.filelocation1.insert(0, filename)

    def browse_file2(self):
        filename = filedialog.askopenfilename(defaultextension=".wav", filetypes=[("Wav files", ".wav"), ("All files", ".*")], initialdir=self.sounds_dir, title="Open a mono audio file .wav with sample frequency 44100 Hz")
        if filename:
            self.filelocation2.delete(0, END)
            self.filelocation2.insert(0, filename)

    def apply_transformation(self):
        try:
            sT.main(
                inputFile1=self.filelocation1.get(),
                window1=self.w1_type.get(),
                M1=int(self.M1.get()),
                N1=int(self.N1.get()),
                H1=int(self.H1.get()),
                inputFile2=self.filelocation2.get(),
                window2=self.w2_type.get(),
                M2=int(self.M2.get()),
                N2=int(self.N2.get()),
                smoothf=float(self.smoothf.get()),
                balancef=float(self.balancef.get()),
            )
            messagebox.showinfo("Success", "Transformation applied. Output file generated.")
        except Exception as e:
            messagebox.showerror("Error", f"Transformation failed: {e}")

    def play_output(self):
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sounds", os.path.basename(self.filelocation1.get())[:-4] + "_stftMorph.wav")
        UF.wavplay(output_file)

if __name__ == "__main__":
    root = Tk()
    root.title("STFT Morph Transformation")
    # Debug: Add a label to root to check if window appears
    Label(root, text="DEBUG: Root window is visible").pack(side=TOP, fill=X)
    # Add a visible border to the frame for debugging
    frame = StftMorph_frame(root)
    frame.config(borderwidth=5, relief="groove", bg="#e0e0e0")
    frame.pack(fill=BOTH, expand=True)
    root.mainloop()
