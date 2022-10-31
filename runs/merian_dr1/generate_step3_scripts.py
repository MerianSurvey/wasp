from collections import defaultdict
from re import template
from tracemalloc import start
import lsst.daf.butler as dafButler

### # # # # ### 
###  PARAMS ###
### # # # # ### 
Nscripts = 10
template_script = './merian_dr1_step3_template.yaml'
### # # # # ### 

butler = dafButler.Butler('/projects/MERIAN/repo/')

grouped_by_tract = defaultdict(set)
for data_id in butler.registry.queryDataIds(
    ["tract", "visit", "detector"],
    datasets="visitSummary",
    collections="DECam/runs/merian/w_2022_29",
    instrument="DECam",
):
    grouped_by_tract[data_id["tract"]].add(data_id)

#print({k: len(v) for k, v in grouped_by_tract.items()})
covered_tracts = sorted(list(grouped_by_tract.keys()))

step = int(len(covered_tracts)/Nscripts)
template = open  ( template_script, 'r' ).read ()
for idx in range(Nscripts):
    start_index = idx * step
    if (idx + 2)*step > len(covered_tracts):
        end_index = len(covered_tracts) + 1
    else:
        end_index = (idx+1)*step
    #print ( start_index, end_index )
    this_scripts_tracts = covered_tracts[start_index:end_index]
    cscript = template.replace ('<TRACTS>', ','.join([ str(x) for x in this_scripts_tracts]))
    open(f'./merian_dr1_step3_BATCH{idx:02d}.yaml', 'w').write(cscript)
    