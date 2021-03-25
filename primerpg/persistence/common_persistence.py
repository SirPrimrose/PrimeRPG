#  Copyright (c) 2021
#  Project: PrimeRPG
#  Author: Primm
import sys
from sqlite3 import OperationalError, IntegrityError
from traceback import print_exc
from typing import List

from primerpg.consts import data_folder
from primerpg.helpers.checksum_helper import has_file_changed
from primerpg.persistence.connection_handler import connection


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
            matching_obj = next(filter(lambda obj: getattr(obj, name_prop) == value, elem_list), None)
            new_dict[key] = getattr(matching_obj, id_prop)
        else:
            matching_obj = next(filter(lambda obj: getattr(obj, name_prop) == key, elem_list), None)
            new_dict[getattr(matching_obj, id_prop)] = value
    return new_dict


def convert_list_values_to_id(
    elem_list: List,
    convert_list: List,
    name_prop="name",
    id_prop="unique_id",
):
    """
    Takes a list and replaces the list items with ids.

    :param elem_list: Each element of the list will be searched to replace the key values of the convert dictionary.
    :param convert_list: List of which to convert key values
    :param name_prop: The name of the property to access a name in an element in elem_list
    :param id_prop: The name of the property to access an id in an element in elem_list
    :return: A new list with the list items replaced by ids
    """
    new_list = []
    for item in convert_list:
        matching_obj = next(filter(lambda obj: getattr(obj, name_prop) == item, elem_list), None)
        new_list.append(getattr(matching_obj, id_prop))
    return new_list


def convert_name_to_id(
    elem_list: List,
    convert_value,
    name_prop="name",
    id_prop="unique_id",
):
    """
    Takes a value and replaces the value with the matching id from the list.

    :param elem_list: Each element of the list will be searched to replace the key values of the convert dictionary.
    :param convert_value: Value for which to convert to an id
    :param name_prop: The name of the property to access a name in an element in elem_list
    :param id_prop: The name of the property to access an id in an element in elem_list
    :return: A new list with the list items replaced by ids
    """
    matching_obj = next(filter(lambda obj: getattr(obj, name_prop) == convert_value, elem_list), None)
    return getattr(matching_obj, id_prop)


def should_reload_from_file(dependencies: List[str], file_name: str, table_name: str) -> bool:
    """Checks if a table should be cleaned and reloaded. This is done by performing a checksum with the file_name and
    all dependencies included in data

    :param dependencies: The dependencies that the table relies on. Could be empty.
    :param file_name: The file name directly relied upon. Required.
    :param table_name: The table name for which to clean if the file has changed.
    :return: True if the table was cleaned, or false if nothing has changed
    """
    json_files = [data_folder / file_name]
    for dependency_name in dependencies:
        json_files.append(data_folder / dependency_name)

    if not has_file_changed(json_files):
        return False

    clean_table(table_name)
    return True


def clean_table(table_name: str):
    connection.commit()
    disable_foreign_keys()
    delete_table_entries(table_name)
    connection.commit()
    enable_foreign_keys()


def delete_table_entries(table_name: str) -> None:
    cursor_obj = connection.cursor()

    stmt = "DELETE from %s" % table_name
    cursor_obj.execute(stmt)


def disable_foreign_keys():
    connection.execute("PRAGMA foreign_keys = 0")


def enable_foreign_keys():
    connection.execute("PRAGMA foreign_keys = 1")
