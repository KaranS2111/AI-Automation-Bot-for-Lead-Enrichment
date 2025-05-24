# 🤖 AI Lead Enrichment Bot

> **Transform your company list into a rich database of leads with AI-powered insights and custom automation pitches**
![demo_pic](https://github.com/user-attachments/assets/1d4ba517-4d75-467c-a775-b1558f24163a)

## 🎯 Overview

The **AI Lead Enrichment Bot** is an intelligent automation tool designed for lead generation and sales intelligence. It takes a simple CSV file containing company names and transforms it into a comprehensive database with:

- **Automated website discovery**
- **Industry classification**
- **AI-generated business summaries**
- **Custom automation pitches tailored for each company**

Perfect for sales teams, marketing agencies, and business development professionals who need to quickly research and qualify leads at scale.

## ✨ Features

### 🔍 **Core Functionality**
- ✅ **Smart Website Discovery** - Automatically finds official company websites using search APIs
- ✅ **Industry Classification** - Categorizes companies using intelligent content analysis
- ✅ **Web Scraping** - Extracts and analyzes homepage content safely and efficiently
- ✅ **AI-Powered Analysis** - Generates business summaries using OpenAI GPT or Google Gemini
- ✅ **Custom Pitch Generation** - Creates tailored automation proposals for each company
- ✅ **Bulk Processing** - Handles multiple companies with progress tracking
- ✅ **Error Resilience** - Robust error handling with detailed logging

### 🖥️ **User Interface**
- ✅ **Streamlit Web App** - Beautiful, intuitive web interface
- ✅ **Real-time Progress** - Live progress bars and status updates
- ✅ **CSV Upload/Download** - Easy file handling with drag-and-drop
- ✅ **Results Preview** - Interactive data tables with sorting and filtering
- ✅ **Sample Data** - Built-in sample files for testing

### 🔧 **Technical Features**
- ✅ **Multiple AI Providers** - Support for OpenAI and Google Gemini APIs
- ✅ **Fallback Mode** - Works without AI APIs for basic enrichment
- ✅ **Rate Limiting** - Prevents API overuse with intelligent delays
- ✅ **Configurable** - Environment variables and command-line options
- ✅ **Logging** - Comprehensive logging for debugging and monitoring

## 🎬 Demo Video

> video_demo.mp4 in GitHub repo contents.
> *The demo video shows the complete workflow from CSV upload to enriched results download*

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Git** (optional, for cloning)

### Method 1: Clone Repository (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/ai-lead-enrichment-bot.git

# Navigate to project directory
cd ai-lead-enrichment-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Direct Download

1. Download the project files from GitHub
2. Extract to your desired directory
3. Open terminal/command prompt in the project directory
4. Follow steps 3-6 from Method 1

### Method 3: Manual Setup

```bash
# Create project directory
mkdir ai-lead-enrichment-bot
cd ai-lead-enrichment-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install pandas==2.0.3 requests==2.31.0 beautifulsoup4==4.12.2 openai==0.28.0 google-generativeai==0.3.2 streamlit==1.28.1 lxml==4.9.3 html5lib==1.1 urllib3==2.0.4 python-dotenv==1.0.0

# Download the Python files and place them in this directory
```

### Verify Installation

```bash
# Test the installation
python -c "import streamlit, pandas, requests, bs4; print('✅ All dependencies installed successfully!')"

# Check Streamlit
streamlit --version
```

## 📖 Usage

### 🌐 Web Interface (Recommended)

1. **Start the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in terminal

3. **Upload your CSV file:**
   - Click "Choose a CSV file" 
   - Select your file with `company_name` column
   - Or download the sample CSV to test

4. **Configure APIs (Optional):**
   - Add OpenAI API key in the sidebar for premium analysis
   - Add Gemini API key for free AI analysis
   - Leave blank for basic enrichment without AI

5. **Process companies:**
   - Click "🚀 Start Enrichment Process"
   - Watch real-time progress
   - View results in the data table

6. **Download results:**
   - Click "📥 Download Enriched CSV"
   - Save the enriched data to your computer

### 💻 Command Line Interface

```bash
# Basic usage
python lead_enrichment_bot.py input_companies.csv

# Specify output file
python lead_enrichment_bot.py input_companies.csv -o enriched_results.csv

# With API keys
python lead_enrichment_bot.py input_companies.csv --openai-key YOUR_OPENAI_KEY --gemini-key YOUR_GEMINI_KEY

# Using environment variables
export OPENAI_API_KEY="your_openai_key_here"
export GEMINI_API_KEY="your_gemini_key_here"
python lead_enrichment_bot.py input_companies.csv
```

### 📝 Input Format

Your CSV file must contain a `company_name` column:

```csv
company_name
OpenAI
DeepMind
Zoho
Freshworks
Slack
Notion
Microsoft
Google
Apple
Amazon
```

### 📊 Output Format

The bot generates a CSV with these 5 columns:

```csv
company_name,website,industry,summary_from_llm,automation_pitch_from_llm
OpenAI,https://openai.com,Technology,"OpenAI is an AI research company...","QF Innovate can help OpenAI automate..."
DeepMind,https://deepmind.com,Technology,"DeepMind is a leading AI research lab...","QF Innovate can develop automated..."
```

## 🔑 API Configuration

### 🆓 Google Gemini API (Recommended - Free)

1. **Get your free API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app)
   - Sign in with your Google account
   - Click "Get API Key" → "Create API Key"
   - Copy your API key

2. **Add to the app:**
   - In Streamlit sidebar: Paste key in "Google Gemini API Key" field
   - For CLI: Use `--gemini-key YOUR_KEY` or set `GEMINI_API_KEY` environment variable

3. **Free quota:**
   - 60 requests per minute
   - 1,500 requests per day
   - Perfect for small to medium datasets

### 💳 OpenAI API (Premium)

1. **Get your API key:**
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Sign in and navigate to API Keys
   - Click "Create new secret key"
   - Copy your API key

2. **Add billing:**
   - Add payment method in OpenAI dashboard
   - Set usage limits to control costs
   - GPT-3.5-turbo costs ~$0.002 per request

3. **Add to the app:**
   - In Streamlit sidebar: Paste key in "OpenAI API Key" field
   - For CLI: Use `--openai-key YOUR_KEY` or set `OPENAI_API_KEY` environment variable

### 🔄 Without APIs (Basic Mode)

The bot works without AI APIs and provides:
- Website discovery
- Industry classification (keyword-based)
- Basic summaries
- Generic automation pitches

## 📊 Sample Data

### Input Example (`input_sample.csv`)
```csv
company_name
OpenAI
Google
Microsoft
Amazon
Tesla
Netflix
```

### Output Example (`output_sample.csv`)
```csv
company_name,website,industry,summary_from_llm,automation_pitch_from_llm
OpenAI,https://openai.com,Technology,"OpenAI develops artificial intelligence systems and large language models for various applications.","QF Innovate can automate OpenAI's customer onboarding process and API usage analytics."
Google,https://google.com,Technology,"Google is a multinational technology company specializing in search, advertising, and cloud services.","QF Innovate can create intelligent data processing workflows and automated reporting systems for Google."
```

## 🏗️ Technical Architecture

### Core Components

1. **LeadEnrichmentBot Class**
   - Main orchestrator
   - Handles API integrations
   - Manages data flow

2. **Website Discovery Engine**
   - DuckDuckGo Instant Answer API
   - Fallback URL construction
   - Domain validation

3. **Web Scraping Module**
   - BeautifulSoup HTML parsing
   - Content cleaning and extraction
   - Rate limiting and retries

4. **AI Analysis Engine**
   - OpenAI GPT-3.5 integration
   - Google Gemini Pro integration
   - Prompt engineering for consistent output

5. **Industry Classification**
   - Keyword-based categorization
   - Content analysis algorithms
   - Machine learning-ready structure

### Data Flow

```
CSV Input → Company Names → Website Discovery → Content Scraping → 
AI Analysis → Industry Classification → Results Assembly → CSV Output
```

### Performance Considerations

- **Rate Limiting**: 1-second delays between requests
- **Timeouts**: 10-15 second timeouts for web requests
- **Error Recovery**: Graceful handling of failed requests
- **Memory Efficiency**: Streaming processing for large datasets
- **Caching**: Future enhancement for repeated requests

## 🛠️ Error Handling

The bot includes comprehensive error handling:

### Network Errors
- **Connection timeouts**: Automatic retries with exponential backoff
- **DNS resolution failures**: Fallback URL construction
- **SSL certificate issues**: Graceful degradation

### API Errors
- **Rate limiting**: Automatic delays and retry logic
- **Authentication failures**: Clear error messages
- **Quota exceeded**: Fallback to basic mode

### Data Errors
- **Missing CSV columns**: Validation with helpful error messages
- **Malformed data**: Skip problematic rows with logging
- **Empty responses**: Default values with error indicators

### Logging

All errors are logged to `logs/enrichment.log` with:
- Timestamp
- Error level (INFO, WARNING, ERROR)
- Detailed error messages
- Stack traces for debugging

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. **"ModuleNotFoundError" when running**
```bash
# Solution: Install dependencies
pip install -r requirements.txt

# Or install individually
pip install streamlit pandas requests beautifulsoup4
```

#### 2. **"Permission denied" error**
```bash
# Solution: Check file permissions
chmod +x lead_enrichment_bot.py

# Or run with python explicitly
python lead_enrichment_bot.py input.csv
```

#### 3. **Streamlit won't start**
```bash
# Solution: Check if port is available
streamlit run streamlit_app.py --server.port 8502

# Or kill existing processes
pkill -f streamlit
```

#### 4. **API errors with Gemini**
- Verify API key is correct
- Check quota limits at [Google AI Studio](https://makersuite.google.com/app)
- Ensure you're in a supported region

#### 5. **Website scraping failures**
- Check internet connection
- Some sites block automated requests (normal behavior)
- The bot will continue with other companies

#### 6. **Slow processing**
- Large datasets take time (1-2 seconds per company)
- Consider processing in smaller batches
- Use basic mode without APIs for faster processing

### Debug Mode

Enable detailed logging:

```bash
# Set debug level
export LOG_LEVEL=DEBUG
python lead_enrichment_bot.py input.csv
```

### Performance Tips

1. **Batch Processing**: Process 50-100 companies at a time
2. **API Keys**: Use Gemini for free processing, OpenAI for premium quality
3. **Network**: Ensure stable internet connection
4. **Resources**: Close other applications for better performance

## 🏆 Acknowledgments

- **OpenAI** for GPT-3.5 API
- **Google** for Gemini Pro API
- **Streamlit** for the amazing web framework
- **BeautifulSoup** for HTML parsing
- **Pandas** for data manipulation

## 🎯 Built for QF Innovate Internship Assignment by Karan Sardar, IIT Roorkee
