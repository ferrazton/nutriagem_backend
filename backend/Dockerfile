# Use an official lightweight Python image.
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container.
WORKDIR /app

# Copy requirements (for caching dependency installation).
COPY requirements.txt /app/

# Install dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire app code into the container.
COPY . /app/

# Expose the port FastAPI will run on.
EXPOSE 8000

# Default command to run the server.
CMD ["uvicorn", "app.main:apiRouter", "--host", "0.0.0.0", "--port", "8000"]
