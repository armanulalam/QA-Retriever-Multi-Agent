import os
from dotenv import load_dotenv
from crewai import Agent
from crewai_tools import SerperDevTool
from crewai import Task
from crewai import Crew, Process

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["SERPER_API_KEY"] = SERPER_API_KEY 
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_MODEL"] = "gpt-4-32k"

search_tool = SerperDevTool()


# Define Agents

# Supervisor Agent
supervisor = Agent(
    role="Supervisor",
    goal="Coordinate all agents to answer user queries about documents.",
    backstory=(
        "You are the intelligent orchestrator who manages and coordinates "
        "the Retriever, Summarizer, QA, and Citation agents to produce the final answer."
    ),
    verbose=True,
    tools=[search_tool],
    memory=True,
    allow_delegation=True
)

# Retriever Agent
retriever = Agent(
    role="Retriever",
    goal="Find the most relevant document sections that match the user's query.",
    backstory=(
        "You are an expert at searching and retrieving relevant information "
        "from large document sets using semantic similarity and keyword matching."
    ),
    verbose=True,
    memory=True,
    tools=[search_tool],
    allow_delegation=False
)

# Summarizer Agent
summarizer = Agent(
    role="Summarizer",
    goal="Summarize retrieved text chunks into concise, informative summaries.",
    backstory=(
        "You have exceptional summarization skills and can turn large texts "
        "into meaningful, compact representations while retaining key insights."
    ),
    verbose=True,
    memory=True,
    tools=[search_tool],
    allow_delegation=False
)

# QA Agent
qa_agent = Agent(
    role="Question Answering Expert",
    goal="Answer the user's query based on the summarized text.",
    backstory=(
        "You are skilled at understanding context and generating accurate, "
        "well-structured answers grounded in the provided summaries."
    ),
    verbose=True,
    memory=True,
    tools=[search_tool],
    allow_delegation=False
)

# Citation Agent
citation_agent = Agent(
    role="Citation Expert",
    goal="Attach correct citations and document references to the final answer.",
    backstory=(
        "You ensure that every claim in the final answer is properly supported "
        "by adding document and paragraph-level citations."
    ),
    verbose=True,
    memory=True,
    tools=[search_tool],
    allow_delegation=False 
)

# Define Tasks

retrieve_task = Task(
    description=(
        "Step 1: Identify and extract the most relevant document sections "
        "for the user query: {query}. Return 3-5 most relevant chunks with source IDs."
    ),
    expected_output="A list of relevant text chunks with their source references.",
    tools=[search_tool],
    agent=retriever,
)

summarize_task = Task(
    description=(
        "Step 2: Summarize the text chunks retrieved by the retriever agent. "
        "Focus only on content related to {query} and remove irrelevant information."
    ),
    expected_output="A concise and focused summary of relevant document sections.",
    agent=summarizer,
)

qa_task = Task(
    description=(
        "Step 3: Using the summary, produce a well-reasoned and factual answer "
        "to the query: {query}."
    ),
    expected_output="A detailed and contextually accurate answer to the query.",
    agent=qa_agent,
)

citation_task = Task(
    description=(
        "Step 4: Add proper document citations to the final answer using the retriever’s output. "
        "Format citations like [DocID, Paragraph No.]."
    ),
    expected_output="Final answer text with correct citations and references.",
    agent=citation_agent,
    tools=[search_tool],
    output_file="Answer.md",
)

# Crew Setup

crew = Crew(
    agents=[supervisor, retriever, summarizer, qa_agent, citation_agent],
    tasks=[retrieve_task, summarize_task, qa_task, citation_task],
    process=Process.sequential, 
)

# Run Demo
result = crew.kickoff(
    inputs={
        "query": "What are the key findings about the impact of social media on mental health?"
    }
)
print(result)