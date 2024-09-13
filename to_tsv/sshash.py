import argparse
from os import listdir
from os.path import isfile, join


def main():
    parser = argparse.ArgumentParser(description="BQF to tsv",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", help="SSHash index folder")
    parser.add_argument("-o", help="tsv file")
    parser.add_argument("-d", help="name of the datasets (first line of REINDEER's output)")
    args = parser.parse_args()

    mypath=args.i
    csv_filename = args.o
    datasets_name = args.d

    datasets_name = datasets_name.split("\t")[1::] # ignoring the first entry in the REINDEER's output (which is "query")
    basenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    filenames= [mypath + "/" + basename for basename in basenames]
    filenames.sort()

    tab = []
    id_reads = [] 
    for filename in filenames:
        res = []
        with open(filename, "r") as fichier:
            for i, ligne in enumerate(fichier):
                ligne = ligne.strip()
                if i == 0:
                    continue
                if not ligne:
                    break
                if not ligne.startswith(">"):
                    res.append(int(ligne))
                else:
                    id_reads.append(ligne)
        tab.append(res)
    # print("all file parsed")    
    reverse = []
    for i in range(len(tab)):
        if len(tab[i]) != len(tab[0]):
            print(f"error: some files have different len (files 0 and {i})")
    for i in range(len(tab[0])):
        line = []
        for j in range(len(tab)):
            line.append(tab[j][i])
        reverse.append(line)
    # print("matrix rotated")
    with open(csv_filename, "w") as fichier:
        fichier.write("id_reads\t" + "\t".join(datasets_name) + "\n")
        for i, line in enumerate(reverse):
            fichier.write(f"{str(id_reads[i])}\t" + "\t".join([str(x) for x in line]) + "\n")
    # print("done")
    
if __name__ == "__main__":
    main()





