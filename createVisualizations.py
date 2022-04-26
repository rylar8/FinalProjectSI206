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

            avgDataMLB.append((avgMLB, topMLB, total))

        except:
            avgDataMLB.append((0, (0,0), 0)) #COVID year

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
    plt.title('MLB v Premier League Average Attendance', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.xticks(ticks = year)
    plt.ylabel('Average Attendance', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.show()

def createTeamComparison():
    #Compare top teams attendance
    dataMLB = getMLBData()
    dataPremLg = getPremLgData()

    dataMLB = int([data[1][0] for data in dataMLB][-3].replace(',', ''))
    dataPremLg = [data[0][1] for data in dataPremLg][-2]

    labels = ['MLB', 'Premier League']

    plt.bar(labels, height= [dataMLB, dataPremLg])
    plt.xlabel('League')
    plt.ylabel('Average Attendance')
    plt.title("Top Team's Average Attendance: MLB v Premier League")
    plt.show()
    
def createPieGraph():
    #Compare top teams proportion of total attendance
    dataMLB = getMLBData()
    dataPremLg = getPremLgData()

    topTeamMLB = int([data[1][0] for data in dataMLB][-3].replace(',', ''))
    topTeamPremLg = [data[0][1] for data in dataPremLg][-2]

    totalMLB = [data[2] for data in dataMLB][-3]
    totalPremLg = [data[0][1] for data in dataPremLg][-2] * 20

    MLBlabels = 'Top Team', 'Rest of League'
    Premlabels = 'Top Team', 'Rest of League'

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('Proportion of Attendance by Top Team')

    ax1.pie([topTeamMLB, totalMLB], explode= (0.3, 0), labels= MLBlabels, autopct='%1.1f%%', shadow = True, textprops={'size': 'x-small'})
    ax1.set_xlabel('MLB')

    ax2.pie([topTeamPremLg, totalPremLg], explode= (0.3, 0), labels= Premlabels, autopct = '%1.1f%%', shadow = True, textprops={'size': 'x-small'})
    ax2.set_xlabel('Premier League')
    plt.show()

def main():
    createTeamComparison()
    createLineGraphs()
    createPieGraph()