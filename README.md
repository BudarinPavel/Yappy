# Infra Yappy Project

## Project Overview

This project is a service designed to detect duplicate videos using vector embeddings. It leverages **Weaviate** as a vector search engine, **Uvicorn** as the ASGI server, and **FastAPI** for the web APIs.

## Features

- **Embedding API**: API that handles generating embeddings for videos.
- **Duplicate Detection**: Checks for similar or duplicate videos based on their vector embeddings.
- **Weaviate Integration**: Vector database management using Weaviate to store and search embeddings.
- **Scalable Architecture**: Microservice-based architecture using Docker.

## Tech Stack

- **Python 3.10**
- **FastAPI**
- **Uvicorn**
- **Weaviate**
- **Docker**

## Prerequisites

- Docker
- Python 3.10
- curl (for testing the APIs)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/BudarinPavel/Yappy
   cd infra_yappy
>>>>>>> d067323 (Initial commit)
