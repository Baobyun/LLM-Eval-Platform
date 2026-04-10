import subprocess
import os
import pandas as pd


class PerformanceTester:
    def __init__(self, jmx_path, report_path):
        self.jmx_path = jmx_path  #  .jmx 脚本路径
        self.report_path = report_path  # 结果输出路径 (jtl文件)

    def run_pressure_test(self):
        """
        一键启动 JMeter 压测
        """
        print(f"正在启动压测脚本: {self.jmx_path}...")

        # 构造命令行指令: jmeter -n -t [脚本] -l [结果文件]
        # -n: 非GUI模式, -t: 指定脚本, -l: 记录采样结果
        command = f"jmeter -n -t {self.jmx_path} -l {self.report_path}"

        try:
            # 执行命令并等待完成
            subprocess.run(command, shell=True, check=True)
            print(f"压测完成,原始数据已保存至: {self.report_path}")
        except Exception as e:
            print(f"压测执行失败: {e}")

    def parse_tp99(self):
        """
        自动化解析 TP99 指标
        """
        # 读取 .jtl 里的毫秒数并排序取第99%个
        if not os.path.exists(self.report_path):
            print("找不到报告")
            return

        # 1. 加载数据(JTL 默认列名为 elapsed, label 等)
        df = pd.read_csv(self.report_path)

        # 2. 获取所有响应时间并排序
        latencies = df['elapsed'].sort_values()

        # 3. 计算 TP99 索引位置
        index = int(len(latencies) * 0.99) - 1
        tp99 = latencies.iloc[max(0, index)]

        # 4. 计算平均值对比
        avg = latencies.mean()

        print(f"--- 自动化性能报告 ---")
        print(f"总样本量: {len(latencies)}")
        print(f"平均响应 (Average): {avg:.2f} ms")
        print(f"TP99 指标: {tp99} ms")
        print(f"------------------------")
        return tp99


# 单独运行使用
# if __name__ == "__main__":  # 添加执行入口
#     # 实例化对象
#     tester = PerformanceTester(
#         jmx_path=r"E:\deepseek_test.jmx",
#         report_path=r"E:\report.jtl"
#     )
#
#     # 执行压测
#     tester.run_pressure_test()