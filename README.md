

# Dentizone AI Service

[![Docker Publish](https://github.com/dentizone/ai/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/dentizone/ai/actions/workflows/docker-publish.yml)

Welcome to the **Dentizone AI Service**, a powerful, modular, and containerized text analysis microservice. Built with Python, FastAPI, and state-of-the-art NLP models, this service provides the main Dentizone platform with advanced capabilities for content moderation, sentiment analysis, and Personally Identifiable Information (PII) detection.

## ✨ Key Features

-   **Modular AI Layers:** A flexible architecture allowing for the combination of different analysis modules (Sentiment, Toxicity, Language, PII) on a per-request basis.
-   **Contact Information Extraction:** Utilizes the Google Gemini model via a specialized agent to accurately detect, extract, and validate contact information (emails, phone numbers, addresses) from user-generated text in any language.
-   **Toxicity & Insult Detection:** Integrates a pre-trained Hugging Face model (`unitary/toxic-bert`) to automatically flag toxic content and insults, helping to maintain a safe platform environment.
-   **Sentiment Analysis:** Leverages a robust sentiment analysis model (`cardiffnlp/twitter-roberta-base-sentiment`) to classify text as positive, neutral, or negative.
-   **Language Detection:** A built-in layer to identify the language of the input text, ensuring that models are applied appropriately.
-   **High-Performance API:** Built with **FastAPI** for a fast, modern, and asynchronous RESTful API experience.
-   **Production-Ready & Optimized:**
    -   Containerized using a multi-stage `Dockerfile` for a small and secure production image.
    -   Includes a CI/CD pipeline with **GitHub Actions** to automatically build and push the Docker image to Docker Hub.
-   **Secure Secret Management:** Integrates with **Infisical** for secure and centralized management of API keys and other secrets.

## 🏛️ Architecture & How It Works

The service is built around a modular "layers" architecture, allowing for flexible and efficient text analysis.

-   **`main.py`**: The FastAPI entry point that exposes several RESTful endpoints. Each endpoint uses a `ReviewLayerBuilder` to construct an analysis pipeline tailored to its specific task.
-   **`layers/models/`**: This directory contains the individual analysis modules:
    -   `ToxicityLayer`: Uses a local Transformers model for insult detection.
    -   `SentimentLayer`: Uses a local Transformers model for sentiment analysis.
    -   `LanguageLayer`: Uses a local Transformers model for language detection.
    -   `ReviewLayer`: The core orchestrator. The `ReviewLayerBuilder` pattern allows for the dynamic assembly of the other layers, creating a custom analysis engine for each API request.
-   **`layers/agent/`**: Contains the `NFEAAgent` (Name, Phone, Email, Address Agent).
    -   This agent communicates with the **Google Gemini API** using a detailed system prompt (`system_prompt.txt`) to perform advanced PII extraction and validation.
-   **`core/`**: Manages shared functionalities, primarily secret management through the `InfisicalSecretManager`.

This design allows the service to perform simple, local analyses (like sentiment) very quickly, while offloading more complex, instruction-based tasks (like PII extraction) to a powerful external LLM.

## 📜 API Endpoints

The following endpoints are available:

-   `GET /all`: Performs a comprehensive analysis, including contact info extraction, toxicity check, and sentiment analysis.
-   `GET /sentiment`: Returns only the sentiment analysis result (positive, neutral, negative).
-   `GET /lang`: Detects the language of the input text.
-   `GET /toxic`: Returns a boolean indicating if the text is considered an insult.
-   `GET /contact-toxic`: A specialized endpoint for content moderation. It returns only the extracted contact information and the toxicity analysis, making it efficient for pre-screening user posts.

**Query Parameter:**
All endpoints accept a single query parameter:
-   `text` (string, required): The input text to be analyzed.

**Example Request:**
```bash
curl "http://localhost:8000/contact-toxic?text=call%20me%20at%20555-1234%20you%20idiot"
```

## 🛠️ Technology Stack

-   **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
-   **Language:** Python 3.11
-   **NLP/ML:**
    -   [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
    -   [PyTorch](https://pytorch.org/) (CPU version for smaller image size)
    -   [Google Gemini API](https://ai.google.dev/docs/gemini_api_overview)
-   **Containerization:** Docker
-   **CI/CD:** GitHub Actions
-   **Secret Management:** [Infisical](https://infisical.com/)

## 🚀 Getting Started

### Prerequisites

-   Python 3.11 or higher
-   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
-   An Infisical account and project set up for secrets.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dentizone/ai.git
    cd dentizone-ai
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Secret Management:**
    Create a `.env` file in the root directory and add your Infisical credentials. This is required for the application to fetch the Google API Key.
    ```.env
    INFISICAL_HOST=https://app.infisical.com
    INFISICAL_CLIENT_ID=your_infisical_client_id
    INFISICAL_CLIENT_SECRET=your_infisical_client_secret
    INFISICAL_PROJECT_ID=your_infisical_project_id
    INFISICAL_ENVIRONMENT_SLUG=dev
    ```
    Ensure your `GoogleAPIStudio` secret is set in your Infisical project.

5.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

## 🐳 Running with Docker

The included `Dockerfile` is optimized for production.

1.  **Build the Docker image:**
    ```bash
    docker build -t dentizone-ai .
    ```

2.  **Run the Docker container:**
    Make sure to pass your Infisical environment variables to the container.
    ```bash
    docker run -d \
      -p 8000:8000 \
      -e INFISICAL_CLIENT_ID="your_client_id" \
      -e INFISICAL_CLIENT_SECRET="your_client_secret" \
      -e INFISICAL_PROJECT_ID="your_project_id" \
      --name dentizone-ai-container \
      dentizone-ai
    ```
    The service will be accessible at `http://localhost:8000`.

## 🔄 CI/CD

This repository uses **GitHub Actions** for its CI/CD pipeline. The workflow defined in `.github/workflows/docker-publish.yml` automatically:
1.  Checks out the code on every push to the `main` branch.
2.  Logs in to Docker Hub using repository secrets.
3.  Builds the Docker image, utilizing layer caching for speed.
4.  Pushes the final image to Docker Hub tagged as `your_dockerhub_username/aiagent:latest`.
