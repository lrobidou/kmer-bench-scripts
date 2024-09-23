# Installations of tools
This markdown contains the commands to install the tools. Some of them require some other tools for preprocessing. Instructions to install these tools are available as well.

WARNING: Clone all the git repositories in a single folder (do not "spread them" accross your filesystem). This is necessary to run the scripts that run the tools.

<!-- vscode-markdown-toc -->
* 1. [REINDEER](#REINDEER)
	* 1.1. [BCALM for REINDEER](#BCALMforREINDEER)
	* 1.2. [REINDEER](#REINDEER-1)
* 2. [SSHash](#SSHash)
	* 2.1. [BCALM for SSHash](#BCALMforSSHash)
	* 2.2. [UST for SSHash](#USTforSSHash)
	* 2.3. [SSHash](#SSHash-1)
* 3. [kmindex](#kmindex)
* 4. [GGCAT](#GGCAT)
* 5. [KMC](#KMC)
* 6. [BQF](#BQF)
	* 6.1. [ntCard for BQF](#ntCardforBQF)
	* 6.2. [BQF](#BQF-1)
* 7. [squeakr](#squeakr)
* 8. [needle](#needle)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


##  1. <a name='REINDEER'></a>REINDEER
###  1.1. <a name='BCALMforREINDEER'></a>BCALM for REINDEER
```bash
git clone --recursive https://github.com/GATB/bcalm bcalm_reindeer
cd bcalm_reindeer/
git checkout --recurse-submodules 9b0f4a0f0d8cc7f78951c131819629cfb47f0165
conda create -p bcalm_env && conda activate ./bcalm_env && conda install anaconda::zlib
mkdir build;  cd build;  cmake ..;  make -j 8
```
###  1.2. <a name='REINDEER-1'></a>REINDEER
```bash
git clone --recursive https://github.com/kamimrcht/REINDEER.git
cd REINDEER
git checkout --recurse-submodules 7d3148fe5c24b4d777989e1cfa6f2b3df0ebc10f
make
```

##  2. <a name='SSHash'></a>SSHash
###  2.1. <a name='BCALMforSSHash'></a>BCALM for SSHash
```bash
git clone --recursive https://github.com/GATB/bcalm bcalm_sshash
cd bcalm_sshash
git checkout --recurse-submodules 28cb70489107e707562a4e39846f16ce17b83646
mkdir build;  cd build;  cmake ..;  make -j 8
```
###  2.2. <a name='USTforSSHash'></a>UST for SSHash
```bash
git clone --recursive https://github.com/jermp/UST UST_SSHash
cd UST_SSHash
git checkout --recurse-submodules b3d07107e52c68098dee590bb6823fe411e1b72d
make
```
###  2.3. <a name='SSHash-1'></a>SSHash
```bash
git clone --recursive https://github.com/lrobidou/sshash
cd sshash
git checkout --recurse-submodules 698dd03e74faa3aa24ef4c91cb6aeeb316e92ec3
mkdir build && cd build && cmake .. && make -j
```

##  3. <a name='kmindex'></a>kmindex
```bash
conda create -p kmindex_env
conda activate ./kmindex_env
conda install -c conda-forge -c tlemane kmindex
```

##  4. <a name='GGCAT'></a>GGCAT
```bash
git clone https://github.com/algbio/ggcat --recursive
cd ggcat
git checkout --recurse-submodules a91ecc97f286b737b37195c0a86f0e11ad6bfc3b
cargo install --path crates/cmdline/ --locked --features "kmer-counters"
```

##  5. <a name='KMC'></a>KMC
```bash
git clone --recursive https://github.com/refresh-bio/kmc
cd kmc
git checkout --recurse-submodules 65bff733bc6487e33f04ff134da50e6b7cb3031f
make -j32
```

##  6. <a name='BQF'></a>BQF
###  6.1. <a name='ntCardforBQF'></a>ntCard for BQF
```bash
git clone --recursive https://github.com/bcgsc/ntCard
cd ntCard/
git checkout --recurse-submodules 9433d03872380c13bb131abf1e388e94862a4f15
./autogen.sh
./configure
make
```
###  6.2. <a name='BQF-1'></a>BQF
```bash
git clone --recursive https://github.com/vicLeva/bqf
cd bqf
git checkout --recurse-submodules 4b534ec8c4736d041aab65ec481a26a708b790d4
mkdir build && cd build
cmake ..
make
```

##  7. <a name='squeakr'></a>squeakr
```bash
git clone --recursive https://github.com/splatlab/squeakr
cd squeakr
git checkout --recurse-submodules dcfaa18f267814d9e7d3437fbfc7348b869dab88
make squeakr
```

##  8. <a name='needle'></a>needle
```bash
git clone --recursive https://github.com/seqan/needle
cd needle
git checkout --recurse-submodules 00ab57de5e68c6abac65629cdda4a8c3ea967204
mkdir build-needle && cd build-needle
cmake .. # readme says "cmake ../needle", but its wrong
make
```
