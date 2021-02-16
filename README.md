# Boar taint variant analysis
Snakemake pipeline for the analysis of a series of variants involved with boar taint  
The variants belong to the genes described in "Robic A., Larzul C., Bonneau M.: Genetic and metabolic aspects of androstenone and skatole deposition in pig adipose tissue: a review. Genetics Selection Evolution 2008, 40:129–143"

The pipeline is a direct continuation of the Sus scrofa variant remapping pipeline (https://github.com/matteobolner/sscrofa_variant_remapping): starting from the remapped variant positions, those belonging to the genes identified to be involved with boar taint are selected and analysed.

For the variant effect prediction, the official Ensembl VEP Docker container was used (https://hub.docker.com/r/ensemblorg/ensembl-vep) in order to avoid compatibility problems and increase reproducibility.


**REQUIREMENTS TO RUN THE PIPELINE:**  
- Snakemake  
- Docker and singularity  

**Graph of the pipeline:**  
![alt text](https://raw.githubusercontent.com/matteobolner/boar_taint_variant_analysis/main/workflow/report/dag.svg)

**Workflow report**  
An HTML report of the pipeline is available in workflow/reports 

**TO DO:**
- improve report by adding more information about the results  
- push pipeline on workflowhub for better accessibility 
