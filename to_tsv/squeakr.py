import argparse
from os import listdir
from os.path import isfile, join


complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
def revcomp(seq):
    reverse_complement = "".join(complement.get(base, base) for base in reversed(seq))
    return reverse_complement


def main():
    parser = argparse.ArgumentParser(description="squeakr to tsv",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", help="squeakr index folder")
    parser.add_argument("-q", help="queried file (fasta)")
    parser.add_argument("-o", help="tsv file")
    parser.add_argument("-d", help="name of the datasets (first line of REINDEER's output)")
    args = parser.parse_args()

    mypath=args.i
    query_filename = args.q
    output_filename = args.o
    datasets_name = args.d

    datasets_name = datasets_name.split("\t")[1::] # ignoring the first entry in the REINDEER's output (which is "query")

    # first line of the tsv
    tsv_data = [["id_reads"] + datasets_name]

    # then, fill the tsv column by column
    
    # fill first column of the tsv (id_reads)
    with open(query_filename) as query_file:
        for ligne in query_file:
            ligne = ligne.strip()
            if ligne.startswith(">"):
                tsv_data.append([ligne])
    # fill every other column
    for dataset in datasets_name:
        kmers_in_this_dataset = {}
        query_output_filename = f"{mypath}/{dataset}.squeakr.output"
        with open(query_output_filename) as query_output_file:
            for ligne in query_output_file:
                ligne = ligne.strip()
                kmer, count = ligne.split()
                count = float(count)
                if kmer in kmers_in_this_dataset:
                    print("error: kmer are repeated in squeakr's output")
                    exit()
                kmers_in_this_dataset[kmer] = count
        # re read the query file to fill a column
        with open(query_filename) as query_file:
            i = 0
            for ligne in query_file:
                ligne = ligne.strip()
                if not ligne.startswith(">"):
                    i += 1
                    kmer = ligne
                    if kmer in kmers_in_this_dataset:
                        count = kmers_in_this_dataset[kmer]
                    elif revcomp(kmer) in kmers_in_this_dataset:
                        count = kmers_in_this_dataset[revcomp(kmer)]
                    else:
                        count = 0
                    tsv_data[i].append(str(count))
    
    with open(output_filename, "w") as output_file:
        for ligne in tsv_data:
            output_file.write("\t".join(ligne) + "\n")



if __name__ == "__main__":
    main()