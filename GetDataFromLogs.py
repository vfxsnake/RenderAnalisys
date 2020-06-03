import os


class PyRender():
    def __init__(self, directory):
        self.Directory = directory
        self.RawFiles = os.listdir(directory)
        self.Files = []

        self.RenderTimeArray  = []

    def GetValidFiles(self):
        for file in self.RawFiles:
            year = None
            month = None
            if file.endswith(".txt"):
                splitEnd = file.split('.')[0]
                splitUnder = splitEnd.split('_')
                try:
                    year = int(splitUnder[-1])
                except:
                    pass
                if (year == 19 or year == 20):
                    try:
                        month = int(splitUnder[-2])
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
            frameNumber = 0
            totalDays = 0
            totalRenderMinuts = 0


            for x, file in enumerate(self.Files):
                currentFile = open('{0}/{1}'.format(self.Directory, file), 'r')

                framePerDay = 0

                for line in currentFile:
                    renderTime = self.getRenderTime(line)
                    # if renderTime>(12*60):
                        # print file
                    if renderTime:
                        self.RenderTimeArray.append(renderTime)
                        totalRenderMinuts += renderTime
                        framePerDay +=1
                        frameNumber +=1
                totalDays = x
                # print 'day {0} totalFrames = {1}'.format(x, framePerDay)
            print "Total Frames {0}".format(frameNumber)
            shotFrames = frameNumber/700
            print "Media Frames per Shot = {0}".format(shotFrames)
            print  "Media day frames: {0}".format(frameNumber/totalDays)
            print "Total render time {0} hrs".format(totalRenderMinuts/60)
            mediaRenderTime = (totalRenderMinuts/60)/frameNumber
            print "Media Render Time = {0}".format((totalRenderMinuts/60)/frameNumber)
            print 'ShotAverageTime {0}'.format(shotFrames* mediaRenderTime)

Analisis = PyRender('C:/Users/vfxsnake/Documents/PyRender/Logs')

Analisis.GetValidFiles()
Analisis.dailyRender()


print min(Analisis.RenderTimeArray)

text = open('data.txt','w+')
for element in Analisis.RenderTimeArray:
    text.write("{0},".format(element))
text.close()