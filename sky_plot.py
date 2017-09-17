import numpy as np
import psrcat as pc
from bokeh.palettes import Viridis6 as palette
cat = pc.PSRCAT('data/psrcat.db')
raj, decj = zip(*[x['JCOORD_RAD'] for x in cat.blocks])
from bokeh.layouts import layout
from bokeh.models import (CustomJS, Slider, ColumnDataSource, WidgetBox, Toggle,
                          HoverTool, LogColorMapper)
from bokeh.plotting import figure, output_file, show


output_file('sky_plot.html')
tools = 'pan'

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

def get_sky_cover_area(RAJ, DECJ, beam_size):
    half_beam = beam_size / 2.0
    RAJ = np.array(RAJ, ndmin=1, copy=False)
    DECJ = np.array(DECJ, ndmin=1, copy=False)
    if len(RAJ) != len(DECJ):
        raise ValueError("RAJ and DECJ have to be in the same dimension.")
    x_low = RAJ - half_beam
    x_up = RAJ + half_beam
    y_low = DECJ - half_beam
    y_up = DECJ + half_beam
    xs = np.zeros((len(RAJ), 4))
    ys = np.zeros((len(RAJ), 4))
    for ii in range(len(x_low)):
        xs[ii, :] = np.array([x_low[ii], x_up[ii], x_up[ii], x_low[ii]])
        ys[ii, :] = np.array ([y_low[ii], y_low[ii], y_up[ii], y_up[ii]])
    return xs, ys

def sky_plot(db_file, obs_entry):
    raj, decj = load_psr_pos(db_file)
    source = ColumnDataSource(data=dict(x=raj, y=decj))

    obs_RAJs = np.array([float(x['RAJ']) for x in obs_entry])
    obs_DECJs = np.array([float(x['DECJ']) for x in obs_entry])
    cover_raj, cover_decj = get_sky_cover_area(obs_RAJs, obs_DECJs, 2.5/60.0)
    cover_raj = np.deg2rad(cover_raj)
    cover_decj = np.deg2rad(cover_decj)

    observers = [x['observer'] for x in obs_entry]
    dates = [x['date'] for x in obs_entry]
    times = [x['time'] for x in obs_entry]
    projects = ['P2030']*len(cover_decj)
    source2 = ColumnDataSource(data=dict(
                x=cover_raj.tolist(),
                y=cover_decj.tolist(),
                project=projects,
                date=dates,
                time=times,
                name=observers,
                ))
    TOOLS = "pan,wheel_zoom,reset,hover,hover,save"
    plot = figure(
        x_range=(-1,7),
        y_range=(-2, 2), tools=TOOLS, toolbar_location="left",
        title="ANTF Catalogue",
        x_axis_label='RAJ (rad)',
        y_axis_label='DECJ (rad)')

    box_color = ["navy"] * len(obs_RAJs)
    box_alpha = [0.4,] * len(obs_RAJs)
    starplot = plot.asterisk('x', 'y', source=source, size=5)
    cover_box = plot.patches('x', 'y', source=source2, line_width=0.5,
                color=box_color,
                fill_alpha=box_alpha)

    pulsar_tooltips = [
        ("RA, DEC : ", "($x, $y)"),
        ]

    obs_tooltips = [
        ("Project", "@project"),
        ("Date", "@date"),
        ("Time", "@time"),
        ("Observer", "@name"),
        ("RA, DEC : ", "($x, $y)"),
        ]

    hover = plot.select(dict(type=HoverTool))
    hover[0].renderers = [starplot]
    hover[0].tooltips = pulsar_tooltips
    hover[1].renderers = [cover_box]
    hover[1].tooltips = obs_tooltips

    code2 = '''\
    object.visible = toggle.active
    '''

    callback_star = CustomJS.from_coffeescript(code=code2, args={})
    toggle1 = Toggle(label="Pulsars", button_type="success", callback=callback_star)
    callback_star.args = {'toggle': toggle1, 'object': starplot}

    callback_box = CustomJS.from_coffeescript(code=code2, args={})
    toggle2 = Toggle(label="Observation Scans", button_type="success", callback=callback_box)
    callback_box.args = {'toggle': toggle2, 'object': cover_box }
    return [plot, toggle1, toggle2]


obs_entry = get_observation_entry('p2030.cimalog_20170720_summary.txt')
sp = sky_plot('data/psrcat.db', obs_entry)

l = layout([
    sp[0],
    sp[1:3],
], sizing_mode='scale_width')

show(l)
