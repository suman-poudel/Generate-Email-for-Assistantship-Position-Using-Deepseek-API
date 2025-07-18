import os
from markitdown import MarkItDown
import streamlit as st
from web_scrape_papers import get_papers_from_google_scholar
import tempfile
from openai import OpenAI

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=DEEPSEEK_API_KEY,
)

model = "deepseek/deepseek-r1-0528:free"


def make_markdown_from_file(data):
    md = MarkItDown(enable_plugins=False)
    markdown_data = md.convert(data)
    limited_markdown = markdown_data.text_content[:100000] + "..." if len(markdown_data.text_content) > 100000 else markdown_data.text_content
    return limited_markdown




def write_email_deepseek(cv, data, model, email_query):
    markdown_cv = make_markdown_from_file(cv)
    st.text_area("CV in markdown format", value=markdown_cv, height=200)
    markdown_data = make_markdown_from_file(data)
    st.text_area("Research Paper Data in markdown format", value=markdown_data, height=200)
    completion = client.chat.completions.create(
        model=model,
        messages=[
        {
            "role": "user",
            "content": [
                        {
                            "type": "text",
                            "text": email_query
                        },
                        {
                            "type": "text",
                            "text": f"CV Summary:\n{markdown_cv}"
                        },
                        {
                            "type": "text",
                            "text": f"Data Summary:\n{markdown_data}"
                        }
                    ]
        },
        ]
    )

    return completion.choices[0].message.content


st.title("Finding Assistantship/PhD Opportunities with Professors")



uploaded_cv = st.file_uploader("Upload your CV in Pdf or docx format", type=["pdf", "docx"])
website_url = st.text_input("Enter the professor's Google Scholar profile URL for scrapping google scholar data", placeholder="https://scholar.google.com/citations?user=XXXXXXXXX&hl=en")
website_url = os.path.join(website_url, "&view_op=list_works&sortby=pubdate")
scrape_button = st.button("Scrape Data from Google Scholar")

if scrape_button:
    if not website_url:
        st.error("Please enter a valid Google Scholar profile URL.")
    else:
        uploaded_data, researcher_name = get_papers_from_google_scholar(website_url)
        
        st.success("Data scraped successfully!")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            # Write the uploaded file's content to the temporary file
            uploaded_data.to_csv(tmp_file.name, index=False)
            # Get the file path
            data_file_path = tmp_file.name
            
else:
    st.write("If you have CSV data of your professor's research papers, you can upload it below.")
    uploaded_data = st.file_uploader("Upload Data in CSV format", type=["csv"])

    if uploaded_data is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            # Write the uploaded file's content to the temporary file
            tmp_file.write(uploaded_data)
            # Get the file path
            data_file_path = tmp_file.name



email_query = (
    '''I have provided my CV and csv data of my professor's research papers. Using the information from my CV and professor's research papers, Write a concise, professional email to the Professor, an expert in specific field, expressing interest in his research, noting alignment with my work, referencing specific papers/topics from his provided research papers (CSV file), highlighting my skills/experiences from my CV as well as academic profile, and proposing collaboration or interest in joining his research group as a Master’s/PhD student. Make the email concise, professional, and engaging. Only return the email content without any additional text or formatting.

    Subject: [Your desired subject line, e.g., Interest in Joining Your Research Group in Water Resources Engineering]

    Dear Professor [Professor's Last Name],

    [Body of the email, referencing specific papers/topics, aligning with your skills/experiences, strong academic profile and proposing collaboration or joining the research group.]

    Sincerely,  
    [Your Name]
    [Institution]
    [University]
    [Country]'''
)



if (uploaded_cv is not None) and (uploaded_data is not None):
    st.success("Files uploaded successfully!")
    try:
        raw_response = write_email_deepseek(uploaded_cv, data_file_path, model, email_query)
        st.text_area("Email for Master's or PhD Student", value=raw_response, height=300)
        print("Email Generated Successfully")
    finally:
        # Clean up the temporary file
        if os.path.exists(data_file_path):
            os.unlink(data_file_path)