import json
import logging
import luigi
import os
import shutil

from luigi.util import requires
from process_slc_pair.Common import getLocalStateTarget
from process_slc_pair.TransferOutputs import TransferOutputs

log = logging.getLogger('luigi-interface')

@requires(TransferOutputs)
class CleanupCompletedProductInputs(luigi.Task):
  paths = luigi.DictParameter()

  def run(self):
    transferOutputs = {}
    with self.input().open('r') as transferOutput:
        transferOutputs = json.load(transferOutput)

    inputBasketDirectory = os.path.join(self.paths['input'], transferOutputs['inputFolder'])
    log.info('Removing input basket directory "{0}"'.format(inputBasketDirectory))
    shutil.rmtree(inputBasketDirectory)

    with self.output().open('w') as output:
      output.write(json.dumps(transferOutputs, indent=4))
  
  def output(self):
    return getLocalStateTarget(self.paths['state'], 'CleanupCompletedProductInputs.json')  