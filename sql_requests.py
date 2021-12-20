import mysql.connector
from mysql.connector import Error
import sqlparse

#Initialize Database
def init_random():
    liste_data=[["1","Lancer de lances",0.1,True],
                ["2","Saut en longueur",0.5,True],
                ["3","Saut en hauteur",1.0,True],
                ["4","Lancer de poids",0.3,True],
                ["5","Volley",10,False],
                ["6","Basketball",10,False],
                ["7","Football",10,False]
                ]
    for values in liste_data :
        request = createCustomInsert("défis",["id","name","coef","solo"],values_list=values)
        sendCustomRequest(request)

#Request sender
def getCustomRequest(sql_request:str,pretify=False):
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='data_leaderboard',
                                            user='root',
                                            password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            if pretify :
                print("\n#########SENDING REQUEST#############")
                print(sqlparse.format(sql_request, reindent=True, keyword_case='upper'))
                print("######################################\n")
            cursor.execute(sql_request)
            records = cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return records
        
def sendCustomRequest(sql_request:str,pretify=False):
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='data_leaderboard',
                                            user='root',
                                            password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            if pretify :
                print("\n#########INSERTING RECORD#############")
                print(sqlparse.format(sql_request, reindent=True, keyword_case='upper'))
                print("######################################\n")
            cursor.execute(sql_request)
            connection.commit()
            print(cursor.rowcount, "record inserted.")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def deleteCustomRequest(sql_request:str,pretify=False):
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='data_leaderboard',
                                            user='root',
                                            password='root')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            if pretify :
                print("#########DELETING RECORDS#############")
                print(sqlparse.format(sql_request, reindent=True, keyword_case='upper'))
                print("######################################")
            cursor.execute(sql_request)
            connection.commit()
            print("deleted.")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#Request creator
def createCustomRequest(select:str="*", table:str="défis", where:str=None)->str:
    q = f"""SELECT {select} FROM {table}"""
    if where != None :
        q = q + f""" WHERE {where}"""
    return q

def createCustomInsert(table:str="défis",column_list:list[str]=[],values_list:list=[]):
    #Formatage colonnes
    colonnes = column_list.__str__()[1:-1]
    colonnes = [i for i in colonnes if i!="\'"]
    colonnes = "(" + "".join(colonnes) + ")"
    values = "(" + values_list.__str__()[1:-1] + ")"
    
    return f"""INSERT INTO {table}""" + colonnes + f"""VALUES {values}"""

def createCustomDelete(table:str="défis",where:str="id = 1") :
    q = f"""DELETE FROM {table} WHERE {where}"""
    return q
    

if __name__ == "__main__":

    # print(getCustomRequest("""SELECT * from défis""",pretify=True))
    # i = createCustomInsert("défis",["id","name","coef","solo"],["1","Lancer de lances",0.3,True])
    # sendCustomRequest(i,pretify=True)
    # deleteCustomRequest(createCustomDelete(),pretify=True)
    pass