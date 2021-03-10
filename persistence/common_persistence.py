import sys
from sqlite3 import OperationalError, IntegrityError
from traceback import print_exc
from typing import List

from persistence.connection_handler import connection


def get_dictionary_from_table(table_name: str, unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = "SELECT * FROM %s WHERE unique_id = ?" % table_name
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return result


def insert_dictionary(table_name: str, my_dict: dict):
    cursor_obj = connection.cursor()
    placeholders = ", ".join(["?"] * len(my_dict))
    columns = ", ".join(my_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)
    try:
        cursor_obj.execute(sql, list(my_dict.values()))
    except OperationalError:
        print_exc()
        print("Encountered error: {0}".format(sys.exc_info()[1]))
        raise
    except IntegrityError:
        print("Integrity error: {0}".format(sys.exc_info()[1]))
        print("Tried to insert {} into table {}".format(my_dict, table_name))


def convert_dict_keys_to_id(
    elem_list: List,
    convert_dict: dict,
    replace_values: bool = False,
    name_prop="name",
    id_prop="unique_id",
):
    """
    Takes a dictionary and replaces the dictionary keys with ids.
    This process is based on id-name association provided in the list_with_names property

    :param elem_list: Each element of the list will be searched to replace the key values of the convert dictionary.
    :param convert_dict: Dictionary of which to convert key values
    :param replace_values: If true, replaces values of the dictionary with the id instead of keys
    :param name_prop: The name of the property to access a name in an element in elem_list
    :param id_prop: The name of the property to access an id in an element in elem_list
    :return: A new dictionary containing the key-value pairs, with the keys replaced by ids
    """
    new_dict = {}
    for key, value in convert_dict.items():
        if replace_values:
            matching_obj = next(
                filter(lambda obj: getattr(obj, name_prop) == value, elem_list), None
            )
            new_dict[key] = getattr(matching_obj, id_prop)
        else:
            matching_obj = next(
                filter(lambda obj: getattr(obj, name_prop) == key, elem_list), None
            )
            new_dict[getattr(matching_obj, id_prop)] = value
    return new_dict
