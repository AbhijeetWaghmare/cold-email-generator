import streamlit as st
from chains import Chain
from portfolio import Portfolio
from langchain_community.document_loaders import WebBaseLoader

from utils import clean_text

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

def create_streamlit_app(llm ,portfolio):
    st.title("📧 Cold Mail generator")
    st.subheader("Turn Job Listings into Job Offers with the Ultimate Cold Email Generator!")

    url_input = st.text_input("Enter URL: ", placeholder="Enter job description link ")
    submit_input = st.button("Submit")

    footer_html = """<div style='text-align: center;'>
        <p>Developed with ❤️ by Abhijeet Waghmare</p>
        </div>"""
    st.markdown(footer_html, unsafe_allow_html=True)

    if submit_input:
        
        try:
            loader = WebBaseLoader(url_input)
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:    
                skills = job.get('skills',[])
                links = portfolio.query_links(skills)
                email = llm.write_email(job, links)
                st.code(email, language="markdown")
                
        except Exception as e:
            st.error(f" Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide",page_title="Cold Email Generator", page_icon="📧")
    
    create_streamlit_app(chain, portfolio)
