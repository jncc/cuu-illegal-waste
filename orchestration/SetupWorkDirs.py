from typing import List
import luigi
import os
import logging
import json

from string import Template
from luigi.util import requires
from orchestration.GetAllSubBaskets import GetAllSubBaskets
from pathlib import Path

log = logging.getLogger('luigi-interface')

@requires(GetAllSubBaskets)
class SetupWorkDirs(luigi.Task):
    stateLocation = luigi.Parameter()
    workingLocation = luigi.Parameter()
    outputLocation = luigi.Parameter()
    staticLocation = luigi.Parameter()
    containerPath = luigi.Parameter()
    templateFile = luigi.Parameter()
    outputSRS = luigi.Parameter()

    def resolveExtraBinds(self, extraBinds: List[str], potentialSymlink: str):
        if Path(potentialSymlink).is_symlink():
            extraBinds.append(str(Path(potentialSymlink).resolve().parent))
        return extraBinds
    
    def getExtraBindsFromBasket(self, basket):
        extraBinds = []
        for file in basket:
            extraBinds = self.resolveExtraBinds(extraBinds, file)
        return list(set(extraBinds))

    def getFilteredExtraBindings(self, input, state, static, working, output, basketFiles: List[str]):
        extraBinds = self.getExtraBindsFromBasket(basketFiles)

        for binding in [input, state, static, working, output]:
            if binding in extraBinds:
                extraBinds.remove(binding)

        bindings = ''

        for bind in extraBinds:
            bindings = '{0} --bind {1}:{1}'.format(bindings, bind)        
        
        return bindings

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

            with open(self.templateFile, 'r') as templateFile:
                jobTemplate = Template(templateFile.read())

            params = {
                'input': str(Path(basket['basketPath']).parent),
                'state': stateDir,
                'static': self.staticLocation,
                'working': workingDir,
                'output': self.outputLocation,
                'containerPath': self.containerPath,
                'inputFolder': pairName,
                'outputSRS': self.outputSRS
            }

            params['extraBinds'] = self.getFilteredExtraBindings(params['input'], params['state'], params['static'], params['working'], params['output'], basket['files'])

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