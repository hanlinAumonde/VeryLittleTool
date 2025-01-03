# use tkinter to create a GUI that can choose a path and display the file information using functions in Function.py

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from Function import getCalculatedList, getPath_StandardFormat, getListSorted

class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文件信息查看器")
        self.window.geometry("800x600")
        
        self.path = tk.StringVar()
        self.path.set("请选择文件夹路径")
        self.fileList = []
        
        #self.image = tk.PhotoImage(file="./img/icon.png")
        self.SortBySizeDsc = True
        self.SortByTimeDsc = True
        
        self.createWidgets()
    
    def createWidgets(self):

        # 创建一个框架，用于放置标签和按钮
        self.windowFrame1 = tk.Frame(self.window)
        # 创建一个标签，用于显示文件夹路径
        label = tk.Label(self.windowFrame1 ,textvariable=self.path, font=("Arial", 12), width=60, height=2)
        label.grid(row=0, column=0)
        
        # 创建一个按钮，用于选择文件夹路径
        selectButton = tk.Button(self.windowFrame1, text="选择文件夹", font=("Arial", 12), width=20, height=2, command=self.selectPath)
        selectButton.grid(row=1, column=0)    
        self.windowFrame1.pack()    

        # 创建一个Treeview，用于显示文件信息
        self.tree = ttk.Treeview(self.window, columns=("name", "size", "time"), show="headings")
        self.tree.heading("name", text="文件名")
        self.tree.heading("size", text="文件大小", command=self.sortBySize)
        self.tree.heading("time", text="最后修改时间", command=self.sortByTime)
        self.tree.column("name", width=200)
        self.tree.column("size", width=100)
        self.tree.column("time", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # 为Treeview的item绑定双击事件,但不包括heading
        self.tree.bind("<Double-1>", self.onDoubleClickItem)

    def selectPath(self):
        path = filedialog.askdirectory()
        self.path.set(path)
        if path:
            self.fileList = getCalculatedList(path)
            self.updateTreeview()

    def onDoubleClickItem(self,event):
        if self.tree.identify_region(event.x, event.y) == "heading":
            return
        if not self.tree.selection():
            return
        item = self.tree.selection()[0]
        path = self.tree.item(item, "tags")[1]
        if self.tree.item(item, "tags")[0] == "True":
            self.path.set(path)
            self.fileList = getCalculatedList(path)
            self.updateTreeview()

    def sortBySize(self):
        self.fileList = getListSorted(self.fileList, "size", self.SortBySizeDsc)
        self.SortBySizeDsc = not self.SortBySizeDsc
        self.updateTreeview()
    
    def sortByTime(self):
        self.fileList = getListSorted(self.fileList, "time", self.SortByTimeDsc)
        self.SortByTimeDsc = not self.SortByTimeDsc
        self.updateTreeview()

    def updateTreeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.fileList:
            self.tree.insert("", "end", values=(
                item.name,
                item.getSizeConverted(),
                item.getDateFormatted()
            ), tags=(item.isDir, getPath_StandardFormat(item.path)))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()