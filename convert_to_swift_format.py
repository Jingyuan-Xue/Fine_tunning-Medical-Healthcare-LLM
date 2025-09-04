#!/usr/bin/env python3
"""
将美容护肤数据集转换为Swift指令微调格式
"""
import json
import random
import os
from typing import Dict, List

def load_dataset(file_path: str) -> Dict:
    """加载原始数据集"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_to_swift_format(data_item: Dict) -> Dict:
    """转换单个数据项为Swift格式"""
    # 直接使用原始问题，不添加科室标签
    instruction = data_item['input'].strip()
    
    # 构建Swift格式
    swift_item = {
        "instruction": instruction,
        "input": "",  # 留空，因为问题已经在instruction中
        "output": data_item['output'].strip()
    }
    
    return swift_item

def split_dataset(data: List[Dict], train_ratio: float = 0.8) -> tuple:
    """划分训练集和验证集"""
    random.shuffle(data)
    split_point = int(len(data) * train_ratio)
    return data[:split_point], data[split_point:]

def save_jsonl(data: List[Dict], file_path: str):
    """保存为JSONL格式"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def main():
    # 设置随机种子以确保可重现性
    random.seed(42)
    
    # 加载原始数据
    print("正在加载原始数据...")
    dataset = load_dataset('final_beauty_skincare_dataset.json')
    raw_data = dataset['data']
    
    print(f"原始数据总数: {len(raw_data)}")
    
    # 转换格式
    print("正在转换数据格式...")
    swift_data = []
    for item in raw_data:
        try:
            swift_item = convert_to_swift_format(item)
            # 简单的质量检查
            if len(swift_item['instruction']) > 5 and len(swift_item['output']) > 10:
                swift_data.append(swift_item)
        except Exception as e:
            print(f"转换失败，跳过该项: {e}")
    
    print(f"转换后有效数据: {len(swift_data)}")
    
    # 划分训练集和验证集
    print("正在划分数据集...")
    train_data, dev_data = split_dataset(swift_data, train_ratio=0.8)
    
    print(f"训练集: {len(train_data)} 条")
    print(f"验证集: {len(dev_data)} 条")
    
    # 保存文件
    print("正在保存文件...")
    save_jsonl(train_data, 'train.jsonl')
    save_jsonl(dev_data, 'dev.jsonl')
    
    # 保存一个小样本用于测试
    sample_data = train_data[:50]
    save_jsonl(sample_data, 'sample.jsonl')
    
    print("转换完成！生成文件:")
    print(f"- train.jsonl ({len(train_data)} 条)")
    print(f"- dev.jsonl ({len(dev_data)} 条)") 
    print(f"- sample.jsonl ({len(sample_data)} 条，用于快速测试)")
    
    # 显示几个样例
    print("\n数据样例:")
    for i, item in enumerate(train_data[:3]):
        print(f"\n样例 {i+1}:")
        print(f"Instruction: {item['instruction'][:100]}...")
        print(f"Output: {item['output'][:100]}...")

if __name__ == "__main__":
    main()