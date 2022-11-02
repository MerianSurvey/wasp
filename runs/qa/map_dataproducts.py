import sys
import subprocess
import numpy as np
import pandas as pd

if 'matplotlib' not in sys.modules:
    import matplotlib
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib import patches

def get_all_tracts ( butler, input_collection='DECam/runs/merian/w_2022_29', skymap='hsc_rings_v1'):
    '''
    Get a list of all tracts that overlap the current footprint
    '''
    tracts = []
    for data_id in butler.registry.queryDataIds(
            'tract',
            datasets="visitSummary",
            collections=input_collection,
            instrument="DECam",
            skymap=skymap
        ):    
        tract_id = data_id['tract']
        tracts.append(tract_id)
    return list(set(tracts))

def get_product_coverage ( butler, data_type, output_collection='DECam/runs/merian/dr1_wide', skymap='hsc_rings_v1' ):
    '''
    '''
    n_completed = {}
    for data_id in butler.registry.queryDataIds (['tract','patch'], datasets=data_type, 
                                                 collections=output_collection, skymap=skymap):
        tract = data_id['tract']
        patch = data_id['patch']
        if tract not in n_completed.keys():
            n_completed[tract] = np.zeros(81, dtype=int)
        n_completed[tract][patch] = 1

    stats = np.zeros([len(n_completed), 2], dtype=int)
    for idx,key in enumerate(n_completed.keys()):
        stats[idx,0] = key
        stats[idx,1] = n_completed[key].sum()
    return stats

def make_map ( data_products, skymap ):
    fig, ax = plt.subplots(1,1,figsize=(70,6))
    ax.set_aspect('equal')
    for key in data_products.index:
        #\\ set color
        ncompleted = data_products.loc[key]
        if ncompleted < 0:
            color = 'grey'
        elif ncompleted < (81./2.):
            color = 'tab:red'
        elif ncompleted < 75:
            color = 'tab:orange'
        else:
            color = 'tab:green'

        skytract = skymap.generateTract(key)
        vertices = skytract.vertex_list
        ra_l = [ np.rad2deg(float(vertices[idx][0])) for idx in range(4) ]
        dec_l = [ np.rad2deg(float(vertices[idx][1])) for idx in range(4)]
        
        width = height = 1.6796988294693618 # \\ force 
        rect = patches.Rectangle ( (min(ra_l),min(dec_l)), 
                                   width,#max(ra_l)-min(ra_l),
                                   height,#max(dec_l)-min(dec_l),
                                   facecolor='None', edgecolor=color, lw=1)

        ax.add_patch ( rect )
        if ncompleted > 0:
            ax.text ( np.rad2deg(float(skytract.ctr_coord[0])), np.rad2deg(float(skytract.ctr_coord[1])), 
                      '%i/81' % data_products.loc[key], color=color,
                      ha='center', va='center', fontsize=5 )

    #plt.tight_layout ()
    plt.subplots_adjust ( left=0.01, right=0.99, bottom=0.01, top=0.99)

    ax.set_xlim ( 0., 360. )
    ax.set_ylim ( -10., 10. )
        
def main ( butler, data_products=['objectTable','objectTable_tract', 'deepCoadd_forced_src','deepCoadd_calexp'] ):
    all_tracts = get_all_tracts ( butler )
    
    df = pd.DataFrame ( index=all_tracts, columns=data_products )
    for dp in data_products:
        stats = get_product_coverage( butler, dp )
        df.loc[stats[:,0],dp] = stats[:,1]
    df = df.replace(np.NaN,-1)
    return df
