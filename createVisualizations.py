import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np


def openDatabase(db_name = 'AttendanceDatabase'):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def getMLBData():
    cur, conn = openDatabase()

    avgDataMLB = []
    year = 2012
    while year != 2022:
        cur.execute(
            """
            SELECT AttendanceMLB.avgAttendance, AttendanceMLB.totAttendance, MLBteams.teamName, AttendanceMLB.year
            FROM AttendanceMLB
            JOIN MLBteams ON MLBteams.team_id = AttendanceMLB.team_id
            """)
        dataMLB = cur.fetchall()
        dataMLB = [tup for tup in dataMLB if tup[3] == year]

        total = 0
        for team in dataMLB:
            total += int(team[0].replace(',', ''))
        avgMLB = total//30

        try:
            topMLB = sorted(dataMLB, key = lambda tup: tup[0])[-1]

            avgDataMLB.append((avgMLB, topMLB))

        except:
            avgDataMLB.append((0, 0)) #COVID year

        year += 1

    return avgDataMLB

def getPremLgData():
    cur, conn = openDatabase()

    avgDataPremLg = []
    year_id = 10
    while year_id != 0:
        cur.execute('SELECT avgHomeAttendance, topTeamsAttendance, year_id FROM AttendancePremierLg')
        dataPremLg = cur.fetchall()
        dataPremLg = [data for data in dataPremLg if data[2] == year_id]

        avgDataPremLg.append(dataPremLg)

        year_id -= 1

    return avgDataPremLg

def createLineGraphs():
    #Compare season by season based on average home attendance
    dataMLB = getMLBData()
    dataPremLg = getPremLgData()

    year = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
    dataMLB = [data[0] for data in dataMLB]
    dataPremLg = [data[0][0] for data in dataPremLg]

    plt.plot(year, dataMLB, color='red', marker='o', label = 'MLB')
    plt.plot(year, dataPremLg, color = 'blue', marker = 'o', label = 'Premier League')
    plt.title('MLB v Premier League Attendance', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.xticks(ticks = year)
    plt.ylabel('Attendance', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()

def createTeamComparison():
    #Compare top teams attendance
    dataMLB = getMLBData()
    dataPremLg = getPremLgData()

    dataMLB = [data[1] for data in dataMLB]
    dataPremLg = [data[0][1] for data in dataPremLg]

    plt.barh(dataMLB, dataPremLg)
    plt.xlabel('League')
    plt.ylabel('Attendance')
    plt.title('Top Teams Attendance')
    plt.tight_layout()
    plt.show()
    
    
def createPieGraph():
    #Compare top teams proportion of total attendance
    dataMLB = getMLBData()
    dataPremLg = getPremLgData()

def main():
    createTeamComparison()
    #createLineGraphs()
    #createPieGraph()

main()