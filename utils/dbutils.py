import pymysql
import logging
from collections import defaultdict
from os import path

logger = logging.getLogger()

def get_connection(connect_info):
    """
    :param connect_info: A dictionary containing the information necessary to make a PyMySQL connection.
    :return: The connection. May raise an Exception/Error.
    """
    cnx = pymysql.connect(**connect_info)
    return cnx

def get_sql_from_file(file_name=None):

    """Get the SQL instruction from a sql file

    Args:
        file_name (str): The path to the sql file

    return:
        statements (list): A list of sql statements to be executed.
    """
    # File does not exist
    if path.isfile(file_name) is False:
        print("File load error: {}".format(file_name))
        return None

    with open(file_name, "r") as sql_file:
        result = sql_file.read().split(';')
        result.pop() #Drop the last entry
        for idx, statement in enumerate(result):
            result[idx] = statement + ";"
        return result

def run_multiple_sql_statements(statements, fetch=True, cur=None, conn=None, commit=True):

    try:
        if conn is None:
            raise ValueError("Connection cannot be None.")

        if cur is None:
            cur = conn.cursor()

        if statements is None:
            raise ValueError("Sql statement list is empty")

        for idx, statement in enumerate(statements):
            logger.debug("Executing SQL = " + statement)
            res = cur.execute(statement)
        if fetch:
            data = cur.fetchall()
        else:
            data = None
        if commit == True:
            conn.commit()
    except Exception as e:
        raise(e)

    return (res, data)


def parse_str_for_db(string, table_name):

    # res = defaultdict(str)
    # if table_name == "user_info":
    #
    # elif table_name == "addresses":
    #
    # elif table_name == "listing":
    #
    # elif table_name == "order_info":
    #     pass
    pass

def template_to_where_clause(template):
    """ Converts a dictionary to a WHERE clause

    Args:
        template: One of those weird templates
    return
        result (string): WHERE clause corresponding to the template.
    """

    if template is None or template == {}:
        result = ("", None)
    else:
        args = []
        terms = []
        for k,v in template.items():
            terms.append(" " + k + "=%s ")
            args.append(v)
        w_clause = "AND".join(terms)
        w_clause = " WHERE " + w_clause
        result = (w_clause, args)

    return result


def create_select(table_name, template, fields=None, order_by=None, limit=None, offset=None, is_select=True):
    """ Produce a select statement: sql string and args.

    Args:
        table_name(str): Table name: May be fully qualified dbname.tablename or just tablename.
        template (dict): A dictionary of the form { "field1" : value1, "field2": value2, ...}
        fields (list): A list of request fields of the form, ['fielda', 'fieldb', ...]
        limit (int): Select a limited number of records.
        offset (int): Specifies the number of rows to skip before starting to return rows from the query.
        order_by (list): a list of column names used to sort the result-set
    return:
        A tuple of the form (sql string, args), where the sql string is a template.
    """
    if is_select:
        if fields is None:
            field_list = " * "
        else:
            field_list = " " + ",".join(fields) + " "
    else:
        field_list = None

    w_clause, args = template_to_where_clause(template)
    if is_select:
        sql = "select " + field_list + " from " +  table_name + " " + w_clause
    else:
        sql = "delete from " + table_name + " " + w_clause
    return (sql, args)