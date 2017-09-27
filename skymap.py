import matplotlib.pyplot as plt
import numpy as np
import psrcat as pc

cat = pc.PSRCAT('data/psrcat.db')
raj, decj = zip(*[x['JCOORD_RAD'] for x in cat.blocks])
obs_entry = get_observation_entry('p2030.cimalog_20170720_summary.txt')

def load_psr_pos(db_file):
    cat = pc.PSRCAT(db_file)
    raj, decj = zip(*[x['JCOORD_RAD'] for x in cat.blocks])
    return raj, decj

def get_observation_entry(summary_file):
    f = open(summary_file, 'r')
    entries = []
    info_list = ['date', 'time' ,'RAJ', 'DECJ', 'observer']
    for line in f.readlines():
        info = {}
        line = line.strip()
        l = line.split()
        num_ele = len(l)
        if num_ele < 5:
            raise RuntimeError("Observation summary file should have "
                    "'date', 'time' ,'RAJ', 'DECJ', 'observer' in the column.")
        for i in range(4):
            info[info_list[i]] = l[i]
        observers = ''
        for i in range(4, num_ele):
             observers += l[i] + ' '
        info[info_list[4]] = observers
        entries.append(info)
    return entries

def map_projection(db_file, obs_entry):
    raj, decj = load_psr_pos(db_file)
    
    #source = ColumnDataSource(data=dict(x=raj, y=decj))

    obs_RAJs = np.array([float(x['RAJ']) for x in obs_entry])
    obs_DECJs = np.array([float(x['DECJ']) for x in obs_entry])



    fig = plt.figure(figsize=(8, 6))
    plt.title('ANTF Catalogue')
    #plt.plot(raj, decj, '.')
    #plt.subplot(111, projection = "mollweide")
    ax = fig.add_subplot(111, projection='mollweide')
    ax.plot(obs_RAJs, obs_DECJs, '.')
    plt.grid(True)
    plt.xlabel('Right Ascension (rad)')
    plt.ylabel('Declination (rad)')
    plt.show()
    #plt.plot(decj)
    #plt.show()


if __name__ == '__main__' :
    sp=sky_plot('data/psrcat.db')
    sp