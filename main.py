import countryAPI
from presentData import DataPresenter
from convertData import DataConverter

NewPresenter = DataPresenter()
NewConverter = DataConverter(maxBatchSize=None)

uploadData = input('Record Countries in Database? Examine Existing Data? Create and Test Experiment Data? \n(R/E/C)\n')

if uploadData == 'R':
    NewConverter.convertFiles()
    countryAPI.recordData(NewConverter.recordedCountries)
elif uploadData == 'E':
    NewPresenter.initParams(NewConverter.allFiles, unrecordedData=None)
elif uploadData == 'C':
    NewConverter.convertFiles()
    NewPresenter.initParams(NewConverter.allFiles, unrecordedData=NewConverter.recordedCountries)
else:
    print('Invalid. Re-run program with valid option.')