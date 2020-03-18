from random import randint
import matplotlib.pyplot as plt
import csv, os, countryAPI
import numpy as np

class DataPresenter:
    def __init__(self):
        return

    def initParams(self, allFiles, unrecordedData):
        self.allFiles = allFiles
        self.collectSelectFiles()
        
        try:
            self.minYear = int(input('Earliest year to survey? \n(Blank for default)\n'))
        except:
            self.minYear = 1980
        try:
            self.maxYear = int(input('Max year to survey? \n(Blank for default)\n'))
        except:
            self.maxYear = 2020

        collectData = input('Test Data or Start Over? \n(T/s)\n')
        if collectData == 'T':
            self.dataOrganize(unrecordedData)
        else:
            self.initParams(self.allFiles, unrecordedData)

    def collectSelectFiles(self):
        self.selectFiles = []
        newIndex = ''
        while newIndex != 'E':
            newIndex = input('Select from this array? \n (Indices 0 to %s, click "E" to exit) %s \n' % (len(self.allFiles)-1, self.allFiles))
            try:
                if self.allFiles[int(newIndex)] not in self.selectFiles:
                    self.selectFiles.append(self.allFiles[int(newIndex)])
                if len(self.selectFiles) == len(self.allFiles):
                    break
            except:
                if newIndex == 'E':
                    print('Confirmed.')
                    break
                else:
                    print('Not acceptable input.')
                    continue
        print('Your files: %s' % self.selectFiles)
        return self.selectFiles
    
    def dataOrganize(self, unrecordedData):
        if unrecordedData == None:
            self.allData = countryAPI.collectData(self.selectFiles)
        else:
            self.allData = unrecordedData
        observeSpecs = ''
        dataToObserve = []
        while observeSpecs != 'E':
            observeSpecs = input('What data would you like to observe, from %s? \n(Indices 0 to %s, click "E" to exit)\n' % (self.selectFiles, len(self.selectFiles)-1))
            try:
                observeSpecData = self.selectFiles[int(observeSpecs)]
                dataToObserve.append(observeSpecData[:-4])
                if len(dataToObserve) == len(self.selectFiles):
                    break
            except:
                print('Error. Try another value.')
        self.siftData(dataToObserve)
    
    def siftData(self, dataToObserve):
        self.graphData = {}
        allCountryIds = []
        countrySelect = input('Select Specific Countries? \n(Y/n)\n')
        if countrySelect == 'Y':
            newCountryAdd = ''
            while newCountryAdd != 'E':
                newCountryAdd = input('Enter country. \n(Click "E" to exit)\n')
                if newCountryAdd in list(self.allData.keys()):
                    allCountryIds.append(newCountryAdd)
                elif newCountryAdd == 'E':
                    break
                else:
                    print('Invalid request. Try Again.')
        else:
            allCountryIds = list(self.allData.keys())
        for countryId in allCountryIds:
            countryData = self.allData[countryId]
            self.graphData[countryId] = []
            for data in dataToObserve:
                specCountryData = countryData[data].items()
                specCountryData = [dataItem for dataItem in specCountryData if int(dataItem[0]) >= int(self.minYear) and int(dataItem[0]) <= int(self.maxYear)]
                specCountryData = sorted(specCountryData, key=lambda dataItem: dataItem[0])
                self.graphData[countryId].append(specCountryData)
            self.plotData(dataToObserve)
    
    def plotData(self, dataToObserve):
        fig, ax = plt.subplots(1, 1)
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))

        colorDict = dict([[countryId, (randint(0, 1), randint(0, 1), randint(0, 1))] for countryId in list(self.graphData.keys())])

        for countryId in list(self.graphData.keys()):
            countryData = self.graphData[countryId]
            for specCountryData in countryData:
                allYears = [yearData[0] for yearData in specCountryData]
                allData = [yearData[1] for yearData in specCountryData]
                plt.plot(allYears, allData, color=colorDict[countryId])
            #ax.legend(countryId)
        dataToObserve = str(dataToObserve).replace("[", "").replace("]", "").replace("'", "")
        plt.xlabel('Years from %s to %s' % (self.minYear, self.maxYear)) 
        plt.ylabel('Readings of %s among selected countries' % dataToObserve) 
        plt.show()