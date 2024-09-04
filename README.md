# Content Readability Scorer

## Description

The Content Readability Scorer is a Streamlit-based web application that analyzes the readability of web content. It uses the Firecrawl API to fetch web content and applies various readability metrics to provide insights into the complexity and accessibility of the text.

## Features

- Analyzes web content for readability using multiple metrics:
  - Flesch Reading Ease
  - Flesch-Kincaid Grade Level
  - SMOG Index
  - Coleman-Liau Index
  - Automated Readability Index
- Provides additional text statistics:
  - Average sentence length
  - Average word length
  - Total word count
  - Total sentence count
- Visualizes readability scores using a bar chart
- Offers interpretation of readability scores

## Installation

1. Clone this repository:

2. Install the required dependencies:

   
   pip install -r requirements.txt
   ```

3. Set up your Firecrawl API key:
   - Create a .env` file in the project root
   - Add your Firecrawl API key to the .env` file:
     
     FIRECRAWL_API_KEY=your_api_key_here
     ```

## Usage

1. Run the Streamlit app:

   
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually http://localhost:8501`)

3. Enter a URL in the sidebar and click "Analyze Content"

4. View the readability analysis results, visualizations, and interpretations

## Dependencies

- streamlit
- pandas
- matplotlib
- seaborn
- firecrawl
- python-dotenv
- beautifulsoup4
- textstat

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Firecrawl](https://firecrawl.com/) for providing the web scraping API
- [Streamlit](https://streamlit.io/) for the easy-to-use web app framework
- [textstat](https://pypi.org/project/textstat/) for readability calculations

## Disclaimer

This tool provides a basic readability analysis and should not be considered a comprehensive content evaluation. For thorough content assessment, consider consulting with content strategy experts and conducting user testing.
