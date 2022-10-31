import matplotlib.pyplot as plt
from matplotlib import patches

def show_inputvisits ( tractinfo, n708_intract, n540_intract, reduced_n708, reduced_n540 ):
    tract_ra = tractinfo.ctr_coord.getRa().asDegrees()
    tract_dec = tractinfo.ctr_coord.getDec().asDegrees()
    
    fig, axarr = plt.subplots ( 1,2, figsize=(16,6) )
    ax = axarr[0]
    ax.set_aspect('equal')
    tv = [tractinfo.vertex_list[1].getRa().asDegrees(), tractinfo.vertex_list[1].getDec().asDegrees()]
    rect = patches.Rectangle(tv, 1.67, 1.67, facecolor='lightgrey', )
    ax.add_patch(rect)
    for vt in tractinfo.vertex_list:
        ax.scatter ( vt.getRa().asDegrees(), vt.getDec().asDegrees(), edgecolor='k', facecolor='None' )

    for name,visit in reduced_n540.loc[n540_intract].iterrows():
        circ = patches.Circle ( visit[['racenter','deccenter']], 1.1, facecolor='None', edgecolor='C0')
        ax.add_patch(circ)

    #fig = plt.figure(figsize=(8,6))
    ax = axarr[1]
    ax.set_aspect('equal')
    tv = [tractinfo.vertex_list[1].getRa().asDegrees(), tractinfo.vertex_list[1].getDec().asDegrees()]
    rect = patches.Rectangle(tv, 1.67, 1.67, facecolor='lightgrey', )
    ax.add_patch(rect)
    for vt in tractinfo.vertex_list:
        ax.scatter ( vt.getRa().asDegrees(), vt.getDec().asDegrees(), edgecolor='k', facecolor='None' )

    for name,visit in reduced_n708.loc[n708_intract].iterrows():
        circ = patches.Circle ( visit[['racenter','deccenter']], 1.1, facecolor='None', edgecolor='tab:red')
        ax.add_patch(circ)

    for ax in axarr:
        ax.set_xlabel('RA (deg)')
        ax.set_ylabel('Dec (deg)')
        ax.text ( tract_ra, tract_dec, tractinfo.getId(), va='center', ha='center', zorder=1)

    axarr[0].text ( 0.0275, 0.975, 'N540', fontsize=18, transform=axarr[0].transAxes, ha='left', va='top')
    axarr[1].text ( 0.0275, 0.975, 'N708', fontsize=18, transform=axarr[1].transAxes, ha='left', va='top')
    axarr[0].text ( 0.975, 0.0275, '\n'.join(reduced_n540.loc[n540_intract,'expnum'].values.astype(str)),
                  fontsize=13, transform=axarr[0].transAxes, ha='right', va='bottom', color='k')
    axarr[1].text ( 0.975, 0.0275, '\n'.join(reduced_n708.loc[n708_intract,'expnum'].values.astype(str)),
                  fontsize=13, transform=axarr[1].transAxes, ha='right', va='bottom', color='k')
    plt.savefig(f'../scripts/tract{tractinfo.getId()}_visits.png', facecolor='w', transparent=False)