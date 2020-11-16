from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, text
import pymysql
import pandas as pd
import dbutils

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
            raise Exception("Could not get a connection.")

        self._engine = create_engine('mysql+pymysql://{username}:'
                               '{password}@{host}/{db_name}'.format(username=self._connect_info['user'],
                                                                    password=self._connect_info['password'],
                                                                    host=self._connect_info['host'],
                                                                    db_name=self._connect_info['db']))
        # reflect the tables
        self.Base.prepare(self._engine, reflect=True)
        self._User_info = self.Base.classes.User_info
        self._Addresses = self.Base.classes.Addresses
        self._Listings = self.Base.classes.Listings
        self._Order_info = self.Base.classes.Order_info
        self._tables = [self._User_info, self._Addresses, self._Listings, self._Order_info]

        #Create session
        self._Session = sessionmaker(bind=self._engine)

    def create_session(self):
        new_session = self._Session()
        return new_session

    def commit_and_close_session(self, cur_session):
        cur_session.commit()
        cur_session.close()

    def print_tables(self):
        """ ToString method

        Print information of the data tables.

            return:
                None
        """
        for table in self._tables:
            print("DataTable: ")
            print("Table name: " + table.__table__.name)
            print("Database name: " + self._connect_info['db'])
            print("Key columns: ", [str(primary_key).split(".")[1] for primary_key in table.__table__.primary_key])
            print("Number of rows: " + str(self.get_row_count(table)) + " row(s)")
            print("A few sample rows:")
            print(str(self.get_sample_rows(table)))
            print()

    def get_row_count(self, table):
        """ Get the number of rows in the table.

        return:
            Returns the count of the number of rows in the table.
        """
        session = self.create_session()
        row_count = session.query(table).count()
        self.commit_and_close_session(session)
        return row_count


    def get_sample_rows(self, table, number_rows=_rows_to_print):
        """ Get some sample rows from the data table.

        Args:
            number_rows (int): Number of rows to include in a sample of the data.

        return:
            A Pandas dataframe containing the first _row_to_print number of rows.
        """
        query = "select * from " + table.__table__.name + " limit " \
                                + str(number_rows)
        res = pd.read_sql(query, self._cnx)
        return res

    def get_info(self, table, template=None):
        """ Query the User_info table

        Args:
            table: A table class object
            template (dict): A dictionary of the form { "field1" : value1, "field2": value2, ...}

        return:
            None
        """
        # session = self.create_session()
        # sql, _ = dbutils.create_select(table_name=table.__table__.name,
        #                                template=template)
        # stmt = text(sql)

        #Ignore above
        query = "select * from " + table.__table__.name
        res = pd.read_sql(query, self._cnx)
        return res

    def get_table(self, table_name):

        if table_name == "user_info":
            return self._User_info

        elif table_name == "addresses":
            return self._Addresses

        elif table_name == "listing":
            return self._Listings

        elif table_name == "order_info":
            return self._Order_info()

    def update_info(self, table, user_info):
        pass



    def add_user_info(self, info):
        """ Add a new entry to the database

        Args:
            info (dict): A dictionary representation of the user to be added.
a
        return:
            None
        """
        # info = dbutils.parse_str_for_db(new_user_info, "user_info")
        new_user= self._User_info(uni=info["uni"],
                                  user_name=info["user_name"],
                                  email=info["email"],
                                  phone_number=info["phone_number"],
                                  credential=info["credential"])

        session = self.create_session()
        session.add(new_user)
        self.commit_and_close_session(session)
    def add_address(self, info):
        """ Add a new entry to the Addresses table.

        Args:
            info (dict): A dictionary representation of the information to be added.

        return:
            None
        """
        # info = dbutils.parse_str_for_db(new_address_info, "addresses")
        new_address= self._Addresses(address_id=info["address_id"],
                                  uni=info["uni"],
                                  country=info["country"],
                                  state=info["state"],
                                  city=info["city"],
                                  address=info["address"],
                                  zipcode=info["zipcode"])

        session = self.create_session()
        session.add(new_address)
        self.commit_and_close_session(session)

    def add_listing(self, info):
        """ Add a new entry to the Listings table.

        Args:
            info (dict): A dictionary representation of the information to be added.

        return:
            None
        """
        # info = dbutils.parse_str_for_db(new_listing_info, "listings")
        new_listing= self._Listings(listing_id=info["listing_id"],
                                  isbn=info["isbn"],
                                  uni=info["uni"],
                                  title=info["title"],
                                  category=info["category"],
                                  price=info["price"],
                                  description=info["description"],
                                  image_url=info["image_url"],
                                  is_sold=info["is_sold"])

        session = self.create_session()
        session.add(new_listing)
        self.commit_and_close_session(session)


    def add_order_info(self, info):

        """ Add a new entry to the Order_info table.

        Args:
            info (dict): A dictionary representation of the information to be added.

        return:
            None
        """
        # info = dbutils.parse_str_for_db(new_order_info, "listings")
        new_order = self._Order_info(order_id=info["order_id"],
                                  buyer_uni=info["buyer_uni"],
                                  seller_uni=info["seller_uni"],
                                  listing_id=info["listing_id"],
                                  transaction_amt=info["transaction_amt"],
                                  status=info["status"])

        session = self.create_session()
        session.add(new_order)
        self.commit_and_close_session(session)