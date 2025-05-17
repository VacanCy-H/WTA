import random
import math
import time
from utils import calculate_threat

def simulated_annealing(data):
    num_weapons = data['num_weapons']
    num_targets = data['num_targets']
    
    # 初始化
    current = [random.randint(0, num_targets-1) for _ in range(num_weapons)]
    best = current.copy()
    best_threat = calculate_threat(current, data)
    
    start = time.time()
    temp = 1000
    cooling_rate = 0.95

    for _ in range(1000):
        # 生成邻居
        new = current.copy()
        idx = random.randint(0, num_weapons-1)
        new[idx] = random.randint(0, num_targets-1)
        
        # 计算威胁
        new_threat = calculate_threat(new, data)
        delta = new_threat - best_threat
        # 接受条件
        if delta < 0 or math.exp(-delta / temp) > random.random():
            current = new
            best_threat = new_threat
            best = current.copy()
        
        temp *= cooling_rate
    
    return best, best_threat, time.time()-start