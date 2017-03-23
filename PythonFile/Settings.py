#class for save settings.
class Settings():
    
    #init
    def __init__(self, fn='settings.txt'):
        self.fileName=fn
        self.settingArray=[150,150,4,2,5,300,4,100]
    #write to file
    def writeSettings(self):
        try:
            file=open(self.fileName,'w')
            for i in range(0,len(self.settingArray)):
                file.write(str(self.settingArray[i])+'\n')
            closeFile(file)
            return True
        except:
            return False
    #read from file
    def readSettings(self):
        file=open(self.fileName,'r')
        res=file.read()
        file.close()
        self.settingArray= res.split('\n')
        return self.settingArray
    #write track bar value to array before save the file
    def writeSetting(self,settingName,value):
        if(settingName=="Th1"):
              self.settingArray[0]=value
        if(settingName=="Th2"):
              self.settingArray[1]=value
        if(settingName=="Blur"):
              self.settingArray[2]=value
        if(settingName=="E"):
              self.settingArray[3]=value
        if(settingName=="Y1"):
              self.settingArray[4]=value
        if(settingName=="Y2"):
              self.settingArray[5]=value
        if(settingName=="X1"):
              self.settingArray[6]=value
        if(settingName=="X2"):
              self.settingArray[7]=value

        self.writeSettings()
