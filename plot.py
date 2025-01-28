# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 09:32:28 2024

@author: aarregui
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from src.utils import *

plt.rcParams["figure.figsize"] = (25,12)


output_folder = os.path.join('output', 'experimentation')

window_sizes = [500, 1700, 2500]
 
data_file_name = 'python-main-op.csv'
data_path = os.path.join('data', data_file_name)
suffix = 'MP_AV'


data = pd.read_csv(data_path, index_col = 0)
series = data['current'].to_numpy()
true_ops = data['op_id'].to_numpy()


data['op_ex'] = get_ops(true_ops)

plt.plot(series, color = 'blue', lw = 2)
plt.xlabel('Time', fontsize = 20)
plt.ylabel('Simulated Signal', fontsize = 20)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.savefig(os.path.join(output_folder, 'series.png'))
plt.show()



#%%


main_index = data.loc[data['op_ex'] == 4].index.values
main = data.loc[data['op_ex'] == 4, 'current'].to_numpy()
secondary_index = data.loc[data['op_ex'] == 5].index.values
secondary = data.loc[data['op_ex'] == 5, 'current'].to_numpy()

fig = plt.figure("constrained")
gs = GridSpec(2, 2, figure=fig)
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(series, color = 'blue', lw = 2)
ax1.set_xlabel('Time', fontsize = 20)
ax1.tick_params(axis = 'both', labelsize = 15)
ax1.text(-0.05, 1, '(a)', transform=ax1.transAxes, size=30)
ax1.set_xmargin(0)


# identical to ax1 = plt.subplot(gs.new_subplotspec((0, 0), colspan=3))
ax2 = fig.add_subplot(gs[1, 0])
x_range = np.arange(1700, 3350)
ax2.plot(main_index, main, color = 'blue', lw = 2)
ax2.tick_params(axis = 'both', labelsize = 15)
ax2.set_xlabel('Time', fontsize = 20)
#ax2.set_title('Main process', fontsize = 25)
ax2.text(-0.1, 1, '(b)', transform=ax2.transAxes, size=30)


ax3 = fig.add_subplot(gs[1, 1])
x_range = np.arange(77900, 78900)
ax3.plot(secondary_index, secondary, color = 'blue', lw = 2)
ax3.tick_params(axis = 'both', labelsize = 15)
#ax3.set_title('Secondary process', fontsize = 25)
ax3.set_xlabel('Time', fontsize =20)
ax3.text(-0.1, 1, '(c)', transform=ax3.transAxes, size=30)
fig.tight_layout(h_pad=3, w_pad = 5)
plt.savefig(os.path.join(output_folder, 'series_ops.png'))
plt.show()


#%%


plt.plot(series, color = 'blue', lw = 2)
plt.xlabel('Time', fontsize = 20)
plt.ylabel('Simulated Signal', fontsize = 20)
plt.tick_params(axis = 'both', labelsize = 15)
plt.show()



plt.plot(main_index, main, color = 'blue', lw = 2)
plt.tick_params(axis = 'both', labelsize = 15)
plt.ylabel('Simulated Signal', fontsize = 20)
plt.xlabel('Time', fontsize = 20)
plt.show()



plt.plot(secondary_index, secondary, color = 'blue', lw = 2)
plt.tick_params(axis = 'both', labelsize = 15)
plt.ylabel('Simulated Signal', fontsize = 20)
plt.xlabel('Time', fontsize =20)
plt.show()