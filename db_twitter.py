#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 17:28:58 2020

@author: yousuf
"""
import sqlite3
from sqlite3 import Error

#conn = sqlite3.connect('test.db')
#conn.execute('''CREATE TABLE COMPANY
#         (ID INT PRIMARY KEY     NOT NULL,
#         NAME           TEXT    NOT NULL,
#         AGE            INT     NOT NULL,
#         ADDRESS        CHAR(50),
#         SALARY         REAL);''')
#conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");
#
#conn.commit()
#conn.close()


class DB_Twitter:
    def __init__(self,db_name,db_path):
        self.db_name=db_name
        self.db_path=db_path
    def open_con(self):
        try:
            self.conn=sqlite3.connect(self.db_path+self.db_name)
        except Error as e:
            print(e)
    def command(self,text):
        self.conn.execute(text)
    def command_w_commit(self,text):
        self.conn.execute(text)
        self.conn.commit()
    def close_w_commit(self):
        self.conn.commit()
        self.conn.close()
    def close(self):
        self.conn.close()
    





















