def FIFO(pages, capacity):
    page_faults = 0
    memory = []
    outs = []

    for page in pages:
        if page not in memory:
            if len(memory) < capacity:
                memory.append(page)
            else:
                removed_page = memory.pop(0)
                memory.append(page)
                outs.append(removed_page)
            page_faults += 1

    return page_faults, outs


'''
result = FIFO([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3)
print("Page Faults:", result[0])
print("Pages that were replaced:", result[1])
'''

def LRU(pages, capacity):
    page_faults = 0
    memory = []
    outs = []

    for page in pages:
        if page not in memory:
            if len(memory) < capacity:
                memory.append(page)
            else:
                removed_page = memory.pop(0)
                memory.append(page)
                outs.append(removed_page)
            page_faults += 1
        else:
            # Move the accessed page to the end to show that it was recently used
            memory.remove(page)
            memory.append(page)

    return page_faults, outs

'''
result = LRU([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3)
print("Page Faults:", result[0])
print("Pages that were replaced:", result[1])
'''

def MRU(pages, capacity):
    page_faults = 0
    memory = []
    outs = []

    for page in pages:
        if page not in memory:
            if len(memory) < capacity:
                memory.append(page)
            else:
                removed_page = memory.pop(-1)
                memory.append(page)
                outs.append(removed_page)
            page_faults += 1
        else:
            # Move the accessed page to the end to show that it was recently used
            memory.remove(page)
            memory.append(page)

    return page_faults, outs

'''
result = MRU([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3)
print("Page Faults:", result[0])
print("Pages that were replaced:", result[1])
'''

def Clock(pages, capacity):
    page_faults = 0
    memory = []
    outs = []
    pointer = 0
    reference_bits = [0] * capacity

    for page in pages:
        if page not in memory:
            if len(memory) < capacity:
                memory.append(page)
                reference_bits[len(memory) - 1] = 1
            else:
                while reference_bits[pointer] == 1:
                    reference_bits[pointer] = 0
                    pointer = (pointer + 1) % capacity
                removed_page = memory[pointer]
                memory[pointer] = page
                reference_bits[pointer] = 1
                outs.append(removed_page)
                pointer = (pointer + 1) % capacity
            page_faults += 1
        else:
            index = memory.index(page)
            reference_bits[index] = 1

    return page_faults, outs

'''
result = Clock([1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3)
print("Page Faults:", result[0])
print("Pages that were replaced:", result[1])
'''