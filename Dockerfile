FROM python:3.10-alpine
WORKDIR /app
COPY ./src ./src
COPY ./main.py ./
COPY requirements.txt .
RUN pip3 install -r requirements.txt
VOLUME /var 
EXPOSE 5199

CMD ["python3", "main.py"]