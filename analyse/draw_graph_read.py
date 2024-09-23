import collections
import matplotlib.pyplot as plt

from covxy import covx_covy
import numpy as np
from constants import sshash, ggcat, needle, reindeer, kmindex, bqf, squeakr, k, alpha

# ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
colors = {
    "sshash": "#d62728",
    "ggcat": "#ff7f0e",
    "needle": "#1f77b4",
    "reindeer": "#2ca02c",
    "kmindex": "#9467bd",
    "bqf": "#8c564b",
    "squeakr" : "#e377c2",
}

# data[name] = (cov_x, cov_y, size_points)
covxy = {
    "sshash": covx_covy(sshash, k), 
    "ggcat": covx_covy(ggcat, k),
    "needle": covx_covy(needle, k),
    "reindeer": covx_covy(reindeer, k),
    "kmindex": covx_covy(kmindex, k),
    "bqf": covx_covy(bqf, k),
    "squeakr": covx_covy(squeakr, k)
}

covxy_log = {
    "sshash": covx_covy(sshash, k, log=True), 
    "ggcat": covx_covy(ggcat, k, log=True),
    "needle": covx_covy(needle, k, log=True),
    "reindeer": covx_covy(reindeer, k, log=True),
    "kmindex": covx_covy(kmindex, k, log=False),  # kmindex is already in log
    "bqf": covx_covy(bqf, k, log=True),
    "squeakr": covx_covy(squeakr, k, log=True)
}
    
def get_nb_row():
    with open(sshash, "r") as fichier:
        for ligne in fichier:
            ligne = ligne.strip().split()
            ligne = ligne[1:]
            return len(ligne)

def matrix(filename):
    matrix = []
    with open(filename, "r") as fichier:
        for i, ligne in enumerate(fichier):
            if i == 0:
                # skipping header
                continue
            ligne = ligne.strip().split()
            ligne = ligne[1:]  # remove name of read
            # print(ligne)
            ligne = [int(float(x)) for x in ligne]
            matrix.append(ligne)
    return matrix

def compute_histo(sshash_matrix, other_matrix):
    histo = {}
    for (ligne_sshash, ligne_other) in zip(sshash_matrix, other_matrix):
        for x_sshash, x_other in zip(ligne_sshash, ligne_other):
            if x_sshash in histo:
                histo[x_sshash].append(x_other)
            else:
                histo[x_sshash] = [x_other]
    keys = histo.keys()
    for x_sshah in keys:
        ligne = histo[x_sshah]
        ligne = collections.Counter(ligne)
        histo[x_sshah] = ligne
    return histo

def print_comparison(histo):
    sshash_values = list(histo.keys())
    sshash_values.sort()
    for sshash_value in sshash_values:
        print(str(sshash_value) + "\t" + str(histo[sshash_value]))
    # compute FPR
    nb_zero = 0
    nb_non_zero = 0
    if 0 in histo:
        zero_response = histo[0]
        for response in zero_response:
            nb_times = zero_response[response]
            if response == 0:
                nb_zero += nb_times
            else:
                nb_non_zero += nb_times
    print(nb_zero, nb_non_zero, nb_non_zero / (nb_zero + nb_non_zero))

def filter_out_0(covx, covy, sizes):
    filtered_covx, filtered_covy, filtered_sizes = [],[],[]
    for (x, y, size) in zip(covx, covy, sizes):
        if (x, y) != (0, 0): # TODO caution they are floats
            filtered_covx.append(x)
            filtered_covy.append(y)
            filtered_sizes.append(size)
    return filtered_covx, filtered_covy, filtered_sizes


def get_praph_size():
    """
    Get the coordinate of the corner of the graph. To do that, just plot the whole sshash graph and returns the coordinates.
    """
    cov_x, cov_y, size_points = covx_covy(sshash)
    plt.scatter(cov_x, cov_y, s=size_points)
    xlim = plt.xlim()
    ylim = plt.ylim()
    plt.clf()
    return xlim, ylim

def check_that_I_did_not_forget_a_name(names_to_plot, names_to_ignore=[]):
    expected_names = sorted(names_to_plot + names_to_ignore)

    if sorted(expected_names) != sorted(covxy.keys()):
        print("error: not all datasets are going to be plotted, some keys were forgotten")
        print("datasets available to plot:", sorted(covxy.keys()))
        print("plotting:", sorted(names_to_plot))
        print("explicitely ignoring:", sorted(names_to_ignore))
        exit()

def plot_legend():
    # place the legend and force the points in the legend to have the same size
    lgnd =plt.legend(loc="best")
    for handle in lgnd.legend_handles:
        handle.set_sizes([30.0])
        
def draw_complete_graph():
    names_to_plot = ["needle", "ggcat", "sshash", "reindeer", "kmindex", "bqf", "squeakr"]
    check_that_I_did_not_forget_a_name(names_to_plot)

    for name in names_to_plot:
        cov_x, cov_y, size_points = covxy[name]
        color = colors[name]
        plt.scatter(cov_x, cov_y, s=size_points, label=name, alpha=alpha, color=color)

    plot_legend()
    plt.xlabel("Proportion of bases covered by the positive k-mers of a query")
    plt.ylabel("Average abundance of k-mers from a query")
    plt.title("Coverage of queries according to benchmarked tools.")
    plt.savefig("graphs/bench_whole_graph.png")
    plt.clf()


def draw_not_0_graph():
    names_to_plot = ["needle", "ggcat", "sshash", "reindeer", "kmindex", "bqf", "squeakr"]
    check_that_I_did_not_forget_a_name(names_to_plot)

    for name in names_to_plot:
        cov_x, cov_y, size_points = filter_out_0(*covxy[name])
        color = colors[name]
        plt.scatter(cov_x, cov_y, s=size_points, label=name, alpha=alpha, color=color)

    plot_legend()
    plt.xlabel("Proportion of bases covered by the positive k-mers of a query")
    plt.ylabel("Average abundance of k-mers from a query")
    plt.title("Coverage of queries according to benchmarked tools.\nThe point (0,0) is excluded, to focus on the positive queries.")
    plt.savefig("graphs/bench_filtered_graph.png")
    plt.clf()

def draw_not_0_not_needle_graph():
    names_to_plot = ["ggcat", "sshash", "reindeer", "kmindex", "bqf", "squeakr"]
    names_to_not_plot = ["needle"]
    check_that_I_did_not_forget_a_name(names_to_plot, names_to_not_plot)
    
    for name in names_to_plot:
        cov_x, cov_y, size_points = filter_out_0(*covxy[name])
        size_points = [10*x for x in size_points]
        color = colors[name]
        plt.scatter(cov_x, cov_y, s=size_points, label=name, alpha=alpha, color=color)

    plot_legend()
    plt.xlabel("Proportion of bases covered by the positive k-mers of a query")
    plt.ylabel("Average abundance of k-mers from a query")
    plt.title("Coverage of queries according to benchmarked tools.\nThe point (0,0) and the tool Needle are excluded.")
    plt.savefig("graphs/bench_whole_graph_filtered_and_not_needle.png")
    # plt.show()
    plt.clf()

def draw_not_0_not_needle_log_graph():
    names_to_plot = ["ggcat", "sshash", "reindeer", "kmindex", "bqf", "squeakr"]
    names_to_not_plot = ["needle"]
    check_that_I_did_not_forget_a_name(names_to_plot, names_to_not_plot)
    
    for name in names_to_plot:
        cov_x, cov_y, size_points = filter_out_0(*covxy_log[name])
        size_points = [10*x for x in size_points]
        if name == "sshash":
            continue
        elif name == "reindeer":
            cov_x_sshash, cov_y_sshash, size_points_sshash = filter_out_0(*covxy_log["sshash"])
            size_points_sshash = [10*x for x in size_points_sshash]
            np.append(cov_x, cov_x_sshash)
            np.append(cov_y, cov_y_sshash)
            np.append(size_points, size_points_sshash)
            label="sshash and reindeer"
        else:
            # continue
            label = name
        color = colors[name]
        plt.scatter(cov_x, cov_y, s=size_points, label=label, alpha=alpha, color=color)

    plot_legend()
    plt.xlabel("Proportion of bases covered by the positive k-mers of a query")
    plt.ylabel("Average abundance of k-mers from a query")
    plt.title("Log of coverage of queries according to benchmarked tools.\nThe point (0,0) and the tool Needle are excluded.")
    plt.savefig("graphs/bench_whole_graph_filtered_and_not_needle_log.png")
    plt.clf()
    
def main():
    # sshash_matrix = matrix(sshash)
    # ggcat_matrix = matrix(ggcat)
    # needle_matrix = matrix(needle)
    # reindeer_matrix = matrix(reindeer)
    
    # cov_x, cov_y, size_points = covx_covy(sshash)
    # plt.scatter(cov_x, cov_y, s=size_points)
    # xlim = plt.xlim()
    # ylim = plt.ylim()
    # plt.savefig("covxy_SSHash.png")
    # plt.clf()

    # cov_x, cov_y, size_points = covx_covy(sshash, True)
    # plt.scatter(cov_x, cov_y, s=size_points)
    # plt.xlim(xlim)
    # plt.ylim(ylim)
    # plt.savefig("covxy_SSHash_filtered.png")
    # plt.clf()

    # cov_x, cov_y, size_points = filter_out_0(*covx_covy(sshash))

    # plt.scatter(cov_x, cov_y, s=size_points)
    # plt.xlim(xlim)
    # plt.ylim(ylim)
    # plt.savefig("covxy_SSHash_post_filtered.png")
    # plt.clf()

    # cov_x, cov_y, size_points = covx_covy(ggcat)
    # plt.scatter(cov_x, cov_y, s=size_points)
    # plt.xlim(xlim)
    # plt.ylim(ylim)
    # plt.savefig("covxy_ggcat.png")
    # plt.clf()

    # cov_x, cov_y, size_points = covx_covy(ggcat, True)
    # plt.scatter(cov_x, cov_y, s=size_points)
    # plt.xlim(xlim)
    # plt.ylim(ylim)
    # plt.savefig("covxy_ggcat_filtered.png")
    # plt.clf()

    # sshash_histo = compute_histo(sshash_matrix, sshash_matrix)
    # ggcat_histo = compute_histo(sshash_matrix, ggcat_matrix)
    # needle_histo = compute_histo(sshash_matrix, needle_matrix)
    # reindeer_histo = compute_histo(sshash_matrix, reindeer_matrix)

    draw_complete_graph()
    draw_not_0_graph()
    draw_not_0_not_needle_graph()
    draw_not_0_not_needle_log_graph()

    # print_comparison(sshash_histo)
    # print_comparison(ggcat_histo)
    # print_comparison(needle_histo)
    # print_comparison(reindeer_histo)

if __name__ == "__main__":
    main()