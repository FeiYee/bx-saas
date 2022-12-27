FROM python:3.10.8

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

CMD [ "sh", "entrypoint.sh" ]
