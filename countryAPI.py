import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('Your-key-here.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'Your-url-here'
})

db = firestore.client()

def recordData(allCountryEnviData):
    dbRecordedCountries = db.collection(u'countries')
    recordedCountries = dbRecordedCountries.stream()
    recordedCountryIds = [country.id for country in recordedCountries]

    for countryId in list(allCountryEnviData.keys()):
        if countryId in recordedCountryIds:
            dbCountry = dbRecordedCountries.document(countryId)
            for dataCategory in allCountryEnviData[countryId]:
                [(countryKey, countryData)] = dataCategory.items()
                dbCountry.update({countryKey: countryData})
        else:
            dbCountry = dbRecordedCountries.document(countryId)
            for dataCategory in allCountryEnviData[countryId]:
                [(countryKey, countryData)] = dataCategory.items()
                dbCountry.set({countryKey: countryData})

def collectData(selectFiles):
    dbRecordedCountries = db.collection(u'countries')
    recordedCountries = dbRecordedCountries.stream()

    collectedData = {}
    for country in recordedCountries:
        collectedData[country.id] = country.to_dict()
    return collectedData


