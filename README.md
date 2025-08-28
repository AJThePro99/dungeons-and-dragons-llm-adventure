# Dungeons & Dragons Adventure 

This is a small project exploring how conversation chaining and involving multiple 'characters' in a single chat looks like.

This is a minimal game that is inspired from Dungeons & Dragons type of narration and experience.

## How to run the code

1. Clone this repository
2. Set up a virtual environment (recommended)

    ```python
    python -m venv .venv
    ```

    ```python
    python .venv/Scripts/activate
    ```

3. Install the required packages

    ```python
    pip install -r requirements.txt
    ```

4. Use a local LLM service or a cloud provider for inference. You can modify the [`config.py`](./config.py) LLM Configuration constants to suit your need.

    For my use case,I've used LM Studio as my LLM server provider (Ollama also works), and tried this program with `openai/gpt-oss-20b` and `google/gemma-3-4b`

    (This program supports any LLM Model, with or without reasoning)

5. Start the game

    ```py
    python main.py
    ```

---

## Future Plans

- [ ] Improve narration and add actions like dice rolls and results
- [ ] Integrate a RAG module to ground the actual rules of D&D
- [ ] Dynamic Player Creation and saving current state of an ongoing campaign
