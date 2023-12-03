import os
import time
import shutil
from win10toast import ToastNotifier

class DownloadMonitor:
    def __init__(self, filePath):
        self.filePath = filePath
        self.checkInterval = 1
        self.previousSize = 0
        
    def GetFileSize(self):
        return os.path.getsize(self.filePath)
    
    def isDownloadFin(self):
        currentSize = self.GetFileSize()
        
        if currentSize == self.previousSize:
            return True
    
        self.previousSize = currentSize
        return False
            
    def mainMonitor(self):
        if self.filePath.endswith(".tmp"):
            return False
        
        while not self.isDownloadFin():
            time.sleep(self.checkInterval)
            
        return True

class DownloadFileOrganiser:
    def __init__(self, dirPath):
        self.dirPath = dirPath
        
    def userInfo(self, new_file_path):
        toast = ToastNotifier()
        toast.show_toast(
            "File Moved",
            "Downloaded file moved to: " + new_file_path,
            duration = 20,
            icon_path = "icon.ico",
            threaded = True,
        )
        
    def categorizeFile(self, fileDir, fileName, fileType):
        baseDir = os.path.expanduser("~")
        
        if fileType in [".png", ".jpg"]:
            isExist = os.path.exists(baseDir + "\\Documents\\Images")
            if not isExist:
                os.makedirs(baseDir + "\\Documents\\Images")
            newFolder = str(baseDir + "\\Documents\\Images")
            
            newDir = newFolder + "\\" + fileName
            shutil.move(fileDir, newDir)
            self.userInfo(newFolder)
        elif fileType in [".txt", ".doc", ".docx", ".word"]:
            isExist = os.path.exists(baseDir + "\\Documents\\Text")
            if not isExist:
                os.makedirs(baseDir + "\\Documents\\Text")
            newFolder = str(baseDir + "\\Documents\\Text")
            
            newDir = newFolder + "\\" + fileName
            shutil.move(fileDir, newDir)
            self.userInfo(newFolder)
        elif fileType == ".pdf":
            isExist = os.path.exists(baseDir + "\\Documents\\PDF")
            if not isExist:
                os.makedirs(baseDir + "\\Documents\\PDF")
            newFolder = str(baseDir + "\\Documents\\PDF")
            
            newDir = newFolder + "\\" + fileName
            shutil.move(fileDir, newDir)
            self.userInfo(newFolder)
        elif fileType in [".html", ".css", ".js", ".php"]:
            isExist = os.path.exists(baseDir + "\\Documents\\Website Stuff")
            if not isExist:
                os.makedirs(baseDir + "\\Documents\\Website Stuff")
            newFolder = str(baseDir + "\\Documents\\Website Stuff")
            
            newDir = newFolder + "\\" + fileName
            shutil.move(fileDir, newDir)
            self.userInfo(newFolder)
        else:
            isExist = os.path.exists(baseDir + "\\Documents\\Uncategorizable")
            if not isExist:
                os.makedirs(baseDir + "\\Documents\\Uncategorizable")
            newFolder = str(baseDir + "\\Documents\\Uncategorizable")
            
            newDir = newFolder + "\\" + fileName
            shutil.move(fileDir, newDir)
            self.userInfo(newFolder)
        
    def DownloadMonitorStart(self, fileName):
        filePath = os.path.join(self.dirPath, fileName) 
        downloadMonitor = DownloadMonitor(filePath)
        return downloadMonitor.mainMonitor()
              
    def listFiles(self, dirPath):
        return [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]

    def observer(self):
        fileDir = ""
        fileName = ""
        fileDataType = ""
        isDownloadFin = False
        
        filesBefore = set(self.listFiles(self.dirPath))
        
        while(True):            
            time.sleep(1)
            
            filesNow = set(self.listFiles(self.dirPath))
            newFiles = filesNow - filesBefore
            
            if newFiles:
                for newFile in newFiles:
                    isDownloadFin = self.DownloadMonitorStart(newFile)
                    
                    if isDownloadFin:
                        fileDir = str(self.dirPath + "\\" + newFile)
                        fileName = newFile
                        fileDataType = os.path.splitext(self.dirPath+newFile)[1]
                        self.categorizeFile(fileDir, fileName, fileDataType)
                
            filesBefore = filesNow

    def main(self):
        while(True):
            try:
                self.observer()
            except Exception as e:
                print(e)
                
if __name__ == "__main__":
    DownloadFileOrganiser = DownloadFileOrganiser(os.path.expandvars('%USERPROFILE%\\Downloads'))
    DownloadFileOrganiser.main()