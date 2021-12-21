import mysql.connector
from mysql.connector.errors import Error,IntegrityError
import sqlparse
import re

from werkzeug.utils import format_string

global_pretify = False
global_echo_connection = False

class Client(object):
       
    def __init__(self,host='localhost',database='data_leaderboard', user='root',password='root'):
        self.connection = mysql.connector.connect(host=host,database=database,user=user,password=password)
        self.host = host
        self.database = database
        
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            if global_echo_connection :
                print("Connected to MySQL Server version ", db_Info)
            self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def pretify_sql(self,sql):
        print("\n--------------REQUEST----------------")
        print(sqlparse.format(sql, reindent=True, keyword_case='upper'))
        print("--------------------------------------\n")
        return

    def formatage_string(self,string:str)->str:
        string = string.replace("'",r"\'")
        string = "\'"+string+"\'"
        return string

    #TRUNCATE
    def TruncateAll(self,database_name:str):
        self.cursor.execute(f"""
                SELECT
                    Concat('TRUNCATE TABLE ', TABLE_NAME)
                FROM
                    INFORMATION_SCHEMA.TABLES
                WHERE
                    table_schema = '{database_name}';
                """)
        records = self.cursor.fetchall()
        records = [("SET FOREIGN_KEY_CHECKS=0;",)] + records + [("SET FOREIGN_KEY_CHECKS=1;",)]
        for request in records :
            self.cursor.execute(request[0])
        self.connection.commit()
        print(f"All tables from {database_name} have been truncated")

    def process_send(self,sql,pretify=global_pretify) :
        if pretify :
            self.pretify_sql(sql)
        self.cursor.execute(sql)
        self.connection.commit()
        #self.connection.close()
        return
    def process_get(self,sql,pretify=global_pretify) :
        if pretify :
            self.pretify_sql(sql)
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        #self.connection.close()
        return records
    
    #Ecriture SQL
    def fast_delete_on_pk(self,table:str,pk_name,pk):
        if type(pk) == str :
            pk = self.formatage_string(pk)
        sql = f"DELETE FROM {table} WHERE {pk_name} = {pk}"
        return sql
    def fast_insert(self,table:str,names:list[str],values:list) :
        colonnes = names.__str__()[1:-1]
        colonnes = [i for i in colonnes if i!="\'"]
        colonnes = "(" + "".join(colonnes) + ")"
        #Délétions des espaces en trop
        for i,v in enumerate(values) :
            if type(v) == str :
                values [i] = v.strip()
                
        values = "(" + values.__str__()[1:-1] + ")"
        sql = f"INSERT INTO {table} {colonnes} VALUES {values}"
        return sql
    
    def get_table(self,table:str,filter="*"):
        sql = f"SELECT {filter} FROM {table}"
        return self.process_get(sql)
    
    #Défis
    def createDéfis(self, name:str, coef:float, solo:bool)->None:
        sql = self.fast_insert('défis',['name','coef','solo'],[name,coef,solo])
        self.process_send(sql)
        return
    def deleteDéfis(self, name:str)->None:
        sql = self.fast_delete_on_pk('défis','name',name)
        self.process_send(sql)
        return
    
    #Teams
    def createTeam(self,name:str):
        sql = self.fast_insert('teams',['name'],[name])
        self.process_send(sql)
        return
    def deleteTeam(self,name:str):
        sql = self.fast_delete_on_pk('teams','name',name)
        self.process_send(sql)
        return
    
    #DéfiSolo
    def createDéfiSolo(self,id:int,défi_name:str,team_name:str,points:float):
        sql = self.fast_insert('défisolo',['id', 'défi_name', 'team_name','points'],[id, défi_name, team_name,points])
        self.process_send(sql)
        return
    def deleteDéfiSolo(self,id:int):
        sql = self.fast_delete_on_pk('défisolo','id',id)
        self.process_send(sql)
        return
    
    #DéfiVs
    def createDéfiVs(self,id:int,défi_name:str,team1_name:str,team2_name:str,victoire1:bool):
        sql = self.fast_insert('défivs',['id', 'défi_name', 'team1_name','team2_name','victoire1'],[id, défi_name, team1_name,team2_name,victoire1])
        print(sql)
        self.process_send(sql)
        return
    def deleteDéfiVs(self,id:int):
        sql = self.fast_delete_on_pk('défivs','id',id)
        self.process_send(sql)
        return


    #SERVICES
    def get_max_id(self,table:str):
        sql = f"SELECT MAX(id) FROM {table}"
        id_list = self.process_get(sql)
        try :
            if id_list[0][0] == None :
                return 0
            return id_list[0][0]
        except :
            raise Error(msg="Error while getting id_list max")
    
    def get_team_points(self,team_name:str):
        team_name = self.formatage_string(team_name)
        sql1 = fr"""
        SELECT SUM(ds.points*d.coef)
        FROM défisolo AS ds JOIN défis as d
        ON ds.défi_name =d.name
        WHERE ds.team_name={team_name}
        """
        sql2 = fr"""
        SELECT SUM(d.coef)
        FROM défivs AS dvs JOIN défis as d
        ON dvs.défi_name = d.name
        WHERE (dvs.team1_name={team_name} AND victoire1) OR
		(dvs.team2_name={team_name} AND NOT victoire1)
        """
        s1 = self.process_get(sql1)[0][0]
        s2 = self.process_get(sql2)[0][0]
        s1 = 0 if s1==None else s1
        s2 = 0 if s2==None else s2
        return s1+s2
    
    def get_all_teams_points(self):
        team_list = [i[0] for i in self.get_table('teams')]
        if len(team_list) == 1 and team_list[0][0] == None :
            return {}
        dict_point = {}
        
        for team in team_list :
            dict_point[team] = self.get_team_points(team)
        
        return sorted(dict_point.items(),key=lambda t:t[1],reverse=True)
        
    #WITH SUPPORT
    def __enter__(self):
        return self
       
    def __exit__(self,type,value,traceback) :
        if global_echo_connection :
            print("Connexion closed")
        self.close()     

if __name__ == "__main__" :
    with Client() as c :
        #prompt = input("Entrez y si vous souhaitez réinitialiser le contenu des tables")
        #if prompt == "y" or prompt == "Y" :
            #c.TruncateAll(c.database)
        #c.createDéfiSolo(1,'Sucage de bite','oui',10)
        #c.createDéfiSolo(2,'Sucage de bite','oui',12)
        #print(c.get_max_id('défisolo'))
        #print(c.get_table('teams','name'))
        print(c.get_all_teams_points())
        