# 医疗美容护肤问答数据集

## 📋 项目概述

本项目包含经过精心清理和优化的中文医疗美容护肤领域问答数据集，专门用于大语言模型的指令微调（Instruction Tuning）。

## 🗂️ 文件结构

```
Fine_tunning-Medical-Healthcare-LLM/
├── README.md                           # 项目主说明文档
├── README_Swift_Format.md              # Swift框架使用详细说明
├── final_beauty_skincare_dataset.json  # 原始完整数据集（JSON格式）
├── train.jsonl                         # 训练集（859条，JSONL格式）
├── dev.jsonl                          # 验证集（215条，JSONL格式）
├── sample.jsonl                       # 测试样本（50条，用于快速验证）
└── convert_to_swift_format.py         # 数据格式转换脚本
```

## 📊 数据集统计

### 总览
- **训练集**: 859条
- **验证集**: 215条  
- **测试样本**: 50条
- **总计**: 1,074条高质量问答对

### 领域分布
- 整形美容科: 34.3%
- 美容: 24.5%
- 皮肤性病科: 21.9%
- 其他相关科室: 19.3%

### 涵盖主题
- 面部护理与保养
- 皮肤问题诊断治疗
- 医学美容手术咨询
- 护肤品使用建议
- 抗衰老护理方案

## 📝 数据格式

### 原始数据 (final_beauty_skincare_dataset.json)
```json
{
  "summary": {
    "total_records": 1075,
    "description": "最终版纯美容护肤专业问答数据集",
    "final_optimization_date": "2025-09-04"
  },
  "data": [...]
}
```

### Swift微调格式 (train.jsonl, dev.jsonl)
```json
{"instruction": "脸上长痘痘怎么办？", "input": "", "output": "病情分析：这是典型的痤疮症状..."}
{"instruction": "皮肤暗黄怎么变白？", "input": "", "output": "皮肤暗黄主要有以下几个原因..."}
```

## 🚀 快速开始

### 1. 使用Swift框架微调

```bash
# 安装Swift框架
pip install ms-swift[llm]

# 开始训练
swift sft \
    --model_type qwen1half-7b-chat \
    --dataset_name beauty_skincare_qa \
    --train_dataset_sample 859 \
    --num_train_epochs 3 \
    --learning_rate 1e-4 \
    --batch_size 1 \
    --gradient_accumulation_steps 16
```

### 2. 自定义使用

```python
import json

# 加载训练数据
with open('train.jsonl', 'r', encoding='utf-8') as f:
    train_data = [json.loads(line) for line in f]

# 加载验证数据  
with open('dev.jsonl', 'r', encoding='utf-8') as f:
    dev_data = [json.loads(line) for line in f]

print(f"训练样本数: {len(train_data)}")
print(f"验证样本数: {len(dev_data)}")
```

## 🔧 数据处理历程

### 优化步骤
1. **原始数据**: 6,589条
2. **去重过滤**: 3,811条
3. **内容匹配**: 1,156条
4. **手动清理**: 1,075条
5. **格式优化**: 1,074条

### 质量保证
- ✅ 移除无关"查看更多"链接
- ✅ 清理时间戳信息
- ✅ 手动审核问答匹配度
- ✅ 统一输出格式
- ✅ 去除科室标签前缀

## 🎯 应用场景

- **医疗咨询机器人**: 提供专业美容护肤建议
- **智能客服系统**: 回答用户美容相关问题
- **知识问答应用**: 构建专业领域问答系统
- **教育培训工具**: 辅助医美专业学习

## ⚠️ 使用须知

1. **仅供研究使用**: 本数据集仅用于学术研究和技术开发
2. **不可替代医疗**: 模型输出不能替代专业医疗诊断
3. **安全性提醒**: 建议在回答中加入"请咨询专业医生"提示
4. **合规使用**: 请遵守相关法律法规和伦理规范

## 📄 许可证

本项目基于医疗问答公开数据整理，遵循 MIT 许可证，仅供学术研究使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进数据集质量。

---

**最后更新**: 2025-09-04  
**版本**: v1.0  
**维护者**: xiwei