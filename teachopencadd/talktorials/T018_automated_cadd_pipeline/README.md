# T018 · Automated pipeline for lead optimization

Authors:

- Armin Ariamajd, 2021, CADD seminar 2021, Charité/Freie Universität Berlin
- Melanie Vogel, 2021, CADD seminar 2021, Charité/Freie Universität Berlin
- Andrea Volkamer, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Dominique Sydow, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Corey Taylor, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)


## Aim of this talktorial

In this talktorial, we will learn how to develop an **automated structure-based virtual screening pipeline**. 
The pipeline is **particularly suited for the hit expansion and lead optimization** phases of a drug discovery project, where a promising ligand (i.e. an initial hit or lead compound) needs to be structurally modified in order to improve its binding affinity and selectivity for the target protein. The general architecture of the pipeline can thus be summarized as follows (Figure 1).


* **Input**
    * Target protein structure and a promising ligand (e.g. lead or hit compound), plus specifications of the processes that need to be performed.
      
      
* **Processes**
    * Detection of the most druggable binding site for the given protein structure.
    * Finding derivatives and structural analogs for the ligand. 
    * Using those analogs to perform docking calculations on the selected protein binding site.
    * Analyzing and vizualizing predicted protein–ligand interactions and binding modes for each analog.
    
    
* **Output**
    * New ligand structure(s) optimized for affinity and selectivity.


![Pipeline overview](images/sb_vs_pipeline.png)

*Figure 1*: General architecture of the automated structure-based virtual screening pipeline.


<a id='#Contents-in-Theory'></a>

### Contents in [*Theory*](#theory)

- [Drug design pipeline](#Drug-design-pipeline)
- [Binding site detection](#Binding-site-detection) 
- [Chemical similarity](#Chemical-similarity)
- [Molecular docking](#Molecular-docking)
- [Protein-ligand interactions](#Protein–ligand-interactions)
- [Visual inspection of docking results](#Visual-inspection-of-docking-results)

[comment]: <> (If you change a title, you must update the TOC label, to make cross-references functional on our website!)


<a id='Contents-in-Practical'></a>

### Contents in [*Practical*](#practical)

- [Outline of the virtual screening pipeline](#Outline-of-the-virtual-screening-pipeline)
- [Creating a new project](#Creating-a-new-project)
- [The input data](#The-input-data)
- [Processing the input protein data](#Processing-the-input-protein-data)
- [Processing the input ligand data](#Processing-the-input-ligand-data)
- [Binding site detection](#Binding-site-detection)
- [Ligand similarity search](#Ligand-similarity-search)
- [Molecular docking](#Molecular-docking)
- [Analysis of protein–ligand interactions](#Analysis-of-protein–ligand-interactions)
- [Selection of the best optimized ligand](#Selection-of-the-best-optimized-ligand)
- [Putting the pieces together: A fully automated pipeline](#Putting-all-the-pieces-together:-A-fully-automated-pipeline)

[comment]: <> (If you change a title, you must update the TOC label, to make cross-references functional on our website!)


### References

*Note:* due to the extensive references in each category, details are hidden by default.

<details>

<summary>Click here for a complete list of references </summary>

* TeachOpenCADD teaching platform
    1. Journal article on *TeachOpenCADD* teaching platform for computer-aided drug design: [D. Sydow *et al.*, *J. Cheminform.* **2019**, 11, 29.](https://doi.org/10.1186/s13321-019-0351-x)
    2. [*TeachOpenCADD* website](https://projects.volkamerlab.org/teachopencadd/index.html) at [Volkamer lab](https://volkamerlab.org/)
    3. This talktorial is inspired by the *TeachOpenCADD* talktorials T013-T017
* Drug design pipeline
    4. Book on drug design: [*G. Klebe*, *Drug Design*, Springer, **2013**.](https://doi.org/10.1007/978-3-642-17907-5)
    5. Review article on early stages of drug discovery: [Hughes *et al.*, *Br. J. Pharmacol.* **2011**, 162, 1239-1249.](https://doi.org/10.1111/j.1476-5381.2010.01127.x)
    6. Review article on computational drug design: [Sliwoski *et al.*, *Pharmacol. Rev.* **2014**, 66, 334-395.](https://doi.org/10.1124/pr.112.007336)
    7. Review article on computational drug discovery: [Leelananda *et al.*, *Beilstein J. Org. Chem.* **2016**, 12, 2694-2718.](https://doi.org/10.3762/bjoc.12.267)
    8. Review article on free software for building a virtual screening pipeline: [Glaab, *Brief. Bioinform.* **2016**, 17, 352-366.](https://doi.org/10.1093/bib/bbv037)
    9. Review article on automating drug discovery: [Schneider, *Nat. Rev. Drug Discov.* **2018**, 17, 97-113.](https://doi.org/10.1038/nrd.2017.232)
    10. Review article on structure-based drug discovery: [Batool *et al.*, *Int. J. Mol. Sci.* **2019**, 20, 2783.](https://doi.org/10.3390/ijms20112783)
* Binding site detection and the *DoGSiteScorer* program
    11. Book chapter on prediction and analysis of binding sites: [Volkamer *et al.*, *Applied Chemoinformatics*, Wiley, **2018**, pp. 283-311.](https://doi.org/10.1002/9783527806539.ch6g)
    12. Journal article on binding site and druggability predictions using *DoGSiteScorer*: [Volkamer *et al.*, *J. Chem. Inf. Model.* **2012**, *52*, 360-372.](https://doi.org/10.1021/ci200454v)
    13. Journal article describing the *ProteinsPlus* web-portal: [R. Fahrrolfes *et al.*, *Nucleic Acids Res.* **2017**, 45, W337-W343.](https://doi.org/10.1093/nar/gkx333)
    14. [*ProteinsPlus* website](https://proteins.plus/), and information regarding the usage of its *DoGSiteScorer* [REST-API](https://proteins.plus/help/dogsite_rest)
    15. *TeachOpenCADD* talktorial on binding site detection: [Talktorial T014](https://projects.volkamerlab.org/teachopencadd/talktorials/T014_binding_site_detection.html)
    16. *TeachOpenCADD* talktorial on querying online API web-services: [Talktorial T011](https://projects.volkamerlab.org/teachopencadd/talktorials/T011_query_online_api_webservices.html)
* Chemical similarity and the *PubChem* online database
    17. Review article on molecular similarity in medicinal chemistry: [G. Maggiora *et al.*, *J. Med. Chem.* **2014**, 57, 3186-3204.](https://doi.org/10.1021/jm401411z)
    18. Journal article on extended-connectivity fingerprints: [D. Rogers *et al.*, *J. Chem. Inf. Model.* **2010**, 50, 742-754.](https://doi.org/10.1021/ci100050t)
    19. Journal article describing the latest developments of the *PubChem* web-services: [S. Kim *et al.*, *Nucleic Acids Res.* **2019**, 47, D1102-D1109.](https://doi.org/10.1093/nar/gky1033)
    20. [*PubChem* website](https://pubchem.ncbi.nlm.nih.gov/), and information regarding the usage of its [APIs](https://pubchemdocs.ncbi.nlm.nih.gov/programmatic-access)
    21. Description of *PubChem*'s [custom substructure fingerprint](https://ftp.ncbi.nlm.nih.gov/pubchem/specifications/pubchem_fingerprints.pdf) and [*Tanimoto* similarity measure](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-016-0163-1) used in its similarity search engine.  
    22. *TeachOpenCADD* talktorial on compound similarity: [Talktorial T004](https://projects.volkamerlab.org/teachopencadd/talktorials/T004_compound_similarity.html)
    23. *TeachOpenCADD* talktorial on data acquisition from *PubChem*: [Talktorial T013](https://projects.volkamerlab.org/teachopencadd/talktorials/T013_query_pubchem.html)
* Molecular docking and the *Smina* program
    24. Review article on molecular docking algorithms: [X. Y. Meng *et al.*, *Curr. Comput. Aided Drug Des.* **2011**, 7, 146-157.](https://doi.org/10.2174/157340911795677602)
    25. Review article on different software used for molecular docking: [N. S. Pagadala *et al.*, *Biophys. Rev.* **2017**, 9, 91-102.](https://doi.org/10.1007/s12551-016-0247-1)
    26. Review article on evaluation and comparison of different docking algorithms: [G. L. Warren *et al*, *J. Med. Chem.* **2006**, 49, 5912-5931.](https://doi.org/10.1021/jm050362n)
    27. Review article on evaluation of ten docking programs on a diverse set of protein-ligand complexes: [Z. Wang *et al.*, *Phys. Chem. Chem. Phys.* **2016**, 18, 12964-12975.](https://doi.org/10.1039/C6CP01555G)
    28. Journal article describing the *Smina* docking program and its scoring function: [D. R. Koes *et al.*, *J. Chem. Inf. Model.* **2013**, 53, 1893-1904.](https://doi.org/10.1021/ci300604z) 
    29. [*OpenBabel* documentation](http://openbabel.org/wiki/Main_Page)
    30. [*Smina* documentation](https://sourceforge.net/projects/smina/)
    31. *TeachOpenCADD* talktorial on protein–ligand docking: [Talktorial T015](https://projects.volkamerlab.org/teachopencadd/talktorials/T015_protein_ligand_docking.html)
    32. Quantifying the chemical beauty of drugs: [G. Bickerton *et al.*, *Nat. Chem* **2012**, 4(2), 90-98.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3524573/)
* Protein-ligand interactions and the *PLIP* program
    33. Review article on protein-ligand interactions: [X. Du *et al.*, *Int. J. Mol. Sci.* **2016**, 17, 144.](https://doi.org/10.3390/ijms17020144)
    34. Journal article analyzing the types and frequencies of different protein-ligand interactions in available protein-ligand complex structures: [R. Ferreira de Freitas *et al.*, *Med. Chem. Commun.* **2017**, 8, 1970-1981.](https://doi.org/10.1039/C7MD00381A)
    35. Journal article describing the *PLIP* algorithm: [S. Salentin *et al.*, *Nucleic Acids Res.* **2015**, 43, W443-447.](https://doi.org/10.1093/nar/gkv315)
    36. [*PLIP* website](https://plip-tool.biotec.tu-dresden.de/plip-web/plip/index)
    37. [*PLIP* documentation](https://github.com/pharmai/plip)
    38. *TeachOpenCADD* talktorial on protein-ligand interactions: [Talktorial T016](https://projects.volkamerlab.org/teachopencadd/talktorials/T016_protein_ligand_interactions.html)
* Visual inspection of docking results and the *NGLView* program
    39. Journal article describing the NGLView program: [H. Nguyen *et al.*, *Bioinformatics* **2018**, 34, 1241-1242.](https://doi.org/10.1093/bioinformatics/btx789)
    40. [*NGLView* documentation](http://nglviewer.org/nglview/latest/api.html)
    41. *TeachOpenCADD* talktorial on advanced NGLView usage: [Talktorial T017](https://projects.volkamerlab.org/teachopencadd/talktorials/T017_advanced_nglview_usage.html)
</details>
