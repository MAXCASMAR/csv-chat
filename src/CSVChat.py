import pandas as pd
import os
from PostgresDatabase import PostgresDatabase
from keys import REPLICATE_API_TOKEN, OPENAI_API_KEY
import replicate 
from config import REPLICATE_MODEL_ID, CSV_PATH, SCHEMA, TABLE_NAME
from openai import OpenAI

try:
    # export environment variables
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
except:
    # Set OpenAI API Client
    client = OpenAI(api_key=OPENAI_API_KEY)

# read csv data
DATA = pd.read_csv(CSV_PATH)

# utils functions
def get_schema(_) -> dict:
    """
    Retrieves the schema of the provided table name from the PostgresDatabase.

    Returns:
        A dictionary representation of the table's schema.
    """
    SCHEMA_QUERY = f"""SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'listings';"""
    return PostgresDatabase().select(SCHEMA_QUERY).to_dict()

def run_query(query: str) -> pd.DataFrame:
    """
    Executes a given SQL query using the PostgresDatabase and returns the result.

    Args:
        query: A string containing the SQL query to be executed.

    Returns:
        The result of the query execution.
    """
    return PostgresDatabase().select(query)

def get_llm_openai_response(prompt: str) -> str:
    """
    Generates a response from a Large Language Model (LLM) based on the provided prompt.
    
    Args:
        prompt (str): The input prompt or question to be sent to the LLM.

    Returns:
        The response from the LLM as a string.
    
    """
    # Generar respuesta
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0, 
    )
    return response.choices[0].message.content.replace("sql", "").strip().replace("\n", " ").replace("```", "").strip()

def get_llm_response(prompt: str, replicate_model_id: str = REPLICATE_MODEL_ID) -> str:
    """
    Generates a response from a Large Language Model (LLM) based on the provided prompt.
    
    Args:
        prompt (str): The input prompt or question to be sent to the LLM.
        replicate_model_id (str): The id of the replicate model to use.

    Returns:
        The response from the LLM as a string.
    
    """
    response = ""
    for event in replicate.stream(
        replicate_model_id,
        input={
        "top_k": 50,
        "top_p": 0.9,
        "prompt": prompt,
        "temperature": 0.6,
        "max_new_tokens": 512,
        "prompt_template": "<s>[INST] {prompt} [/INST]"
    }
    ):
        response += str(event)
    
    return response.strip().replace("\\_", "_").replace("\_", "_")


class CSVChat:
    """
    A class to generate natural language answers for user questions using SQL queries.
    """
    def __init__(self, replicate_model_id: str = REPLICATE_MODEL_ID):
        self.replicate_model_id = replicate_model_id 
        self.df = DATA
        self.schema = SCHEMA
        self.db = PostgresDatabase()
        self.dhead = self.df.head().to_markdown()
        self.table_name = TABLE_NAME
    
    def __call__(self, question: str) -> str:
        """
        Processes a question, generates a SQL query, executes it and then formulates a natural language response.

        Args:
            question (str): The user's question.

        Returns:
            A natural language answer to the question based on tabular data.
        """
        self.question = question
        self.build_sql_template()
        self.sql_query = get_llm_response(self.sql_template)
        print(self.sql_query)
        self.sql_response = run_query(self.sql_query)
        self.build_answer_template()
        self.answer = get_llm_response(self.answer_template)
        return self.answer

    def build_sql_template(self):
        """
        Builds a template for generating a SQL query based on the given schema and data frame.
        """

        self.sql_template = f"""Based on the table schema, some observations, and unique values of some columns below, write a SQL query that would answer the user's question, ONLY RETURN THE SQL QUERY, no pre-amble:
        
        SCHEMA:
        {self.schema}

        It is important to understand the attributes of the dataframe before working with it. There could be more than one where conditions in the final sql query. This is the result of running `df.head().to_markdown()`

        <df>
        {self.dhead}
        </df>

        Unique values of some columns:
        listing_type: 'for-sale', 'for-rent'
        property_type: 'apartment', 'house'

        Table name: {self.table_name}
        Question: {self.question}
        Postgres SQL Query:"""

    def build_answer_template(self,):
        """
        Builds a template for generating a natural language answer based on the SQL query and its response.
        """
        self.answer_template = f"""Based on the table schema below, question, sql query, and sql response, write a natural language response. ONLY RETURN THE RESPONSE, no pre-amble:
        {self.schema}

        Question: {self.question}
        SQL Query: {self.sql_query}
        SQL Response: {self.sql_response}"""

if __name__ == "__main__":
    chat = CSVChat()
    question = "¿Cuál es el precio promedio de los apartamentos en venta?"
    answer = chat(question)
    print(answer)




        
