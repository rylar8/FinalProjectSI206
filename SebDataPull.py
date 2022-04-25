from decimal import Rounded
from tkinter import Y
import unittest
import sqlite3
import json
import os
from bs4 import BeautifulSoup
import requests
import re


# Name: Sebastian Roclore
# Who did you work with: Ryley Larson

def getAttendancePrem(year):
    baseURL = 'https://www.worldfootball.net/attendance/eng-premier-league-'
    endURL = '/1/'
    try:
        year = str(year)
        r = requests.get(baseURL + year + endURL)
        soup = BeautifulSoup(r.text, 'html.parser')
        box = soup.find('div', class_ = 'box')
        data = box.find_all('td', align = 'right', class_ = 'hell')
        data2 = box.find_all('td', align = 'right', class_ = 'dunkel')  
    except:
        print('Exception')

    i = 1
    data1List1 = []
    for datum in data:
        if i % 2 == 0:
            a = str(datum)
            data1List1.append(a)
        i += 1
    data1List2 = []
    for x in data1List1:
        data1List2.append(x[31:-5])
    n = 0
    for n in range(0, len(data1List1)):
        data1List2[n] = data1List2[n][:2] + data1List2[n][3:]
    # print(data1List2)

    i = 1
    data2List1 = []
    for datum2 in data2:
        if i % 2 == 0:
            a = str(datum2)
            data2List1.append(a)
        i += 1
    data2List2 = []
    for x in data2List1:
        data2List2.append(x[33:-5])
    n = 0
    for n in range(0, len(data2List2)):
        p = data2List2[n].split('.') 
        a = ''.join(p)
        data2List2[n] = a
    # print(data2List2)

    info = []
    item = 0
    # sorted List of all avg Attendance
    for item in range(0, len(data1List2)):
        info.append(int(data1List2[item]))
        info.append(int(data2List2[item]))
    info = sorted(info, reverse= True)

    # overall yearly avg Attendance
    # number = 0
    # for item in range(0, len(data1List2)):
    #     number += int(data1List1[item])
    #     number += int(data1List2[item])
    # tot = number / (len(data1List1) + len(data1List2))
    # tot = round(tot, 2)
    # print(tot)
    return info

def one_year_less(year):
    a = year.split('-')
    a[0] = int(a[0])
    a[0] -= 1
    a[0] = str(a[0])
    a[1] = int(a[1])
    a[1] -= 1
    a[1] = str(a[1])
    b = '-'.join(a)
    return b


def ten_years(recent_year):
    d = {}
    year = recent_year
    while len(d.keys()) < 10:
        d[year] = getAttendancePrem(year)
        year = one_year_less(year)
    return d

def avgHomeAttendance(dict):
    d = {}
    for x,y in dict.items():
        sum = 0
        for attendance in y:
            sum += attendance
        avg = sum / 20
        avg = round(avg, 1)
        d[x] = avg
    return d

def topTeamsAttendance(year, dict):
    for x,y in dict.items():
        if x == year:
            return y[0]
        continue

def avgHomeAttendancebyYear(year, dict):
    for x,y in dict.items():
        sum = 0
        for attendance in y:
            sum += attendance
        avg = sum / 20
        avg = round(avg, 1)
        if x== year:
            return avg
    return avg   
    

def createDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS AttendancePremierLg (year_id INTEGER PRIMARY KEY, season TEXT, avgHomeAttendance INTEGER, topTeamsAttendance INTEGER)')
    conn.commit()
    return cur, conn

# def delete(db_name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path+'/'+db_name)
#     cur = conn.cursor()
    
#     cur.execute('DROP TABLE IF EXISTS AttendancePremierLg')
#     conn.commit()
#     return cur, conn

def addData(year, db_name):
    cur, conn = createDatabase(db_name)
    data = ten_years(year)
    i = 1
    while i < 11:
        if i == 1:
            y = year
        else:
            y = one_year_less(y)
        att = avgHomeAttendancebyYear(y, data)
        top = topTeamsAttendance(y, data)
        cur.execute('INSERT INTO AttendancePremierLg (year_id, season, avgHomeAttendance, topTeamsAttendance) VALUES (?, ?, ?, ?)', (i, y, att, top))
        i += 1
        conn.commit()
    return


# def get_teams_by_season(season):
#     url = "https://football-web-pages1.p.rapidapi.com/league-table.json"

#     querystring = {"comp":"1", "year":{season}}

#     headers = { 
# 	    "X-RapidAPI-Host": "football-web-pages1.p.rapidapi.com",
# 	    "X-RapidAPI-Key": "e34cfc2358mshb0d0a32b739f2e0p1fa103jsnf9f3985beab7"
#     }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     year_table = json.loads(response.text)
#     L = []
#     for x,y in year_table.items():
#         for teams in y.items():
#             t = teams[1]
#             for team in t:
#                 try:
#                     val = team['name']
#                     L.append(val)
#                 except:
#                     break   
#     return L

# def get_team_ids():
#     L = [] 



# def prem_data_grab(season):
#     # L = get_teams_by_season(season)

#     url = "https://football-web-pages1.p.rapidapi.com/attendances.json"

#     headers = {
#         "X-RapidAPI-Host": "football-web-pages1.p.rapidapi.com",
#         "X-RapidAPI-Key": "e34cfc2358mshb0d0a32b739f2e0p1fa103jsnf9f3985beab7"
#     }

#     data_dict = {}
    
#     for i in range(1, 21):
#         querystring = {"comp":"1","team":{i},"sort":"average","type":"home"}
#         response = requests.request("GET", url, headers=headers, params=querystring)
#         json_data = json.loads(response.text)
#         for x,y in json_data["attendances"].items():
#             if x == 'team':
#                 # if y['name'] in L:
#                     team = y['name']
#                     data_dict[team] = []
#             elif x == 'matches':
#                 for match in y:
#                     if match["attendance"] != 0:
#                         data_dict[team].append(match["attendance"])
#     for x,y in data_dict.items():
#         sum = 0
#         tot = 0
#         for num in y:
#             sum += num
#             tot += 1
#         avg = sum / tot
#         avg = round(avg, 1)
#         data_dict[x] 
    
#     print(data_dict)
#     print(len(data_dict))
#     return data_dict



# class TestAllMethods(unittest.TestCase):
#     def test_data_grab():
#         data_grab()
#         return




def main():
    # prem_data_grab("2021-2022")
    # print(get_teams_by_season("2013-2014"))
    # print(getAttendancePrem("2021-2022"))
    # print(one_year_less("2021-2022"))
    # print(ten_years("2020-2021"))
    addData("2020-2021", "AttendanceDatabase")
    # print(avgHomeAttendancebyYear('2020-2021', ten_years('2020-2021'))) 
    # delete("AttendanceDatabase")
    return 1



if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
