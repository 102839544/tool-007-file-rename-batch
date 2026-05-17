#!/usr/bin/env python3
"""
批量重命名工具 - 批量重命名文件
"""
import sys, os, re, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        root.title("批量重命名工具 v1.0")
        root.geometry("750x550")
        self.files = []
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#1565c0", height=50)
        f.pack(fill="x")
        tk.Label(f, text="📝 批量重命名工具", font=("Arial",14,"bold"),
                 fg="white", bg="#1565c0").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="添加文件", command=self.add_files,
                  bg="#1565c0", fg="white", padx=12).pack(side="left", padx=5)
        tk.Button(bf, text="添加文件夹", command=self.add_folder,
                  bg="#1565c0", fg="white", padx=12).pack(side="left", padx=5)
        tk.Button(bf, text="清空", command=self.clear,
                  bg="#d9534f", fg="white", padx=12).pack(side="left", padx=5)
        
        # 重命名规则
        rf = tk.LabelFrame(main, text="重命名规则", padx=10, pady=5)
        rf.pack(fill="x", pady=10)
        
        tk.Label(rf, text="模式：").grid(row=0, column=0, sticky="w")
        self.pattern = tk.StringVar(value="文件_{n}")
        tk.Entry(rf, textvariable=self.pattern, width=30).grid(row=0, column=1, padx=5)
        tk.Label(rf, text="{n}=序号, {name}=原名").grid(row=0, column=2, sticky="w", padx=5)
        
        tk.Label(rf, text="起始序号：").grid(row=1, column=0, sticky="w", pady=5)
        self.start_num = tk.StringVar(value="1")
        tk.Entry(rf, textvariable=self.start_num, width=10).grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Button(rf, text="预览", command=self.preview,
                  padx=15).grid(row=0, column=3, padx=10)
        tk.Button(rf, text="执行重命名", command=self.rename,
                  bg="#4caf50", fg="white", padx=15).grid(row=1, column=3, padx=10)
        
        # 文件列表
        cols = ("原文件名", "新文件名")
        self.tree = tk.ttk.Treeview(main, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=350)
        self.tree.pack(fill="both", expand=True, pady=5)
        
        self.status = tk.Label(main, text="添加文件并设置重命名规则",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def add_files(self):
        fs = filedialog.askopenfilenames(title="选择文件")
        for f in fs:
            if f not in self.files:
                self.files.append(f)
        self.refresh_list()
    
    def add_folder(self):
        folder = filedialog.askdirectory(title="选择文件夹")
        if folder:
            for f in Path(folder).iterdir():
                if f.is_file():
                    self.files.append(str(f))
            self.refresh_list()
    
    def clear(self):
        self.files.clear()
        self.refresh_list()
    
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for f in self.files:
            self.tree.insert("", "end", values=(Path(f).name, ""))
        self.status.config(text=f"已添加 {len(self.files)} 个文件")
    
    def preview(self):
        pattern = self.pattern.get()
        try:
            start = int(self.start_num.get())
        except:
            start = 1
        
        for i, item in enumerate(self.tree.get_children()):
            old_name = Path(self.files[i]).name
            ext = Path(self.files[i]).suffix
            new_name = pattern.replace("{n}", str(start + i))
            new_name = new_name.replace("{name}", Path(self.files[i]).stem)
            new_name += ext
            self.tree.item(item, values=(old_name, new_name))
        
        self.status.config(text="预览完成，确认后点击「执行重命名」")
    
    def rename(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("提示", "请先添加文件并预览")
            return
        
        ok = 0
        for item in items:
            values = self.tree.item(item)["values"]
            if len(values) < 2 or not values[1]:
                continue
            
            idx = self.tree.index(item)
            old_path = Path(self.files[idx])
            new_path = old_path.parent / values[1]
            
            try:
                old_path.rename(new_path)
                ok += 1
            except Exception as e:
                print(f"重命名失败: {e}")
        
        messagebox.showinfo("完成", f"成功重命名 {ok} 个文件")
        self.status.config(text=f"✅ 完成：{ok} 个文件已重命名")

if __name__ == "__main__":
    import tkinter.ttk
    root = tk.Tk()
    App(root)
    root.mainloop()
