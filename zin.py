#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os

class TextAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Analyzer - Untitled.txt")
        self.root.geometry("800x600")

        # Configure style for a modern look
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Variables
        self.current_filename = "Untitled.txt"
        self.is_text_hidden = False

        # Create Main Frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Text Area
        self.text_area = tk.Text(
            self.main_frame,
            font=("Consolas", 12),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="white",
            wrap=tk.WORD
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Status Bar (Analyzer)
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X)

        self.lbl_words = ttk.Label(self.status_frame, text="Words: 0", foreground="#007acc")
        self.lbl_words.pack(side=tk.LEFT, padx=10)

        self.lbl_chars = ttk.Label(self.status_frame, text="Characters: 0", foreground="#007acc")
        self.lbl_chars.pack(side=tk.LEFT, padx=10)

        self.lbl_lines = ttk.Label(self.status_frame, text="Lines: 0", foreground="#007acc")
        self.lbl_lines.pack(side=tk.LEFT, padx=10)

        self.lbl_status = ttk.Label(self.status_frame, text="Ready", foreground="#6a9955")
        self.lbl_status.pack(side=tk.RIGHT, padx=10)

        # Bind Events
        self.bind_shortcuts()
        self.text_area.bind('<KeyRelease>', self.update_stats)

        # Initial Stats
        self.update_stats()

    def bind_shortcuts(self):
        # Ctrl+Q: Exit
        self.root.bind('<Control-q>', self.exit_app)

        # Ctrl+R: Rename File
        self.root.bind('<Control-r>', self.rename_file)

        # F9: Toggle Hide/Show Text
        self.root.bind('<F9>', self.toggle_text_visibility)

    def update_stats(self, event=None):
        """Analyzes the text and updates the status bar."""
        if self.is_text_hidden:
            self.lbl_words.config(text="Words: --")
            self.lbl_chars.config(text="Chars: --")
            self.lbl_lines.config(text="Lines: --")
            return

        content = self.text_area.get("1.0", tk.END)

        # Count Characters (excluding the final newline added by Tkinter)
        char_count = len(content) - 1 if content.endswith('\n') else len(content)

        # Count Lines
        line_count = int(self.text_area.index('end-1c').split('.')[0])

        # Count Words
        words = content.split()
        word_count = len(words)

        self.lbl_words.config(text=f"Words: {word_count}")
        self.lbl_chars.config(text=f"Characters: {char_count}")
        self.lbl_lines.config(text=f"Lines: {line_count}")
        self.lbl_status.config(text="Updated")

    def exit_app(self, event=None):
        """Exits the application (Ctrl+Q)."""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

    def rename_file(self, event=None):
        """Opens a dialog to rename the file (Ctrl+R)."""
        new_name = simpledialog.askstring(
            "Rename File",
            "Enter new file name:",
            initialvalue=self.current_filename
        )

        if new_name:
            self.current_filename = new_name
            self.root.title(f"Text Analyzer - {self.current_filename}")
            self.lbl_status.config(text=f"Renamed to {self.current_filename}")

    def toggle_text_visibility(self, event=None):
        """Hides or Shows the text content (F9)."""
        if self.is_text_hidden:
            # Show Text
            self.text_area.config(state=tk.NORMAL, bg="#1e1e1e", fg="#d4d4d4")
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", self.hidden_content)
            self.is_text_hidden = False
            self.lbl_status.config(text="Text Visible")
        else:
            # Hide Text
            self.hidden_content = self.text_area.get("1.0", tk.END)
            self.text_area.config(state=tk.DISABLED, bg="#2d2d2d", fg="#2d2d2d") # Make it look empty/dark
            # Actually, to truly hide without losing data in a disabled widget,
            # we clear it and store in variable, or just change colors to match background.
            # Let's clear it visually but keep data in memory variable for simplicity in this demo
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(state=tk.DISABLED)

            self.is_text_hidden = True
            self.lbl_status.config(text="Text Hidden (Press F9 to show)")

        self.update_stats()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextAnalyzerApp(root)
    root.mainloop()
