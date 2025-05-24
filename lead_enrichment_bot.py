import pandas as pd
import requests
from bs4 import BeautifulSoup
import openai
import google.generativeai as genai
import time
import json
import re
from urllib.parse import urljoin, urlparse
import logging
from typing import Dict, List, Optional, Tuple
import os
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CompanyData:
    name: str
    website: str = ""
    industry: str = ""
    company_size: str = ""
    location: str = ""
    summary: str = ""
    automation_pitch: str = ""

class LeadEnrichmentBot:
    def __init__(self, openai_api_key: str = None, gemini_api_key: str = None):
        self.openai_api_key = openai_api_key
        self.gemini_api_key = gemini_api_key
        
        if openai_api_key:
            openai.api_key = openai_api_key
        
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_company_website(self, company_name: str) -> str:
        try:
            search_url = f"https://api.duckduckgo.com/?q={company_name}&format=json&no_redirect=1"
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'Answer' in data and data['Answer']:
                    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data['Answer'])
                    if urls:
                        return urls[0]
                
                if 'RelatedTopics' in data:
                    for topic in data['RelatedTopics']:
                        if isinstance(topic, dict) and 'FirstURL' in topic:
                            url = topic['FirstURL']
                            if company_name.lower().replace(' ', '') in url.lower():
                                return url
            
            company_clean = company_name.lower().replace(' ', '').replace('inc', '').replace('llc', '').replace('ltd', '')
            return f"https://www.{company_clean}.com"
            
        except Exception as e:
            logger.warning(f"Error searching for {company_name} website: {e}")
            company_clean = company_name.lower().replace(' ', '').replace('inc', '').replace('llc', '').replace('ltd', '')
            return f"https://www.{company_clean}.com"
    
    def get_company_basic_info(self, company_name: str) -> Dict[str, str]:
        try:
            website = self.search_company_website(company_name)
            try:
                response = requests.get(website, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    description = meta_desc.get('content', '') if meta_desc else ''
                    
                    industry = self.infer_industry_from_content(description + ' ' + soup.get_text()[:1000])
                    
                    return {
                        'website': website,
                        'industry': industry,
                        'company_size': 'Unknown',
                        'location': 'Unknown'
                    }
            except:
                pass
            
            return {
                'website': website,
                'industry': 'Unknown',
                'company_size': 'Unknown',
                'location': 'Unknown'
            }
            
        except Exception as e:
            logger.error(f"Error getting basic info for {company_name}: {e}")
            return {
                'website': 'Unknown',
                'industry': 'Unknown',
                'company_size': 'Unknown',
                'location': 'Unknown'
            }
    
    def infer_industry_from_content(self, content: str) -> str:
        content_lower = content.lower()
        
        industry_keywords = {
            'Technology': ['software', 'tech', 'ai', 'artificial intelligence', 'machine learning', 'saas', 'platform', 'app', 'digital'],
            'Healthcare': ['health', 'medical', 'healthcare', 'hospital', 'clinic', 'pharma', 'medicine'],
            'Finance': ['finance', 'banking', 'investment', 'fintech', 'financial', 'trading', 'payments'],
            'E-commerce': ['ecommerce', 'e-commerce', 'retail', 'shopping', 'marketplace', 'store'],
            'Education': ['education', 'learning', 'training', 'school', 'university', 'course'],
            'Manufacturing': ['manufacturing', 'production', 'factory', 'industrial', 'automotive'],
            'Real Estate': ['real estate', 'property', 'housing', 'construction', 'building'],
            'Marketing': ['marketing', 'advertising', 'agency', 'brand', 'campaign', 'social media'],
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return industry
        
        return 'Unknown'
    
    def scrape_website_content(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                return ""
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            text = soup.get_text()
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:3000]
            
        except Exception as e:
            logger.warning(f"Error scraping {url}: {e}")
            return ""
        
    #WITH OPENAI
    def analyze_with_openai(self, company_name: str, website_content: str, industry: str) -> Tuple[str, str]:
        try:
            prompt = f"""
            Analyze the following company information:
            
            Company: {company_name}
            Industry: {industry}
            Website Content: {website_content[:2000]}
            
            Please provide:
            1. A concise summary (2-3 sentences) of what this company does
            2. A custom AI automation pitch (2-3 sentences) that QF Innovate could offer them
            
            Format your response as:
            SUMMARY: [your summary here]
            PITCH: [your automation pitch here]
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            summary = ""
            pitch = ""
            
            if "SUMMARY:" in content and "PITCH:" in content:
                parts = content.split("PITCH:")
                summary = parts[0].replace("SUMMARY:", "").strip()
                pitch = parts[1].strip()
            else:
                summary = content[:150]
                pitch = "Custom AI automation solution tailored to your business needs."
            
            return summary, pitch
            
        except Exception as e:
            logger.error(f"OpenAI API error for {company_name}: {e}")
            return "Unable to generate summary", "Custom AI automation solution available"
        

    #WITH GEMINI
    def analyze_with_gemini(self, company_name: str, website_content: str, industry: str) -> Tuple[str, str]:
        try:
            prompt = f"""
            Analyze this company and provide insights:
            
            Company: {company_name}
            Industry: {industry}
            Website Content: {website_content[:2000]}
            
            Please provide:
            1. SUMMARY: A concise 2-3 sentence summary of what this company does
            2. PITCH: A 2-3 sentence custom AI automation pitch that QF Innovate could offer them
            
            Keep responses professional and focused on business value.
            """
            
            response = self.gemini_model.generate_content(prompt)
            content = response.text
            
            summary = ""
            pitch = ""
            
            if "SUMMARY:" in content and "PITCH:" in content:
                parts = content.split("PITCH:")
                summary = parts[0].replace("SUMMARY:", "").strip()
                pitch = parts[1].strip()
            elif "1." in content and "2." in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if '1.' in line or 'SUMMARY' in line.upper():
                        summary = line.replace('1.', '').replace('SUMMARY:', '').strip()
                    elif '2.' in line or 'PITCH' in line.upper():
                        pitch = line.replace('2.', '').replace('PITCH:', '').strip()
            else:
                summary = content[:150]
                pitch = "Custom AI automation solution tailored to optimize your business processes."
            
            return summary, pitch
            
        except Exception as e:
            logger.error(f"Gemini API error for {company_name}: {e}")
            return "Unable to generate summary", "Custom AI automation solution available"
    
    def enrich_company(self, company_name: str) -> CompanyData:
        logger.info(f"Enriching data for: {company_name}")
        company = CompanyData(name=company_name)
        basic_info = self.get_company_basic_info(company_name)
        company.website = basic_info['website']
        company.industry = basic_info['industry']
        company.company_size = basic_info['company_size']
        company.location = basic_info['location']

        website_content = ""
        if company.website and company.website != 'Unknown':
            website_content = self.scrape_website_content(company.website)
        
        if self.gemini_api_key:
            summary, pitch = self.analyze_with_gemini(company_name, website_content, company.industry)
        elif self.openai_api_key:
            summary, pitch = self.analyze_with_openai(company_name, website_content, company.industry)
        else:
            summary = f"{company_name} operates in the {company.industry} industry."
            pitch = "QF Innovate can provide custom AI automation solutions to streamline your business processes."
        
        company.summary = summary
        company.automation_pitch = pitch
        time.sleep(1)
        
        return company
    
    def process_csv(self, input_file: str, output_file: str = None) -> pd.DataFrame:
        try:
            df = pd.read_csv(input_file)
            
            if 'company_name' not in df.columns:
                raise ValueError("CSV must contain 'company_name' column")
            
            results = []
            total_companies = len(df)
            
            logger.info(f"Processing {total_companies} companies...")
            
            for idx, row in df.iterrows():
                company_name = row['company_name']
                logger.info(f"Processing {idx + 1}/{total_companies}: {company_name}")
                
                try:
                    company_data = self.enrich_company(company_name)
                    results.append({
                        'company_name': company_data.name,
                        'website': company_data.website,
                        'industry': company_data.industry,
                        'summary_from_llm': company_data.summary,
                        'automation_pitch_from_llm': company_data.automation_pitch
                    })
                except Exception as e:
                    logger.error(f"Error processing {company_name}: {e}")
                    results.append({
                        'company_name': company_name,
                        'website': 'Error',
                        'industry': 'Error',
                        'summary_from_llm': f'Error processing: {str(e)}',
                        'automation_pitch_from_llm': 'Unable to generate pitch'
                    })
            
            results_df = pd.DataFrame(results)
            
            if output_file:
                results_df.to_csv(output_file, index=False)
                logger.info(f"Results saved to {output_file}")
            
            return results_df
            
        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            raise

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Lead Enrichment Bot')
    parser.add_argument('input_file', help='Input CSV file with company names')
    parser.add_argument('-o', '--output', help='Output CSV file (optional)')
    parser.add_argument('--openai-key', help='OpenAI API key')
    parser.add_argument('--gemini-key', help='Google Gemini API key')
    
    args = parser.parse_args()
    
    bot = LeadEnrichmentBot(
        openai_api_key=args.openai_key or os.getenv('OPENAI_API_KEY'),
        gemini_api_key=args.gemini_key or os.getenv('GEMINI_API_KEY')
    )
    
    output_file = args.output or args.input_file.replace('.csv', '_enriched.csv')
    results_df = bot.process_csv(args.input_file, output_file)
    
    print(f"\nProcessing complete! Results saved to {output_file}")
    print(f"Processed {len(results_df)} companies successfully.")

if __name__ == "__main__":
    main()