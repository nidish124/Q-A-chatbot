FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
CMD ["python", "-m","streamlit", "run", "streamlit_app.py"]