import numpy as np
import pandas as pd
from skipper import observe

dirname = '../../packages/skipper/pointings'

def load_fall ( early_vvds=True ):
    pointings = []
    for filter_name in ['n708','n540']:
        vvds = pd.read_csv ( f'{dirname}/vvds_{filter_name}.csv', index_col='object.1')
        if early_vvds:
            mask = vvds.RA < 345.
            vvds.loc[mask, 'object'] = vvds.loc[mask, 'object'].apply ( lambda x: x.split('_')[0] +'early' + '_' + '_'.join(x.split('_')[1:]) )
            vvds.loc[~mask, 'object'] = vvds.loc[~mask, 'object'].apply ( lambda x: x.split('_')[0] +'late' + '_' +  '_'.join(x.split('_')[1:]))
        xmm = pd.read_csv ( f'{dirname}/xmm_{filter_name}.csv', index_col='object.1')

        mastercat = pd.concat([vvds, xmm])
        mastercat['proposer'] = 'Leauthaud'
        pointings.append(mastercat)
    return pointings

def _load_mastercat_cosmos ( fname = f'{dirname}/cosmosgama_n540.csv' ):
    mastercat = pd.read_csv ( fname )
    mastercat = mastercat.set_index('object')
    mastercat['wait'] = "False"
    mastercat['proposer'] = 'Leauthaud'
    mastercat = mastercat.drop('object.1', axis=1)
    mastercat['object'] = mastercat.index
    return mastercat

def load_spring ():
    # \\ load Shany's pointings (expanded for S21A HSC coverage)
    halpha_s2022a = pd.read_csv(f'{dirname}/gama_2022A.csv', index_col='object.1')

    # \\ load Shany's old pointings
    oiii_pointings = _load_mastercat_cosmos ()
    halpha_pointings = _load_mastercat_cosmos ( f'{dirname}/S2021A.csv')
    
    # \\ add priorities to GAMA field
    is_high = (halpha_s2022a['dec'] > 1.5)
    is_early = (halpha_s2022a['RA'] < 160.)
    is_late = (halpha_s2022a['RA'] > 210.)

    halpha_s2022a['priority_name'] = 'GAMA'
    halpha_s2022a.loc[is_high&~is_early, 'priority_name'] = 'GAMAhigh'
    halpha_s2022a.loc[is_early, 'priority_name'] = 'GAMAearly'
    halpha_s2022a.loc[is_late, 'priority_name'] = 'GAMAlate'    
    
    # \\ copy & modify Halpha catalog to be OIII catalog
    get_catalog_objects = lambda x: x['object'].str.extract(r'(.*?(?=_))')[0]
    oiii_s2022a = halpha_s2022a.copy()
    oiii_s2022a['filter'] = 'N540'
    oiii_s2022a['object'] = [ xo.replace('N708','N540') for xo in oiii_s2022a['object'] ]
    oiii_s2022a.index = oiii_s2022a['object']
    oiii_s2022a['expTime'] = 900.

    # \\ add COSMOS pointings
    halpha_cosmos = halpha_pointings.loc[get_catalog_objects(halpha_pointings)=='COSMOS'].copy()
    halpha_cosmos['priority_name'] = 'COSMOS'
    halpha_s2022a = pd.concat([halpha_s2022a, halpha_cosmos], sort=False)                                   

    oiii_cosmos = oiii_pointings.loc[get_catalog_objects(oiii_pointings)=='COSMOS'].copy()
    oiii_cosmos['priority_name'] = 'COSMOS'
    oiii_s2022a = pd.concat([oiii_s2022a, oiii_cosmos], sort=False)    
    
    return halpha_s2022a, oiii_s2022a

def load_copilot ( copilot_path, pointings, filter_name ):
    '''
    Load copilot output 
    '''
    if filter_name == 'n708':
        skySB_0 = 21.
        teff_min = 200.
    elif filter_name == 'n540':
        skySB_0 = 22.1
        teff_min = 300.    
        
    coo = observe.CopilotOutput( copilot_path, pointings, skySB_0=skySB_0)
    reobs = coo.flag_for_reobservation ( min_teff = teff_min )

    sorter = coo.merian_sidecar.sort_values('t_eff')['object'].duplicated(keep='last')
    merian_sidecar = coo.merian_sidecar.loc[~sorter]
    observed = merian_sidecar.loc[~np.in1d(merian_sidecar['object'], reobs)]
    return observed