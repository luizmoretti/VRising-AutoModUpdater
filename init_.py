import thunderchecker
import localdir
import thunderdownload
import unzipfiles
from time import sleep

class callHelpers:
    def __init__(self):
        #Run ThunderChecker
        thunderchecker.ThunderModsChekerUpdate()
        sleep(10)
        
        #Run LocalDir
        localdir.LocalDirChecker()
        sleep(2)
        
        #Run ThunderDownload
        thunderdownload.ThunderModsDownload()
        sleep(4)
        
        #Run Unzipper
        unzipfiles.UnzipFiles()
        sleep(5)
        
        