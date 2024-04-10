# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 16:11:16 2024

@author: aarregui
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (25,12)


#SET SEED
np.random.seed(10)



os.chdir(os.path.join('D:\\', 'repositorios-local', 'motif-discovery'))
    
# Configuración de OP1
periodos1 = 30
ops1 = 4
time_op1 = [2 * 60, 10 * 60]
mean_op1 = [4, 10]
amp_op1 = [0, 1]
time_stop1 = [0.5 * 60, 2 * 60]
dt = 1

formas1 = np.arange(4)  # 0 plana, 1 ascendente, 2 descendente, 3 harmonico

op1 = {}
op1['form'] = np.random.randint(min(formas1), max(formas1) + 1, ops1)
op1['dur'] = np.random.randint(time_op1[0], time_op1[1] + 1, ops1)
op1['mean'] = np.random.randint(mean_op1[0], mean_op1[1] + 1, ops1)
op1['amp'] = np.random.rand(ops1)
op1['stop'] = np.zeros(ops1)
op1['stop'][0] += 10 * 150

# Configuración de OP2
periodos2 = 5
ops2 = 2
time_op2 = [5 * 60, 10 * 60]
mean_op2 = [1, 5]
amp_op2 = [0, 1]
time_stop2 = [0.5 * 60, 2 * 60]

formas2 = np.arange(1, 3)  # 1 ascendente, 2 descendente

op2 = {}
op2['form'] = np.random.randint(min(formas2), max(formas2) + 1, ops2)
op2['dur'] = np.random.randint(time_op2[0], time_op2[1] + 1, ops2)
op2['mean'] = np.random.randint(mean_op2[0], mean_op2[1] + 1, ops2)
op2['amp'] = np.random.rand(ops2)
op2['stop'] = np.zeros(ops2)
op2['stop'][0] += 10 * 150

total_ops = ops1 + ops2
total_periodos = periodos1 + periodos2

tabla1 = np.zeros((ops1 * periodos1, 3))
per_m, op_m = np.meshgrid(np.arange(1, periodos1 + 1), np.arange(1, ops1 + 1))
tabla1[:, 0] = per_m.T.flatten()
tabla1[:, 1] = op_m.T.flatten()
tabla1[:, 2] = 1

tabla2 = np.zeros((ops2 * periodos2, 3))
per_m, op_m = np.meshgrid(np.arange(1, periodos2 + 1), np.arange(1, ops2 + 1))
tabla2[:, 0] = per_m.T.flatten()
tabla2[:, 1] = op_m.T.flatten()
tabla2[:, 2] = 2

tabla = np.vstack((tabla1, tabla2))


data = pd.DataFrame(tabla)
data.columns = [ 'op_ex', 'phase_ex', 'op_id']

data['diff'] = data['op_ex'].diff()
data.loc[data['diff'] != 0] = 1

data['general_ex'] = data['diff'].cumsum().astype(int)


cambios = data['general_ex'].diff().ne(0).cumsum()


# Dividir la serie en grupos
grupos = [g.reset_index(drop=True) for _, g in data.groupby(cambios)]

# Mezclar los grupos
np.random.shuffle(grupos)

# Concatenar los grupos nuevamente en una serie
s_reordenada = pd.concat(grupos)

data = pd.concat(grupos, ignore_index = True)

idx = np.where(data['op_id'] == 2)[0]
data.loc[idx-1, 'op_id'] = 2

tabla = data[['op_ex', 'phase_ex', 'op_id']].to_numpy()


#%%


for cont in range(len(tabla)):
    
    type_op = tabla[cont, 2]
    op_index = int(tabla[cont, 1]-1)
    
    if np.random.rand() > 0.9:
        t_mod = np.random.randint(9, 12) / 10
    else:
        t_mod = 1
    
    if type_op == 1:
        time_op = np.arange(dt, op1['dur'][op_index] * t_mod, dt)
        op_array = np.repeat(type_op, len(time_op))
        
        forma = op1['form'][op_index]
        if forma == 0:
            serie_op = op1['mean'][op_index] * np.ones_like(time_op) + 0.2 * np.random.rand(len(time_op))
        elif forma == 1:
            serie_op = np.linspace(op1['mean'][op_index], op1['mean'][op_index] + op1['amp'][op_index], len(time_op)) + 0.2 * np.random.rand(len(time_op))
        elif forma == 2:
            serie_op = np.linspace(op1['mean'][op_index], op1['mean'][op_index] - op1['amp'][op_index], len(time_op)) + 0.2 * np.random.rand(len(time_op))
        elif forma == 3:
            serie_op = op1['mean'][op_index] + op1['amp'][op_index] * np.cos(time_op / max(time_op) * 5) + 0.1 * np.random.rand(len(time_op))
    
        if op1['stop'][op_index] != 0:
            time_stop = np.arange(dt, op1['stop'][op_index] * np.random.randint(5, 16) / 10, dt)
            serie_stop = 0.3*np.random.rand(len(time_stop))
        else:
            time_stop = np.array([time_op[-1]+1])
            serie_stop = serie[-1]+0.2*np.random.rand(1)
        
        if len(time_stop) != 1:
            op_stop = np.repeat(0, len(time_stop))
        else:
            op_stop = np.array([type_op])
        
        if cont == 0:
            time_op = time_op + time_stop[-1]
            time = np.concatenate((time_stop, time_op))
            serie = np.concatenate((serie_stop, serie_op))
            ops = np.concatenate((op_stop, op_array))
                
          
        elif cont == len(tabla) - 1:
            time_stop = np.arange(dt, op1['stop'][0] * np.random.randint(5, 16) / 10, dt)
            op_stop = np.repeat(0, len(time_stop))
            serie_stop = 0.3*np.random.rand(len(time_stop))
            time = np.concatenate((time, time_op, time_stop))
            serie = np.concatenate((serie, serie_op, serie_stop))
            ops = np.concatenate((ops, op_array, op_stop))
        
        else:
            time_stop = time_stop + time[-1]
            time_op = time_op + time_stop[-1]
            time = np.concatenate((time, time_stop, time_op))
            serie = np.concatenate((serie, serie_stop, serie_op))
            ops = np.concatenate((ops, op_stop, op_array))
    else:
        
        time_op = np.arange(dt, op2['dur'][op_index] * t_mod, dt)
        op_array = np.repeat(type_op, len(time_op))
        
        forma = op2['form'][op_index]
        if forma == 0:
            serie_op = op2['mean'][op_index] * np.ones_like(time_op) + 0.2 * np.random.rand(len(time_op))
        elif forma == 1:
            serie_op = np.linspace(op2['mean'][op_index], op2['mean'][op_index] + op2['amp'][op_index], len(time_op)) + 0.2 * np.random.rand(len(time_op))
        elif forma == 2:
            serie_op = np.linspace(op2['mean'][op_index], op2['mean'][op_index] - op2['amp'][op_index], len(time_op)) + 0.2 * np.random.rand(len(time_op))
        elif forma == 3:
            serie_op = op2['mean'][op_index] + op2['amp'][op_index] * np.cos(time_op / max(time_op) * 5) + 0.1 * np.random.rand(len(time_op))
    
        if op2['stop'][op_index] != 0:
            time_stop = np.arange(dt, op2['stop'][op_index] * np.random.randint(5, 16) / 10, dt)
            serie_stop = 0.3*np.random.rand(len(time_stop))
        else:
            time_stop = np.array([time_op[-1]+1])
            serie_stop = serie[-1]+0.2*np.random.rand(1)
        
        if len(time_stop) != 1:
            op_stop = np.repeat(0, len(time_stop))
        else:
            op_stop = np.array([type_op])
        
        if cont == 0:
            #Se incluye parada al principio
            time_op = time_op + time_stop[-1]
            time = np.concatenate((time_stop, time_op))
            serie = np.concatenate((serie_stop, serie_op))
            ops = np.concatenate((op_stop, op_array))
            
            
        if cont == len(tabla) - 1:
            #Se añade parada al final
            time_stop = np.arange(dt, op2['stop'][0] * np.random.randint(5, 16) / 10, dt)
            serie_stop = 0.3*np.random.rand(len(time_stop))
            op_stop = np.repeat(0, len(time_stop))
            time = np.concatenate((time, time_stop))
            serie = np.concatenate((serie, serie_op, serie_stop))
            ops = np.concatenate((ops, op_array, op_stop))
        
        else:
            time_stop = time_stop + time[-1]
            time_op = time_op + time_stop[-1]
            time = np.concatenate((time, time_stop, time_op))
            serie = np.concatenate((serie, serie_stop, serie_op))
            ops = np.concatenate((ops, op_stop, op_array))


plt.plot(np.arange(len(serie)), serie)
plt.show()

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(serie, 'b')
ax2.plot(ops, 'g')
plt.show()


#%%


#store data
data_path = os.path.join('data', 'python-main-op.csv')

simulated_data = pd.DataFrame({'current': serie, 'op_id': ops})
simulated_data['op_id'] = simulated_data['op_id'].astype(int)

simulated_data.to_csv(data_path)

