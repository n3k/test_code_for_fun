"""
A non-empty array A consisting of N integers is given.

A peak is an array element which is larger than its neighbours. More precisely, it is an index P such that 0 < P < N − 1 and A[P − 1] < A[P] > A[P + 1].

For example, the following array A:
    A[0] = 1
    A[1] = 5
    A[2] = 3
    A[3] = 4
    A[4] = 3
    A[5] = 4
    A[6] = 1
    A[7] = 2
    A[8] = 3
    A[9] = 4
    A[10] = 6
    A[11] = 2

has exactly four peaks: elements 1, 3, 5 and 10.

You are going on a trip to a range of mountains whose relative heights are represented by array A, as shown in a figure below. You have to choose how many flags you should take with you. The goal is to set the maximum number of flags on the peaks, according to certain rules.

Flags can only be set on peaks. What's more, if you take K flags, then the distance between any two flags should be greater than or equal to K. The distance between indices P and Q is the absolute value |P − Q|.

For example, given the mountain range represented by array A, above, with N = 12, if you take:

        two flags, you can set them on peaks 1 and 5;
        three flags, you can set them on peaks 1, 5 and 10;
        four flags, you can set only three flags, on peaks 1, 5 and 10.

You can therefore set a maximum of three flags in this case.

Write a function:

    class Solution { public int solution(int[] A); }

that, given a non-empty array A of N integers, returns the maximum number of flags that can be set on the peaks of the array.

For example, the following array A:
    A[0] = 1
    A[1] = 5
    A[2] = 3
    A[3] = 4
    A[4] = 3
    A[5] = 4
    A[6] = 1
    A[7] = 2
    A[8] = 3
    A[9] = 4
    A[10] = 6
    A[11] = 2

the function should return 3, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..400,000];
        each element of array A is an integer within the range [0..1,000,000,000].
"""		
		
		
import random
N = random.randint(1,400000)
A = [random.randint(1,1000000000) for _ in xrange(N)]

#N = random.randint(1,20)
#A = [random.randint(1,1000) for _ in xrange(N)]

#A = [707, 110, 285, 469, 985, 867, 973, 83, 4, 799, 233, 712, 850, 424]
#N = len(A)

print(A)

def identify_peaks():
    # returns array of indexes into A
    peaks = []
    j = 1
    while j < N - 1:
        if A[j] > A[j-1] and A[j] > A[j+1]:
            peaks.append(j)
            # print(j, A[j])
            j = j + 2
        else:
            j = j + 1
    return peaks


def peaks_at_minimum_distance(peaks, distance):
    j = 1
    result = []
    while j < len(peaks):
        candidate = False
        for i in xrange(0, j):            
            if (peaks[j] - peaks[i]) >= distance:
                # Candidate, check the current vector
                candidate = True
                for k in result:
                    if abs(peaks[j] - k) < distance:
                        candidate = False
                        break
        if candidate:            
            result.append(peaks[j])
        j = j + 1
    if len(result) > 0:
        if result[0] - peaks[0] >= distance:
            result.append(peaks[0])
    return result
        

def calculate_flags_on_peaks():
    peaks = identify_peaks()
    print(peaks)
    peaks_count = len(peaks)
    if peaks_count <= 2:
        return peaks_count
    for i in xrange(2, peaks_count+1):
        nPeaksAtDistance = peaks_at_minimum_distance(peaks, i)
        #print(nPeaksAtDistance, i)
        if len(nPeaksAtDistance) < i:
            return i-1
    

flags = calculate_flags_on_peaks()
print("-> %d Flags!" % flags)
