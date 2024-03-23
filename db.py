import pyodbc as odbc

try:
    conn = odbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+servername+';DATABASE='+database+';UID='+username+';PWD='+password)
    print('connected successfully')
except Exception as e:
    print('veuillez revoir vos information de connection ',e)