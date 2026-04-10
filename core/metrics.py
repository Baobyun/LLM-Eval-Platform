import numpy as np


class RagEvaluator:
    @staticmethod
    def calculate_hit_rate(hit_list):
        """
        计算命中率
        hit_list: [1, 0, 0] 表示检索了3条，第1条是正确的. hit_list 的长度随意
        """
        return 1.0 if sum(hit_list) > 0 else 0.0

    @staticmethod
    def calculate_ndcg(hit_list):
        """
        计算 nDCG (基于排名折损),
        """
        if not hit_list or sum(hit_list) == 0:
            return 0.0

        # 1. 计算实际的 DCG (Discounted Cumulative Gain)
        dcg = 0.0
        for i, hit in enumerate(hit_list): # 会自动遍历传入的列表长度，实现了动态 Top-K 的 nDCG。enumerate返回一个枚举对象，常用于需要同时访问索引和元素的场景
            if hit > 0:
                # 排名越靠后，分母 log 越大，得分越低 (折损)
                dcg += hit / np.log2(i + 2)

        # 2. 计算理想情况下的 IDCG (Ideal DCG)
        # 结果重新排序，把 1 全堆到前面，造一个理想模板
        sorted_hits = sorted(hit_list, reverse=True)

        # 初始化满分为 0
        idcg = 0.0

        # 计算这个理想模板能得多少分
        for i, hit in enumerate(sorted_hits):
            if hit > 0:
                # i+2 是为了防止 i=0 时 log2(1)=0 导致分母为 0 的崩溃
                idcg += hit / np.log2(i + 2)

        # 最终得分 = 实际分 / 满分
        return dcg / idcg if idcg > 0 else 0.0