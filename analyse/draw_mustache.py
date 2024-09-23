import matplotlib.pyplot as plt
import read_kmers
import math
import covxy
from constants import sshash, ggcat, needle, reindeer, kmindex, bqf, squeakr ,k
from covxy import get_matrix_gouped_by_read

def mustache_kmer(truth_matrix, tool_matrix, filter_out_zero=False, errors_only=False):
    vector_to_plot = []
    for l_truth, l_tool in zip(truth_matrix, tool_matrix):
        for kmer_truth, kmer_tool in zip(l_truth, l_tool):
            if kmer_truth == 0 and kmer_tool == 0 and filter_out_zero:
                continue
            if errors_only:
                if kmer_truth == kmer_tool:
                    continue
            data_point = abs(kmer_truth - kmer_tool)**2
            vector_to_plot.append(data_point)
    return vector_to_plot

def mustache_reads(truth_matrix_grouped_by_reads, tool_matrix_grouped_by_reads, filter_out_zero=False, errors_only=False):
    vector_to_plot = []
    for read_truth, read_tool in zip(truth_matrix_grouped_by_reads, tool_matrix_grouped_by_reads):
        covx_truth = covxy.compute_covy(read_truth, k)
        covx_tool = covxy.compute_covy(read_tool, k)
        for covx_truth_specific_dataset, covx_tool_specific_dataset in zip(covx_truth, covx_tool):
            if covx_truth_specific_dataset == 0 and covx_tool_specific_dataset == 0 and filter_out_zero:
                continue
            if errors_only:
                if covx_truth_specific_dataset == covx_tool_specific_dataset:
                    continue
            data_point = abs(covx_truth_specific_dataset - covx_tool_specific_dataset)**2
            vector_to_plot.append(data_point)
    return vector_to_plot

def compute_log(tools):
    tools_log = []
    for name, tool in tools:
        tool_log = []
        for ligne in tool:
            tool_log.append([math.log2(x+1) for x in ligne])
        tools_log.append((name, tool_log))
    return tools_log
    
def compute_log_matrix_gouped_by_read(matrix_gouped_by_read):
    matrix_gouped_by_read_log = []
    for matrix_for_a_read in matrix_gouped_by_read:
        matrix_for_a_read_log = []
        for ligne_for_a_read in matrix_for_a_read:
            matrix_for_a_read_log.append([math.log2(x+1) for x in ligne_for_a_read])
        matrix_gouped_by_read_log.append(matrix_for_a_read_log)
    return matrix_gouped_by_read_log

def compute_log_reads(list_name_and_matrix_gouped_by_read):
    list_name_and_matrix_gouped_by_read_log = []
    for name, matrix_gouped_by_read in list_name_and_matrix_gouped_by_read:
        matrix_gouped_by_read_log = compute_log_matrix_gouped_by_read(matrix_gouped_by_read)
        list_name_and_matrix_gouped_by_read_log.append((name, matrix_gouped_by_read_log))
    return list_name_and_matrix_gouped_by_read_log


#######################
# MUSTACHES for kmers #
#######################

def draw_kmers_mustache_all_points(sshash_res, tools):
    names = []
    data = []

    for name, res in tools:
        names.append(name)
        data.append(mustache_kmer(sshash_res, res, filter_out_zero=False, errors_only=False))

    plt.boxplot(data)
    plt.xticks([y + 1 for y in range(len(data))], labels=names)
    plt.title("Average square of errors of tools compared to SSHash.")
    plt.savefig("graphs/mustaches/kmers/mustaches_kmer_all_points.png")
    plt.clf()

def draw_kmers_mustache_errors(sshash_res, tools):
    names = []
    data = []

    for name, res in tools:
        names.append(name)
        data.append(mustache_kmer(sshash_res, res, filter_out_zero=False, errors_only=True))

    plt.boxplot(data)
    plt.xticks([y + 1 for y in range(len(data))], labels=names)
    plt.title("Average square of errors of tools compared to SSHash.\nCorrect answers are filtered out.")
    plt.savefig("graphs/mustaches/kmers/mustaches_kmer_error_points.png")
    plt.clf()

def draw_kmers_mustache_errors_no_needle(sshash_res, tools):
    names = []
    data = []

    for name, res in tools:
        if name == "needle":
            continue
        names.append(name)
        data.append(mustache_kmer(sshash_res, res, filter_out_zero=False, errors_only=True))

    plt.boxplot(data)
    plt.xticks([y + 1 for y in range(len(data))], labels=names)
    plt.title("Average square of errors of tools compared to SSHash.\nCorrect answers are filtered out.")
    plt.savefig("graphs/mustaches/kmers/mustaches_kmer_error_points_no_needle.png")
    plt.clf()

def draw_kmers_mustache_errors_log(sshash_res, tools):
    names = []
    data = []

    for name, res in tools:
        names.append(name)
        data.append(mustache_kmer(sshash_res, res, filter_out_zero=False, errors_only=True))

    plt.boxplot(data)
    plt.xticks([y + 1 for y in range(len(data))], labels=names)
    plt.title("Average square of errors of log response of tools compared to SSHash.\nCorrect answers are filtered out.")
    plt.savefig("graphs/mustaches/kmers/mustaches_kmer_error_points_logs.png")
    plt.clf()

#######################
# MUSTACHES for reads #
#######################

def draw_reads_mustache_all_points(sshash_res, tools):
    names = []
    data = []

    for name, res in tools:
        names.append(name)
        data.append(mustache_reads(sshash_res, res, filter_out_zero=False, errors_only=False))

    plt.boxplot(data)
    plt.xticks([y + 1 for y in range(len(data))], labels=names)
    plt.title("Average square of errors of tools compared to SSHash.")
    plt.savefig("graphs/mustaches/reads/mustaches_read_all_points.png")
    plt.clf()


def draw_reads_mustache_errors(sshash_res, tools):
    names = []
    data = []

    for name, res in tools:
        names.append(name)
        data.append(mustache_reads(sshash_res, res, filter_out_zero=False, errors_only=True))

    plt.boxplot(data)
    plt.xticks([y + 1 for y in range(len(data))], labels=names)
    plt.title("Average square of errors of tools compared to SSHash.\nCorrect answers are filtered out.")
    plt.savefig("graphs/mustaches/reads/mustaches_read_error_points.png")
    plt.clf()

def draw_reads_mustache_errors_no_needle(sshash_res, tools):
    names = []
    data = []

    for name, res in tools:
        if name == "needle":
            continue
        names.append(name)
        data.append(mustache_reads(sshash_res, res, filter_out_zero=False, errors_only=True))

    plt.boxplot(data)
    plt.xticks([y + 1 for y in range(len(data))], labels=names)
    plt.title("Average square of errors of tools compared to SSHash.\nCorrect answers are filtered out.")
    plt.savefig("graphs/mustaches/reads/mustaches_read_error_points_no_needle.png")
    plt.clf()

def draw_reads_mustache_errors_log(sshash_res, tools):
    names = []
    data = []

    for name, res in tools:
        names.append(name)
        data.append(mustache_reads(sshash_res, res, filter_out_zero=False, errors_only=True))

    plt.boxplot(data)
    plt.xticks([y + 1 for y in range(len(data))], labels=names)
    plt.title("Average square of errors of log response of tools compared to SSHash.\nCorrect answers are filtered out.")
    plt.savefig("graphs/mustaches/reads/mustaches_read_error_points_logs.png")
    plt.clf()


###################
# Draw all graphs #
###################

def draw_graph_kmers():
    sshash_res = read_kmers.parse_csv_file(sshash)
    ggcat_res = read_kmers.parse_csv_file(ggcat)
    needle_res = read_kmers.parse_csv_file(needle)
    reindeer_res = read_kmers.parse_csv_file(reindeer)
    kmindex_res = read_kmers.parse_csv_file(kmindex)
    bqf_res = read_kmers.parse_csv_file(bqf)
    squeakr_res = read_kmers.parse_csv_file(squeakr)
    tools = [
        ("ggcat", ggcat_res),
        ("needle", needle_res),
        ("reindeer", reindeer_res),
        # ("kmindex", kmindex_res),
        ("bqf", bqf_res),
        ("squeakr", squeakr_res)
    ]

    # draw mustaches for kmers, in "not log" space
    draw_kmers_mustache_all_points(sshash_res, tools)
    draw_kmers_mustache_errors(sshash_res, tools)
    draw_kmers_mustache_errors_no_needle(sshash_res, tools)

    # transform data into log space, except for kmindex
    sshash_res_log = [[math.log2(x+1) for x in ligne] for ligne in sshash_res]
    tools_log = compute_log(tools)
    # add kmindex into the data
    tools_log.append(("kmindex", kmindex_res))

    # draw mustaches for kmers, in "log" space
    draw_kmers_mustache_errors_log(sshash_res_log, tools_log)

def draw_graph_reads():
    sshash_res = get_matrix_gouped_by_read(sshash)
    tools = [
        ("ggcat", get_matrix_gouped_by_read(ggcat)),
        ("needle", get_matrix_gouped_by_read(needle)),
        ("reindeer", get_matrix_gouped_by_read(reindeer)),
        ("bqf", get_matrix_gouped_by_read(bqf)),
        ("squeakr", get_matrix_gouped_by_read(squeakr))
    ]

    draw_reads_mustache_all_points(sshash_res, tools)
    draw_reads_mustache_errors(sshash_res, tools)
    draw_reads_mustache_errors_no_needle(sshash_res, tools)

    # transform data into log space, except for kmindex
    sshash_res_log = compute_log_matrix_gouped_by_read(sshash_res)
    tools_log = compute_log_reads(tools)
    # add kmindex into the data
    tools_log.append(("kmindex", get_matrix_gouped_by_read(kmindex)))
    # draw mustaches for kmers, in "log" space
    draw_reads_mustache_errors_log(sshash_res_log, tools_log)

def main():
    draw_graph_kmers()
    draw_graph_reads()
    # matrix = 

    # les_x, les_y = [], []
    # for matrix_for_a_read in matrix:
    #     # get a coverage for each dataset 
    #     coverages = compute_covx(matrix_for_a_read, k)

    # draw_histo_errors_no_needle(sshash_res, tools)

