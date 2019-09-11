import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def swap(A,i,j):
    if i != j:
        A[i], A[j] = A[j], A[i]

def bubblesort(A):
    if len(A) == 1:
        return
    swapped = True
    for i in range(len(A) - 1):
        if not swapped:
            break
        swapped = False
        for j in range(len(A) - 1 - i):
            if A[j] > A[j + 1]:
                swap(A, j, j + 1)
                swapped = True
            yield A

def insertionsort(A):
    for i in range(1, len(A)):
        j = i
        while j > 0 and A[j] < A[j - 1]:
            swap(A, j, j - 1)
            j -= 1
            yield A

def mergesort(A, start, end):
    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from mergesort(A, start, mid)
    yield from mergesort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A

def merge(A, start, mid, end):
    merged = []
    leftIdx = start
    rightIdx = mid + 1

    while leftIdx <= mid and rightIdx <= end:
        if A[leftIdx] < A[rightIdx]:
            merged.append(A[leftIdx])
            leftIdx += 1
        else:
            merged.append(A[rightIdx])
            rightIdx += 1

    while leftIdx <= mid:
        merged.append(A[leftIdx])
        leftIdx += 1

    while rightIdx <= end:
        merged.append(A[rightIdx])
        rightIdx += 1

    for i, sorted_val in enumerate(merged):
        A[start + i] = sorted_val
        yield A

def quicksort(A, start, end):
    if start >= end:
        return
    pivot = A[end]
    pivotIdx = start
    for i in range(start, end):
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            pivotIdx += 1
        yield A
    swap(A, end, pivotIdx)
    yield A

    yield from quicksort(A, start, pivotIdx - 1)
    yield from quicksort(A, pivotIdx + 1, end)





####################################################
##################### M A I N ###################### 
####################################################

print("\n\n####################################################")
print("          WELCOME TO SORTING VISUALIZER")
print("####################################################\n\n")


N = int(input("Enter number of integers you want to sort:\n"))

####################################################
######## GENERATING N RANDOM INTEGERS ##############
print("Generating random integers")
A = [x + 1 for x in range(N)]
random.seed(time.time())
random.shuffle(A)
#printing progress bar
for i in range(5):
    for j in range(i):
        print(".",end="")
    print()
#printing the array
print("\nNumbers generated are:\n")
print(A)

####################################################
################### D R I V E R ####################

print("\n####################################################\n")
speed_msg="Enter speed of sorting:\n\
            1/Fast\n\
            2/Medium\n\
            3/Slow\n\
            4/Manual\n\
C H O I C E:"
speed=input(speed_msg)

speedofSort=0
if speed=='1':
	speedofSort=10
elif speed=='2':
	speedofSort=100
elif speed=='3':
	speedofSort=500
elif speed=='4':
    speedofSort=int(input("Enter any value from 1 to 1000 in millisec\n\
                (1 being fastest,1000 being slowest)\n\
    S P E E D:"))
    if speedofSort<0:
        print("speed cannot be negative")
        exit()
else:
    print("INVALID CHOICE")
    exit()

print("\n####################################################\n")
sortChooser_msg = "Enter sorting method:\n\
                   1/Bubble Sort\n\
                   2/Insertion Sort\n\
                   3/Merge Sort\n\
                   4/Quick Sort\n\
C H O I C E:"
sortingSelection = input(sortChooser_msg)


if sortingSelection == "1":
    title = "Bubble sort"
    generator = bubblesort(A)

elif sortingSelection == "2":
    title = "Insertion sort"
    generator = insertionsort(A)

elif sortingSelection == "3":
    title = "Merge sort"
    generator = mergesort(A, 0, N - 1)

elif sortingSelection == "4":
    title = "Quicksort"
    generator = quicksort(A, 0, N - 1)

else:
    print("PLEASE SELECT 1,2,3 NEXT TIME")
    exit()

####################################################
######## SETTING UP MATPLOTLIB SUBPLOT #############
fig, ax = plt.subplots()
ax.set_title(title)
bar_rects = ax.bar(range(len(A)), A, align="edge")

ax.set_xlim(0, N)
ax.set_ylim(0, int(1.07 * N))


####################################################
################ SETTING UP LABELS #################
noOfOperations = ax.text(0.02, 0.95, "", transform=ax.transAxes)
timeTaken = ax.text(0.02, 0.91, "", transform=ax.transAxes)
interval= ax.text(0.02, 0.87, "Interval duration:"+str(speedofSort)+"ms", transform=ax.transAxes)

i = [0]
start_time=time.time()


####################################################
################ UPDATING THE FIG ##################
def update_fig(A, rects, i):
    for rect, val in zip(rects, A):
        rect.set_height(val)

    i[0] += 1
    noOfOperations.set_text("No. of operations:"+str(i[0]))
    # timeTaken.set_text("Time taken:"+str(time.time()-start_time)[:4]+"sec")
    time_elapsed=(time.time()-start_time)
    time_elapsed=float("{0:.2f}".format(time_elapsed))
    time_elapsed=str(time_elapsed)
    timeTaken.set_text("Time taken:"+time_elapsed+" sec")


####################################################
################ ANIMATING EACH FRAME ##############
anim = animation.FuncAnimation(fig, func=update_fig,
    fargs=(bar_rects, i), frames=generator, interval=speedofSort,
    repeat=False)
plt.show()
