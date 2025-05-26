

 # 使用官方 Python 3.12 镜像作为基础
 FROM python:3.12-slim

 # 设置工作目录
 WORKDIR /app

 # 复制 requirements.txt 并安装依赖
 COPY requirements.txt .
 RUN pip install --no-cache-dir -r requirements.txt

 # 复制项目其余文件
 COPY . .

 # 设置环境变量
 ENV FLASK_APP=app/main.py
 ENV FLASK_RUN_HOST=0.0.0.0
 ENV FLASK_RUN_PORT=5000
 ENV PYTHONUNBUFFERED=1

 # 暴露端口（可选）
 EXPOSE 5000

 # 启动 Flask 应用
 CMD ["flask", "run"]