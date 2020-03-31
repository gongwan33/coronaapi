from flask import jsonify, request, session, app, current_app, make_response, send_file, Response
import re
import pandas as pd
import math

"""
    :param lon: longitude 
    :param lat: latitude
    :param W: image width
    :param H: image height
"""
def millerToXY (lon, lat, W, H):
    xy_coordinate = []
    mill = 2.3   # a constant of Miller cast
    x = lon*math.pi/180  
    y = lat*math.pi/180
    y = 1.25*math.log(math.tan(0.25*math.pi+0.4*y))
    x = (W/2)+(W/(2*math.pi))*x 
    y = (H/2)-(H/(2*mill))*y 
    xy_coordinate.append((x,y))
    return xy_coordinate

def yearConv(year):
    if year is not None and len(year) == 2:
        return '20' + year
    else:
        return year

def colToDateStr(col):
    match = re.fullmatch("(\d*)\/(\d*)\/(\d*)", col)
    if match is not None:
        groups = match.groups()
        year = yearConv(groups[2])
        dateStr = year + '-' + groups[0] + '-' + groups[1]
        return dateStr
    else:
        return None


def dfToDict(df, date):
    resDict = []
    for index, row in df.iterrows():
        areaKey = row['Country/Region']
        if row['Province/State'] is not None and type(row['Province/State']) is str and len(str(row['Province/State']).strip()) > 0:
            areaKey += ' ' + str(row['Province/State'])
        
        if areaKey != None and len(areaKey) > 0:
            areaDict = {}
            areaDict['name'] = areaKey
            areaDict['lat'] = row['Lat']
            areaDict['lng'] = row['Long']

            dateData = {
                    'date': '1900-01-01',
                    'number': '-1',
            }

            if date == 'latest':
                lastCol = df.columns[-1]
                dateStr = colToDateStr(lastCol) 
                if dateStr is not None:
                    dateData['date'] = dateStr
                    dateData['number'] = row[lastCol]
            else: 
                for col in df.columns:
                    if type(col) is str:
                        dateStr = colToDateStr(col)
                        if dateStr is not None:
                            if date == dateStr:
                                dateData['date'] = dateStr
                                dateData['number'] = row[col]

            areaDict['data']= dateData
            resDict.append(areaDict)

    return resDict

def getDateList(df):
    dateList = []
    for col in df.columns:
        date = colToDateStr(col)
        if date is not None:
            dateList.append(date);

    return dateList;

def setRoutes(app):
    @app.route('/corona/nz/YTExsed193847dkdIEDUCJkdslei394803/<date>', methods = ['GET'])
    def getCoronaData(date):
        try: 
            dataDir = app.config['SOURCE_DATA']
            confirmedDat = dataDir + '/time_series_covid19_confirmed_global.csv'
            deathDat = dataDir + '/time_series_covid19_deaths_global.csv'
            recoveredDat = dataDir + '/time_series_covid19_recovered_global.csv'

            confirmDf = pd.read_csv(confirmedDat)
            deathDf = pd.read_csv(deathDat)
            recoveredDf = pd.read_csv(recoveredDat)

            confirmDict = dfToDict(confirmDf, date)
            deathDict = dfToDict(deathDf, date)
            recoveredDict = dfToDict(recoveredDf, date)

            return jsonify({
                'confirmedDateList': getDateList(confirmDf),
                'confirmed': confirmDict,
                'deathsDateList': getDateList(deathDf),
                'deaths': deathDict,
                'recoveredDateList': getDateList(recoveredDf),
                'recovered': recoveredDict,
            })
        except Exception as e:
            print(e)
            return jsonify({
                'Info': str(e) 
            }), 404


