FROM python:3.11.8

WORKDIR /app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir \
    requests \
    beautifulsoup4 \
    scipy \
    pandas \
    numpy \
    numba \
    psutil \
    scikit-learn
