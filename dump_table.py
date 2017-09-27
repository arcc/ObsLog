#! python

if __name__ == "__main__":
    import sqlite3 as sql
    import argparse
    from pprint import pprint
    p = argparse.ArgumentParser()
    p.add_argument('dbfile', type=str)
    p.add_argument('table', type=str)
    args = p.parse_args()

    dbfile = args.dbfile
    table = args.table

    try:
        conn = sql.connect(dbfile)
        cur = conn.cursor()
        cur.execute("SELECT * FROM {}".format(table))
        results = cur.fetchall()
        pprint(results)
    except:
        print "failed to dump table ", dbfile