from flask import jsonify, request, session, app, current_app, make_response, send_file, Response
import re
import pandas as pd

def yearConv(year):
    if year is not None and len(year) == 2:
        return '20' + year
    else:
        return year

def dfToDict(df, date):
    resDict = {}
    for index, row in df.iterrows():
        areaKey = row['Country/Region']
        if row['Province/State'] is not None and type(row['Province/State']) is str and len(str(row['Province/State']).strip()) > 0:
            areaKey += ' ' + str(row['Province/State'])
        
        if areaKey != None and len(areaKey) > 0:
            areaDict = {}
            areaDict['lat'] = row['Lat']
            areaDict['long'] = row['Long']

            for col in df.columns:
                if type(col) is str:
                    match = re.fullmatch("(\d*)\/(\d*)\/(\d*)", col)
                    if match is not None:
                        groups = match.groups()
                        year = yearConv(groups[2])
                        dateStr = year + '-' + groups[0] + '-' + groups[1]
                        if date == dateStr:
                            areaDict[dateStr] = row[col]

            resDict[areaKey] = areaDict

    return resDict

def setRoutes(app):
    @app.route('/corona/nz/YTExsed193847dkdIEDUCJkdslei394803/<date>', methods = ['GET'])
    def getCoronaData(date):
        try: 
            dataDir = app.config['SOURCE_DATA']
            confirmedDat = dataDir + '/time_series_19-covid-Confirmed.csv'
            deathDat = dataDir + '/time_series_19-covid-Deaths.csv'
            recoveredDat = dataDir + '/time_series_19-covid-Recovered.csv'

            confirmDf = pd.read_csv(confirmedDat)
            deathDf = pd.read_csv(deathDat)
            recoveredDf = pd.read_csv(recoveredDat)

            confirmDict = dfToDict(confirmDf, date)
            deathDict = dfToDict(deathDf, date)
            recoveredDict = dfToDict(recoveredDf, date)

            return jsonify({
                'confirmed': confirmDict,
                'deaths': deathDict,
                'recovered': recoveredDict,
            })
        except Exception as e:
            print(e)
            return jsonify({
                'Info': str(e) 
            }), 404


