# use tkinter to create a GUI that can choose a path and display the file information using functions in Function.py

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from Function import deleteFile, getCalculatedList, getPath_StandardFormat, getListSorted, openFile

class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文件信息查看器")
        self.window.geometry("800x600")
        
        self.path = tk.StringVar()
        self.path.set("请选择文件夹路径")
        self.firstPath = self.path.get()
        self.fileList = []
        
        #self.folderImage = tk.PhotoImage(file="./img/folder.png")
        #self.fileImage = tk.PhotoImage(file="./img/file.png")
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

        # 创建一个按钮，用于返回上一级目录
        backButton = tk.Button(self.windowFrame1, text="返回上一级", font=("Arial", 12), width=20, height=2, command=self.goBack, state=tk.DISABLED)
        backButton.grid(row=2, column=0)
        self.windowFrame1.pack()    

        # 创建一个Treeview，用于显示文件信息
        self.tree = ttk.Treeview(self.window, columns=("icon","name", "size", "time"), show="headings")
        self.tree.heading("icon",text="")
        self.tree.heading("name", text="文件名")
        self.tree.heading("size", text="文件大小", command=lambda:self.sortBy("size"))
        self.tree.heading("time", text="最后修改时间", command=lambda:self.sortBy("time"))
        self.tree.column("icon", width=30)
        self.tree.column("name", width=200)
        self.tree.column("size", width=100)
        self.tree.column("time", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # 为Treeview的item绑定双击事件,但不包括heading
        self.tree.bind("<Double-1>", self.onDoubleClickItem)
        # 为Treeview的item绑定右键菜单
        self.tree.bind("<Button-3>", self.onRightClickItem)
        # 为Treeview的item绑定delete键
        self.tree.bind("<Delete>", self.operateFile("delete"))

    # 选择文件夹路径
    def selectPath(self):
        path = filedialog.askdirectory()
        self.path.set(path)
        if path:
            if self.firstPath == "请选择文件夹路径":
                self.firstPath = path
            self.fileList = getCalculatedList(path)
            self.windowFrame1.winfo_children()[2].config(state=tk.NORMAL)
            self.updateTreeview()


    # 返回上一级目录
    def goBack(self):
        path = self.path.get()
        if path == "请选择文件夹路径":
            return
        path = path.split("/")
        path = "/".join(path[:-1])
        if path == self.firstPath:
            self.windowFrame1.winfo_children()[2].config(state=tk.DISABLED)
        self.path.set(path)
        self.fileList = getCalculatedList(path)
        self.updateTreeview()

    # 双击Treeview的item时触发
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
            self.windowFrame1.winfo_children()[2].config(state=tk.NORMAL)
            self.updateTreeview()
        else:
            openFile(path)
    
    # 右键Treeview的item时触发,弹出菜单
    def onRightClickItem(self,event):
        item = self.tree.selection()[0]
        if self.tree.item(item, "tags")[0] == "True":
            return
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="打开文件", command=lambda: self.operateFile("open"))
        menu.add_command(label="删除文件", command=lambda: self.operateFile("delete"))
        menu.post(event.x_root, event.y_root)
    
    # 操作文件
    def operateFile(self,type:str):
        if not self.tree.selection():
            return
        item = self.tree.selection()[0]
        path = self.tree.item(item, "tags")[1]
        if type == "open":
            openFile(path)
        else:
            deleteFile(path)
            self.fileList = getCalculatedList(self.path.get())
            self.updateTreeview()

    # 根据文件大小或最后修改时间排序
    def sortBy(self, index:str):
        if index == "size":
            self.fileList = getListSorted(self.fileList, "size", self.SortBySizeDsc)
            self.SortBySizeDsc = not self.SortBySizeDsc
        else:
            self.fileList = getListSorted(self.fileList, "time", self.SortByTimeDsc)
            self.SortByTimeDsc = not self.SortByTimeDsc
        self.updateTreeview()

    # 更新Treeview
    def updateTreeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.fileList:
            self.tree.insert("", "end", values=(
                #"",
                "文件夹" if item.isDir else "文件",
                item.name,
                item.getSizeConverted(),
                item.getDateFormatted()
            #), image=self.folderImage if item.isDir else self.fileImage, tags=(item.isDir, getPath_StandardFormat(item.path)))
            ), tags=(item.isDir, getPath_StandardFormat(item.path)))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()