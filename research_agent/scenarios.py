"""Cross-industry portfolio scenarios: every example below is FICTIONAL."""
from __future__ import annotations

SCENARIOS = {
    "healthcare": {
        "label":"医疗科技 · 产品与市场研究",
        "company":"NeuroBridge Medical（虚构）",
        "prompt":"研究 NeuroBridge Medical 的技术、客户、竞争、财务与核心风险，列出需要人工核实的问题。",
        "steps":[
            ("technology","技术与产品","技术 产品 研发 临床 疗效 工艺 技术壁垒 产品管线"),
            ("market","市场与客户","市场规模 目标客户 患者 需求 销量 渠道 增长"),
            ("competition","竞争与商业模式","竞争 对手 竞品 定价 收入 商业模式 替代"),
            ("risk","风险与合规","风险 注册 法规 合规 专利 现金流"),
            ("milestone","行动计划与里程碑","里程碑 计划 时间 试点 监管 交付 投后"),
        ],
        "documents":None,
        "cases":None,
    },
    "consumer": {
        "label":"消费品牌 · 竞品与增长策略",
        "company":"LumenLeaf（虚构生活方式品牌）",
        "prompt":"分析 LumenLeaf 的消费者画像、渠道表现、竞品价格、营销效率和增长风险，提出下一步验证清单。",
        "steps":[
            ("audience","客户与需求洞察","消费者 目标客群 用户需求 复购 反馈 客单价"),
            ("channels","渠道与转化漏斗","电商 渠道 访问 转化 订单 GMV 退货"),
            ("competitors","竞品与品牌定位","竞品 价格 促销 定位 差异化 市场"),
            ("economics","经营效率与单位经济","毛利率 获客成本 CAC 投放 ROAS 费用"),
            ("experiments","风险与增长实验","风险 库存 试验 AB测试 假设 迭代 验证"),
        ],
        "documents":[
            ("brand-profile","品牌定位与消费者调研（合成）","虚构品牌LumenLeaf销售可重复使用的生活方式水杯。模拟用户访谈摘要：主要消费者为22–35岁城市白领与户外活动爱好者；购买动机包括设计、便携及清洁便利。当前问卷样本偏向自有社群，不能代表全部市场。用户反馈：保温能力受认可，但杯盖漏水问题仍待验证。"),
            ("brand-channels","渠道运营月报（合成）","虚构2026年8月渠道运营月报：官方电商访问量100000次、下单2100笔、转化率2.1%；线下快闪活动意向客户600人、现场成交54笔。平均订单金额129元；线上退货率8%。各渠道统计口径不同，不能直接推断增量因果。"),
            ("brand-competition","竞品与定价研究（合成）","虚构竞品调研：A牌售价119元，主打性价比；B牌售价159元，主打设计感。LumenLeaf标准款售价129元。竞品折扣频率每季波动，样本仅限指定店铺的公开商品页截面；需继续核对材料、漏水性能与真实评分。"),
            ("brand-economics","投放与运营风险记录（合成）","虚构财务数据：本月广告费用42000元，归因订单700笔，简单获客成本CAC约60元/笔；ROAS按归因销售额计算约2.15，但归因方式可能重复计数。单品毛利率为43%，渠道费用和退款后净利润未核算。主要风险：退货、漏水投诉、库存积压。建议A/B测试详情页的容量卖点和漏水说明。"),
        ],
        "cases":[
            ("消费者22到35岁 白领 水杯 漏水投诉","brand-profile"),
            ("渠道访问100000次 2100单 转化率2.1%","brand-channels"),
            ("快闪600个意向 54单 线下转化","brand-channels"),
            ("A牌119元 B牌159元 LumenLeaf129元","brand-competition"),
            ("广告42000元 CAC 60 ROAS 2.15","brand-economics"),
            ("毛利率43% 退货 库存积压风险","brand-economics"),
        ],
    },
    "procurement":{
        "label":"企业采购 · 供应商评估",
        "company":"Northstar Operations（虚构采购团队）",
        "prompt":"对比 Northstar Operations 的候选供应商在报价、交期、质量、履约风险上的差异，并列出需要采购经理人工确认的条款。",
        "steps":[
            ("requirements","需求与采购约束","需求 采购 规格 验收 SLA 交付 数量"),
            ("quotes","报价与总拥有成本","供应商 报价 单价 物流 维护 TCO 成本"),
            ("delivery","交付与产能","交期 供货 产能 延误 库存 起订量"),
            ("quality","质量、服务与合规","质量 缺陷 验收 售后 合规 审计"),
            ("recommendation","风险与决策待办","风险 付款 合同 备选 试单 人工确认"),
        ],
        "documents":[
            ("procurement-rfq","采购需求与验收标准（合成）","虚构采购团队Northstar Operations计划采购800台手持条码扫描器。要求电池续航不少于10小时、首批交付不晚于30天、缺陷率低于1%、提供12个月保修及明确退换货规则。正式采购前须审核信息安全和供应商资质。"),
            ("procurement-alpha","供应商Alpha报价与交期（合成）","虚构供应商Alpha：每台报价680元，800台设备合计544000元，运输费8000元；预计交付21天，最低起订量500台，保修12个月；历史抽检缺陷率0.8%。付款条款为30%预付款、70%验收后支付。历史缺陷率并非本批次合格保证。"),
            ("procurement-beta","供应商Beta报价与交期（合成）","虚构供应商Beta：每台报价630元，800台设备合计504000元，运输费25000元；预计交付45天，最低起订量200台，保修6个月；历史抽检缺陷率1.4%。付款条款为50%预付款、50%发货前支付。报价未涵盖保修期外维护成本。"),
            ("procurement-risk","供应商风险审查纪要（合成）","虚构风险审查：Alpha满足30天交期和缺陷率门槛，但报价高；Beta价格低但交期45天且缺陷率1.4%，不满足本次硬约束。需向双方索取第三方质检报告、质量体系证书、数据安全说明及违约赔偿条款，试单后再作最终决策。"),
        ],
        "cases":[
            ("采购800台扫描器 续航10小时 30天交货","procurement-rfq"),
            ("验收缺陷率低于1% 保修12个月","procurement-rfq"),
            ("Alpha 680元 800台运输费8000元 21天","procurement-alpha"),
            ("Beta 630元运输费25000元交期45天","procurement-beta"),
            ("Alpha 缺陷率0.8% 预付款30%","procurement-alpha"),
            ("Beta 缺陷率1.4% 不满足要求 风险","procurement-risk"),
        ],
    },
}

def ensure_scenario(name: str) -> str:
    if name not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {name}")
    return name

def scenario_catalog() -> list[dict[str,str]]:
    return [{"id":k,"label":v["label"],"company":v["company"],"prompt":v["prompt"]}
            for k,v in SCENARIOS.items()]
