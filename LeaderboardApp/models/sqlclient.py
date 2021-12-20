import mysql.connector
import sqlparse

class Client(object):
       
    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                            database='data_leaderboard',
                                            user='root',
                                            password='root')
        self.cursor = self.connection.cursor()

    def createDéfis(self, name:str, coef:float, solo:bool)->None:
        sql = "INSERT INTO Défis(name, coef, solo) VALUES (?,?,?,?)"
        values = [name, coef, solo]
        self.cursor.execute(sql, values)
        self.connection.commit()
        self.connection.close()
        return

    def getQuestion(self, title):
        sql = "SELECT Description FROM Questions WHERE QuestionName = ?"
        values = [title]
        self.cursor.execute(sql, values)
        results = self.cursor.fetchone()
        question = results[0]
        self.connection.close()
        return question

    def getAnswer(self, title):
        try:
            sql = "SELECT CorrectAnswer FROM Questions WHERE QuestionName = ?"
            values = [title]
            self.cursor.execute(sql, values)
            results = self.cursor.fetchone()
            correctAnswer = results[0]
            self.connection.close()
            return correctAnswer
        except pypyodbc.Error as err:
            return err