import os,time

class FileInfoItem:
    def __init__(self, name:str, fullPath:str, size:float, lastModifyTime: float):
        self.name = name
        self.path = fullPath
        self.size = size
        self.lastModifyTime = lastModifyTime
    
    def getDateFormatted(self) -> str:
        time_obj = time.strptime(time.ctime(self.lastModifyTime))
        return time.strftime("%Y/%m/%d %H:%M", time_obj)
    
    def getSizeConverted(self):
        # 定义单位转换
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(self.size)
        unit_index = 0
        
        # 当文件大于1024字节时，转换到下一个单位
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        
        # 保留两位小数
        return f"{size:.2f} {units[unit_index]}"


def getPath_StandardFormat(path:str) -> str:
    seperatePath = os.path.split(path)
    return seperatePath[0] + '/' + seperatePath[1]


def getTotalSizeAndLatestModTime(folderPath:str) -> tuple:
    totalSize = 0.
    latestModTime = 0.
    with os.scandir(folderPath) as entries:
        for entry in entries:
            if not entry.is_dir():
                try:
                    fileInfo = entry.stat()
                    #获取文件大小和最近修改时间
                    totalSize += fileInfo.st_size
                    if fileInfo.st_mtime >= latestModTime:
                        latestModTime = fileInfo.st_mtime
                except OSError as e:
                    print(f"获取文件信息时出错: {e}, 文件名: {entry.name}， 路径: {entry.path}")
            else:
                resTuple = getTotalSizeAndLatestModTime(getPath_StandardFormat(entry.path))
                totalSize += resTuple[0]
                if resTuple[1] >= latestModTime:
                    latestModTime = resTuple[1]
    if latestModTime == 0. :
        latestModTime = os.stat(folderPath).st_mtime
    return (totalSize, latestModTime)

def getCalculatedList(curPath:str) -> list:
    resList = []
    with os.scandir(curPath) as entries:
        for entry in entries:
            if entry.is_dir():
                (resSize, resTime) = getTotalSizeAndLatestModTime(getPath_StandardFormat(entry.path))
                resList.append(FileInfoItem(entry.name, entry.path, resSize, resTime))
            else:
                try:
                    fileInfo = entry.stat()
                    resList.append(FileInfoItem(entry.name, entry.path, fileInfo.st_size, fileInfo.st_mtime))
                except OSError as e:
                    print(f"获取文件信息时出错: {e}, 文件名: {entry.name}， 路径: {entry.path}")
    return resList

def getSize(element:FileInfoItem):
        return element.size
def getTime(element:FileInfoItem):
        return element.lastModifyTime

def getListSorted(reslist:list, index:str, asc:bool) -> list:
    if index == "size":
        reslist.sort(key=getSize,reverse=True) if asc else reslist.sort(key=getSize,reverse=False)
    else:
        reslist.sort(key=getTime,reverse=False) if asc else reslist.sort(key=getTime,reverse=True)
    return reslist