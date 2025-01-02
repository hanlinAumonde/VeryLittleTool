# use tkinter to create a GUI that can choose a path and display the file information using functions in Function.py

import tkinter as tk

from tkinter import filedialog

from Function import getCalculatedList, getPath_StandardFormat, getListSorted

class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文件信息查看器")
        self.window.geometry("800x600")
        
        self.path = tk.StringVar()
        self.path.set("请选择文件夹路径")
        self.fileList = []
        
        self.createWidgets()
    
    def createWidgets(self):
        # 创建一个标签，用于显示文件夹路径
        self.label = tk.Label(self.window, textvariable=self.path, font=("Arial", 12), width=60, height=2)
        self.label.pack()
        
        # 创建一个按钮，用于选择文件夹路径
        self.selectButton = tk.Button(self.window, text="选择文件夹", font=("Arial", 12), width=20, height=2, command=self.selectPath)
        self.selectButton.pack()
        
        #以下按钮必须再选择文件夹路径后才能使用
        
        # 创建一个按钮,  用于根据文件大小排序
        self.sortDscButton = tk.Button(self.window, text="按文件大小降序排序", font=("Arial", 12), width=20, height=2, command=lambda: self.sortBySize(True), state=tk.DISABLED)
        self.sortDscButton.pack()

        self.sortAscButton = tk.Button(self.window, text="按文件大小升序排序", font=("Arial", 12), width=20, height=2, command=lambda: self.sortBySize(False), state=tk.DISABLED)
        self.sortAscButton.pack()

        # 创建一个按钮,  用于根据最后修改时间排序
        self.sortTimeDscButton = tk.Button(self.window, text="按最后修改时间降序排序", font=("Arial", 12), width=20, height=2, command=lambda: self.sortByTime(True), state=tk.DISABLED)
        self.sortTimeDscButton.pack()

        self.sortTimeAscButton = tk.Button(self.window, text="按最后修改时间升序排序", font=("Arial", 12), width=20, height=2, command=lambda: self.sortByTime(False), state=tk.DISABLED)
        self.sortTimeAscButton.pack()

        # 创建一个文本框，用于显示文件信息
        self.text = tk.Text(self.window, font=("Arial", 12), width=80, height=30)
        self.text.pack()
    
    def selectPath(self):
        path = filedialog.askdirectory()
        self.path.set(path)
        if path:
            self.fileList = getCalculatedList(path)
            self.sortAscButton.config(state=tk.NORMAL)
            self.sortDscButton.config(state=tk.NORMAL)
            self.sortTimeAscButton.config(state=tk.NORMAL)
            self.sortTimeDscButton.config(state=tk.NORMAL)

    def sortBySize(self, order:bool):
        self.fileList = getListSorted(self.fileList, "size",order)
        self.text.delete(1.0, tk.END)
        for item in self.fileList:
            self.text.insert(tk.END, f"文件名： {item.name}\n")
            self.text.insert(tk.END, f"文件目录： {getPath_StandardFormat(item.path)}\n")
            self.text.insert(tk.END, f"文件大小： {item.getSizeConverted()}\n")
            self.text.insert(tk.END, f"最后修改时间： {item.getDateFormatted()}\n")
            self.text.insert(tk.END, "-"*80 + "\n")
    
    def sortByTime(self, order:bool):
        self.fileList = getListSorted(self.fileList, "time",order)
        self.text.delete(1.0, tk.END)
        for item in self.fileList:
            self.text.insert(tk.END, f"文件名： {item.name}\n")
            self.text.insert(tk.END, f"文件目录： {getPath_StandardFormat(item.path)}\n")
            self.text.insert(tk.END, f"文件大小： {item.getSizeConverted()}\n")
            self.text.insert(tk.END, f"最后修改时间： {item.getDateFormatted()}\n")
            self.text.insert(tk.END, "-"*80 + "\n")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()