# QA Retriever with Citation Multi Agent

This is a Question Answer Retriever with Citation Multi Agent. The workflow of the agent is given below:
+----------------------------------------------+
|                  User Query                  |
+------------------------+---------------------+
                         |
                         v
+----------------------------------------------+
|        Supervisor/Coordinator Agent          |
|   (Orchestrates and delegates tasks)         |
+------------------------+---------------------+
                         |
    +--------------------+--------------------+
    |                                         |
    v                                         v
+---------+                           +----------------+
|Retriever|                           | Summarizer     |
|  Agent  |                           |  Agent         |
| (Fetches|                           | (Condenses     |
| relevant|                           |  retrieved     |
| chunks) |                           |  text)         |
+---------+                           +----------------+
    |                                         |
    +--------------------+--------------------+
                         |
                         v
                +-------------------+
                |    QA Agent       |
                | (Answers based on |
                |  summarized text) |
                +-------------------+
                         |
                         v
                +-------------------+
                | Citation Agent    |
                | (Adds citations)  |
                +-------------------+
                         |
                         v
+----------------------------------------------+
|           Final Answer with Summary          |
|             and Citations                    |
+----------------------------------------------+

The framework I used for developin the agent is CrewAI and for searching purpose I used Serper API.

# Get Started
1.``` bash
    git clone https://github.com/armanulalam/QA-Retriever-Multi-Agent.git
    ```
2.``` bash
    python -m venv crew
    ```
3.``` bash
    pip install -r requirements.txt
    ```
4.``` bash
    python main.py
    ```


