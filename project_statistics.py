import math

def mean(data: list) -> float:
    n = len(data)
    return sum(data)/n

def stdev(data: list) -> float:
    n = len(data)
    if n < 2:
        return 0.0
    mean_value = mean(data)
    variance = sum((x - mean_value) ** 2 for x in data) / (n - 1)
    return math.sqrt(variance)

def median(data: list) -> float:
    sorted = data.copy().sort()
    data_length = len(sorted)
    if data_length % 2:
        return sorted[math.floor(data_length/2)]
    else: 
        index = data_length/2
        return (sorted[index] + sorted[index - 1])/2
    
