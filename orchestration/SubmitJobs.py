import luigi
import os
import logging
import json

from luigi.util import requires
from orchestration.SetupWorkDirs import SetupWorkDirs
from orchestration.SubmitJob import SubmitJob

log = logging.getLogger('luigi-interface')

@requires(SetupWorkDirs)
class SubmitJobs(luigi.Task):
    stateLocation = luigi.Parameter()
    workingLocation = luigi.Parameter()
    testProcessing = luigi.BoolParameter(default = False)

    def run(self):
        productPairs = []
        with self.input().open('r') as getAllSubBasketsInfo:
            productPairs = json.load(getAllSubBasketsInfo)['productPairs']

        tasks = []
        for pairs in productPairs:
            task = SubmitJob(
                stateLocation = self.stateLocation,
                pairName = pairs['pairName'],
                sbatchScriptPath = pairs['sbatchFile'],
                testProcessing = self.testProcessing
            )

            tasks.append(task)
        
        yield tasks

        output = {
            'submittedPairs': []
        }

        for task in tasks:
            with task.output().open('r') as taskOutput:
                submittedPair = json.load(taskOutput)
                output['submittedPairs'].append(submittedPair)

        with self.output().open('w') as outFile:
            outFile.write(json.dumps(output, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'SubmitJobs.json'))