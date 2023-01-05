# 部署

## 构建

运行命令 `sh build.sh` 构建, 构建后生成dist目录

## 运行
在构建后的目录运行 `sh run.sh` 运行项目

## 配置
配置文件 `server/config.py`, 可根据情况修改neo4j的地址，数据库可选择sqlite或mysql


## 开源部署
### 构建
1. 运行命令 `sh build.sh` 构建
2. 构建后生成dist目录

### 部署
1. 将 dist 目录上传到服务器
2. 在上传后的目录下运行 `sh run.sh` 运行项目


