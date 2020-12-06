import pytest
import dbutils
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

def test_get_connection():
    conn = dbutils.get_connection(_default_connect_info)
    assert conn is not None

def test_get_sql_from_file():
    path = "./schema.sql"
    result = dbutils.get_sql_from_file(path)
    assert len(result) == 8

def test_get_sql_from_Non_exist_file():
    path = "/src/schemas.sql"
    result = dbutils.get_sql_from_file(path)
    assert result is None

def test_run_multiple_sql_statements():
    path = "./schema.sql"
    result = dbutils.get_sql_from_file(path)
    res, data = dbutils.run_multiple_sql_statements(result, conn=_cnx, commit=True, fetch=True)
    assert res == 0
def test_run_multiple_sql_statements_no_conn():
    path = "schema.sql"
    result = dbutils.get_sql_from_file(path)
    with pytest.raises(ValueError) as excinfo:
        dbutils.run_multiple_sql_statements(result, conn=None, commit=True, fetch=True)
    assert "Connection cannot be None." == str(excinfo.value)

def test_run_multiple_sql_statements_no_statement():

    with pytest.raises(ValueError) as excinfo:
        dbutils.run_multiple_sql_statements(None, conn=_cnx, commit=True, fetch=True)
    assert "Sql statement list is empty" == str(excinfo.value)

def test_template_to_where_clause():
    template = {"address_id": "2", "uni": "wl2750"}
    actual = dbutils.template_to_where_clause(template)
    expected = (' WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
    assert actual == expected

def test_create_select():
    template = {"address_id": "2", "uni": "wl2750"}
    actual = dbutils.create_select("Addresses", template, is_select=True)
    expected = ('select  *  from Addresses  WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
    assert actual == expected

def test_create_select_w_field_list():
    template = {"address_id": "2", "uni": "wl2750"}
    fields = ["address_id", "state"]
    actual = dbutils.create_select("Addresses", template, fields=fields, is_select=True)
    expected = ('select  address_id,state  from Addresses  WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
    assert actual == expected


def test_create_delete():
    template = {"address_id": "2", "uni": "wl2750"}
    actual = dbutils.create_select("Addresses", template, is_select=False)
    expected = ('delete from Addresses  WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
    assert actual == expected

def test_create_update():
    template = {"uni": "wl2750"}
    changed_cols = {"email": "wl2750@columbia.edu"}
    actual = dbutils.create_update("User_info", template, changed_cols)
    expected = ('update User_info  set email=%s  WHERE  uni=%s ', ['wl2750@columbia.edu', 'wl2750'])
    assert actual == expected

