"""
Testing dbutilis.py
"""
import pytest
import pymysql
import dbutils #pylint: disable=import-error

#Use this before commit
_default_connect_info = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'sys',
    'port': 3306
}

# _default_connect_info = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'dbuser666',
#     'db': 'sys',
#     'port': 3306
# }

#pylint: disable=missing-function-docstring
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
    path = "./resources/schema.sql"
    result = dbutils.get_sql_from_file(path)
    assert len(result) == 12

def test_get_sql_from_non_exist_file():
    path = "/src/schemas.sql"
    result = dbutils.get_sql_from_file(path)
    assert result is None

def test_run_multiple_sql_statements():
    path = "./resources/schema.sql"
    result = dbutils.get_sql_from_file(path)
    res, _ = dbutils.run_multiple_sql_statements(result, conn=_cnx, commit=True, fetch=True)
    assert res == 0

def test_run_multiple_sql_statements_no_conn():
    path = "../resources/schema.sql"
    result = dbutils.get_sql_from_file(path)
    with pytest.raises(ValueError) as excinfo:
        dbutils.run_multiple_sql_statements(result, conn=None, commit=True, fetch=True)
    assert str(excinfo.value) == "Connection cannot be None."

def test_run_multiple_sql_statements_no_statement():

    with pytest.raises(ValueError) as excinfo:
        dbutils.run_multiple_sql_statements(None, conn=_cnx, commit=True, fetch=True)
    assert str(excinfo.value) == "Sql statement list is empty"

def test_template_to_where_clause():
    template = {"address_id": "2", "uni": "wl2750"}
    actual = dbutils.template_to_where_clause(template)
    expected = (' WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
    assert actual == expected

def test_template_to_where_clause_no_template():
    template = {}
    actual = dbutils.template_to_where_clause(template)
    expected = ("", None)
    assert actual == expected
    actual = dbutils.template_to_where_clause(None)
    expected = ("", None)
    assert actual == expected

def test_template_to_where_clause_1key_n_vals():
    template = {"title": ["%computer%vision%", "%vision%", "%computer%"]}
    actual = dbutils.template_to_where_clause(template, is_like=True, is_or=True)
    expected = (' WHERE  title LIKE %s OR title LIKE %s OR title LIKE %s ',
                ["%computer%vision%", "%vision%", "%computer%"])
    assert actual == expected

    actual = dbutils.template_to_where_clause(template, is_like=True)
    expected = (' WHERE  title LIKE %s AND title LIKE %s AND title LIKE %s ',
                ["%computer%vision%", "%vision%", "%computer%"])
    assert actual == expected

def test_template_to_where_clause_nkeys_n_vals():
    template = {"title": ["%computer%vision%", "%vision%", "%computer%"],
                "isbn": ["%12%", "%34%"]}
    actual = dbutils.template_to_where_clause(template, is_like=True, is_or=True)
    expected = (' WHERE  title LIKE %s OR title LIKE %s OR title LIKE %s '
                'OR isbn LIKE %s OR isbn LIKE %s ',
                ["%computer%vision%", "%vision%", "%computer%", "%12%", "%34%"])
    assert actual == expected

    actual = dbutils.template_to_where_clause(template, is_like=True)
    expected = (' WHERE  title LIKE %s AND title LIKE %s AND title LIKE %s '
                'AND isbn LIKE %s AND isbn LIKE %s ',
                ["%computer%vision%", "%vision%", "%computer%", "%12%", "%34%"])
    assert actual == expected

    template = {"title": ["%computer%vision%", "%vision%", "%computer%"], "isbn": "%34%"}
    actual = dbutils.template_to_where_clause(template, is_like=True)
    expected = (' WHERE  title LIKE %s AND title LIKE %s AND title LIKE %s AND isbn LIKE %s ',
                ["%computer%vision%", "%vision%", "%computer%", "%34%"])
    assert actual == expected

def test_template_to_where_clause_is_like():
    template = {"uni": "%2%"}
    actual = dbutils.template_to_where_clause(template, is_like=True)
    expected = (' WHERE  uni LIKE %s ', ['%2%'])
    assert actual == expected

def test_create_select():
    template = {"address_id": "2", "uni": "wl2750"}
    actual = dbutils.create_select("Addresses", template, is_select=True)
    expected = ('select  *  from Addresses  WHERE  address_id=%s AND uni=%s ', ['2', 'wl2750'])
    assert actual == expected

def test_create_select_single():
    template = {"address_id": "2"}
    actual = dbutils.create_select("Addresses", template, is_select=True)
    expected = ('select  *  from Addresses  WHERE  address_id=%s ', ['2'])
    assert actual == expected

def test_create_select_w_field_list():
    template = {"address_id": "2", "uni": "wl2750"}
    fields = ["address_id", "state"]
    actual = dbutils.create_select("Addresses", template, fields=fields, is_select=True)
    expected = ('select  address_id,state  from Addresses  WHERE  '
                'address_id=%s AND uni=%s ', ['2', 'wl2750'])
    assert actual == expected

def test_create_select_w_field_list_single():
    template = {"address_id": "2"}
    fields = ["address_id", "state"]
    actual = dbutils.create_select("Addresses", template, fields=fields, is_select=True)
    expected = ('select  address_id,state  from Addresses  WHERE  address_id=%s ', ['2'])
    assert actual == expected

def test_create_select_is_like_order_by():
    template = {"title": ["%computer%vision%", "%vision%", "%computer%"]}
    actual = dbutils.create_select("Listings", template, order_by=['category'],
                                   is_select=True, is_like=True, is_or=True)
    expected = ('select  *  from Listings  WHERE  title LIKE %s OR title LIKE %s OR title '
                'LIKE %s order by category', ['%computer%vision%', '%vision%', '%computer%'])
    assert actual == expected

def test_create_select_is_like_limit_by():
    template = {"title": ["%computer%vision%", "%vision%", "%computer%"]}
    actual = dbutils.create_select("Listings", template, order_by=['category'],
                                   limit=10, is_select=True, is_like=True)
    expected = ('select  *  from Listings  WHERE  title LIKE %s AND title LIKE %s AND title '
                'LIKE %s order by category limit 10',['%computer%vision%',
                                                      '%vision%', '%computer%'])
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

def test_create_select_with_like():
    template = {"uni": "%2%", "email": '%columbia%'}
    actual = dbutils.create_select("User_info", template, is_select=True, is_like=True)
    expected = ('select  *  from User_info  WHERE  uni LIKE %s AND email LIKE %s ',
                ['%2%', '%columbia%'])
    assert actual == expected

def test_create_select_with_like_single_field():
    template = {"uni": "%2%"}
    actual = dbutils.create_select("User_info", template, is_select=True, is_like=True)
    expected = ('select  *  from User_info  WHERE  uni LIKE %s ', ['%2%'])
    assert actual == expected

def test_create_select_with_like_three_fields():
    template = {"uni": "%2%", "email": '%columbia%', "credential": "k" }
    actual = dbutils.create_select("User_info", template, is_select=True, is_like=True)
    expected = ('select  *  from User_info  WHERE  uni LIKE %s AND email LIKE %s AND '
                'credential LIKE %s ', ['%2%', '%columbia%', 'k'])
    assert actual == expected
