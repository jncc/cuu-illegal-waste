import logging
import luigi
import os
import re
import shutil
from datetime import datetime
from os.path import basename, join
from luigi import LocalTarget

def getLocalTarget(key):
  return LocalTarget(key)

def getLocalStateTarget(targetPath, fileName):
  targetKey = join(targetPath, fileName)
  return getLocalTarget(targetKey)
