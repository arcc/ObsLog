#! python

if __name__ == "__main__":
    import sqlite3 as sql
    import argparse
    import sys

    a = argparse.ArgumentParser()
    a.add_argument('dbfile', type=str)
    a.add_argument('table', type=str)
    a.add_argument('institution', type=str)
    args = a.parse_args()

    dbfile = args.dbfile
    table = args.table
    institution = '"'+args.institution+'"'

    try:
        conn = sql.connect(dbfile)
        c = conn.cursor()
        c.execute('SELECT duration FROM {} WHERE institution = {}'.format(table, institution))
        f = c.fetchall()
        durations = [f[i][0] for i in range(len(f))]
        total_time = sum(durations)

        sys.stdout.write('\r%s' % total_time + '\n')
        sys.stdout.flush()
    except:
        sys.exit('error')
