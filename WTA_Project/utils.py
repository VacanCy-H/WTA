import os
import json
import random
import numpy as np

def generate_data(num_weapons, num_targets, save_path):
    """生成测试数据"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    data = {
        "num_weapons": num_weapons,
        "num_targets": num_targets,
        "kill_prob": [[round(random.uniform(0.1, 0.9), 2) for _ in range(num_targets)] 
                      for _ in range(num_weapons)],
        "threat_values": [random.randint(1, 10) for _ in range(num_targets)]
    }
    with open(save_path, 'w') as f:
        json.dump(data, f)

def load_data(file_path):
    """加载数据"""
    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_threat(assignment, data):
    """计算剩余威胁"""
    survival = 1.0
    for target in range(data['num_targets']):
        prob = 1.0
        for weapon, t in enumerate(assignment):
            if t == target:
                prob *= (1 - data['kill_prob'][weapon][target])
        survival += data['threat_values'][target] * prob
    return survival