# Talktorials 11

# CADD web services that can be used via a Python API

__Developed at AG Volkamer, Charité__

Dr. Jaime Rodríguez-Guerra, Dominique Sydow

> ⚠ This talktorial series was added back in late 2019. By the time of the v1.3 release, some of the used web services are not available any more. Updates/fixes will be available upon our next major release, scheduled for late 2020.

## Aim of this talktorial

Web services are a convenient way of using software because it frees the user from any installation hassles. A web UI is usually available for easy usage, at the cost of losing the possibility to automate a workflow. Fortunately, the number of web services that provide an API for automated access has been increasing. Some examples in the field of Computer Aided Drug Design include:

- PubChem 
- RCSB PDB
- KLIFS
- Proteins.plus
- SwissDock
- AutoDock Vina (OPAL webservices)

In the underlying notebooks, you will learn how to programmatically use online web-services from Python, always in the context of drug design.
The final goal will be to build a full pipeline that exclusively relies on web-services, without (almost) any local execution!

__Note__: For simplicity, the full lesson will be divided in four notebooks:

- 11_. General info on the use of APIs
- 11a. Querying KLIFS & PubChem for potential kinase inhibitors
- 11b. Docking the candidates against the target obtained in 11a
- 11c. Assessing the results and comparing against known data

### Description of the pipeline and the involved webservices

1. Kinase-Ligand Interaction Fingerprints and Structures database (KLIFS), developed at the Division of Medicinal Chemistry - VU University Amsterdam, is a database that provides information about the protein structure (collected from the PDB) of catalytic kinase domains and the interaction with their ligands. We can obtain the curated protein structure from this database and use the ligand information to retrieve similar ligands from other databases, like PubChem or ChEMBL.
2. Using the ligand information provided by KLIFS, we can query PubChem for similar compounds.
3. After having obtained the protein structure(s) and several candidate ligands, we can dock them online with the Vina installation provided in the OPAL web services. We will also query _proteins.plus'_ DoGSiteScorer for probable binding sites where we will dock the compounds. (part B)
4. The results will be visualized with `nglview` and their interactions fingerprints (computed using `PLIP`) compared with those provided originally in KLIFS. (part C)
