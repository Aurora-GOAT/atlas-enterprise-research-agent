# Interview narrative (truthful portfolio presentation)

## 60-second introduction (Chinese)

“我做了一个叫 Atlas 的企业研究 Agent 原型。之前在医药BD实习时，我接触到一个共性问题：一项业务研究往往要查阅大量资料，但真正耗时的是梳理研究问题、确认每个结论来自哪里、识别资料缺口。我把这个问题转化成产品需求：用5个可见步骤拆解研究任务，基于用户提供的资料检索证据，生成可追溯的研究草稿，并提供效果评测。它有一个可运行的Web界面，也能在不配置API Key的情况下使用。本地示例数据全部是虚构的，我还用10条标注题来测量检索Hit@3和MRR。当前它是个人原型，还没有做真实用户测试、企业权限系统和线上部署；这些也是下一阶段重点。”

## What you can personally demonstrate

1. Show the running web UI and start with the blank workspace.
2. Load six synthetic source docs; explain source provenance and privacy boundary.
3. Enter an ambiguous due-diligence question; walk through five planning steps.
4. Open report and point to `[S#]` references plus explicit gaps.
5. Calculate a what-if revenue scenario through the backend API.
6. Run retrieval benchmark and openly discuss misses/limitations.
7. Open GitHub code and tests; explain why the MVP uses offline TF-IDF rather than claiming a complex proprietary RAG solution.

## Probable follow-up questions

- **Why not use a multi-agent system?** An explainable, bounded workflow is better at the MVP stage. Agent autonomy only makes sense after understanding high-value user actions and permissions.
- **What metrics?** Retrieval Hit@3 and MRR already measurable; real task completion, citation correctness, time saved, cost and adoption need controlled user studies.
- **How avoid hallucinations?** Default report displays extracted facts, marks missing data, and indexes sources; LLM narrative is separate, optional and not independently verified.
- **How scale?** Introduce a persistent index and hybrid retrieval, access control, source versioning and tenant isolation, evaluation harness, monitoring, feedback loops.
- **What did the user interviews show?** None yet; interviews are planned. Do not invent user count, accuracy improvement or working-hour reductions.
- **What is the business value?** Hypothesis: reduce repeated search/compilation work and improve traceability. Not validated; requires actual workflow timing and user observation.

## Resume-ready wording (only after completing and validating)

**Atlas | 企业研究智能体（个人产品与工程项目）**

- 需求设计：面向企业研究的信息溯源与任务拆解痛点，撰写PRD，设计五阶段证据优先工作流与用户界面。
- 原型开发：使用FastAPI、Python、scikit-learn和HTML/CSS/JS构建可运行本地原型，支持PDF/DOCX资料导入、检索、引用、研究报告导出及商业情景测算。
- 效果评估：构建10条合成测试样例，通过Hit@3、MRR记录检索能力，配合自动化测试和CI建立可复现评估；尚未开展真实企业用户验证。
