import subprocess

def get_all_tracts ( butler ):
    '''
    Get a list of all tracts that overlap the current footprint
    '''
    tracts = []
    for data_id in butler.registry.queryDataIds(
            'tract',
            datasets="visitSummary",
            collections="DECam/runs/merian/w_2022_29",
            instrument="DECam",
            skymap='hsc_rings_v1'
        ):    
        tract_id = data_id['tract']
        tracts.append(tract_id)
    return set(tracts)