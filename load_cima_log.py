#! python

# load information from cima log into db system.

# TODO: automatically add new members to db when found in log
# TODO: prevent duplicate entries for pointings
# TODO: parse and load pointing durations into db
# TODO: be able to differentiate between multiple different project codes within a single cima log file

import sqlite3 as sql

# insert new pointing to project pointings table
def insert_new_pointing(dbtable, datetime, instrument, rx, institution,
                        ra, dec, dur, logfile):
    conn = sql.connect(dbtable)
    cur = conn.cursor()
    q = '''INSERT INTO pointings (datetime, instrument, rx, institution,
           ra, dec, duration, logfile) VALUES (?,?,?,?,?,?,?,?)'''
    vals = (datetime, instrument, rx, institution, ra, dec, dur, logfile)

    # check if pointing is already in db
    cur.execute('''SELECT id, datetime, instrument, ra, dec FROM pointings
                WHERE datetime='{}' AND instrument='{}' AND ra={}
                AND dec={}'''.format(datetime, instrument, ra, dec))
    results = cur.fetchone()
    if results:
        print "Pointing {} is already in the table with id={}".format(vals, results[0])
        id = results[0]
    else:
        cur.execute(q, vals) # insertion
        conn.commit()

        # get new pointing id
        cur.execute('''SELECT id FROM pointings
                WHERE datetime='{}' AND instrument='{}' AND ra={}
                AND dec={}'''.format(datetime, instrument, ra, dec))
        id = cur.fetchone()[0]
    conn.close()
    return id


if __name__ == "__main__":
    import os
    import p2030_summary as p2030
    import argparse


    p = argparse.ArgumentParser(description="Load contents of AO CIMA log file into the database.")
    p.add_argument('cimalog', type=str, help="path to CIMA log file")
    p.add_argument('--db', type=str, dest='db', default=os.path.join(os.getcwd(),'db'),
                   help='Path to db root directory. Current default is {}'.format(
                       os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db')))
    args = p.parse_args()

    clog = args.cimalog
    projcode = "p2030" # this should NOT be hardcoded. 
    dbroot = args.db
    memDB = os.path.join(dbroot, 'members.db')
    projDB = os.path.join(dbroot, 'p2030', 'pointings.db') # this should be determined from the projcode

    # open tables
    memDBconn = sql.connect(memDB) # members table
    memDBcur = memDBconn.cursor()

    colnames, log_records = p2030.summarize(clog) # parse CIMA log file

    for r in log_records:
        datetime_str, ra_str, dec_str, observers = r
        observers = observers.split(',')

        # insert new pointing
        pid = insert_new_pointing(projDB, datetime_str, 'arecibo',
                                  'alpha', 'Null', ra_str, dec_str,
                                  0.0, clog)

        # insert observer records
        for obs in observers:
            # names can appear in multiple varieties. this is a massive weak point!
            # version 1: first last (e.g. Michael Smith)
            # version 2: only first name (e.g. Jane)
            # version 3: <first initial> <last name> (e.g. J. Hessels)
            # version 4: <first name> <last initial>
            # etc...
            
            # hardcoded until we can parse names
            if 'Jing' in obs:
                fname = "JING"
                lname = "LUO"
            elif "Keeisi" in obs:
                fname = "KEEISI"
                lname = "CABALLERO"
            elif "J. Hessels" in obs:
                fname = "JASON"
                lname = "HESSELS"
            elif "Yhamil" in obs:
                fname = "YHAMIL"
                lname = "GARCIA"
            else:
                # nothing to do here
                continue

            memDBcur.execute('''SELECT userdb FROM members WHERE firstname='{}'
                                AND lastname='{}' '''.format(fname, lname))
            userDBpath = memDBcur.fetchone()[0]
            userDBpath = os.path.join(dbroot, 'userpointings', userDBpath)
            userDBconn = sql.connect(userDBpath)
            userDBcur = userDBconn.cursor()
            q = '''INSERT INTO userpointings (id, duration) VALUES (?,?)'''
            vals = (pid, 0.0) # FAKE DURATION INSERTION HERE!

            # check if user pointing exists
            userDBcur.execute("SELECT id FROM userpointings WHERE id={}".format(pid))
            results = userDBcur.fetchall()
            if results: # pointing has already been added
                print "pointing {} is already in db file {}".format(pid, userDBpath)
                continue

            # insert new pointing
            userDBcur.execute(q,vals)
            userDBconn.commit()
            userDBconn.close()


