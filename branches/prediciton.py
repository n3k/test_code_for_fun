

import random
import pickle

MAX_INT = 2**31 - 1
MIN_INT = -MAX_INT

NUM_INTS = 10_000_000

def generate_numbers():
    integers = [random.randint(MIN_INT, MAX_INT) for _ in range(NUM_INTS)]
    with open('integers.pkl', 'wb') as f:
        pickle.dump(integers, f)
    with open('integers_sorted.pkl', 'wb') as f:
        integers.sort()
        pickle.dump(integers, f)

def process(numbers):
    sum_of_elements_below_512 = 0
    total = 0

    for x in numbers:
        if x < 512:
            sum_of_elements_below_512 += x
        total += x

    return (sum_of_elements_below_512, total)


def load_and_process(sort=False):
    nums = None
    if sort:
        with open('integers_sorted.pkl', 'rb') as f:
            nums = pickle.load(f) 
    else:
        with open('integers.pkl', 'rb') as f:
            nums = pickle.load(f)     
    print(process(nums))


if __name__ == "__main__":
    #generate_numbers()
    load_and_process(sort=False)

# RUN WITH 
# perf stat -e branches,branch-misses -- python3 ./prediciton.py

''' UNSORTED
 Performance counter stats for 'python3 ./prediciton.py':

       749,782,159      cpu_atom/branches/u                                                     (2.36%)
     2,354,673,677      cpu_core/branches/u                                                     (97.64%)
        30,573,547      cpu_atom/branch-misses/u         #    4.08% of all branches             (2.36%)
        26,665,026      cpu_core/branch-misses/u         #    1.13% of all branches             (97.64%)

       0.762306161 seconds time elapsed

       0.653347000 seconds user
       0.106679000 seconds sys
'''

''' SORTED
 Performance counter stats for 'python3 ./prediciton.py':

       505,786,304      cpu_atom/branches/u                                                     (1.88%)
     2,332,296,144      cpu_core/branches/u                                                     (98.12%)
        20,446,032      cpu_atom/branch-misses/u         #    4.04% of all branches             (1.88%)
           454,045      cpu_core/branch-misses/u         #    0.02% of all branches             (98.12%)

       0.540974710 seconds time elapsed

       0.433873000 seconds user
       0.105700000 seconds sys
'''


''' GROK Analysis
Key Metrics Explained
Branches (cpu_atom/branches/u and cpu_core/branches/u):
These count the total number of branch instructions executed by the CPU (user-space only, as indicated by /u).
cpu_atom and cpu_core likely refer to different CPU cores or clusters (e.g., efficiency vs. performance cores in a heterogeneous architecture like Intel’s Alder Lake or ARM’s big.LITTLE).
Unsorted:
cpu_atom: ~749.8M branches (2.36% of total counter samples)
cpu_core: ~2.35B branches (97.64% of total counter samples)
Sorted:
cpu_atom: ~505.8M branches (1.88% of total counter samples)
cpu_core: ~2.33B branches (98.12% of total counter samples)
Observation: The sorted data has fewer total branches (~2.84B vs. ~3.10B), particularly on cpu_atom. This suggests the sorted dataset leads to fewer branch instructions, possibly due to more predictable control flow.
Branch Misses (cpu_atom/branch-misses/u and cpu_core/branch-misses/u):
These count branches that were incorrectly predicted by the CPU’s branch predictor, causing a pipeline stall and performance penalty.
The percentage next to branch misses indicates the miss rate (branch misses divided by total branches).
Unsorted:
cpu_atom: ~30.6M misses (4.08% miss rate)
cpu_core: ~26.7M misses (1.13% miss rate)
Sorted:
cpu_atom: ~20.4M misses (4.04% miss rate)
cpu_core: ~0.45M misses (0.02% miss rate)
Observation: The sorted dataset drastically reduces branch misses, especially on cpu_core (from 1.13% to 0.02%). The cpu_atom miss rate is nearly unchanged (~4%), suggesting its branch predictor is less sensitive to data ordering.
Execution Time:
Unsorted: 0.762 seconds elapsed (0.653s user, 0.107s sys)
Sorted: 0.541 seconds elapsed (0.434s user, 0.106s sys)
Observation: The sorted dataset runs ~29% faster (0.541s vs. 0.762s). This aligns with fewer branches and branch misses, reducing CPU pipeline stalls.
Why Does Sorting Improve Performance?
Branch prediction relies on patterns in control flow. When data is sorted:

More Predictable Branches: Sorted data often leads to monotonic access patterns, making conditional branches (e.g., if statements in loops) more predictable. For example, in a loop comparing adjacent elements, sorted data may consistently take the same branch path.
Fewer Misses on cpu_core: The cpu_core branch predictor (likely a more advanced one on performance cores) benefits significantly from sorted data, dropping the miss rate to near zero (0.02%). This suggests the predictor adapts well to the regular patterns in sorted data.
Reduced Branch Instructions: Fewer branches in the sorted case (especially on cpu_atom) indicate the algorithm may skip certain conditional paths or execute simpler control flow when data is ordered.
The cpu_atom cores, possibly efficiency cores with simpler predictors, show a high miss rate (~4%) in both cases, suggesting they struggle with the workload’s branching patterns regardless of sorting.
'''