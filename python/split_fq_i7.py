## import necessary modules
import sys
import gzip
import time

start_time = time.time()

read_file = sys.argv[1]
barcode_file = sys.argv[2]

lib_i7 = {}
n9 = ["sciMET_i7_1", "sciMET_i7_2", "sciMET_i7_3"]
mg = ["sciMET_i7_4", "sciMET_i7_5", "sciMET_i7_6"]
emn9 = ["sciMET_i7_8", "sciMET_i7_9"]
emmg = ["sciMET_i7_7"]


## create dictionary for seq and ids for each experimental group
with open(barcode_file, "r") as rf:
    for line in rf:
        line = line.strip()
        line = line.split("\t")
        ids, pos, seq = [line[i] for i in [0, 1, 2]]
        if pos == "1":

            lib_i7[ids] = seq

## processing the read file
## open reading and writing buffers
with gzip.open(read_file, "rt") as inf:
    with gzip.open("n9_passed_reads.fq.gz", "wt") as n9_wf:
        with gzip.open("mg_passed_reads.fq.gz", "wt") as mg_wf:
            with gzip.open("emn9_passed_reads.fq.gz", "wt") as emn9_wf:
                with gzip.open("emmg_passed_reads.fq.gz", "wt") as emmg_wf:
                    while True:
                        first_line = inf.readline()
                        barcode = first_line.split(":")[0][1:11]
                        read = inf.readline()
                        sep = inf.readline()
                        qual = inf.readline()
                        if len(first_line) == 0:
                            break
                        # print(len(barcode))
                        for key, value in lib_i7.items():
                            print(key)
                            print(value)
                            if barcode == value:
                                experiment_key = key
                        if experiment_key in n9:
                            n9_wf.write(first_line + read + sep + qual)
                        elif experiment_key in mg:
                            mg_wf.write(first_line + read + sep + qual)
                        elif experiment_key in emn9:
                            emn9_wf.write(first_line + read + sep + qual)
                        else:
                            emmg_wf.write(first_line + read + sep + qual)

stop_time = time.time()
time_taken = stop_time - start_time
print(time_taken)
