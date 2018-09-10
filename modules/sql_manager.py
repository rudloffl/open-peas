#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  15 14:52:19 2018
@author: Laurent Rudloff
"""

__author__ = 'Larry'

import psycopg2
import sqlite3
import os

class Chester():
    def __init__(self, dbpath='test.sqlite'):
        self.dbpath = dbpath

        self.connectdb()

    def closedb(self,):
        self.cursor.close()
        self.conn.close()

    def connectdb(self):
        initiate = False
        if not os.path.exists(self.dbpath):
            initiate = True

        self.conn = sqlite3.connect(self.dbpath)
        self.cursor = self.conn.cursor()
        if initiate:
            self.createdb()

    def createdb(self,):
        ## CLIENTS TABLE ##
        client_table = """ CREATE TABLE IF NOT EXISTS CLIENT (
                        id integer PRIMARY KEY,
                        company_name text NOT NULL,
                        contact_fname text,
                        contact_lname text,
                        creation_date text,
                        street_number text,
                        street_name1 text,
                        street_name2 text,
                        city text,
                        zipcode text,
                        state text,
                        country text,
                        phone1 text,
                        phone2 text,
                        fax text,
                        mail1 text,
                        mail2 text,
                        longitude real,
                        lattitude real
                        ); """
        self.cursor.execute(client_table)


        ## MATERIALS TABLE ##
        material_table = """ CREATE TABLE IF NOT EXISTS MATERIAL (
                        id integer PRIMARY KEY,
                        common_name text NOT NULL,
                        variety text,
                        seed_supplier text,
                        reference text,
                        link text
                        ); """
        self.cursor.execute(material_table)

        ## STATE TABLE ##
        state_table = """ CREATE TABLE IF NOT EXISTS STATE (
                        id integer PRIMARY KEY,
                        state text NOT NULL,
                        comment text
                        ); """
        self.cursor.execute(state_table)

        ## STATE-LIST TABLE ##
        state_list_table = """ CREATE TABLE IF NOT EXISTS STATELIST (
                        id integer PRIMARY KEY,
                        state_id integer NOT NULL,
                        target_id integer NOT NULL,
                        FOREIGN KEY(state_id) REFERENCES STATE(id)
                        FOREIGN KEY(target_id) REFERENCES TARGET(id)
                        ); """
        self.cursor.execute(state_list_table)

        ## UNIT TABLE ##
        unit_table = """ CREATE TABLE IF NOT EXISTS UNIT (
                        id integer PRIMARY KEY,
                        unit text NOT NULL,
                        common_name text NOT NULL,
                        comment text NOT NULL,
                        measuring_device text NOT NULL,
                        regression integer NOT NULL,
                        range_mini text,
                        range_maxi text
                        ); """
        self.cursor.execute(unit_table)

        ## SPECTRAS TABLE ##
        spectra_table = """ CREATE TABLE IF NOT EXISTS SPECTRA ( id integer PRIMARY KEY"""

        for wl in ["""wl_{}""".format(x) for x in range(950, 1530+1, 2)]:
            spectra_table = spectra_table + ", {} real".format(wl)

        spectra_table = spectra_table + """); """
        self.cursor.execute(spectra_table)

        ## TARGETS TABLE ##
        target_table = """ CREATE TABLE IF NOT EXISTS TARGET (
                        id integer PRIMARY KEY,
                        material_id integer NOT NULL,
                        state_list_id integer NOT NULL,
                        unit_id integer NOT NULL,
                        client_id integer NOT NULL,
                        spectra_id integer NOT NULL,
                        comment text,
                        timestamp text NOT NULL,
                        temperature real,
                        longitude real,
                        lattitude real,
                        FOREIGN KEY(material_id) REFERENCES MATERIAL(id),
                        FOREIGN KEY(state_list_id) REFERENCES STATELIST(state_id),
                        FOREIGN KEY(client_id) REFERENCES CLIENT(id),
                        FOREIGN KEY(spectra_id) REFERENCES SPECTRA(id),
                        FOREIGN KEY(unit_id) REFERENCES UNIT(id)
                        ); """
        self.cursor.execute(target_table)

    def commit(self):
        self.conn.commit()

    def add_state(self,):
        self.__write_db('STATE', {'state':'frozen'})

    def add_target(self,):
        self.__write_db('TARGET', {'unit_id':1})

    def __write_db(self, table_name, dict_data):
        attribnamelist = [x for x in dict_data.keys()]
        valuelist = [dict_data[x] for x in attribnamelist]
        attrib_names = ", ".join(attribnamelist)
        attrib_values = ", ".join("?" * len(attribnamelist))
        sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name, attrib_names, attrib_values)
        self.cursor.execute(sql, valuelist)

    def get_columns(self, table_name):
        self.cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
        return [tup[1] for tup in self.cursor.fetchall()]

def main():
    chester = Chester()
    chester.add_state()
    #chester.add_target()
    chester.commit()
    print(chester.get_columns('MATERIAL'))
    chester.closedb()

if __name__ == '__main__':
    main()
