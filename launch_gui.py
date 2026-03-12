from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "interface-models"
TRANSFORMATIONS_DIR = ROOT / "interface-transformations"


def launch_gui(script_dir: Path, script_name: str) -> None:
    script_path = script_dir / script_name
    if not script_path.exists():
        messagebox.showerror("Launch error", f"Could not find {script_path}")
        return

    try:
        subprocess.Popen([sys.executable, script_name], cwd=script_dir)
    except Exception as exc:
        messagebox.showerror("Launch error", str(exc))


def main() -> None:
    root = tk.Tk()
    root.title("sms-tools GUI launcher")
    root.resizable(False, False)
    root.minsize(360, 180)

    container = tk.Frame(root, padx=18, pady=18)
    container.pack(fill=tk.BOTH, expand=True)

    title = tk.Label(
        container,
        text="Open a graphical interface",
        font=("TkDefaultFont", 14, "bold"),
    )
    title.pack(anchor="w", pady=(0, 8))

    subtitle = tk.Label(
        container,
        text="Choose which sms-tools application to start.",
    )
    subtitle.pack(anchor="w", pady=(0, 14))

    models_button = tk.Button(
        container,
        text="Models GUI",
        width=22,
        font=("TkDefaultFont", 11, "bold"),
        command=lambda: launch_gui(MODELS_DIR, "models_GUI.py"),
    )
    models_button.pack(fill=tk.X, pady=(0, 10))

    transformations_button = tk.Button(
        container,
        text="Transformations GUI",
        width=22,
        font=("TkDefaultFont", 11, "bold"),
        command=lambda: launch_gui(TRANSFORMATIONS_DIR, "transformations_GUI.py"),
    )
    transformations_button.pack(fill=tk.X)

    if len(sys.argv) > 1:
        choice = sys.argv[1].strip().lower()
        if choice in {"models", "model"}:
            launch_gui(MODELS_DIR, "models_GUI.py")
            root.destroy()
            return
        if choice in {"transformations", "transformation", "transforms", "transform"}:
            launch_gui(TRANSFORMATIONS_DIR, "transformations_GUI.py")
            root.destroy()
            return

    root.mainloop()


if __name__ == "__main__":
    main()
