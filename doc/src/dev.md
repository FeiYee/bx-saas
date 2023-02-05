# 开发

## 服务端接口测试
使用 Postman 测试接口方法

### 登录
1. 首先调用接口 `http://localhost:8080/api/login` 获取 token
2. 如图
![login](./asset/dev/login.png)

### 设置请求头
1. 获取登录的返回值中 `access_token` 的值
2. 设置接口的请求头 `Authorization` 值为 `token_type` + ` ` + `access_token` 的值(两个值之间需有空格)
3. 如图
![header](./asset/dev/header.png)
4. `Authorization` 值示例
```
bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzYyODU3NzYsInN1YiI6IjMxMzY4OWJlODgxZDQ3MWZiOTFhNzExYmY3ZDhhNzE2In0.eOpKm77eyfs0DCix1npIfpTJK-Qjg8hpxerCT6TaeCk
```

### 调用接口
1. 调用接口时需设置认证的请求头
2. 如图
![example](./asset/dev/example.png)


## 服务端接口文档
[接口文档地址](http://localhost:8080/docs)
