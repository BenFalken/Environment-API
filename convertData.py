import csv, os

class DataConverter:
    def __init__(self, maxBatchSize):
        self.maxBatchSize = maxBatchSize
        self.allFiles = os.listdir("Data")
        self.recordedCountries = {}

    def convertFiles(self):
        absPath = 'Your-project-pathway'
        totalBatches = 0
        for sheet in self.allFiles:
            with open(absPath+sheet, mode='r') as file:
                reader = csv.reader(file)
                rowsCounted = 0
                for row in reader:
                    if rowsCounted == 4:
                        dateKeys = row
                    if rowsCounted < 5:
                        rowsCounted = rowsCounted + 1
                        continue
                    try:
                        countryKey = row[0]
                        if countryKey in list(self.recordedCountries.keys()):
                            countryData = self.recordedCountries[countryKey]
                        else:
                            countryData = {}
                            self.recordedCountries[countryKey] = countryData
                        specificSheetData = {}
                        for col in range(4, len(row)-1):
                            try:
                                specificSheetData[str(dateKeys[col])] = float(row[col])
                            except:
                                continue
                        countryData[str(sheet[:-4])] = specificSheetData
                        self.recordedCountries[countryKey] = countryData
                        rowsCounted = rowsCounted + 1
                    except:
                        continue
            totalBatches = totalBatches + 1
            if totalBatches == self.maxBatchSize:
                break
        return self.recordedCountries
