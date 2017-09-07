# ATNF Pulsar Catalogue Parsing Module

import numpy as np

DEFAULT_DLIMITER = '@-----------------------------------------------------------------'

class PSRCAT(object):
    def __init__(self, fname, dlimiter=DEFAULT_DLIMITER):
        self.fname = fname
        self.delimiter = dlimiter

        f = open(self.fname, 'r')
        rawdata = f.read()
        rawblocklist = rawdata.split(dlimiter)
        blocks = [self._parseBlock(x) for x in rawblocklist if len(x)>10]

        del rawdata
        del rawblocklist

        for i in range(len(blocks)):
            blocks[i]['JCOORD_RAD'] = self._parsePSRJ(blocks[i]['PSRJ'])
        self.blocks = blocks            

    def _parseBlock(self, blk):
        '''
        Parse a single PSRCAT DB block string and convert into a python dictionary.
        NOTE: COLUMNS 3 AND 4 ARE IGNORED. ONLY FIRST TWO COLUMNS ARE USED.

        Parameters
        ==========
        blk: str
            string containing a single source block in PSRCAT.db file
        
        Returns
        =======
        blkDict: dict
            Dictionary containing the block information as key:value pairs.
        '''
        lines = [l for l in blk.split('\n') if not l.startswith('#') and l is not '']
        blkDict = {}
        for l in lines:
            x = l.split()
            blkDict[x[0]] = x[1]
        return blkDict

    def _parsePSRJ(self, jcoord):
        '''
        Convert PSRJ coordinates to (RA, DEC) as floats in radians.
        PSRCAT/PSRJ formats supported are:
            * J%HH%MM%S%DD%MM
            * J%HH%MM%S%DD
            * J%HH%MM%S%DD%MM%X
        where %HH is hours, %MM is minutes/arcminutes, %S is the declination sign,
        %DD is degrees, and %X is a extra alpha character designating multiple sources 
        at the same coordinates.
        '''
        if len(jcoord) >= 8:
            raj_hours = float(jcoord[1:3])
            raj_mins = float(jcoord[3:5])
            decj_sign = -1 if jcoord[5]=='-' else 1
            decj_degs = float(jcoord[6:8])
            decj_min = float(jcoord[8:10]) if len(jcoord)>=10 else 0
        else:
            print "Error: unrecognized PSRJ format: ", jcoord

        raj_rad = (np.pi/180)*(raj_hours*15 + raj_mins*(15.0/60))
        decj_rad = decj_sign*(np.pi/180)*(decj_degs + decj_min/60)

        return (raj_rad, decj_rad)