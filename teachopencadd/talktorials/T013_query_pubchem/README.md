# T013 · Data acquisition from PubChem

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Jaime Rodríguez-Guerra, 2019-2020, [Volkamer lab, Charité](https://volkamerlab.org/)
- Dominique Sydow, 2019-2020, [Volkamer lab, Charité](https://volkamerlab.org/)
- Yonghui Chen, 2019-2020, [Volkamer lab, Charité](https://volkamerlab.org/)


## Aim of this talktorial

In this notebook, you will learn how to search for compounds similar to an input SMILES in [PubChem](https://pubchem.ncbi.nlm.nih.gov/) with the API web service.


### Contents in *Theory*

- PubChem
- Programmatic access to PubChem


### Contents in *Practical*

* Simple examples for the PubChem API
  * How to get the PubChem CID for a compound
  * Retrieve molecular properties based on a PubChem CID
  * Depict a compound with PubChem
* Query PubChem for similar compounds
  * Determine a query compound
  * Create task and get the job key
  * Download results when job finished
  * Get canonical SMILES for resulting molecules
  * Show the results    


## References

* Literature:
    * PubChem 2019 update: [_Nucleic Acids Res._ (2019), __47__, D1102-1109](https://academic.oup.com/nar/article/47/D1/D1102/5146201)
    * PubChem in 2021: [_Nucleic Acids Res._(2021), __49__, D1388–D1395](https://academic.oup.com/nar/article/49/D1/D1388/5957164)
* Documentation: 
    * [PubChem Source Information](https://pubchem.ncbi.nlm.nih.gov/sources)
    * [PUG REST](https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest)
    * [Programmatic Access](https://pubchemdocs.ncbi.nlm.nih.gov/programmatic-access)
    * [PubChem - Wikipedia](https://en.wikipedia.org/wiki/PubChem)
