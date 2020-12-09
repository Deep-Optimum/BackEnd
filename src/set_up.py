from utils import dbutils
import pymysql

_default_connect_info = {
    'host': 'localhost',
    'user': 'root',
    'password': 'dbuser666',
    'db': 'sys',
    'port': 3306
}
_cnx = pymysql.connect(
    host=_default_connect_info['host'],
    user=_default_connect_info['user'],
    password=_default_connect_info['password'],
    db=_default_connect_info['db'],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

path = "../resources/schema.sql"
sql = dbutils.get_sql_from_file(path)
dbutils.run_multiple_sql_statements(sql, conn=_cnx, commit=True, fetch=True)