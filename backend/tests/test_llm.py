# -*- coding: utf-8 -*-
"""
@File       : test_llm.py
@Date       : 2025-03-01
@Desc       : llama 模型测试


"""

import os
from llama_cpp import Llama

# 模型路径
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)  # 因为 tests 是 backend 的子目录，所以 project_root 指向 backend
model_path = os.path.join(project_root, "llm", "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

# 初始化模型
llm = Llama(model_path=model_path, n_ctx=512, n_gpu_layers=0)

# 简单测试模型输出
prompt = "你好，欢迎使用 tinyllama 模型！"
output = llm(prompt)
print("模型输出:", output)