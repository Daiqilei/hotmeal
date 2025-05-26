# -*- coding: utf-8 -*-
"""
@File       : main.py
@Date       : 2025-03-01 
@Desc       : 应用入口文件。创建 Flask 应用实例并运行


"""

import os
import logging

from dotenv import load_dotenv

from app import create_app

load_dotenv()
logger = logging.getLogger("hotmeal")

# --- 创建应用实例，让工厂函数自动选择配置
app = create_app()



# --- 开发服务器运行入口 ---
if __name__ == '__main__':
    # 开发环境下，使用 SSL 证书
    # 注意：生产环境下，应使用 HTTPS 协议
    # 证书文件路径
    # 计算证书文件的绝对路径（项目根目录下）
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    cert_file = os.path.join(base_dir, 'localhost+2.pem')
    key_file = os.path.join(base_dir, 'localhost+2-key.pem')

    # 从配置中获取 HOST 和 PORT (如果配置对象中有的话)
    # 或者保持从环境变量获取
    host = os.getenv('HOST', '0.0.0.0')
    # 确保 PORT 能正确转换为整数
    try:
        port = int(os.getenv('PORT', 5001))
    except ValueError:
        logger.warning("无效的 PORT 环境变量，将使用默认端口 5001。")
        port = 5001

    debug_mode = app.config.get('DEBUG', False)  # 从配置获取 DEBUG 状态

    logger.info(f"🚀 应用启动中... 环境: {app.config.get('ENV', 'unknown')}")
    logger.info(f"🔗 访问地址: http://{host}:{port}")
    logger.info(f"🐛 Debug 模式: {debug_mode}")

    # 使用 app.run 运行开发服务器
    # 生产环境应使用 Gunicorn/uWSGI
    app.run(host=host,
            port=port,
            debug=debug_mode,
            ssl_context=(cert_file, key_file)# 启用 HTTPS
            )
