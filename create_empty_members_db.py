#! python

if __name__ == "__main__":
    import os
    import sys
    import sqlite3 as sql
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-f', '--force', action='store_true', dest='f',
                   help='overwrite existing files')
    p.add_argument('--dbroot', type=str, default='db',
                   help="db root path")
    args = p.parse_args()

    dbname = os.path.join(args.dbroot, 'members.db')

    if os.path.exists(dbname) and not args.f:
        print "database file already exists: {}".format(dbname)
        sys.exit()
    elif os.path.exists(dbname) and args.f:
        os.remove(dbname)


    conn = sql.connect(dbname)
    c = conn.cursor()

    #create table
    query = '''CREATE TABLE members
               (id INTEGER PRIMARY KEY, firstname text, lastname text, inst text, userdb text)'''
    c.execute(query)
    conn.commit()
    conn.close()