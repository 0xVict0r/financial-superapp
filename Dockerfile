FROM python:3.9

WORKDIR /

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8501

COPY ./ .

ENTRYPOINT [ "streamlit run" ]

CMD ["00_🏠_Home.py"]
