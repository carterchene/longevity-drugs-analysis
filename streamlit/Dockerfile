FROM python:3.10

WORKDIR /usr/src/app

# Install dependencies
COPY streamlit_requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8501
COPY . .

CMD ["streamlit", "run", "drug-analysis.py", "--server.port=8501", "--server.address=0.0.0.0"]