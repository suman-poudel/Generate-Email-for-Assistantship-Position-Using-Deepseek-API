# Generate Email for Assistantship Position Using Deepseek API

This project is a Streamlit-based web application designed to generate professional emails for Master's or PhD assistantship opportunities. It leverages the Deepseek API (via OpenRouter) to create concise and engaging emails based on a user's CV and a professor's research papers, scraped from Google Scholar or uploaded as a CSV file.

## Features
- Upload a CV (PDF or DOCX) and professor's research paper data (CSV or scraped from Google Scholar).
- Convert uploaded files to markdown format for processing.
- Generate a professional email expressing interest in a professor's research, highlighting relevant skills, and proposing collaboration or assistantship opportunities.
- Interactive Streamlit interface for easy file uploads and data input.

## Prerequisites
To run this project, you need:
- Python 3.8 or higher
- A Deepseek API key (via [OpenRouter](https://openrouter.ai/))
- A Google Scholar profile URL for scraping research papers (optional)
- Access to the `MarkItDown` library or a similar markdown conversion tool

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/Generate-Email-for-Assistantship-Position-Using-Deepseek-API.git
   cd Generate-Email-for-Assistantship-Position-Using-Deepseek-API
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

   Sample `requirements.txt`:
   ```
   streamlit
   pandas
   openai
   groq
   markitdown
   ```

   **Note**: The `markitdown` and `web_scrape_papers` libraries may require custom installation or specific versions. Ensure they are compatible with your setup.

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your Deepseek API key:
   ```plaintext
   DEEPSEEK_API_KEY=your-api-key-here
   ```

## Usage
1. **Run the Application**:
   Start the Streamlit app:
   ```bash
   streamlit run main_app_using_open_router.py
   ```

2. **Interact with the App**:
   - Upload your CV in PDF or DOCX format.
   - Provide a Google Scholar profile URL to scrape research papers or upload a CSV file with research paper data.
   - Click the "Scrape Data from Google Scholar" button if using a URL.
   - The app will generate a professional email based on the provided CV and research data.

3. **Output**:
   - The generated email will appear in a text area, ready to be copied and used.
   - Scraped Google Scholar data is saved as a CSV file in the project directory.

## Project Structure
```plaintext
├── main_app_using_open_router.py  # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
└── .env                           # Environment variables (not tracked in Git)
```

## Notes
- **Google Scholar Scraping**: The `get_papers_from_google_scholar` function (not included in this repository) is assumed to be available. Ensure it is implemented or replaced with a suitable alternative.
- **MarkItDown**: The `MarkItDown` library is used for converting files to markdown. Verify its compatibility or replace it with a similar tool if needed.
- **Temporary Files**: The app creates temporary files for processing uploaded data and cleans them up automatically.
- **Error Handling**: Ensure valid file formats and a working API key to avoid runtime errors.

## Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or issues, please open an issue on GitHub or contact the repository owner.