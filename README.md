# Document Retrieval API

This project is a backend system for retrieving documents using a RESTful API. It is built with Python and Flask, utilizing a vector database for efficient document retrieval. The system includes caching, rate limiting, and a background task for scraping news articles.

## Features

- **Document Storage**: Documents are stored in a vector database using Chroma.
- **Caching**: Responses are cached using Redis to ensure faster retrieval.
- **Background Task**: A separate thread scrapes news articles as soon as the server starts.
- **Endpoints**:
  - `/health`: Returns a random response to check if the API is active.
  - `/search`: Returns a list of top results for a given query.

## Requirements

- Python 3.9+
- Redis
- Docker (optional for containerization)

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Create a Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```
4. **Start Redis**:
```bash
redis-server
```
5. **Populate the Database**:
```bash
python populate_database.py
```
6. **Run the Application**:
```bash
python app.py
```

# API Documentation

## Usage

### Health Check
- **Endpoint**: `/health`
- **Method**: `GET`
- **Description**: Checks if the API is active.

### Search
- **Endpoint**: `/search`
- **Method**: `POST`
- **Parameters**:
  - `text`: The prompt text.
  - `top_k`: Number of results to fetch.
  - `threshold`: Similarity score threshold.
  - `user_id`: Unique identifier for the user.
- **Description**: Returns a list of top results for the query.

## Rate Limiting
- Users can make up to **5 requests per hour**. Exceeding this limit will result in a `429` status code.

## Dockerization

### Build and Run Containers
```bash
docker-compose up --build
```
