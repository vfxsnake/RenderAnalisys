import os

def renameLog():
    path = 'Logs'
    files  = os.listdir(path)
    for file in files:
        currentName = file.split('.')[0]
        nameUnderSplit = currentName.split('_')
        newName = "{0}_{1}_{2}.txt".format(nameUnderSplit[-1], nameUnderSplit[-2], nameUnderSplit[-3])
        os.rename('{0}/{1}'.format(path,file), '{0}/{1}'.format(path,newName))


class PyRender():
    def __init__(self, directory):
        self.Directory = directory
        self.RawFiles = os.listdir(directory)
        self.Files = []


        # array of tiem of every frame rendered (data.csv)
        self.RenderTimeArray = []

        # total render Hours per day (Farm Eficienty) perDay.csv
        self.RenderTimeDalyArray = []

        # Total render Frames per day PerDayHarvest.csv
        self.DailyFrameHarvest = []

        # frame increment curve FramesAcomulativive.csv
        self.frameCount = []


    def GetValidFiles(self):
        for file in self.RawFiles:
            year = None
            month = None
            if file.endswith(".txt"):
                splitEnd = file.split('.')[0]
                splitUnder = splitEnd.split('_')
                try:
                    year = int(splitUnder[0])
                except:
                    pass
                if (year == 19 or year == 20):
                    try:
                        month = int(splitUnder[1])
                    except:

                        pass
                    if (month <10 and year == 19):
                        # print file
                        pass
                    else:
                        self.Files.append(file)


    def getRenderTime(self, line):
        if line:
            minutes = None
            dt = None
            try:
                dt = line.split(' ')[-2]
            except:
                return None

            if dt:
                splitIme = dt.split(':')
                try:

                    minutes = float(splitIme[0])*60 + float(splitIme[1]) + float(splitIme[2])/60
                    # if minutes > (12*60):
                    #     print dt

                except:
                    # print line
                    # print splitIme
                    return None
                return minutes


    def dailyRender(self):
        if self.Files:
            self.Files.sort()

            frameNumber = 0
            totalDays = 0
            totalRenderMinuts = 0


            for x, file in enumerate(self.Files):
                # print file
                currentFile = open('{0}/{1}'.format(self.Directory, file), 'r')

                framePerDay = 0
                RenderTimePerDay = 0
                for line in currentFile:
                    renderTime = self.getRenderTime(line)
                    # if renderTime>(12*60):
                        # print file
                    if renderTime:
                        self.RenderTimeArray.append(renderTime)
                        RenderTimePerDay += renderTime
                        totalRenderMinuts += renderTime
                        framePerDay +=1
                        frameNumber +=1
                self.frameCount.append(frameNumber)
                self.DailyFrameHarvest.append(framePerDay)
                totalDays = x
                # print 'day {0} totalFrames = {1}'.format(x, framePerDay)
                self.RenderTimeDalyArray.append(RenderTimePerDay)
            print "Total Frames {0}".format(frameNumber)
            shotFrames = frameNumber/660
            print "Media Frames per Shot = {0}".format(shotFrames)
            print  "Media day frames: {0}".format(frameNumber/totalDays)
            print "Total render time {0} hrs".format(totalRenderMinuts/60)
            mediaRenderTime = (totalRenderMinuts/60)/frameNumber
            print "Media Render Time = {0}".format((totalRenderMinuts/60)/frameNumber)
            print 'ShotAverageTime {0}'.format(shotFrames* mediaRenderTime)


Analisis = PyRender('Logs')

Analisis.GetValidFiles()
Analisis.dailyRender()

text = open('data.csv','w+')
for element in Analisis.RenderTimeArray:
    text.write("{0}\n".format(element/60))
text.close()

text = open('PerDay.csv','w+')
for element in Analisis.RenderTimeDalyArray:
    text.write("{0}\n".format(element/60))
text.close()

text = open('PerDayHarvest.csv','w+')
for element in Analisis.DailyFrameHarvest:
    text.write("{0}\n".format(element))
text.close()

text = open('FramesAcomulativive.csv','w+')
for element in Analisis.frameCount:
    text.write("{0}\n".format(element))
text.close()