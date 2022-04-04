#use the pstats module to profile the program

import cProfile
import pstats

p=pstats.Stats("a_star_network_testing.txt")
p.strip_dirs().sort_stats("cumulative","name").print_stats(30)