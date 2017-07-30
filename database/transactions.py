# encoding: utf-8
"""
transactions

Created by Donzok on 28/07/2017.
Copyright (c) 2017 . All rights reserved.
"""

import sqlite3


def connect():
    conn = sqlite3.connect('files/mealsbot.db')

    return conn


def disconnect(conn):
    conn.close()


def init_db():
    conn = connect()

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS dishes (id             integer primary key, 
                                                         name           text    unique, 
                                                         is_breakfast   boolean, 
                                                         is_lunch       boolean, 
                                                         is_snack       boolean, 
                                                         is_dinner      boolean)''')

    conn.commit()

    disconnect(conn)


def get_random_dish():
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes ORDER BY RANDOM() LIMIT 1")

    dish = cursor.fetchone()

    disconnect(conn)

    if dish is None:
        return -1

    return dish[1]


def get_random_dinner():
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes WHERE is_dinner == 1 ORDER BY RANDOM() LIMIT 1")

    dish = cursor.fetchone()

    disconnect(conn)

    if dish is None:
        return -1

    return dish[1]


def get_random_snack():
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes WHERE is_snack == 1 ORDER BY RANDOM() LIMIT 1")

    dish = cursor.fetchone()

    disconnect(conn)

    if dish is None:
        return -1

    return dish[1]


def get_random_lunch():
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes WHERE is_lunch == 1 ORDER BY RANDOM() LIMIT 1")

    dish = cursor.fetchone()

    disconnect(conn)

    if dish is None:
        return -1

    return dish[1]


def get_random_breakfast():
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dishes WHERE is_breakfast == 1 ORDER BY RANDOM() LIMIT 1")

    dish = cursor.fetchone()

    disconnect(conn)

    if dish is None:
        return -1

    return dish[1]


def add_dish(dish):
    conn = connect()

    cursor = conn.cursor()

    cursor.execute("INSERT INTO dishes VALUES (NULL, ?, ?, ?, ?, ?)", dish)

    conn.commit()

    disconnect(conn)