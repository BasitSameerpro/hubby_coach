# Simple Chatbot with Persona Selection

This project implements a simple chatbot that allows users to select a persona for the AI. It demonstrates basic LLM integration using Ollama for local model execution.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [How to Run](#how-to-run)
- [Understanding the Code](#understanding-the-code)
  - [AI_Persona.py](#ai_personapy)
  - [llm.py](#llmpy)
  - [llmagent.py](#llmagentpy)
- [Interactive vs. Single-Shot Interaction](#interactive-vs-single-shot-interaction)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This chatbot provides a straightforward way to interact with a Locally Running Language Model (LLM) with a customizable persona. Users can choose from predefined roles like "Fitness," "Training," "Motivational," or "Personal" assistant, each with various character styles. The project offers two modes of interaction: a single-shot response and an interactive chat experience.

**Important Note:** This project is designed for demonstration and educational purposes. It is **not** an industry-standard production-ready chatbot.

## Project Structure

The project is organized into four main files:

.
├── config.py
├── AI_Persona.py
├── llm.py
├── llm_agent.py
└── main.py


- `config.py`: (Assumed) This file should contain the `PERSONAS` dictionary which defines the available roles and their characteristics.
- `AI_Persona.py`: Handles the selection of AI persona (role and character).
- `llm.py`: Manages single-shot interactions with the LLM.
- `llm_agent.py`: Manages interactive (conversational) sessions with the LLM using LangGraph.
- `main.py`: The entry point for the application, allowing users to choose between single-shot and interactive modes.

## Features

- **Persona Selection:** Choose from different AI roles (e.g., Fitness, Training, Motivational, Personal) and specific characters within those roles.
- **Single-Shot Interaction:** Get a direct response to a single query based on the selected persona.
- **Interactive Chatting:** Engage in a continuous conversation with the AI, maintaining the selected persona.
- **Local LLM Integration:** Utilizes Ollama for running LLMs locally on your CPU.
- **Conversation Context (Interactive Mode):** Includes basic context summarization in interactive mode to help the model maintain coherence over longer conversations.

## Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.x**
- **Ollama:** A tool for running open-source LLMs locally.
  - You can download Ollama from their official website: [ollama.com](https://ollama.com/)
  - After installing Ollama, you'll need to download a model (e.g., `llama2`, `mistral`). You can do this by running `ollama run <model_name>` in your terminal (e.g., `ollama run llama2`).
- **Required Python Libraries:**
  - `langchain-ollama`
  - `langchain-core`
  - `langgraph`
  - `typing_extensions`

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/BasitSameerpro/hubby_coach.git
    cd hubby_coach
    ```

2.  **Install Ollama and download a model:**
    Follow the instructions on [ollama.com](https://ollama.com/) to install Ollama. Once installed, download a model (e.g., `llama2`):
    ```bash
    ollama run llama2
    ```
    This command will download `llama2` if you don't have it, and then start a session. You can then exit the session.

3.  **Install Python dependencies:**
    ```bash
    pip install langchain-ollama langchain-core langgraph typing_extensions
    ```

## How to Run

To start the chatbot, run the `main.py` file:

```bash
python main.py