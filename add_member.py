#! python

import os
import sys
import sqlite3 as sql

# add new member into database
# 1. add entry in db/members.db
# 2. create new table for new member in db/users: userpointings table

dbRoot = 'db'


def add_member_to_db(membersDB, userRoot, fname, lname, inst, npoints, dbRoot):
    '''
    add a new member into the 'members.db' database
    '''

    inst = inst.upper()

    dbname = fname+lname+'.db'
    userdb = os.path.join(userRoot, dbname)

    conn = sql.connect(membersDB)
    c = conn.cursor()

    # exit if user already exists
    c.execute("SELECT id FROM members WHERE firstname='{}' and lastname='{}'".format(fname,lname))
    results = c.fetchone()
    if results:
        id = results[0]
        print "Member {} already exists with id={}!".format(fname+' '+lname, id)
        print "Goodbye."
        conn.close()
        sys.exit()
    
    # insert new member
    insert_query = '''INSERT INTO members (firstname, lastname, inst, userdb)
                      VALUES ('{}', '{}', '{}', '{}')'''.format(fname, lname, inst, dbname)

    c.execute(insert_query)
    conn.commit()

    conn.close()


def create_userpointings_db(membersDB, fname, lname, userRoot):
    '''
    create userinfo table/db for new member
    '''

    #get user db name from members.db database
    memconn = sql.connect(membersDB)
    memcur = memconn.cursor()
    query = "SELECT userdb FROM members WHERE firstname='{}' and lastname='{}'".format(fname, lname)
    memcur.execute(query)
    result = memcur.fetchone()[0] # userdb name
    result = os.path.join(userRoot, result) # userdb path relative from dbRoot
    memconn.close()

    usrconn = sql.connect(result) #create new userpointings db
    usrcur = usrconn.cursor()


    create_query = '''CREATE TABLE userpointings
                      (id INTEGER PRIMARY KEY, duration REAL)'''
    usrcur.execute(create_query)
    usrconn.commit()
    usrconn.close()



if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('firstname', type=str, help='member first name')
    p.add_argument('lastname', type=str, help='member last name')
    p.add_argument('inst', type=str, help='member institution. e.g. utrgv')
    p.add_argument('--npointings', type=int, default=0, dest='npoints',
                   help='number of pointings user participated in')
    p.add_argument('--db', default=dbRoot, type=str, dest='db',
                   help='path to db root')

    args = p.parse_args()

    dbRoot = args.db
    fname = args.firstname.upper()
    lname = args.lastname.upper()

    membersDB = os.path.join(dbRoot, 'members.db')
    userRoot = os.path.join(dbRoot, 'userpointings')


    try:
        add_member_to_db(membersDB, userRoot, fname, lname, args.inst, args.npoints, dbRoot)
        print "Added {} {} to {}".format(fname, lname, membersDB)
    except:
        print "Failed to add {} {} to {}!".format(fname, lname, membersDB)
        sys.exit()
    
    try:
        create_userpointings_db(membersDB, fname, lname, userRoot)
        print "Created new pointings table: {}".format(os.path.join(userRoot, fname+lname+'.db'))
    except:
        print "Failed to create pointings table! {}".format(os.path.join(userRoot, fname+lname+'.db'))
        sys.exit()
    


