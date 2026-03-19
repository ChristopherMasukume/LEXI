FROM python:3.11-slim 
WORKDIR /app 
# Copy ONLY app folder first 
COPY app/ ./app/ 
# Copy other project-level files if required 
COPY producer.py . 
COPY migration ./migration 
# Install dependencies 
COPY app/requirements.txt . 
RUN pip install -r requirements.txt 
# Run app 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]