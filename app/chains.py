
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

import streamlit as st


GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL = st.secrets["MODEL"]
class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            model=MODEL,
            temperature=0,
            groq_api_key=GROQ_API_KEY,
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
        ### SCRAPE TEXT FOR WEBSITE:
        {page_data}
        
        ### INSTRUCTION:
        The scraped text is from the career's page of a company website.
        Your job is to extract the job postings and return them in JSON format containing the following keys: 'role', 'experience','skills','description'.
        Only return the valid JSON.
        ### NO PREAMBLE
        """
        )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)

        except OutputParserException:
            raise OutputParserException("Content is too big. Unable to parse job.")
        return res if isinstance(res, list) else [res]

    def write_email(self, job, links):
        prompt = PromptTemplate.from_template(
            """
        ### Job Description:
        {job_description}
        
        ### INSTRUCTION:
        You are Abhijeet, a software Engineer. With 1.5 Years of experience in Backend development. Started as chatbot engineer design in and developing chatbots and then transitioned into python backend development. Mostly worked on building APIs in django rest framework and then completed AWS certification. Previous company let go due to financial hardship. I started looking for a job and was not able to find roles and financial expectations. 
Started learning data science and upskilled in SQL,Tableau , PowerBI, Excel,  data cleaning , data visualization , EDA etc. Strong analytical and problem-solving capabilities. A quick learner with an unwavering passion for staying abreast of emerging technologies.

Your job is to write an email to the hiring manager regarding the job mentioned above describing the Abhijeet's capability and add some project links to showcase portfolio{links_list} .
       
 Remember you are Abhijeet.

         Do not provide PREAMBLE.
         ### EMAIL (NO PREAMBLE). 
        """
        )

        chain_email = prompt | self.llm
        res = chain_email.invoke(input={"job_description": job, "links_list": links})
        return res.content
