FROM python:3.9

WORKDIR /app

COPY ./app .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8501
ENTRYPOINT [ "streamlit run" ]
CMD ["00_🏠_Home.py"]
