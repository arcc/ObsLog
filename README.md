# ObsLog
Logging System for ARCC Telescope Observations

This is an Observation Logging tool for ARCC Team Leaders to submit Observation Logs. This project is intended to facilitate
giving proper credit where due for ARCC Members. It will also include ways to obtain sky coverage plots and figures to quantify 
the effect of the ARCC research group on the scientific community.


### TODO:

1. Provide Arecibo Support (parse session cmd files) for Survey (P2030) and Timing Observations
2. Provide GBT Support (parse session cmd files) for Survey (GBNCC)
3. Ability to update local ATNF catalogue
4. Ability to parse, search, and plot ATNF entries on celestial plot
5. Web form to input observation log and upload relevant CMD file

#### TODO Item 3
1. Use hash (or other equivilent method) to determine if an update is needed
2. If update is needed then download latest tar.gz file from ATNF and extract psrcat.db and copy it locally. (gz support for db file?)
