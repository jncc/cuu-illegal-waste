import luigi
import os
import logging
import json

from string import Template
from luigi.util import requires
from orchestration.GetAllSubBaskets import GetAllSubBaskets

log = logging.getLogger('luigi-interface')

@requires(GetAllSubBaskets)
class SetupWorkDirs(luigi.Task):
    stateLocation = luigi.Parameter()
    workingLocation = luigi.Parameter()
    outputLocation = luigi.Parameter()
    staticLocation = luigi.Parameter()
    containerPath = luigi.Parameter()

    def run(self):
        pairBaskets = []
        with self.input().open('r') as inputFile:
            pairBaskets = json.load(inputFile)['subBaskets']

        productPairs = []
        for basket in pairBaskets:
            pairName = os.path.basename(os.path.normpath(basket['basketPath']))
            baseWorkDir = os.path.join(self.workingLocation, pairName)
            workingDir = os.path.join(baseWorkDir, 'working')
            stateDir = os.path.join(baseWorkDir, 'state')
            sbatchFile = os.path.join(workingDir, 'process_illegal_waste.sbatch')

            if not os.path.exists(baseWorkDir):
                os.makedirs(baseWorkDir)

            if not os.path.exists(stateDir):
                os.mkdir(stateDir)

            if not os.path.exists(workingDir):
                os.mkdir(workingDir)

            with open(os.path.join('orchestration/templates/process_illegal_waste_job_template.sbatch'), 'r') as templateFile:
                jobTemplate = Template(templateFile.read())
            
            params = {
                'input': basket['basketPath'],
                'state': stateDir,
                'static': self.staticLocation,
                'working': workingDir,
                'output': self.outputLocation,
                'containerPath': self.containerPath,
                'firstInput': basket['files'][0],
                'secondInput': basket['files'][1],
                'outputBaseFolder': self.outputLocation
            }

            sbatchContents = jobTemplate.substitute(params)
            sbatchFile = os.path.join(baseWorkDir, 'process_illegal_waste.sbatch')

            with open(sbatchFile, 'w') as f:
                f.write(sbatchContents)

            productPairs.append({
                'pairName': pairName,
                'basketPath': basket['basketPath'],
                'products': basket['files'],
                'sbatchFile': sbatchFile
            })

        output = {
            'productPairs': productPairs
        }
        with self.output().open('w') as outFile:
            outFile.write(json.dumps(output, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'SetupWorkDirs.json'))