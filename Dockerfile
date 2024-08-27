FROM python:3.10.14
EXPOSE 8000
COPY ./app /app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip config set global.index-url --site https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
ENTRYPOINT ["python", "main.py"]

