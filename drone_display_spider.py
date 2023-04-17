import numpy as np
import matplotlib.pyplot as plt
import requests
import time
#from IPython.display import Audio, display
#from IPython.core.display import HTML

plt.ion()
slep = 0.1

sound_file = 'sonar-sweep-beep-80957.mp3'

def plot_spider(ax, n, w, s, e, slep):
    direction = ['', 'North', 'West', 'South', 'East']
    data = [e, n, w, s]
    data.append(data[0])

    if max([n,s]) == s:
        lon = -s
    else:
        lon = n

    if max([w,e]) == w:
        lat = -w
    else:
        lat = e


    angles = np.linspace(0, 2 * np.pi, 4, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    ax.clear()
    ax.plot(angles, data, '-', color='k')
    ax.fill(angles, data, alpha=0.25, color='b')
    ax.set_rmax(1)
    ax.set_thetagrids(angles * 180 / np.pi, direction)
    plt.title("DRONE CONFIDENCE WEIGHTS PER ANTENNA")
    plt.pause(slep)

plt.style.use('ggplot')
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(polar=True)

moving_avg_step = 5
n_percs = [0 for i in range(moving_avg_step)]
w_percs = [0 for i in range(moving_avg_step)]
s_percs = [0 for i in range(moving_avg_step)]
e_percs = [0 for i in range(moving_avg_step)]
index = 0
while True:
    n = "http://api.thingspeak.com/channels/2104187/fields/field1/last.txt"
    w = "http://api.thingspeak.com/channels/2104187/fields/field2/last.txt"
    s = "http://api.thingspeak.com/channels/2104187/fields/field3/last.txt"
    e = "http://api.thingspeak.com/channels/2104187/fields/field4/last.txt"

    n_perc = round(float(requests.get(n).text), 5)
    w_perc = round(float(requests.get(w).text), 5)
    s_perc = round(float(requests.get(s).text), 5)
    e_perc = round(float(requests.get(e).text), 5)

    n_percs[index] = n_perc
    w_percs[index] = w_perc
    s_percs[index] = s_perc
    e_percs[index] = e_perc

    index = (index + 1)%moving_avg_step

    #display(HTML(f'<audio src="{sound_file}" autoplay controls></audio>'))
  
    plot_spider(ax, np.mean(n_percs), np.mean(w_percs), np.mean(s_percs), np.mean(e_percs), slep)

    print('cycle')

    time.sleep(0.5)