import os
from luigi import LocalTarget

def getLocalTarget(key):
  return LocalTarget(key)

def getLocalStateTarget(targetPath, fileName):
  targetKey = os.path.join(targetPath, fileName)
  return getLocalTarget(targetKey)

def getOutputPatternFromInputs(startFile, endFile):
    startFilename = os.path.basename(startFile)
    endFilename = os.path.basename(endFile)
    
    satellite = startFilename[0:3]
    startDate = startFilename[17:25]
    endDate = endFilename[17:25]

    return '{0}_coh_vv_{1}_{2}'.format(satellite, startDate, endDate)
