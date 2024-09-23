The script `query_all.sh` can be used to query all constructed indexes.
The scripts creates the output folder (`<path_to_results_folder>`).
Recall that
- `<TOOLS>` refers to the folder in which you cloned the git repositories of the tools when installing them
- `<INDEXES>` refers to the folder in which you want to put the indexes.

Simply run:
```bash
./query_all.sh <path_to_results_folder> <QUERY.fa> <TOOLS> <INDEXES> | grep -v --fixed-strings "[squeakr_console] [error]"
```
You might see some output from some tools. Some tools (e.g. squeakr) emits errors in case of a negative k-mer (hence the `grep` in the command).

Ceck that everything is fine:
```bash
ls <path_to_results_folder>  # bqf  ggcat.jsonl  kmindex  needle.out  reindeer.txt  squeakr  sshash
```

Tools have different outputs. To analyse them, we must compute a common format.
The names of the files in the common format will be drown from REINDEER's output.
That is, `head <path_to_results_folder>/reindeer.txt -n 1`.

Compute the common format with:
```bash
./to_tsv/run.sh <path_to_results_folder> <QUERY.fa>
```
Results are store in the `to_tsv` folder.

To generate graphs, you first need to pass some values to the python scripts.
Run:
```bash
./analyse/generate_constants.sh to_tsv <K> <ALPHA> > analyse/constants.py
```
To generate the Python constants that will be used to generate the graphs. `<K>` is the size of k-mers and `<ALPHA>` is a value controlling the transparancy of some graph. Using 0.4 is recommanded.

Check values in `analyse/constants.py` and change the value of `k` or `alpha` if necessary.

Finally, running:
```bash
python analyse/draw_every_graph.py
```
Will draw graphs in the `graphs` folder.