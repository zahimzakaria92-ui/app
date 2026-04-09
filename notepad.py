#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import tkinter.font as tkfont

class ArabicNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Notepad")
        self.root.geometry("800x600")
        self.file_path = None

        # ✅ ضبط الخط الافتراضي بطريقة آمنة ومتوافقة
        try:
            default_font = tkfont.nametofont("TkDefaultFont")
            default_font.configure(family="Noto Sans Arabic", size=12)
        except (tkfont.FontNotFoundError, tk.TclError):
            pass  # استخدام خط النظام الافتراضي إذا لم يكن الخط مثبتاً

        # شريط القوائم
        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="📄 new ", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="📂 open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="💾 save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="🚪 exit", command=self.root.destroy, accelerator="Ctrl+Q")
        self.menu_bar.add_cascade(label="file", menu=self.file_menu)
        root.config(menu=self.menu_bar)

        # منطقة النص
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Noto Sans Arabic", 14))
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)

        # دعم الكتابة من اليمين لليسار (محمي من أخطاء إصدارات Tk القديمة)
        try:
            self.text_area.config(direction='rtl')
        except tk.TclError:
            pass

        # اختصارات لوحة المفاتيح
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-q>", lambda e: self.root.destroy())

        # تأكيد الإغلاق
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("📝 Notepad - new")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("ملفات نصية", "*.txt"), ("جميع الملفات", "*.*")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, f.read())
                self.file_path = path
                self.root.title(f"📝 Notepad - {path}")
            except Exception as e:
                messagebox.showerror(" error ", f" open   :\n{e}")

    def save_file(self):
        if self.file_path:
            self._write_to_file(self.file_path)
        else:
            path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("ملفات نصية", "*.txt"), ("جميع الملفات", "*.*")])
            if path:
                self.file_path = path
                self._write_to_file(path)
                self.root.title(f"📝 Notepad - {path}")

    def _write_to_file(self, path):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("save", "    ✅")
        except Exception as e:
            messagebox.showerror("خطأ", f"  الملف:\n{e}")

    def on_closing(self):
        if messagebox.askokcancel("_confirmation", "_do you want to exit the notepad?   "):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ArabicNotepad(root)
    root.mainloop()
