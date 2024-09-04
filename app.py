import os
os.environ['MPLBACKEND'] = 'Agg'  # Set this before importing matplotlib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re
import textstat

# Load environment variables
load_dotenv()

# Initialize FirecrawlApp with the API key
firecrawl_api_key = os.getenv('FIRECRAWL_API_KEY')
firecrawl_app = FirecrawlApp(api_key=firecrawl_api_key)

# Set up the Streamlit app
st.title('Content Readability Scorer')

# Sidebar for user input
st.sidebar.header('User Input')
url = st.sidebar.text_input('Enter URL to analyze:')
analyze_button = st.sidebar.button('Analyze Content')

def simple_sentence_tokenize(text):
    return re.findall(r'[^.!?]+[.!?]', text)

def simple_word_tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def analyze_readability(url):
    result = firecrawl_app.scrape_url(url, params={'formats': ['html']})
    html_content = result.get('html', '')
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract main content (you might need to adjust this based on the website structure)
    main_content = soup.find('main') or soup.find('article') or soup.find('body')
    text_content = main_content.get_text(separator=' ', strip=True)
    
    # Clean the text
    text_content = re.sub(r'\s+', ' ', text_content)
    
    # Calculate readability scores
    flesch_reading_ease = textstat.flesch_reading_ease(text_content)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(text_content)
    smog_index = textstat.smog_index(text_content)
    coleman_liau_index = textstat.coleman_liau_index(text_content)
    automated_readability_index = textstat.automated_readability_index(text_content)
    
    # Calculate additional metrics
    sentences = simple_sentence_tokenize(text_content)
    words = simple_word_tokenize(text_content)
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    return {
        'flesch_reading_ease': flesch_reading_ease,
        'flesch_kincaid_grade': flesch_kincaid_grade,
        'smog_index': smog_index,
        'coleman_liau_index': coleman_liau_index,
        'automated_readability_index': automated_readability_index,
        'avg_sentence_length': avg_sentence_length,
        'avg_word_length': avg_word_length,
        'total_words': len(words),
        'total_sentences': len(sentences)
    }

def interpret_score(score, metric):
    if metric == 'flesch_reading_ease':
        if score >= 90: return 'Very Easy'
        elif score >= 80: return 'Easy'
        elif score >= 70: return 'Fairly Easy'
        elif score >= 60: return 'Standard'
        elif score >= 50: return 'Fairly Difficult'
        elif score >= 30: return 'Difficult'
        else: return 'Very Difficult'
    else:  # For grade-level scores
        if score <= 6: return 'Easy'
        elif score <= 10: return 'Average'
        elif score <= 14: return 'Difficult'
        else: return 'Very Difficult'

if analyze_button and url:
    with st.spinner('Analyzing content readability...'):
        try:
            results = analyze_readability(url)
            
            st.subheader('Readability Analysis Results')
            
            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Flesch Reading Ease", f"{results['flesch_reading_ease']:.2f}", 
                          interpret_score(results['flesch_reading_ease'], 'flesch_reading_ease'))
                st.metric("Flesch-Kincaid Grade", f"{results['flesch_kincaid_grade']:.2f}", 
                          interpret_score(results['flesch_kincaid_grade'], 'grade'))
                st.metric("SMOG Index", f"{results['smog_index']:.2f}", 
                          interpret_score(results['smog_index'], 'grade'))
            with col2:
                st.metric("Coleman-Liau Index", f"{results['coleman_liau_index']:.2f}", 
                          interpret_score(results['coleman_liau_index'], 'grade'))
                st.metric("Automated Readability Index", f"{results['automated_readability_index']:.2f}", 
                          interpret_score(results['automated_readability_index'], 'grade'))
            
            st.subheader('Additional Metrics')
            st.write(f"Average Sentence Length: {results['avg_sentence_length']:.2f} words")
            st.write(f"Average Word Length: {results['avg_word_length']:.2f} characters")
            st.write(f"Total Words: {results['total_words']}")
            st.write(f"Total Sentences: {results['total_sentences']}")
            
            # Visualize results
            fig, ax = plt.subplots()
            scores = [results['flesch_reading_ease'], results['flesch_kincaid_grade'], 
                      results['smog_index'], results['coleman_liau_index'], 
                      results['automated_readability_index']]
            labels = ['Flesch Reading Ease', 'Flesch-Kincaid Grade', 'SMOG Index', 
                      'Coleman-Liau Index', 'Automated Readability Index']
            sns.barplot(x=labels, y=scores, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
            ax.set_ylabel('Score')
            ax.set_title('Readability Scores')
            st.pyplot(fig)
            
            st.subheader('Interpretation')
            st.write("""
            - Flesch Reading Ease: Higher scores indicate easier readability (0-100 scale).
            - Other indices approximate the U.S. grade level needed to understand the text.
            - Aim for a Flesch Reading Ease score above 60 for general audience content.
            - For most web content, aim for a grade level between 7-9 for optimal readability.
            """)
            
        except Exception as e:
            st.error(f"Error analyzing {url}: {str(e)}")

# Firecrawl API key status
st.sidebar.subheader('Firecrawl API Status')
if firecrawl_api_key:
    st.sidebar.success('Firecrawl API key is set')
else:
    st.sidebar.error('Firecrawl API key is not set')
