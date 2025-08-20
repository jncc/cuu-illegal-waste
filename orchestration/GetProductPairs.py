import luigi
import os
import logging
import json

from luigi.util import requires
from orchestration.GetProducts import GetProducts

log = logging.getLogger('luigi-interface')

@requires(GetProducts)
class GetProductPairs(luigi.Task):
    stateLocation = luigi.Parameter()

    def getDatesFromName(self, productName):
        return productName[-54:-23] # gets the date part of the name, e.g. 20180728T181506_20180728T181533

    def run(self):
        products = []
        with self.input().open('r') as inputFile:
            products = json.load(inputFile)

        productNames = []
        for productPath in products['products']:
            filename = os.path.basename(productPath)
            productNames.append(filename)

        productNames.sort(key=lambda x: self.getDatesFromName(x))

        productPairs = []
        for i in range(len(productNames)-1):
            firstProduct = productNames[i]
            secondProduct = productNames[i+1]

            firstDate = firstProduct[17:32]
            secondDate = secondProduct[17:32]

            satelliteCode = firstProduct[0:3]

            name = f'{satelliteCode}_{firstDate}_{secondDate}'

            productPairs.append({
                'pairName': name,
                'products': [firstProduct, secondProduct]
            })

        with self.output().open('w') as outFile:
            outFile.write(json.dumps(productPairs, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'GetProductPairs.json'))