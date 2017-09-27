# /usr/bin/env python


# Purpose: parse p2030 cima log file and extract observers,
# sources, and observation times into a file

# observation delimiter
DLMT = "BEGIN   executive: CIMA executive starting ..."

if __name__ == "__main__":
    import os
    import argparse
    from datetime import datetime

    p = argparse.ArgumentParser()
    p.add_argument('logfile', type=str)
    p.add_argument('-o', dest='outdir', type=str, default=os.getcwd())
    args = p.parse_args()

    of = os.path.join(args.outdir, os.path.basename(args.logfile) + '_summary.txt')

    # write buffer
    buf = ''

    with open(args.logfile, 'r') as f:
        # get observation blocks from log file
        blks = [x.split('\n') for x in f.read().split(DLMT)]
        blks = blks[1:] # ignore the first element
    
    log_records = []
    for blk in blks:
        # (timestamp, ra, dec, observers)
        blk_records = []
        observers = [x.split('mode for ')[1].strip("'") for x in [l for l in blk if "e: CIMA session" in l]][0]
        src_lines = [l for l in blk if "pnt tr" in l and len(l.split()) > 10 and "vw_send" in l]
        
        for src in src_lines:
            src = src.split()
            timestamp = src[0]+' '+src[1]
            sra = src[8]
            sdec = src[9]

            ra_deg = float(sra[:2]) * 15.0
            ra_deg += float(sra[2:4]) * 15.0 / 60.0
            ra_deg += float(sra[4:]) * 15.0 / 3600.0 

            dec_deg = float(sdec[:2]) 
            dec_deg += float(sdec[2:4]) * 15.0 / 60.0
            dec_deg += float(sdec[4:]) * 15.0 / 3600.0

            blk_records.append((str(x) for x in (timestamp, ra_deg, dec_deg, observers)))
        log_records.extend(blk_records)

    for r in log_records:
        buf += ' '.join(r) + '\n'
    
    with open(of, 'w') as f:
        f.write(buf)



