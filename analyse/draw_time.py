import matplotlib.pyplot as plt

# time taken by tools on Pfloyd
# tools_times_index = [
#     # CCLE
#     ("sshash", (("bcalm","84m31.682s"), ("ust","6m53.149s"), ("sshash", "9m7.286s"))),
#     ("REINDEER_reads", (("REINDEER_reads", "499m59.786s"),)),
#     ("REINDEER", (("bcalm", "137m40.659s"), ("REINDEER", "13m18.214s"))),
#     ("kmindex", (("kmindex", "64m22.768s"),)),
#     ("ggcat", (("decompression", "58m33.252s"), ("ggcat", "64m29.967s"))),
#     ("BQF", (("kmc", "39m5.432s"), ("BQF", "42m47.024s"))),
#     ("squeakr", (("ntcard", "16m14.893s"), ("squeakr", "14m16.983s"))),
#     ("needle", (("needle", "15m35.215s"),)),
# ]

tools_times_index = [
    # CCLE vs TARA
    ("sshash", (("bcalm","84m31.682s"), ("ust","6m53.149s"), ("sshash", "9m7.286s"))),
    ("TARA_sshash", (("bcalm","136m28.988s"), ("ust","21m43.200s"), ("TARA_sshash", "12m49.430s"))),

    ("REINDEER", (("bcalm", "137m40.659s"), ("REINDEER", "13m18.214s"))),
    ("TARA_REINDEER", (("bcalm", "231m2.888s"), ("TARA_REINDEER", "75m10.500s"))),

    ("kmindex", (("kmindex", "64m22.768s"),)),
    ("TARA_kmindex", (("TARA_kmindex", "53m18.354s"),)),
]


# # time taken by tools on Bielefeld's cluster
# tools_times_index_CCCLE = [
#     ("sshash", (("bcalm","160m51.425s"), ("ust","34m18.934s"), ("compression", "49m1.449s"), ("sshash", "48m35.938s"))),  # could be /10
#     ("REINDEER", (("REINDEER", "464m0.700s"),)),
#     ("bqf", (("kmc", "21m12.025s"), ("bqf", "99m30.911s"))),
#     ("squeakr", (("ntcard", "24m40.517s"), ("squeakr", "90m49.433s"))),

#     ("ggcat", (("decompression", "32m55.691s"),("ggcat", "28m3.426s"))),
#     ("needle", (("needle", "18m16.044s"),)),
#     ("kmindex", (("kmindex", "23m1.656s"),)),
# ]


def parse_time(time):
    time = time.removesuffix("s")
    minutes, seconds = time.split("m")
    minutes, seconds = float(minutes), float(seconds)
    return minutes * 60 + seconds

def main():
    bottom = [0] * len(tools_times_index)

    labels_to_color_and_seen = {
        "bcalm":("#1f77b4", False),
        "ust":("#ff7f0e", False),
        "decompression":("#2ca02c", False),
        "kmc":("#d62728", False),
        "ntcard":("#9467bd", False),
    }
    names = [name for (name, _times) in tools_times_index]
    for i, (name, steps_times) in  enumerate(tools_times_index):
        print(steps_times)
        for step, time in steps_times:
            time = parse_time(time)
            bars = [0] * len(tools_times_index)
            bars[i] = time
            color, label, hatch = None, step, None
            if step == name:
                color = "b"

                # if it is the first tool, add the label for the main step
                # else, don't repeat it
                if i == 0:
                    label = "main step"
                else:
                    label = None
                hatch = "/"
            else:
                color = labels_to_color_and_seen[step][0]
                label_already_seen = labels_to_color_and_seen[step][1]
                label = label if not label_already_seen else ""
                labels_to_color_and_seen[step]=(color, True)
            plt.bar(names, bars,bottom=bottom, label = label, color=color, hatch = hatch)
            bottom[i] += time
    plt.ylabel("time (in seconds)")
    plt.legend()

    plt.show()

if __name__ == "__main__":
    main()