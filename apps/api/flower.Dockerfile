FROM python:3.10
WORKDIR /app
COPY ./req.txt /app/req.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/req.txt
COPY ./ /app
CMD ["celery", "flower", "--port=5555"]