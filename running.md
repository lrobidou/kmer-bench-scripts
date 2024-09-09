# Instructions to run the tools
<!-- vscode-markdown-toc -->
* 1. [Before starting](#Beforestarting)
* 2. [REINDEER](#REINDEER)
* 3. [SSHash](#SSHash)
* 4. [kmindex](#kmindex)
* 5. [GGCAT](#GGCAT)
* 6. [BQF](#BQF)
* 7. [squeakr](#squeakr)
* 8. [Needle](#Needle)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
After the installation, running the tools is done using the scripts provided in the repository.

##  1. <a name='Beforestarting'></a>Before starting
- You must do a `chmod +x` on all files in `run_tools` before running them.  
- Always use absolute paths wahen using the scripts.
- `<DATA>` refers to the folder containing your fastq.gz files. This collection of scripts expect that each datasets is made of pairs of files, nameed `<NAME>_1.fastq.gz` and `<NAME>_2.fastq.gz`. Each name should be unique (one name should refer to one and only one pair of file). If there are not trainling `/` after `<DATA>`, do not put one in the command.
- `<TOOLS>` refers to the folder in which you cloned the git repositories of the tools when installing them 
- `<INDEXES>` refers to the folder in which you want to put the indexes. This repository should exists (i.e. run `mkdir <INDEXES>` before running the scripts).

Run `./run_tools/make_file_input_bcalm.sh <DATA>` to create the file of files necessary to run BCALM, which is used by REINDEER and SSHash in `<DATA>/bcalm_fof`.

##  2. <a name='REINDEER'></a>REINDEER
```bash
# run bcalm in parallel and place the output in a dedicated folder (one per bcalm)
# WARNING: there is a difference between run_bcalm_reindeer.sh and run_bcalm.sh. The two scripts does not use the same options for BCALM. Do not confuse them.
./run_tools/run_bcalm_reindeer.sh <DATA>/bcalm_fof <TOOLS>/bcalm_reindeer/build/bcalm <DATA>/bcalms_reindeer
# move the bcalm files out of their directory
./run_tools/move_bcalm_files_out_of_tmp.sh <DATA>/bcalms_reindeer
# remove the aforementioned folders
rm -r data/therese/bcalms_reindeer/*_tmp
# run REINDEER on the bcalms
./run_tools/run_REINDEER_from_BCALM.sh <DATA>/bcalms_reindeer <INDEXES>/REINDEER
```
Alternatively, one can run REINDEER directly from the reads, although it is slower
```bash
./run_tools/run_REINDEER_raw_reads.sh <DATA> <TOOLS>/REINDEER/Reindeer <INDEXES>
```

##  3. <a name='SSHash'></a>SSHash
```bash
# run bcalm in parallel and place the output in a dedicated folder (one per bcalm)
# WARNING: there is a difference between run_bcalm_reindeer.sh and run_bcalm.sh. The two scripts does not use the same options for BCALM. Do not confuse them.
./run_tools/run_bcalm.sh <DATA>/bcalm_fof <TOOLS>/bcalm_sshash/build/bcalm <DATA>/bcalms_sshash
# move the bcalm files out of their directory
./run_tools/move_bcalm_files_out_of_tmp.sh <DATA>/bcalms_sshash
# remove the aforementioned folders
rm -r data/therese/bcalms_sshash/*_tmp
# run UST
./run_tools/run_UST.sh <DATA>/bcalms_sshash <TOOLS>/UST_SSHash/ust
mv data/therese/bcalms_sshash/*_tmp/* data/therese/bcalms_sshash/
# remove temp folders after UST
rm -r data/therese/bcalms_sshash/*_tmp
# run SSHash
./run_tools/run_sshash.sh <DATA>/bcalms_sshash <TOOLS>/sshash/build/sshash <INDEXES>/sshash
# remove temp folders after SSHash
rm -r indexes/therese/sshash/*_tmp
```

##  4. <a name='kmindex'></a>kmindex
```bash
# you may see a warning if this is your first run, ignore it
./run_tools/run_kmindex.sh <DATA> <INDEXES>/kmindex
```

##  5. <a name='GGCAT'></a>GGCAT
You must first uncompress the fastq.gz into fasta. Place the `uncompress.sh` script into the <DATA> folder, and then run
```bash
./uncompress.sh 
```
Then:
```bash
./run_tools/run_create_GGCAT_colors.sh <DATA>  # create a file mapping color to fasta files
./run_tools/run_ggcat.sh <DATA>/GGCAT_color_mapping.in <INDEXES>   # run GGCAT
```

##  6. <a name='BQF'></a>BQF
```bash
# create a file of file for each dataset
./run_tools/run_prepare_kmc.sh <DATA>
# count k-mers using KMC
./run_tools/run_kmc.sh <DATA> <TOOLS>/kmc/bin/kmc <TOOLS>/kmc/bin/kmc_tools
# index k-mers and their counts
./run_tools/run_bqf.sh <DATA>/kmc <TOOLS>/bqf/build/bin/bqf <INDEXES>/BQF
```

##  7. <a name='squeakr'></a>squeakr
```bash
# create run ntCard to estimate the number of kmers in each dataset
./run_tools/run_ntcard.sh <DATA> <TOOLS>/ntCard/ntcard
# run squeakr using the estimation of the number of k-mer
./run_tools/run_squeakr.sh <DATA> <DATA>/ntcards <TOOLS>/squeakr/scripts/lognumslots.sh <TOOLS>/squeakr/squeakr <INDEXES>/squeakr
```

##  8. <a name='Needle'></a>Needle
```bash
./run_tools/run_needle.sh <DATA> <INDEXES>/needle <TOOLS>/needle/build-needle/bin/needle
```