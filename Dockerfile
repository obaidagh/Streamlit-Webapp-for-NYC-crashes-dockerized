FROM python:3.9.7-alpine

CMD mkdir /stapp
COPY . /stapp

WORKDIR /stapp
EXPOSE 8501

RUN pip3 install -r requirements.txt

CMD streamlit run Main.py
