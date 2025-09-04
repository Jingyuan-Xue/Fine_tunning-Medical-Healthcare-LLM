# 美容护肤问答数据集 - Swift 指令微调格式

## 📋 数据集概览

本数据集已转换为 Swift 框架所需的标准 JSONL 格式，专用于医疗美容领域的指令微调 (Instruction Tuning)。

### 📊 数据统计
- **训练集**: `train.jsonl` - 860条
- **验证集**: `dev.jsonl` - 215条  
- **测试样本**: `sample.jsonl` - 50条（用于快速测试）
- **总数据量**: 1,075条高质量问答对

### 🏥 领域分布
- 整形美容科: 369条 (34.3%)
- 美容: 263条 (24.5%)
- 皮肤性病科: 235条 (21.9%)
- 其他相关科室: 208条 (19.3%)

## 📋 数据格式

每行为一个独立的JSON对象，包含以下字段：

```json
{
  "instruction": "【皮肤性病科】脸上长痘痘怎么办？",
  "input": "",
  "output": "病情分析：这是典型的痤疮症状..."
}
```

### 字段说明
- **instruction**: 用户问题（已包含科室标签）
- **input**: 留空（所有信息已在instruction中）
- **output**: 专业医疗建议和治疗方案

## 🚀 Swift 使用指南

### 1. 数据集配置

```python
# Swift 训练配置示例
{
    "dataset_name": "beauty_skincare_qa",
    "train_file": "train.jsonl",
    "val_file": "dev.jsonl",
    "template_type": "default",  # 或 "chatml"
    "max_length": 512,
    "batch_size": 8
}
```

### 2. 模板格式

Swift会自动将数据转换为对话格式：

**Human**: 【皮肤性病科】脸上长痘痘怎么办？

**Assistant**: 病情分析：这是典型的痤疮症状...

### 3. 推荐超参数

```yaml
# 训练参数建议
learning_rate: 2e-5
num_epochs: 3-5
warmup_ratio: 0.1
save_steps: 100
eval_steps: 100
max_grad_norm: 1.0
```

## ⚡ 快速开始

### 1. 环境准备
```bash
# 安装Swift框架
pip install ms-swift[llm]
```

### 2. 开始训练
```bash
# 使用Swift进行指令微调
swift sft \
    --model_type qwen1half-7b-chat \
    --dataset beauty_skincare_qa \
    --train_dataset_sample 860 \
    --num_train_epochs 3 \
    --lora_target_modules ALL \
    --gradient_checkpointing true \
    --batch_size 1 \
    --learning_rate 1e-4 \
    --gradient_accumulation_steps 16 \
    --warmup_ratio 0.05 \
    --save_total_limit 2
```

### 3. 验证效果
```bash
# 使用sample.jsonl快速测试
swift sft \
    --ckpt_dir output/qwen1half-7b-chat/vx-xxx/checkpoint-xxx \
    --eval_dataset beauty_skincare_qa \
    --val_dataset_sample 50
```

## 🎯 数据质量保证

### ✅ 已完成清理
- ✅ 去除"查看更多关于..."无关内容
- ✅ 清理时间戳信息
- ✅ 手动审核并移除不合理条目
- ✅ 统一输出格式和结构
- ✅ 确保问答内容匹配度

### 📏 质量标准
- 问题长度: 5-200字符
- 回答长度: 10-500字符
- 科室标签准确性: 100%
- 医疗专业性: 高质量专业回答

## 🏆 预期效果

使用本数据集微调后的模型应该能够：

1. **专业性**: 提供准确的美容护肤医疗建议
2. **针对性**: 根据科室信息给出专业回答
3. **安全性**: 避免给出不当或危险的医疗建议
4. **实用性**: 回答贴近实际应用场景

## 📝 注意事项

### ⚠️ 重要提醒
- 本数据集仅用于研究和学习目的
- 微调后的模型不能替代专业医疗诊断
- 建议在回答中加入"请咨询专业医生"的提醒
- 使用时请遵守相关法律法规和伦理规范

### 🔧 技术建议
- 建议使用LoRA等参数高效微调方法
- 推荐在7B-13B规模的模型上使用
- 可以与通用对话数据集混合训练
- 建议加入负采样和对比学习

## 📄 许可证

本数据集基于医疗问答公开数据整理，仅供学术研究使用。

---

**生成时间**: 2025-09-04  
**版本**: v1.0  
**维护者**: xiwei