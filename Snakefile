rule all:
    input:
        "data/stats/variants_in_v10.csv",
        "data/stats/number_of_variants_in_v10.txt",
        "data/stats/variants_in_v11.csv",
        "data/stats/number_of_variants_in_v11.txt",
        "data/taint_vcf/taint_variants.vcf",
        "data/stats/taint_variants_stats.csv",
        "data/stats/vcf_as_csv.csv"

rule get_variant_number_v10:
    input:
        genes = "data/starting_data/taint_genes.txt",
        coords = "data/starting_data/complete_coords_v10.csv"
    output:
        vars = "data/stats/variants_in_v10.csv",
        vars_number ="data/stats/number_of_variants_in_v10.txt"
    run:
        shell("grep -f {input.genes} {input.coords} > {output.vars}")
        shell("grep -f {input.genes} {input.coords} | wc -l > {output.vars_number}")

rule get_variant_number_v11:
    input:
        genes = "data/starting_data/taint_genes.txt",
        coords = "data/starting_data/remapped_and_verified_vars.csv"
    output:
        vars = "data/stats/variants_in_v11.csv",
        vars_number ="data/stats/number_of_variants_in_v11.txt"
    run:
        shell("grep -f {input.genes} {input.coords} > {output.vars}")
        shell("grep -f {input.genes} {input.coords} | wc -l > {output.vars_number}")

rule taint_ensembl_ids:
    input:
        genes = "data/starting_data/taint_genes.txt",
        coords = "data/stats/variants_in_v11.csv"
    output:
        ids = temp("data/starting_data/taint_ensembl_ids.csv")
    run:
        shell("cut -d ',' -f 5 {input.coords}  | sort -u > {output.ids}")


rule variants_in_vcf_by_ensembl_id:
    input:
        ids = "data/starting_data/taint_ensembl_ids.csv",
        vcf = "data/starting_data/vars_sscrofa11.vcf",
        header = "data/starting_data/updated_header.txt"
    output:
        taint_vcf = "data/taint_vcf/taint_variants.vcf"
    run:
        shell("cat {input.header} > {output.taint_vcf}")
        shell("grep -f {input.ids} {input.vcf} >> {output.taint_vcf}")

rule vcf_stats:
    input:
        "data/taint_vcf/taint_variants.vcf"
    output:
        "data/stats/taint_variants_stats.csv",
        "data/stats/vcf_as_csv.csv"
    script:
        "scripts/vcf_stats.py"
