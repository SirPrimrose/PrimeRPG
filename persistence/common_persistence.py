from persistence.connection_handler import connection


def get_dictionary_from_table(table_name: str, unique_id: int):
    cursor_obj = connection.cursor()

    stmt_args = (unique_id,)
    statement = 'SELECT * FROM %s WHERE unique_id = ?' % table_name
    cursor_obj.execute(statement, stmt_args)
    result = cursor_obj.fetchone()

    return result


def insert_dictionary(table_name: str, my_dict: dict):
    cursor_obj = connection.cursor()
    placeholders = ', '.join(['?'] * len(my_dict))
    columns = ', '.join(my_dict.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)
    cursor_obj.execute(sql, list(my_dict.values()))
