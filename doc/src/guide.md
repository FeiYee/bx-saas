# 指南


## Server
### 安装依赖
`pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt`

### 初始化
`python migration.py`

### 运行
`python main.py`

### 开发运行
`uvicorn main:app --port 8080 --reload`


## Client
### 开发运行
`npm run dev`

### 构建
`npm run build`


## Doc
### 安装
`python -m pip install mkdocs`

### 运行
`mkdocs serve -a localhost:8020`


## 其他

### Server 未安装依赖
```shell
python3 -m pip install numpy
python3 -m pip install sklearn
python3 -m pip install pyecharts
python3 -m pip install matplotlib
python3 -m pip install neo4j
```
