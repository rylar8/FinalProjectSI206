import sqlite3
import os
import matplotlib.pyplot as plt


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
            '''
            SELECT AttendanceMLB.avgAttendance, AttendanceMLB.totAttendance, MLBteams.teamName
            FROM AttendanceMLB WHERE year = ?
            JOIN MLBteams ON MLBteams.team_id = AttendanceMLB.team_id
            ''', (year,))
        dataMLB = cur.fetchall()

        total = 0
        for team in dataMLB:
            total += team[0]
        avgMLB = total//30
        avgDataMLB.append(avgMLB)

    return avgDataMLB

def getPremLgData():
    cur, conn = openDatabase()

    avgDataPremLG = []

def createLineGraphs():
    #Compare season by season based on average home attendance

def createTeamComparison():
    #Compare top teams attendance

def createPieGraph():
    #Compare top teams proportion of total attendance

def main():
    createTeamComparison()
    createLineGraphs()
    createPieGraph()

#main()