import subprocess

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
    return n_completed
    