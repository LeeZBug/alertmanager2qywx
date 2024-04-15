FROM python:3.9.19
COPY ./app /app
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
ENV TZ=Asia/Shanghai
RUN pip install -i https://mirror.nju.edu.cn/pypi/web/simple -r /app/requirements.txt
CMD ["python", "/app/main.py"]