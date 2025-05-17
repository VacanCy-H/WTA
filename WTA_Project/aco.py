import random
import numpy as np
import time
from utils import calculate_threat

def ant_colony(data, num_ants=10, iterations=50):
    num_weapons = data['num_weapons']
    num_targets = data['num_targets']
    
    # 构造信息素矩阵，先初始化为0.1
    pheromone = np.ones((num_weapons, num_targets)) * 0.1
    best = None
    best_threat = float('inf')
    
    start = time.time()
    for _ in range(iterations):
        # 蚂蚁构建解
        solutions = []
        for _ in range(num_ants):
            # 初始化蚂蚁分配表
            assignment = []
            for w in range(num_weapons):
                probs = pheromone[w] / pheromone[w].sum()
                assignment.append(np.random.choice(num_targets, p=probs))
            threat = calculate_threat(assignment, data)
            solutions.append((assignment, threat))
            
            if threat < best_threat:
                best = assignment
                best_threat = threat
        
        # 更新信息素
        pheromone *= 0.9
        for assign, threat in solutions:
            for w, t in enumerate(assign):
                pheromone[w][t] += 1/(threat + 1e-6)
                
    return best, best_threat, time.time()-start