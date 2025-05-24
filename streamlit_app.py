import streamlit as st
import pandas as pd
import io
import os
from lead_enrichment_bot import LeadEnrichmentBot
import time

st.set_page_config(
    page_title="AI Lead Enrichment Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Lead Enrichment Bot</h1>
        <p>Transform your company list into a rich database of leads with AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
 
    with st.sidebar:
        st.header("🔧 Configuration")
        

        st.subheader("API Keys")
        openai_key = st.text_input("OpenAI API Key", type="password", help="Optional: For GPT-powered analysis")
        gemini_key = st.text_input("Google Gemini API Key", type="password", help="Optional: Free alternative to OpenAI")
        
 
        st.info("""
        **API Information:**
        - **Gemini API**: Free with quota from [Google AI Studio](https://makersuite.google.com/app)
        - **OpenAI API**: Requires paid account
        - **Without APIs**: Basic enrichment will still work
        """)
        

        st.subheader("✨ Features")
        st.markdown("""
        - 🔍 Company website discovery
        - 🏢 Industry classification
        - 📝 AI-powered summaries
        - 💡 Custom automation pitches
        - 📊 Bulk processing
        - 📥 CSV export
        """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload Your Company List")
 
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="CSV should contain a 'company_name' column"
        )
        
        sample_data = pd.DataFrame({
            'company_name': ['OpenAI', 'DeepMind', 'Zoho', 'Freshworks', 'Slack', 'Notion']
        })
        
        st.download_button(
            label="📥 Download Sample CSV",
            data=sample_data.to_csv(index=False),
            file_name="sample_companies.csv",
            mime="text/csv"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                if 'company_name' not in df.columns:
                    st.error("❌ CSV must contain a 'company_name' column")
                    return
                
                st.success(f"✅ Successfully loaded {len(df)} companies")
                
               
                st.subheader("📋 Data Preview")
                st.dataframe(df.head(), use_container_width=True)
                
            
                if st.button("🚀 Start Enrichment Process", type="primary", use_container_width=True):
                    process_companies(df, openai_key, gemini_key)
                    
            except Exception as e:
                st.error(f"❌ Error reading CSV: {str(e)}")
    
    with col2:
        st.header("📊 Process Overview")
        
        st.markdown("""
        <div class="feature-box">
            <h4>🔄 Enrichment Process</h4>
            <ol>
                <li><strong>Website Discovery</strong> - Find official websites</li>
                <li><strong>Content Scraping</strong> - Extract homepage content</li>
                <li><strong>Industry Classification</strong> - Categorize companies</li>
                <li><strong>AI Analysis</strong> - Generate summaries & pitches</li>
                <li><strong>Export Results</strong> - Download enriched data</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📈 Output Fields")
        output_fields = [
            "company_name", "website", "industry", 
            "summary_from_llm", "automation_pitch_from_llm"
        ]
        
        for field in output_fields:
            st.write(f"• **{field}**")

def process_companies(df, openai_key, gemini_key):
 
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        bot = LeadEnrichmentBot(
            openai_api_key=openai_key if openai_key else None,
            gemini_api_key=gemini_key if gemini_key else None
        )
        
   
        results = []
        total_companies = len(df)
        
        status_text.text("🔄 Starting enrichment process...")
        
        for idx, row in df.iterrows():
            company_name = row['company_name']
            

            progress = (idx + 1) / total_companies
            progress_bar.progress(progress)
            status_text.text(f"🔄 Processing {idx + 1}/{total_companies}: {company_name}")
            
            try:
                company_data = bot.enrich_company(company_name)
                
                results.append({
                    'company_name': company_data.name,
                    'website': company_data.website,
                    'industry': company_data.industry,
                    'summary_from_llm': company_data.summary,
                    'automation_pitch_from_llm': company_data.automation_pitch
                })
                
            except Exception as e:
                st.warning(f"⚠️ Error processing {company_name}: {str(e)}")
                results.append({
                    'company_name': company_name,
                    'website': 'Error',
                    'industry': 'Error',
                    'summary_from_llm': f'Error: {str(e)}',
                    'automation_pitch_from_llm': 'Unable to generate pitch'
                })
        
     
        progress_bar.progress(1.0)
        status_text.text("✅ Enrichment process completed!")
        
 
        results_df = pd.DataFrame(results)
        
        st.markdown("""
        <div class="success-box">
            <h4>🎉 Enrichment Complete!</h4>
            <p>Your company data has been successfully enriched with AI-powered insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("📊 Enriched Results")
        st.dataframe(results_df, use_container_width=True)
        
        csv_buffer = io.StringIO()
        results_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Enriched CSV",
            data=csv_data,
            file_name=f"enriched_companies_{int(time.time())}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )
        
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Companies Processed", len(results_df))
        
        with col2:
            successful = len([r for r in results if r['website'] != 'Error'])
            st.metric("Successful Enrichments", successful)
        
        with col3:
            success_rate = (successful / len(results_df)) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        status_text.text("❌ Process failed")

def show_demo():
    """Show demo results"""
    st.header("🎬 Demo Results")
    

    demo_data = pd.DataFrame({
        'company_name': ['OpenAI', 'Slack', 'Notion'],
        'website': ['https://openai.com', 'https://slack.com', 'https://notion.so'],
        'industry': ['Technology', 'Technology', 'Technology'],
        'summary_from_llm': [
            'OpenAI is an AI research company developing artificial general intelligence for the benefit of humanity.',
            'Slack is a business communication platform that brings teams together through organized conversations.',
            'Notion is an all-in-one workspace that combines notes, tasks, wikis, and databases for productivity.'
        ],
        'automation_pitch_from_llm': [
            'QF Innovate can help OpenAI automate customer onboarding and API usage analytics with custom AI workflows.',
            'QF Innovate can develop automated meeting summarization and task extraction bots for Slack workspaces.',
            'QF Innovate can create intelligent content organization and automated workflow templates for Notion users.'
        ]
    })
    
    st.dataframe(demo_data, use_container_width=True)


st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>🤖 AI Lead Enrichment Bot | Built for QF Innovate Internship Task</p>
    <p>Powered by OpenAI, Google Gemini, and Beautiful Soup</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()