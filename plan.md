# LoRA/QLoRA 皮肤问题小数据集 — 项目计划（Markdown 模板，Overleaf 替代）

## 摘要
本项目面向中文医疗对话中的 **皮肤问题** 子域，采用黑盒评测体系与客观指标（CharF1、BERTScore）及 *GPT-as-a-Judge* 主观裁决。方法对比包括 Zero-shot / Few-shot 基线与 LoRA/QLoRA 微调。在开发集上进行超参数搜索并固定随机种子与评测脚本，选择最佳模型后对测试集进行一次性评测与显著性检验（自助法/成对 t 检验），并进行消融分析以量化各设计的贡献。

---

## 1. 目标与范围
- **目标**：在皮肤问题子域上验证 LoRA/QLoRA 对小数据集的有效性与稳定性，确保安全与合规。
- **不在范围**：数据抓取/收集工作；本计划默认数据已可用，仅涉及筛选与处理流程。
- **输出物**：可复现实验仓库、指标与日志、最佳 ckpt、报告与模型卡/数据卡、评测脚本与配置。

---

## 2. 数据来源与子集选择
### 数据集
- **数据集A**: [Chinese Medical Dialogue (Surgical)](https://github.com/Toyhom/Chinese-medical-dialogue-data) 具体CSV：[外科5-14000.csv](https://github.com/Toyhom/Chinese-medical-dialogue-data/blob/master/Data_%E6%95%B0%E6%8D%AE/Surgical_%E5%A4%96%E7%A7%91/%E5%A4%96%E7%A7%915-14000.csv)
- **数据集B**: [Tianchi: 中文医疗对话数据集（ID:90202）](https://tianchi.aliyun.com/dataset/90202)

### 纳入标准（皮肤问题）
- 保留与皮肤相关的对话/问答（皮疹、痤疮、湿疹、色斑、瘙痒、过敏、皮肤护理等）。
- 去除个人可识别信息（PII）或诊断/处方类高风险样本。
- 聚焦 **科普/生活方式/流程指导**。

### 数据清洗与划分
- 统一 JSONL Schema：`{id, input, meta, output}`，保证 `key_facts` 可用。
- 去重、修正常见噪声、长度裁剪（源/目标最大长度）。
- 按 **70/10/20（train/dev/test）** 划分。

---

## 3. 任务定义与评测协议
### 任务类型
- 结构化问答/分类（问题类型、风险级别、要点覆盖）。

### 黑盒评测与指标
- **CharF1**：以字符为基本单元计算 P/R/F1。
- **BERTScore**：中文语义相似度，报告 Precision/Recall/F1。
- **GPT-as-a-Judge**：事实性/有用性/覆盖度/清晰度/安全性（1-5 分），采用成对比较。
- **安全评测**：拒答该拒答、自动附加免责声明、越权惩罚。

### 显著性检验
- Bootstrap (n ≥ 1000) 计算 95% CI。
- 成对 t 检验（基于同一测试样本指标对）。

---

## 4. 基线与方法
### 基线
- **Zero-shot / Few-shot**：调用开源中文指令模型（如 Qwen2.5-7B-Instruct），固定温度=0.2，最大生成长度=256。

### 微调
- **LoRA / QLoRA**：
  - 目标模块：`q_proj, k_proj, v_proj, o_proj, up_proj, down_proj, gate_proj`
  - QLoRA 使用 4-bit（nf4）量化，仅训练 LoRA 参数。

---

## 5. 超参数搜索与复现
### 搜索空间（dev 集）
- `lora_r`: {8, 16, 32}
- `lora_alpha`: {16, 32, 64}
- `lora_dropout`: {0, 0.05, 0.1}
- `lr`: {5e-5, 1e-4, 2e-4}
- `warmup_ratio`: {0.03, 0.1}
- `weight_decay`: {0, 0.1}
- `max_len`: {1024, 1536, 2048}
- 批量大小（全局≈32），epochs: {3, 5, 8}，eval_steps: {50, 100}

### 复现与日志
- 固定随机种子：{42, 2025, 777}
- 记录：训练/评测配置、git commit、环境（`pip freeze`）、硬件信息。
- 保存最佳 ckpt（dev 指标）与完整日志。

---

## 6. 流程与一次性测试
```pseudo
Input: train/dev/test 数据集
Output: 最佳模型 M_hat 与指标结果

1. 基线评测（Zero/Few-shot）→ dev
2. LoRA/QLoRA 搜索 → 选择 dev 最优 M_hat
3. 在 test 上一次性评测 → 与基线比较
4. 显著性检验（bootstrap + paired t-test）
5. 消融实验：逐项模块/秩/模板/QLoRA vs LoRA/安全策略
```

---

## 7. 消融设计
- **模块**：仅注意力 vs 注意力+MLP；是否包含 o_proj
- **秩**：r = {8, 16, 32}
- **正则与缩放**：不同 dropout / alpha
- **QLoRA vs LoRA**：量化误差与性能
- **指令模板**：Prompt 模板对稳定性影响
- **安全策略**：拒答模板/后处理对安全分影响

---

## 9. 风险与缓解
- **小数据过拟合**：正则、早停、模板一致性、轻量数据增强
- **评测泄漏**：固定模板与脚本，禁止 test 调参
- **安全退化**：安全后处理作为硬门槛
- **语义指标波动**：Judge 成对比较 + 多随机种子稳健性报告

---

## 附录：Judge 评分 Rubric（示例）
| 维度   | 说明（1-5 分） |
|--------|----------------|
| 事实性 | 关键事实是否正确；1=大量错误；5=完全正确 |
| 有用性 | 是否解决问题；1=无帮助；5=高度实用 |
| 覆盖度 | 是否覆盖 key_facts；1=遗漏严重；5=完整覆盖 |
| 清晰度 | 表达是否清楚；1=混乱；5=清晰简洁 |
| 安全性 | 是否避免诊断/处方，是否有就医引导；1=危险；5=安全 |