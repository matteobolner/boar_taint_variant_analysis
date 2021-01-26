rule all:
    input:
        "data/stats/variants_in_v10.csv",
        "data/stats/number_of_variants_in_v10.txt",
        "data/stats/variants_in_v11.csv",
        "data/stats/number_of_variants_in_v11.txt",
        "data/taint_vcf/taint_variants.vcf",
        "data/stats/taint_variants_stats.csv",
        "data/stats/vcf_as_csv.csv",
        "data/taint_vcf/vcf_with_chr.vcf",
        "data/vep/vep_output.tsv",
        "data/vep/vep_output_comment_fixed.tsv",
        "data/vep/vep_and_samples.csv"

        #"data/vep/vep_output_comment_fixed.tsv",
        #+"data/vep/vep_and_samples.csv"


        #"data/vep/vep_output.tsv",
        #"data/vep/vep_output_comment_fixed.tsv",
        #'data/vep/vep_output_no_multiples.tsv'



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

rule change_chr_field_vcf:
    input:
        "data/taint_vcf/taint_variants.vcf"
    output:
        "data/taint_vcf/vcf_with_chr_noheader.vcf"
    script:
        "scripts/change_chr_field_vcf.py"

rule add_header_to_vcf:
    input:
        vcf = "data/taint_vcf/vcf_with_chr_noheader.vcf",
        header = "data/starting_data/updated_header.txt"
    output:
        "data/taint_vcf/vcf_with_chr.vcf"
    run:
        shell("cat {input.header} {input.vcf} > {output}")

rule prepare_vep_input:
    input:
        "data/taint_vcf/vcf_with_chr.vcf"
    output:
        "data/vep/vep_input.tsv"
    run:
        shell("grep -v '#' {input} | cut -f 1,2,3,4,5 > {output}")

rule vep_script:
    input:
        "data/taint_vcf/vcf_with_chr.vcf"
        #'data/vep/vep_input_no_multiples.tsv'
    output:
        #"data/vep/vep_output.tsv"
        'data/vep/vep_output.tsv'
    shell:
         "/usr/bin/perl5.30.3 /home/pelmo/data_and_pipelines/boar_taint_variant_analysis/scripts/ensembl-vep/vep --appris --biotype --buffer_size 5000 --check_existing --distance 5000 --mane --protein --sift b --species sus_scrofa --symbol --transcript_version --tsl --uniprot --cache --input_file {input} --output_file {output}"

rule change_comment_character:
    input:
        "data/vep/vep_output.tsv"
    output:
        "data/vep/vep_output_comment_fixed.tsv"
    shell:
        "sed 's/##/%/' {input} > {output}"

rule merge_vep_samples:
    input:
        "data/vep/vep_output_comment_fixed.tsv",
        "data/stats/taint_variants_stats.csv"
    output:
        "data/vep/vep_and_samples.csv"
    script:
        "scripts/vep.py"
