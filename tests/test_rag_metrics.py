import pytest  # 目前的 test_metrics_accuracy 看起来像个普通函数无装饰器，但只要文件名以 test_ 开头，Pytest 引擎就能识别并运行它
from core.metrics import RagEvaluator


def test_metrics_accuracy():
    # 情况 A：第一名就命中了
    case_a = [1, 0, 0, 0, 0]
    # 情况 B：最后一名才命中
    case_b = [0, 0, 0, 0, 1]  # 虚拟hit_list，真实的 RAG 系统中，hit_list 不是手写的，而是由测试代码对比标准答案生成的
    # 真实项目举例：
    # def get_hit_list_from_rag(query, expected_id, k=3):
    #     # 1. 模拟调用检索器，返回 k 条结果，即top-K的控制
    #     search_results = rag_system.search(query, top_k=k)
    #
    #     # 2. 自动化比对：中了一个就是 1，没中就是 0
    #     # 生成类似 [0, 1, 0] 的列表
    #     return [1 if doc.id == expected_id else 0 for doc in search_results]



    # 验证 Hit Rate：只要有 1，命中率就是 1
    assert RagEvaluator.calculate_hit_rate(case_a) == 1.0
    assert RagEvaluator.calculate_hit_rate(case_b) == 1.0

    # 验证 nDCG：情况 A 应该比情况 B 分数高
    score_a = RagEvaluator.calculate_ndcg(case_a)
    score_b = RagEvaluator.calculate_ndcg(case_b)

    print(f"排名第1命中得分: {score_a}")
    print(f"排名第5命中得分: {score_b}")

    assert score_a > score_b