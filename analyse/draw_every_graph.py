import draw_graph_read
import draw_graph_kmer
import draw_mustache
import draw_size
import draw_time
# import tabs_vs_bio

def main():
    draw_graph_read.main()
    draw_graph_kmer.main()
    draw_mustache.main()
    # tab, tab_log = tabs_vs_bio.main()
    # print(tab)
    # print(tab_log)
    

if __name__ == "__main__":
    main()