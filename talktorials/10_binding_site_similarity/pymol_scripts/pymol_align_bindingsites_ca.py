'''
This script aligns all pairs of input proteins (binding site CA atoms).
'''

import pymol
import pickle
import pandas as pd
import sys
import numpy as np

# Launch PyMol
pymol.finish_launching()

# Get the parameter (radius from ligand)
radius = sys.argv[1]

# Load PDB IDs
pdb_ids = pickle.load(open("../data/T10/pdb_ids.p", "rb"))

# Create DataFrame to store align results
align_df = pd.DataFrame(index=pdb_ids, columns=pdb_ids)

def align_structures(m1, m2, align_df):
	# Fetch PDB structures	
	pymol.cmd.fetch(m1, "i")
	pymol.cmd.fetch(m2, "m")

	# Select binding site CA atoms
	pymol.cmd.select("i_bs", "(byres i within " + radius + " of (i and resn STI)) and name CA")
	pymol.cmd.select("m_bs", "(byres m within " + radius + " of (m and resn STI)) and name CA")

	# Align binding sites
	aln = pymol.cmd.align(mobile="m_bs", target="i_bs", quiet=1)

	# Save align results to DataFrame
	align_df.loc[m1, m2] = aln

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
pickle.dump(align_df, open("../data/T10/align_df_bindingsites_ca.p", "wb"))
