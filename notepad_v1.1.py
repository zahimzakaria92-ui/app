#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق مفكرة بسيط شبيه بمفكرة ويندوز
يعمل على لينكس باستخدام مكتبة tkinter
"""

import tkinter as tk
from tkinter import filedialog, messagebox, font

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مفكرة - Notepad")
        self.root.geometry("800x600")

        # المتغير لتخزين مسار الملف الحالي
        self.current_file = None

        # إنشاء منطقة النص
        self.text_area = tk.Text(root, wrap='word', undo=True,
                                 font=('Arial', 12),
                                 bg='#ffffff', fg='#000000')
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # إضافة شريط التمرير
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        # إنشاء القائمة
        self.create_menu()

        # ربط اختصارات لوحة المفاتيح
        self.bind_shortcuts()

    def create_menu(self):
        """إنشاء شريط القوائم"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # قائمة ملف
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="file", menu=file_menu)
        file_menu.add_command(label="new", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="save as", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="exit", command=self.exit_app, accelerator="Alt+F4")

        # قائمة تحرير
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="edit", menu=edit_menu)
        edit_menu.add_command(label="undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="select all", command=self.select_all, accelerator="Ctrl+A")

        # قائمة تنسيق
        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="format", menu=format_menu)
        format_menu.add_command(label="font ...", command=self.change_font)

        # قائمة مساعدة
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="help", menu=help_menu)
        help_menu.add_command(label="about", command=self.about)

    def bind_shortcuts(self):
        """ربط اختصارات لوحة المفاتيح"""
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-S>', lambda e: self.save_as_file())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-x>', lambda e: self.cut())
        self.root.bind('<Control-c>', lambda e: self.copy())
        self.root.bind('<Control-v>', lambda e: self.paste())
        self.root.bind('<Control-a>', lambda e: self.select_all())

    def new_file(self):
        """إنشاء ملف جديد"""
        if self.text_area.get('1.0', 'end-1c').strip():
            response = messagebox.askyesnocancel("save", "Do you want to save the changes before creating a new file?")
            if response is True:
                self.save_file()
            elif response is False:
                pass
            else:
                return

        self.text_area.delete('1.0', 'end')
        self.current_file = None
        self.root.title("مفكرة - Notepad")

    def open_file(self):
        """فتح ملف موجود"""
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                self.text_area.delete('1.0', 'end')
                self.text_area.insert('1.0', content)
                self.current_file = file_path
                self.root.title(f"Notepad - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file:\n{str(e)}")

    def save_file(self):
        """حفظ الملف الحالي"""
        if self.current_file:
            try:
                content = self.text_area.get('1.0', 'end-1c')
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """حفظ الملف باسم جديد"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                content = self.text_area.get('1.0', 'end-1c')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)

                self.current_file = file_path
                self.root.title(f"Notepad - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")

    def undo(self):
        """تراجع"""
        try:
            self.text_area.edit_undo()
        except:
            pass

    def redo(self):
        """إعادة"""
        try:
            self.text_area.edit_redo()
        except:
            pass

    def cut(self):
        """قص"""
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        """نسخ"""
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        """لصق"""
        self.text_area.event_generate("<<Paste>>")

    def select_all(self):
        """تحديد الكل"""
        self.text_area.tag_add('sel', '1.0', 'end')
        return 'break'

    def change_font(self):
        """تغيير الخط"""
        # نافذة بسيطة لتغيير الخط
        font_window = tk.Toplevel(self.root)
        font_window.title("اختر الخط")
        font_window.geometry("300x200")

        tk.Label(font_window, text="Font Size:").pack(pady=5)

        font_size_var = tk.StringVar(value="12")
        font_sizes = ["8", "10", "12", "14", "16", "18", "20", "24"]
        font_combo = tk.OptionMenu(font_window, font_size_var, *font_sizes)
        font_combo.pack(pady=5)

        def apply_font():
            try:
                size = int(font_size_var.get())
                current_font = font.Font(font=self.text_area['font'])
                current_font.configure(size=size)
                self.text_area.configure(font=current_font)
                font_window.destroy()
            except:
                messagebox.showerror("Error", "Invalid font size")

        tk.Button(font_window, text="Apply", command=apply_font).pack(pady=10)

    def about(self):
        """عن التطبيق"""
        messagebox.showinfo("About", "Simple Notepad Application\nBuilt with Python and Tkinter\nRuns on Linux Systems")

    def exit_app(self):
        """الخروج من التطبيق"""
        if self.text_area.get('1.0', 'end-1c').strip():
            response = messagebox.askyesnocancel("Save", "Do you want to save the changes before exiting?")
            if response is True:
                self.save_file()
                self.root.destroy()
            elif response is False:
                self.root.destroy()
            else:
                return
        else:
            self.root.destroy()


def main():
    # إنشاء النافذة الرئيسية كتطبيق مستقل
    root = tk.Tk()

    # إعدادات لجعل النافذة تبدو كتطبيق مستقل
    root.wm_attributes('-type', 'normal')  # نوع نافذة عادي
    root.focus_force()  # فرض التركيز على النافذة

    # إنشاء التطبيق
    app = NotepadApp(root)

    # تشغيل التطبيق
    root.mainloop()


if __name__ == "__main__":
    main()
