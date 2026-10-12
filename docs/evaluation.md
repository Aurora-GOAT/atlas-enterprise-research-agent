# Retrieval evaluation report

The reported benchmark is **synthetic and source-labeled**, with 10 benchmark questions matched to six explicitly fictional business documents. Run `POST /api/evaluate/demo` or the web UI `质量评估` tab to reproduce.

Results are generated from actual local execution and are included below; **these numbers are not real-world task success, factual accuracy or validated time saved**.

**Local result:** Hit@3 = **100.0%**, MRR = **1.000**, N = **10**.

| # | Query | Hit@3 | Reciprocal rank |
|---:|---|:---:|---:|
| 1 | NeuroBridge 公司定位 创业团队 目标科室 | Yes | 1.000 |
| 2 | 目标医院600家 潜在客户市场 访谈 | Yes | 1.000 |
| 3 | 神经调控治疗计划软件 工程样机 临床疗效 注册 | Yes | 1.000 |
| 4 | 国产和进口品牌 竞品差异化 低价毛利 | Yes | 1.000 |
| 5 | 首年收入1350万元 现金跑道20个月 | Yes | 1.000 |
| 6 | 知识产权 注册风险 临床里程碑 风险预警 | Yes | 1.000 |
| 7 | 设备定价45万元 首年30台 | Yes | 1.000 |
| 8 | 每月烧钱120万元 账面现金2400万元 | Yes | 1.000 |
| 9 | 医院销售周期 远程维护服务 设备竞争 | Yes | 1.000 |
| 10 | 投后监测KPI 现金跑道不足12个月 | Yes | 1.000 |

**Interpretation:** This is a small, easy, artificial benchmark. High scores do not prove generalization or claim correctness. Future testing needs diverse public documents and a blind, human-labeled benchmark.
