import math
import numpy as np
#import pandas as pd
# \\ XXX only load if LSST stack is loaded?
from lsst import geom as afwGeom

def load_merian_visits ():
    '''
    Load all previous Merian visits from copilot output
    '''
    raise NotImplementedError

def visits_to_tract ():
    '''
    Find Merian visits within a tract
    '''
    raise NotImplementedError

def write_reduction ( tract_id, visits, suffix='testWide')

def make_afw_coords(coord_list):
    """
    ~ From Johnny Greco's musulsb ~
    
    Convert list of ra and dec to lsst.afw.coord.IcrsCoord.
    Parameters
    ----------
    coord_list : list of tuples or tuple
        ra and dec in degrees.
    Returns
    -------
    afw_coords : list of lsst.afw.coord.IcrsCoord
    """
    if type(coord_list[0]) in (float, int, np.float64):
        ra, dec = coord_list
        afw_coords = afwGeom.SpherePoint(afwGeom.Angle(ra, afwGeom.degrees),
                                         afwGeom.Angle(dec, afwGeom.degrees))
    else:
        afw_coords = [
            afwGeom.SpherePoint(afwGeom.Angle(ra, afwGeom.degrees),
            afwGeom.Angle(dec, afwGeom.degrees)) for ra, dec in coord_list]
    return afw_coords


def tracts_n_patches(coord_list, skymap=None,
                     data_dir='/tigress/HSC/DR/s18a_wide/'):
    """m
    ~ From Johnny Greco's musulsb ~
        
    Find the tracts and patches that overlap with the 
    coordinates in coord_list. Pass the four corners of 
    a rectangle to get all tracts and patches that overlap
    with this region.

    Parameters
    ----------
    coord_list : list (tuples or lsst.afw.coord.IcrsCoord)
        ra and dec of region
    data_dir : string, optional
        Rerun directory. Will use name in .superbutler 
        by default.
    skymap : lsst.skymap.ringsSkyMap.RingsSkyMap, optional
        The lsst/hsc skymap. If None, it will be created.

    Returns
    -------
    region_ids : structured ndarray
        Tracts and patches that overlap coord_list.
    tract_patch_dict : dict
        Dictionary of dictionaries, which takes a tract 
        and patch and returns a patch info object.
    """
    if type(coord_list[0])==float or type(coord_list[0])==int:
        coord_list = [make_afw_coords(coord_list)]
    elif type(coord_list[0])!=afwGeom.SpherePoint:
        coord_list = make_afw_coords(coord_list)

    if skymap is None:
        import lsst.daf.persistence
        butler = lsst.daf.persistence.Butler(data_dir)
        skymap = butler.get('deepCoadd_skyMap', immediate=True)

    tract_patch_list = skymap.findTractPatchList(coord_list)
    return tract_patch_list
    ids = []
    tract_patch_dict = {}
    for tract_info, patch_info_list in tract_patch_list:
        patch_info_dict = {}
        for patch_info in patch_info_list:
            patch_index = patch_info.getIndex()
            patch_id = str(patch_index[0])+','+str(patch_index[1])
            ids.append((tract_info.getId(), patch_id))
            patch_info_dict.update({patch_id:patch_info})
        tract_patch_dict.update({tract_info.getId():patch_info_dict})
    region_ids = np.array(ids, dtype=[('tract', int), ('patch', 'S4')])
    return region_ids, tract_patch_dict

def visits_in_tract ( tractinfo, coord_list, match_radius=0.5 ):
    #if type(coord_list[0])==float or type(coord_list[0])==int:
    #coord_list = make_afw_coords(coord_list)
    
    mask = np.zeros(len(coord_list), dtype=bool)
    for idx,ac in enumerate(coord_list):
        in_tract = np.zeros([9], dtype=bool)
        jdx = 0
        for rasign in [-1,0,1]:
            for decsign in [-1,0,1]:
                cc = np.array([ac[0] + match_radius*rasign, ac[1] + match_radius*decsign])                
                cc = make_afw_coords(cc)
                in_tract[jdx] = tractinfo.contains(cc)
                jdx += 1
        mask[idx] = np.any(in_tract)
    return mask

def jd_to_date(jd):
    """
    From https://gist.github.com/jiffyclub/1294443
    Convert Julian Day to date.
    
    Algorithm from 'Practical Astronomy with your Calculator or Spreadsheet', 
        4th ed., Duffet-Smith and Zwart, 2011.
    
    Parameters
    ----------
    jd : float
        Julian Day
        
    Returns
    -------
    year : int
        Year as integer. Years preceding 1 A.D. should be 0 or negative.
        The year before 1 A.D. is 0, 10 B.C. is year -9.
        
    month : int
        Month as integer, Jan = 1, Feb. = 2, etc.
    
    day : float
        Day, may contain fractional part.
        
    Examples
    --------
    Convert Julian Day 2446113.75 to year, month, and day.
    
    >>> jd_to_date(2446113.75)
    (1985, 2, 17.25)
    
    """
    jd = jd + 0.5
    
    F, I = math.modf(jd)
    I = int(I)
    
    A = math.trunc((I - 1867216.25)/36524.25)
    
    if I > 2299160:
        B = I + 1 + A - math.trunc(A / 4.)
    else:
        B = I
        
    C = B + 1524
    
    D = math.trunc((C - 122.1) / 365.25)
    
    E = math.trunc(365.25 * D)
    
    G = math.trunc((C - E) / 30.6001)
    
    day = C - E + F - math.trunc(30.6001 * G)
    
    if G < 13.5:
        month = G - 1
    else:
        month = G - 13
        
    if month > 2.5:
        year = D - 4716
    else:
        year = D - 4715
        
    return year, month, day