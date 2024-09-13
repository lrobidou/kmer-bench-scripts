import argparse
from os import listdir
from os.path import isfile, join

def compute_kmer_per_read(query_filepath):
    kmer_per_read = []
    id_read, n = None, 0
    with open(query_filepath, "r") as query_file:
        for ligne in query_file:
            ligne = ligne.strip()
            if ligne.startswith(">"):
                print(id_read, ligne)
                if id_read == None:
                    id_read = ligne
                    n = 1
                elif ligne == id_read:
                    n += 1
                else:
                    id_read = ligne
                    kmer_per_read.append(n)
                    n = 1
    return kmer_per_read
                

def filter_read_id(string_iter):
    for s in string_iter:
        if s.startswith(">"):
            yield s

def filter_not_blank_line(string_iter):
    for s in string_iter:
        if s.strip():
            yield s

def count_nb_line(filepath):
    n = 0
    with open(filepath, "r") as fichier:
        for ligne in fichier:
            n += 1
    return n

def read_ids(query_filepath):
    with open(query_filepath, "r") as query_file:
        for ligne in query_file:
            ligne = ligne.strip()
            if ligne.startswith(">"):
                yield ligne

def main():
    parser = argparse.ArgumentParser(description="BQF to tsv",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", help="BQF index folder")
    parser.add_argument("-q", help="queried file (fasta)")
    parser.add_argument("-o", help="tsv file")
    parser.add_argument("-d", help="name of the datasets (first line of REINDEER's output)")
    args = parser.parse_args()

    mypath=args.i
    query = args.q
    csv_filename = args.o
    datasets_name = args.d

    datasets_name = datasets_name.split("\t")[1::] # ignoring the first entry in the REINDEER's output (which is "query")
    filenames= [mypath + "/" + basename + ".bqf.txt" for basename in datasets_name]

    nb_line = int(count_nb_line(query) / 2)
    matrix = []
    for _ in range(nb_line):
        matrix.append([None] * len(filenames))

    for i, filename in enumerate(filenames):
        with open(filename, "r") as query_result_file, open(query, "r") as query_file:

            # TODO: bqf results files are weird
            query_result_file = list(filter_not_blank_line(query_result_file))[:-1]
            query_file = filter_read_id(query_file)
            for j, (ligne_result, read) in enumerate(zip(query_result_file, query_file, strict=True)):
                ligne_result = ligne_result.strip()
                read = read.strip()
                # results should be in form of "Sequence1190 : (min:0, max:0, average:0, presence ratio:0)"
                # extract the average
                if not ligne_result.startswith("Sequence"):
                    print("result line is ill-formed:")
                    print(ligne_result)
                    exit()
                average = ligne_result.split(",")[2].strip()  # "average:0"
                average = average.split(":")[1]  # "0"
                average = int(average)
                matrix[j][i] = average

    with open(csv_filename, "w") as fichier:
        fichier.write("id_reads\t" + "\t".join(datasets_name) + "\n")
        for results, read_id in zip(matrix, read_ids(query), strict=True):
            fichier.write(read_id + " \t" + "\t".join((str(x) for x in results)) + "\n")
    
if __name__ == "__main__":
    main()





