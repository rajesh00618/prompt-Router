# Prompt Router

An intelligent intent-based prompt routing application powered by Google's Gemini Flash AI.

## Overview
This application acts as a smart gateway for processing user inputs. It first analyzes the user's message to classify its underlying "intent" (e.g., coding, writing, analysis) using a lightweight LLM Prompt. Based on the determined intent, it then routes the message to a specialized "expert" system prompt, which handles the request to generate a highly contextual and accurate final response. 

The architecture is split into two primary LLM interactions:
1.  **Intent Classification**: Determines what the user is asking.
2.  **Expert Generation**: Dynamically selects an expert persona and generates the final output based on the user's intent.

All interactions are logged in `route_log.jsonl` for observability and auditing purposes.

## Features
- **Dynamic Routing**: Intelligently classifies requests and directs them to the optimal expert AI profile.
- **Robust Parsing**: Handles structured JSON responses from the Gemini API safely with fallback logic.
- **Auditing**: Comprehensive request logging to track intents, confidence scores, user inputs, and final outputs.
- **Batch Testing**: A test suite (`test_router.py`) to quickly validate the router against multiple edge cases and common queries.

## Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/rajesh00618/prompt-Router.git
    cd prompt-Router
    ```

2.  **Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    # source venv/bin/activate  # macOS/Linux
    ```

3.  **Install Dependencies**
    ```bash
    pip install google-generativeai python-dotenv
    ```

4.  **Environment Variables**
    Create a `.env` file in the root directory and add your Google Gemini API Key:
    ```env
    GOOGLE_API_KEY=your_api_key_here
    ```

## Usage

You can run the main router module directly to see a demonstration:

```bash
python router.py
```

### Running the Test Suite
To automatically run the router against a robust batch of varied prompts:

```bash
python test_router.py
```
