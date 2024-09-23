import collections
import matplotlib.pyplot as plt
import read_kmers
from collections import Counter

from covxy import covx_covy

from constants import sshash, ggcat, needle, reindeer, kmindex, bqf, squeakr

def average(lst): 
    return sum(lst) / len(lst) 

def compute_histo(sshash, outil):
    if len(sshash) != len(outil):
        print(f"len(sshash) != len(outil)")
        exit()
    if len(sshash[0]) != len(outil[0]):
        print(f"len(sshash[0]) != len(outil[0])")
        exit()

    histo = {}

    
    for l1, l2 in zip(sshash, outil):
        for k1, k2 in zip(l1, l2):
            if k1 in histo:
                histo[k1].append(abs(k1-k2)**2)
            else:
                histo[k1] = [abs(k1-k2)**2]
    # print(histo)
    return histo
    

def compare(name, sshash, outil):
    if len(sshash) != len(outil):
        print(f"len(sshash) != len(outil)")
        exit()
    if len(sshash[0]) != len(outil[0]):
        print(f"len(sshash[0]) != len(outil[0])")
        exit()
    
    nb_kmers = len(sshash) * len(sshash[0])
    fpr = 0

    ok_rate = 0

    histo = compute_histo(sshash, outil)

    
    for l1, l2 in zip(sshash, outil):
        for k1, k2 in zip(l1, l2):
            # print(k1, k2)
            if k1 == 0 and k2 > 0:
                fpr += 1
            if k1 >0 and k1 == k2:
                ok_rate +=1
    for key in histo:
        histo[key] = average(histo[key])
    return fpr/nb_kmers, ok_rate/nb_kmers, histo

def main():
    sshash_res = read_kmers.parse_csv_file(sshash)
    ggcat_res = read_kmers.parse_csv_file(ggcat)
    needle_res = read_kmers.parse_csv_file(needle)
    reindeer_res = read_kmers.parse_csv_file(reindeer)
    kmindex_res = read_kmers.parse_csv_file(kmindex)
    bqf_res = read_kmers.parse_csv_file(bqf)
    squeakr_res = read_kmers.parse_csv_file(squeakr)

    # for name, outil in outils:
    #     fpr, ok_rate, histo = compare(sshash_res, outil)
    #     # print(fpr, ok_rate, histo)
    #     les_x, les_y = [], []
    #     for x in sorted(histo.keys()):
    #         les_x.append(x)
    #         les_y.append(histo[x])
    #     plt.bar(les_x, les_y, label=name)
    # plt.xlabel("True abundance of kmers")
    # plt.ylabel("Average of squared error")
    # plt.legend(loc="best")
    # plt.title("Average of squared error of kmers.")
    # plt.savefig("histo.png")
    # plt.clf()

    outils = [
        ("ggcat", ggcat_res),
        ("needle", needle_res),
        ("reindeer", reindeer_res),
        ("kmindex", kmindex_res),
        ("bqf", bqf_res),
        ("squeakr", squeakr_res)
    ]
    for name, outil in outils:
        fpr, ok_rate, histo = compare(name, sshash_res, outil)

        les_x, les_y = [], []
        for x in sorted(histo.keys()):
            les_x.append(x)
            les_y.append(histo[x])
        plt.bar(les_x, les_y, label=name)
        plt.xlabel("True abundance of kmers")
        plt.ylabel("Average of squared error")
        plt.legend(loc="best")
        plt.title(f"Average of squared error by {name}.")
        plt.savefig(f"graphs/histo_{name}.png")
        plt.clf()
    
    # print stats for each tool:
    print(r"\begin{table}")
    print(r"    \begin{tabular}{@{}cccc@{}}")
    print(r"        \toprule")
    print(r"        name & FPR(\%) & square\_of\_distance\_from\_truth & square\_of\_distance\_from\_truth\_present\_kmers")
    print(r"        \midrule")
    # flatten histo
    liste_distance = []
    for name, outil in outils:
        # compute the average square error for all kmers
        fpr, _, _ = compare(name, sshash_res, outil)
        histo = compute_histo(sshash_res, outil)
        for key in histo:
            res = histo[key]
            liste_distance.extend(res)
        nb_kmers = len(outil) * len(outil[0])
        avg_square_error_all_kmers = sum(liste_distance) / nb_kmers
        # compute the average square error for present kmers
        nb_kmers = 0
        for key in histo:
            if key:
                res = histo[key]
                nb_kmers += len(res)
                liste_distance.extend(res)
        avg_square_error_present_kmers = sum(liste_distance) / nb_kmers
        
        # square_of_distance_from_truth = average()
        print(f"        {name} & {fpr*100} & {avg_square_error_all_kmers:.2E} {avg_square_error_present_kmers:.2E}")
    print(r"        \bottomrule")
    print(r"    \end{tabular}")
    print(r"\end{table}")