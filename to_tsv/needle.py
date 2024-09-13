import argparse


def main():
    parser = argparse.ArgumentParser(description="BQF to tsv",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", help="needle output")
    parser.add_argument("-o", help="tsv file")
    parser.add_argument("-d", help="name of the datasets (first line of REINDEER's output)")
    args = parser.parse_args()

    needle_output_filename=args.i
    tsv_filename = args.o
    datasets_name = args.d

    datasets_name = datasets_name.split("\t")[1::] # ignoring the first entry in the REINDEER's output (which is "query")
    datasets_name = "\t".join(datasets_name)
    header = f"id_reads	{datasets_name}\n" 

    with open(tsv_filename, "w") as tsv:
        with open(needle_output_filename, "r") as needle_output:
            tsv.write(header)
            for ligne in needle_output:
                tsv.write(ligne)

if __name__ == "__main__":
    main()