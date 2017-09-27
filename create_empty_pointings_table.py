#! python

if __name__ == "__main__":
    import os
    import sys
    import sqlite3 as sql
    import argparse

    default_db_root = os.path.join(os.getcwd(), 'db')

    p = argparse.ArgumentParser()
    p.add_argument('-f', '--force', action='store_true', dest='f',
                   help='overwrite existing files')
    p.add_argument('projCode', type=str, help="Project Code")
    p.add_argument('--dbroot', type=str, default=default_db_root,
                   help="db root path. Current default is "+default_db_root)
    args = p.parse_args()
    proj = args.projCode.lower()
    projroot = os.path.join(args.dbroot, proj)

    #create project directory if it doesn't already exist
    try:
        if not os.path.isdir(projroot):
            os.mkdir(projroot)
    except:
        print "unable to create project directory: {}".format(projroot)
        print "Goodbye."
        sys.exit()
    
    dbname = os.path.join(projroot, 'pointings.db')

    if os.path.exists(dbname) and not args.f:
        print "database file already exists: {}".format(dbname)
        sys.exit()
    elif os.path.exists(dbname) and args.f:
        os.remove(dbname)


    conn = sql.connect(dbname)
    c = conn.cursor()

    #create table
    query = '''CREATE TABLE members
               (id INTEGER PRIMARY KEY, datetime TEXT,
                instrument TEXT, rx TEXT, leadobs TEXT,
                institution TEXT, ra REAL, dec REAL,
                duration REAL, proj TEXT, logfile TEXT)'''
    c.execute(query)
    conn.commit()
    conn.close()