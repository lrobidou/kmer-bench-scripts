import argparse


def get_kmindex_file(path):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    assert len(onlyfiles) == 1
    return path + "/" + onlyfiles[0]

def main():
    parser = argparse.ArgumentParser(description="kmindex to tsv",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", help="kmindex output folder")
    parser.add_argument("-o", help="tsv file")
    parser.add_argument("-d", help="name of the datasets (first line of REINDEER's output)")
    args = parser.parse_args()

    mypath=args.i
    csv_filename = args.o
    datasets_name = args.d

    kmindex_file = get_kmindex_file(mypath)

    first = True
    with open(csv_filename, "w") as out:
        with open(kmindex_file, "r") as fichier:
            for ligne in fichier:
                if first:
                    first = False
                    first_line = ligne.strip('\n')
                    assert datasets_name.split("\t")[1::] == first_line.split("\t")[1:: ]
                out.write(ligne)

if __name__ == "__main__":
    main()
