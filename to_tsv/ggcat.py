import argparse
import json

def get_id_reads(query):
    id_reads = []
    with open(query, "r") as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne.startswith(">"):
                id_reads.append(ligne)
    return id_reads


def main():
    parser = argparse.ArgumentParser(description="BQF to tsv",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", help="GGCAT output")
    parser.add_argument("-q", help="queried file (fasta)")
    parser.add_argument("-o", help="tsv file")
    parser.add_argument("-d", help="name of the datasets (first line of REINDEER's output)")
    args = parser.parse_args()

    ggcat_output=args.i
    query = args.q
    csv_filename = args.o
    datasets_name = args.d

    datasets_name = datasets_name.split("\t")[1::] # ignoring the first entry in the REINDEER's output (which is "query")
    matrix = []
    nb_read = 0
    with open(query, "r") as fichier:
        for ligne in fichier:
            nb_read += 1
    nb_read /= 2
    nb_read = int(nb_read)

    for _ in range(nb_read):
        matrix.append([0] * len(datasets_name))

    with open(ggcat_output, "r") as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne:
                data = json.loads(ligne)
                query_index = data["query_index"]
                matches = data["matches"]
                for match in matches:
                    val = matches[match]
                    match = int(match)
                    matrix[query_index][match] = val

    id_reads = get_id_reads(query)
    with open(csv_filename, "w") as fichier:
        fichier.write("id_reads\t" + "\t".join(datasets_name) + "\n")
        for i, line in enumerate(matrix):
            fichier.write(f"{str(id_reads[i])}\t" + "\t".join([str(x) for x in line]) + "\n")



if __name__ == "__main__":
    main()