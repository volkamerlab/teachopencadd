# T012 · Data acquisition from KLIFS

Authors:

- Dominique Sydow, 2019-2020, [Volkamer lab, Charité](https://volkamerlab.org/)
- Jaime Rodríguez-Guerra, 2019-2020, [Volkamer lab, Charité](https://volkamerlab.org/)
- David Schaller, 2020, [Volkamer lab, Charité](https://volkamerlab.org/)


## Aim of this talktorial

KLIFS is a database for kinase-ligand interaction fingerprints and structures. In this talktorial, we will use the programmatic access to this database (KLIFS OpenAPI) and the `opencadd` package to interact with its rich content. 
First, we will use a query kinase (EGFR) to fetch all available structures and explore their bound ligands and interaction fingerprints. Then, we will explore the bioactivity data for the EGFR inhibitor Gefitinib in order to find off-targets. Last but not least, we offer a convenience function that allows you to easily explore different (if you want random) kinases.


### Contents in *Theory*

- Kinases
- EGFR and Gefitinib
- KLIFS database
- KLIFS OpenAPI
- `opencadd`


### Contents in *Practical*

- Define kinase and ligand of interest: EGFR and Gefitinib
- Generate a KLIFS Python client
- Explore the KLIFS OpenAPI
  - Kinase groups
  - Kinase families
  - Kinases
  - Structures
  - Interaction fingerprints
  - Structure coordinates
  - Ligands
- Case study: EGFR (using `opencadd`)
  - Get all structures for EGFR
  - Average interaction fingerprint
  - Select an example EGFR-Gefitinib structure
  - Show the structure with `nglview`
  - Show all kinase-bound ligands with `rdkit`
  - Explore profiling data for Gefitinib
- Explore random kinase in KLIFS (show example structure and all bound ligands)


### References

* Introduction to protein kinases and inhibition ([Chapter 9 in _Med. Chem. Anticancer Drugs_ (2008), 251-305](https://www.sciencedirect.com/science/article/pii/B9780444528247000093))
* Kinase classification by Manning _et al._ ([_Science_ (2002), __298__, 1912-1934](https://science.sciencemag.org/content/298/5600/1912))
* Kinase-centric computational drug development ([_Annu. Rep. Med. Chem._ (2017), __50__, 197-236](https://www.sciencedirect.com/science/article/pii/S0065774317300040?via%3Dihub))
* EGFR and Gefitinib 
  * Review on the EGFR family ([_Pharmacol. Res._ (2019), __139__, 395-411](https://www.sciencedirect.com/science/article/abs/pii/S104366181831747X?via%3Dihub) and [_Front. Cell Dev. Biol._ (2016), __8__](https://www.frontiersin.org/articles/10.3389/fcell.2016.00088/full))
  * EGFR kinase details on [UniProt](https://www.uniprot.org/uniprot/P00533)
  * Gefitinib details on [PubChem](https://pubchem.ncbi.nlm.nih.gov/compound/Gefitinib)
* KLIFS - a kinase-inhibitor interactions database
   * Main database/website reference ([_Nucleic Acids Res._ (2020)](https://academic.oup.com/nar/advance-article/doi/10.1093/nar/gkaa895/5934416))
   * Introduction of the KLIFS website & database ([_Nucleic Acids Res._ (2016), __44__, 6, D365–D371](https://doi.org/10.1093/nar/gkv1082))
   * Initial KLIFS dataset, binding mode classification, residue numbering ([_J. Med. Chem._ (2014), __57__, 2, 249-277](https://pubs.acs.org/doi/abs/10.1021/jm400378w))
* NGLView, the interactive molecule visualizer ([_Bioinformatics_ (2018), __34__, 1241–124](https://doi.org/10.1093/bioinformatics/btx789))
