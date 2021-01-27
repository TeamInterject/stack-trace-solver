FROM python:3
WORKDIR /sts-be
ENV FLASK_APP=src/main.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
COPY ["./requirements.txt", "./"]
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]