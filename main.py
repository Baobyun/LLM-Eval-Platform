"""
一键自动化
"""
import subprocess
from core.performance import PerformanceTester
from core.metrics import RagEvaluator

def run_full_pipeline():
    # 执行性能压测
    tester = PerformanceTester(
        jmx_path=r"E:\deepseek_test.jmx",
        report_path=r"E:\report.jtl"
    )

    tester.run_pressure_test()

    # 自动计算并输出TP99
    tp99_score = tester.parse_tp99()

    # 模拟RAG精度评测
    mock_hits = [1, 0, 0, 1, 0]
    ndcg = RagEvaluator.calculate_ndcg(mock_hits)

    print(f"RAG 检索精度 (nDCG): {ndcg:.4f}")
    print("全链路评测任务完成,报告已生成。")


def generate_report():
    print(" 正在生成 Allure 自动化报表")

    # 1. 运行 pytest 并将结果存入 temp_results 文件夹
    subprocess.run("pytest tests/ --alluredir=./reports/allure_raw", shell=True)

    # 2. 将原始结果转化为 HTML 报表并自动打开
    subprocess.run("allure serve ./reports/allure_raw", shell=True)

if __name__ == "__main__":
    run_full_pipeline()
    generate_report()