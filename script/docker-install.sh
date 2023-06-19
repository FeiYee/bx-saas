#!/bin/sh

# 删除旧版本
sudo apt-get remove -y docker \
        docker-engine \
        docker.io \
        containerd \
        runc

sudo apt-get update -y

# 安装依赖
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加仓库源
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update -y


# 安装 docker-ce, docker-ce-cli, containerd.io, docker-compose-plugin
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
# sudo apt-get install -y http://mirrors.tencent.com/docker-ce/linux/ubuntu/dists/bionic/pool/stable/amd64/docker-ce_20.10.19~3-0~ubuntu-bionic_amd64.deb
# sudo apt-get install -y http://mirrors.tencent.com/docker-ce/linux/ubuntu/dists/bionic/pool/stable/amd64/docker-ce-cli_20.10.9~3-0~ubuntu-bionic_amd64.deb
# sudo apt-get install -y http://mirrors.tencent.com/docker-ce/linux/ubuntu/dists/bionic/pool/stable/amd64/containerd.io_1.6.9-1_amd64.deb
# sudo apt-get install -y http://mirrors.tencent.com/docker-ce/linux/ubuntu/dists/bionic/pool/stable/amd64/docker-compose-plugin_2.6.0~ubuntu-bionic_amd64.deb

# 启动docker服务
sudo systemctl start docker

# 开机时启动docker服务
sudo systemctl enable docker

# Docker Compose 安装
# sudo curl -L "https://github.com/docker/compose/releases/download/2.12.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# sudo chmod +x /usr/local/bin/docker-compose

sudo cp daemon.json /etc/docker/daemon.json


sleep 60

# 添加当前用户到docker组
sudo gpasswd -a ${USER} docker

sudo newgrp docker

sudo systemctl restart docker

# ubuntu
sudo systemctl daemon-reload
sudo service docker restart

# centos
# sudo systemctl reload-daemon

# sudo systemctl restart docker
