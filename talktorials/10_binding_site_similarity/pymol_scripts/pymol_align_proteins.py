'''
This script aligns all pairs of input proteins.
'''

import pymol
import pickle
import pandas as pd
import sys
import numpy as np

# Launch PyMol
pymol.finish_launching()

# Load PDB IDs
pdb_ids = pickle.load(open("../data/T10/pdb_ids.p", "rb"))

# Create DataFrame to store align results
align_df = pd.DataFrame(index=pdb_ids, columns=pdb_ids)

def align_structures(m1, m2, align_df):
	# Fetch PDB structures	
	pymol.cmd.fetch(m1, "i")
	pymol.cmd.fetch(m2, "m")

	# Align proteins
	aln = pymol.cmd.align(mobile="m", target="i", quiet=1, object="{}_{}".format(m1, m2))

	# Save align results to DataFrame
	align_df.loc[m1, m2] = aln

	# Save sequence alignment to file
	pymol.cmd.save(filename="../data/T10/alignment/alignment_proteins_" + "{}_{}".format(m1, m2) + ".aln", selection="{}_{}".format(m1, m2))

	# Reinitialize PyMol for next structure pair to be loaded
	pymol.cmd.reinitialize()

	return align_df

# Iterate over all structure pairs
for n, immobile in enumerate(pdb_ids):
	for mobile in pdb_ids[n:]:
		align_df = align_structures(mobile, immobile, align_df)
		align_df = align_structures(immobile, mobile, align_df)

# Quit PyMol
pymol.cmd.quit()

# Save results to file
pickle.dump(align_df, open("../data/T10/align_df_proteins.p", "wb"))
