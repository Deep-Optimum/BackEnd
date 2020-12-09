from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from utils import dbutils as dbutils
import logging
import os

# Gets or creates a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # set log level
# define file handler and set formatter
file_handler = logging.FileHandler('../logfile.log')
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) # add file handler to logger

# Makes print look better the RDBDataTable rows a little better.
pd.set_option('display.width', 256)
pd.set_option('display.max_columns', 12)


class data_tables():

    _default_connect_info = {
        'host': 'localhost',
        'user': 'root',
        'password': 'dbuser666',
        'db': 'sys',
        'port': 3306
    }

    #Use the following before commit - Travis does not use PW
    # _default_connect_info = {
    #     'host': 'localhost',
    #     'user': 'root',
    #     'password': '',
    #     'db': 'sys',
    #     'port': 3306
    # }
    _rows_to_print = 10
    Base = automap_base()

    def __init__(self, connect_info=None):

        # If there is not explicit connect information, use the default connection
        # You can use the default.
        if connect_info is None:
            self._connect_info = data_tables._default_connect_info

        cnx = pymysql.connect(
            host=self._connect_info['host'],
            user=self._connect_info['user'],
            password=self._connect_info['password'],
            db=self._connect_info['db'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

        if cnx is not None:
            self._cnx = cnx
        else:
            logger.error("Could not get a connection.")
            raise Exception("Could not get a connection.")

        #Create table
        path = "./resources/schema.sql"
        dbutils.run_multiple_sql_statements(dbutils.get_sql_from_file(path), conn=self._cnx)

        self._engine = create_engine('mysql+pymysql://{username}:'
                '{password}@{host}/{db_name}'.format(username=self._connect_info['user'],
                                                     password=self._connect_info['password'],
                                                     host=self._connect_info['host'],
                                                     db_name=self._connect_info['db']))

        #reflect the tables
        self.Base.prepare(self._engine, reflect=True)
        self._User_info = self.Base.classes.User_info
        self._Addresses = self.Base.classes.Addresses
        self._Listings = self.Base.classes.Listings
        self._Order_info = self.Base.classes.Order_info

        self._tables = [self._User_info, self._Addresses, self._Listings, self._Order_info]
        self._key_cols = None
        self.get_key_cols()

        #Create session
        self._Session = sessionmaker(bind=self._engine)

    def get_key_cols(self):
        """ Create a dictionary of key columns for each table.

        return:
              a dictionary object.
        """
        if self._key_cols:
            return self._key_cols

        self._key_cols = dict()
        for table in self._tables:
            keys_list = [str(primary_key).split(".")[1] for
                         primary_key in table.__table__.primary_key]
            self._key_cols[table.__table__.name] = keys_list

        return self._key_cols

    def create_session(self):
        """ Create a new session

        return:
              a new session object.
        """
        new_session = self._Session()
        return new_session

    def commit_and_close_session(self, cur_session):
        """ Commit and close a session.

        return:
              None
        """
        cur_session.commit()
        cur_session.close()

    def __str__(self):
        """ ToString method

        Print information of the data tables.

        return:
              a string representation of all tables.
        """
        result = "\n"
        result += "DataTables: "

        for table in self._tables:
            result += "\nTable name: {}".format( table.__table__.name)
            result += "\nDatabase name: {}".format(self._connect_info['db'])
            result += "\nTable type: {}".format(str(type(self)))
            result += "\nKey columns: {}".format(str(self._key_cols[table.__table__.name]))
            result += "\nNumber of rows: {} {}".format(str(self.get_row_count(table)), "row(s)")
            result += "\nA few sample rows: \n" + str(self.get_sample_rows(table)[0])
            result += "\n"

        return result

    def get_row_count(self, table):
        """ Get the number of rows in the table.

        return:
              Returns the count of the number of rows in the table if successful else None.
        """
        try:
            session = self.create_session()
            row_count = session.query(table).count()
            self.commit_and_close_session(session)
            return row_count

        except Exception as e:
            logger.error(e)
            return None

    def get_sample_rows(self, table, number_rows=_rows_to_print):
        """ Get some sample rows from the data table.

        Args:
            number_rows (int): Number of rows to include in a sample of the data.

        return:
            A Pandas dataframe containing the first number_rows number of rows
            if successful else None.
        """
        try:
            session = self.create_session()
            res = pd.read_sql(session.query(table).limit(number_rows).statement, self._engine)
            self.commit_and_close_session(session)
            return res, True

        except Exception as e:
            logger.error(e)
            return None, False

    def get_table_class(self, table_name):
        """ Get a table Class

        Args:
            table_name (str): The name of the table

        return:
            A SQLAlchemy table class
        """
        if table_name == "User_info":
            return self._User_info

        if table_name == "Addresses":
            return self._Addresses

        if table_name == "Listing":
            return self._Listings

        if table_name == "Order_info":
            return self._Order_info

    def get_info(self, table_name, template, get_similar=False, order_by=None, is_or=False):
        """ Query the User_info table

        Args:
            table_name (str): The name of the table
            template (dict): A dictionary of the form {"field1" : value1, "field2": value2, ...}
            get_similar (bool): query based on pattern
            order_by (list): a list of category
            is_or (bool): if true then OR is used in the query

        return:
            a tuple (res. boolean)
            If success, aPandas dataframe containing the query result (a list of dictionaries)
             and true. Otherwise None, false
        """
        if not table_name or table_name == "":
            logger.error("Table name cannot be null or empty.")
            return None, False

        try:
            session = self.create_session()
            if get_similar:
                stmt, args = dbutils.create_select(table_name=table_name, template=template,
                                                   is_like=True, order_by=order_by, is_or=is_or)
            else:
                stmt, args = dbutils.create_select(table_name=table_name, template=template,
                                                   order_by=order_by, is_or=is_or)
            res = pd.read_sql_query(stmt, self._engine, params=args)
            self.commit_and_close_session(session)
            return res, True
        except Exception as e:
            logger.error(e)
            return None, False

    def update_info(self, table_name, template, new_values):
        """ Query the User_info table

        Args:
            table_name: The name of the table
            template (dict): A dictionary of the form {"field1" : value1, "field2": value2, ...}
                            It defines which matching rows to update.
            new_values (dict): A dictionary containing fields and the values to set for the
                            corresponding fields in the records.
        return:
            True if successfully added uer info. False otherwise.
        """
        if not table_name or table_name == "":
            logger.error("Table name cannot be null or empty.")
            return False

        try:
            session = self.create_session()
            stmt, args = dbutils.create_update(table_name=table_name, template=template,
                                               changed_cols=new_values)

            # res = pd.read_sql_query(stmt, self._engine, params=args)
            # self.commit_and_close_session(session)
            cur = self._cnx.cursor()
            cur.execute(stmt, args)
            # res = pd.read_sql_query(stmt, con=self._cnx, params=args)
            self._cnx.commit()
            self.commit_and_close_session(session)
            return True
        except Exception as e:
            logger.error(e)
            return False


    def add_user_info(self, info):
        """ Add a new entry to the database

        Args:
            info (dict): A dictionary representation of the user to be added.

        return:
            True if successfully added uer info. False otherwise
        """
        new_user = self._User_info(uni=info["uni"],
                                   user_name=info["user_name"],
                                   first_name=info['first_name'],
                                   last_name=info['last_name'],
                                   email=info["email"],
                                   phone_number=info["phone_number"],
                                   credential=info["credential"])
        try:
            session = self.create_session()
            session.add(new_user)
            self.commit_and_close_session(session)
            return True
        except Exception as e:
            logger.error(e)
            return False


    def add_address(self, info):
        """ Add a new entry to the Addresses table.

        Args:
            info (dict): A dictionary representation of the information to be added.

        return:
            True if successfully added uer info. False otherwise.
        """
        new_address = self._Addresses(address_id=info["address_id"],
                                  uni=info["uni"],
                                  country=info["country"],
                                  state=info["state"],
                                  city=info["city"],
                                  address=info["address"],
                                  zipcode=info["zipcode"])

        try:
            session = self.create_session()
            session.add(new_address)
            self.commit_and_close_session(session)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def add_listing(self, info):
        """ Add a new entry to the Listings table.

        Args:
            info (dict): A dictionary representation of the information to be added.

        return:
            True if successfully added uer info. False otherwise.
        """
        new_listing = self._Listings(listing_id=info["listing_id"],
                                  isbn=info["isbn"],
                                  uni=info["uni"],
                                  title=info["title"],
                                  category=info["category"],
                                  price=info["price"],
                                  description=info["description"],
                                  image_url=info["image_url"],
                                  is_sold=info["is_sold"])
        try:
            session = self.create_session()
            session.add(new_listing)
            self.commit_and_close_session(session)
            return True
        except Exception as e:
            logger.error(e)
            return False


    def add_order_info(self, info):

        """ Add a new entry to the Order_info table.

        Args:
            info (dict): A dictionary representation of the information to be added.

        return:
            True if successfully added uer info. False otherwise.
        """
        new_order = self._Order_info(order_id=info["order_id"],
                                  buyer_uni=info["buyer_uni"],
                                  seller_uni=info["seller_uni"],
                                  listing_id=info["listing_id"],
                                  transaction_amt=info["transaction_amt"],
                                  status=info["status"],
                                  buyer_confirm=info["buyer_confirm"],
                                  seller_confirm=info["seller_confirm"])
        try:
            session = self.create_session()
            session.add(new_order)
            self.commit_and_close_session(session)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def delete_info(self, table_name, template):
        """ Delete an entry for a table

        Args:
            table_name: The name of the table
            template (dict): A dictionary of the form {"field1" : value1, "field2": value2, ...}
                            It defines which matching rows to update.

        return:
            True if successfully delete info. False otherwise.
        """
        if not table_name or table_name == "":
            logger.error("Table name cannot be null or empty.")
            return False
        try:
            session = self.create_session()
            stmt, args = dbutils.create_select(table_name=table_name, template=template, is_select=False)
            # res = pd.read_sql_query(stmt, self._engine, params=args)
            cur = self._cnx.cursor()
            cur.execute(stmt, args)
            self._cnx.commit()
            self.commit_and_close_session(session)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def import_from_csv(self, table_name, filepath):
        """ Import data from .csv file into table

        Args:
            table_name(str): Table name: May be fully qualified dbname.tablename or just tablename.
            filepath (str): A relative path to the dummy .csv file

        return:
            True if successfully imported. False if not.
        """
        if not table_name or table_name == "":
            logger.error("Table name cannot be null or empty.")
            return False

        if not os.path.isfile(filepath):
            logger.error("File does not exist.")
            return False

        read = pd.read_csv(filepath)

        if table_name == "User_info":
            for i, line in read.iterrows():
                info = line.to_dict()
                self.add_user_info(info)
            return True
        elif table_name == "Addresses":
            for i, line in read.iterrows():
                info = line.to_dict()
                self.add_address(info)
            return True
        elif table_name == "Listings":
            for i, line in read.iterrows():
                info = line.to_dict()
                self.add_listing(info)
            return True
        elif table_name == "Order_info":
            for i, line in read.iterrows():
                info = line.to_dict()
                self.add_order_info(info)
            return True
        else:
            logger.error("Table name not in database.")
            return False

    # def search_book_by_title(self, key_words=None):
    #     session, title_col = self.create_session(), self._tables[2].title
    #     if not key_words:
    #         self.commit_and_close_session(session)
    #         return session.query(self._tables[2]).all()
    #     res = session.query(self._tables[2]).filter(title_col.like(key_words[0]))
    #     for key_word in key_words:
    #         res = res.union(session.query(self._tables[2]).filter(title_col.like(key_word)))
    #     # res = res.order_by(self._tables[2].category).all()
    #     # print(res)
    #     res = pd.read_sql_query(res, self._engine)
    #     self.commit_and_close_session(session)
    #     return res
