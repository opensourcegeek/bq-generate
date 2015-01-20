import argparse
import logging

import MySQLdb

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


QUERY = """
  select
    column_name,
    column_type
  from
    information_schema.columns
  where
    table_schema='{}'
    and table_name='{}'
"""

TYPE_MAPPING = {
  "int"    : "INTEGER",
  "char"   : "STRING",
  "decimal": "FLOAT",
  "float"  : "FLOAT",
  "double" : "FLOAT"
}


def generate_types(args):
    LOGGER.debug(args)
    all_columns_with_types = lookup_columns_with_types_from_table(args)
    all_columns_with_bigquery_types = []; aadd = all_columns_with_bigquery_types.append
    for column_name_with_type in all_columns_with_types:
        column_name, column_type = column_name_with_type
        LOGGER.debug(column_name + " - " + column_type)
        bigquery_type = map_mysql_type_to_bigquery_type(column_type)
        LOGGER.debug(column_name + " - " + column_type + " ----> " + map_mysql_type_to_bigquery_type(column_type))
        aadd(column_name + ":" + bigquery_type)
    print "Following is the schema "
    print ""
    print ",".join(all_columns_with_bigquery_types)


def map_mysql_type_to_bigquery_type(sql_type_name):
    for mapped_type_name, bigquery_type_name in TYPE_MAPPING.items():
        if mapped_type_name in sql_type_name:
            return bigquery_type_name


def lookup_columns_with_types_from_table(args):
    res = _run_query(args)
    LOGGER.debug(res)
    return res


def _run_query(args):
    password = _get_password_from_file(args.password_from_file)
    conn = None
    cursor = None
    try:
        conn = MySQLdb.connect(host=args.host, user=args.user, passwd=password)
        cursor = conn.cursor()
        cursor.execute(QUERY.format(args.database, args.table))
        return cursor.fetchall()

    except Exception, e:
        LOGGER.exception(e)

    finally:
        if conn is not None:
            conn.close()

        if cursor is not None:
            cursor.close()



def _get_password_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def clean_input_parameters(args):
    errors_found = False

    if args.host is None or args.host == '':
        LOGGER.info("Using localhost as host name to connect to")

    if args.database is None or args.database == '':
        LOGGER.error("Need database name")
        errors_found = True

    if args.user is None or args.user == '':
        LOGGER.error("Need user name")
        errors_found = True

    if args.password_from_file is None or args.password_from_file == '':
        LOGGER.error("Need password file name")
        errors_found = True

    if args.table is None or args.table == '':
        LOGGER.error("Need table name")
        errors_found = True

    if errors_found:
        LOGGER.error("Please use --help option to check input parameters")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", help="The name of database to use")
    parser.add_argument("--host", help="The host to connect to, it can be IP address or Domain name")
    parser.add_argument("--table", help="The name of table to lookup columns")
    parser.add_argument("--user", help="User name to connect to database")
    parser.add_argument("--password-from-file", help="Clear text password will be loaded from this file")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    clean_input_parameters(args)
    generate_types(args)
