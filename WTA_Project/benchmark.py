# benchmark.py
import os
import matplotlib.pyplot as plt
from utils import generate_data, load_data
from sa import simulated_annealing
from aco import ant_colony

def run_benchmark():
    # 创建目录
    os.makedirs("data", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    # 定义测试用例
    test_cases = [
        ("small", 10, 4),      # 小规模：10武器，4目标
        ("medium", 50, 20),    # 中规模：50武器，20目标
        ("large", 200, 50)     # 大规模：200武器，50目标
    ]

    results = []

    for case_name, weapons, targets in test_cases:
        # 生成/加载数据
        filename = f"data/{case_name}.json"
        if not os.path.exists(filename):
            generate_data(weapons, targets, filename)
        
        data = load_data(filename)
        print(f"\n=== 正在测试 {case_name} 规模 ===")
        print(f"武器数量: {weapons}, 目标数量: {targets}")

        # 运行算法
        sa_assignment, sa_threat, sa_time = simulated_annealing(data)
        aco_assignment, aco_threat, aco_time = ant_colony(data)

        results.append({
            "规模": case_name,
            "SA": {"威胁值": sa_threat, "时间": sa_time},
            "ACO": {"威胁值": aco_threat, "时间": aco_time}
        })

        # 打印当前结果
        print(f"[SA] 威胁: {sa_threat:.2f} 耗时: {sa_time:.2f}s")
        print(f"[ACO] 威胁: {aco_threat:.2f} 耗时: {aco_time:.2f}s")

    # 可视化结果
    plot_results(results)

def plot_results(results):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows系统可用
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 准备数据
    sizes = [r["规模"] for r in results]
    sa_threats = [r["SA"]["威胁值"] for r in results]
    aco_threats = [r["ACO"]["威胁值"] for r in results]
    sa_times = [r["SA"]["时间"] for r in results]
    aco_times = [r["ACO"]["时间"] for r in results]

    # 创建画布
    plt.figure(figsize=(12, 6))

    # 威胁值对比
    plt.subplot(1, 2, 1)
    bar_width = 0.35
    index = range(len(sizes))
    
    plt.bar(index, sa_threats, bar_width, label='SA', color='b', alpha=0.7)
    plt.bar([i + bar_width for i in index], aco_threats, bar_width, label='ACO', color='r', alpha=0.7)
    
    plt.xlabel('数据规模')
    plt.ylabel('剩余威胁值')
    plt.title('威胁值对比')
    plt.xticks([i + bar_width/2 for i in index], sizes)
    plt.legend()

    # 运行时间对比
    plt.subplot(1, 2, 2)
    plt.bar(index, sa_times, bar_width, label='SA', color='b', alpha=0.7)
    plt.bar([i + bar_width for i in index], aco_times, bar_width, label='ACO', color='r', alpha=0.7)
    
    plt.xlabel('数据规模')
    plt.ylabel('运行时间 (秒)')
    plt.title('运行时间对比')
    plt.xticks([i + bar_width/2 for i in index], sizes)
    plt.legend()

    # 保存和显示
    plt.tight_layout()
    plt.savefig("results/comparison.png")
    plt.show()

    # 打印表格结果
    print("\n=== 最终结果汇总 ===")
    print(f"{'规模':<10} | {'SA威胁值':<10} | {'SA时间':<10} | {'ACO威胁值':<10} | {'ACO时间':<10}")
    print("-"*60)
    for r in results:
        print(f"{r['规模']:<10} | {r['SA']['威胁值']:<10.2f} | {r['SA']['时间']:<10.2f} | "
              f"{r['ACO']['威胁值']:<10.2f} | {r['ACO']['时间']:<10.2f}")

if __name__ == "__main__":
    run_benchmark()