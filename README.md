# Company Information Extraction System

A robust AI-powered system that leverages Google's Gemini API to extract essential company details from textual content and generates structured CSV output. This project demonstrates the use of LangChain and intelligent agents for automated data processing and extraction.

## 🎯 Project Overview

This system analyzes essays or documents containing company information and automatically extracts:

- **Company Names** (Full official names)
- **Founding Dates** (Normalized to YYYY-MM-DD format)
- **Founders** (Complete list of founding members)

In certain scenarios, the complete date information may not be available. To handle such cases:

-**If only the year is provided, default the date to January 1st of that year. 
-**If the year and month are provided, default the date to the 1st day of the specified month.

The extracted data is then exported to a clean, structured CSV file for further analysis or integration with other systems.

## 🚀 Features

- **AI-Powered Extraction**: Uses Google Gemini 2.5 Flash Lite for intelligent text processing
- **Smart Date Normalization**: Converts various date formats to standardized YYYY-MM-DD
- **Robust JSON Parsing**: Handles markdown-wrapped JSON responses
- **Error Handling**: Graceful fallback for parsing failures
- **CSV Export**: Clean, structured output ready for analysis
- **Single API Call**: Efficient processing of entire documents

## 📋 Requirements

```
langchain-google-genai
python-dotenv
```

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/DevilGod129/AI_assignment.git
   cd AI_assignment
   ```

2. **Install dependencies**:

   ```bash
   pip install langchain-google-genai python-dotenv
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:

   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

   Get your API key from: https://ai.google.dev/

## 📁 Project Structure

```
company-extraction-system/
├── main.py              # Main extraction script
├── essay_text.py        # Contains the essay data
├── .env                 # Environment variables (not in repo)
├── .gitignore          # Git ignore file
├── company_info.csv    # Output file (gitignored)
└── README.md           # This file
```

## 🎮 Usage

1. **Prepare your data**: Update `essay_text.py` with your essay content
2. **Run the extraction**:
   ```bash
   python main.py
   ```
3. **Check output**: The system will generate `company_info.csv` with extracted data

## 📊 Expected Output

The system processes the provided essay and extracts **28 companies**. Here's the complete expected output:

```csv
S.N.,Company Name,Founded in,Founded by
1,The Coca-Cola Company,1886-05-08,['Dr. John Stith Pemberton']
2,Sony Corporation,1946-05-07,"['Masaru Ibuka', 'Akio Morita']"
3,McDonald's Corporation,1955-04-15,['Ray Kroc']
4,Intel Corporation,1968-07-18,"['Robert Noyce', 'Gordon Moore']"
5,"Samsung Electronics Co., Ltd.",1969-01-13,['Lee Byung-chul']
6,Microsoft Corporation,1975-04-04,"['Bill Gates', 'Paul Allen']"
7,Apple Inc.,1976-04-01,"['Steve Jobs', 'Steve Wozniak', 'Ronald Wayne']"
8,Oracle Corporation,1977-06-16,"['Larry Ellison', 'Bob Miner', 'Ed Oates']"
9,NVIDIA Corporation,1993-04-05,"['Jensen Huang', 'Chris Malachowsky', 'Curtis Priem']"
10,Amazon.com Inc.,1994-07-05,['Jeff Bezos']
11,Google LLC,1998-09-04,"['Larry Page', 'Sergey Brin']"
12,Alibaba Group Holding Limited,1999-06-28,['Jack Ma']
13,SAP SE,1972-04-01,"['Dietmar Hopp', 'Hans-Werner Hector', 'Hasso Plattner', 'Klaus Tschira', 'Claus Wellenreuther']"
14,LinkedIn Corporation,2002-12-28,['Reid Hoffman']
15,"Facebook, Inc.",2004-02-04,['Mark Zuckerberg']
16,"Twitter, Inc.",2006-03-21,"['Jack Dorsey', 'Biz Stone', 'Evan Williams']"
17,Spotify AB,2006-04-23,"['Daniel Ek', 'Martin Lorentzon']"
18,YouTube LLC,2005-02-14,"['Steve Chen', 'Chad Hurley', 'Jawed Karim']"
19,"Tesla, Inc.",2003-07-01,"['Elon Musk', 'Martin Eberhard', 'Marc Tarpenning', 'JB Straubel', 'Ian Wright']"
20,"Airbnb, Inc.",2008-08-01,"['Brian Chesky', 'Joe Gebbia', 'Nathan Blecharczyk']"
21,"PayPal Holdings, Inc.",1998-12-01,"['Peter Thiel', 'Max Levchin', 'Luke Nosek', 'Ken Howery']"
22,"Stripe, Inc.",2010-01-01,"['Patrick Collison', 'John Collison']"
23,"Square, Inc.",2009-02-20,"['Jack Dorsey', 'Jim McKelvey']"
24,"Zoom Video Communications, Inc.",2011-04-21,['Eric Yuan']
25,"Slack Technologies, LLC",2009-01-01,"['Stewart Butterfield', 'Eric Costello', 'Cal Henderson', 'Serguei Mourachov']"
26,"Rivian Automotive, Inc.",2009-06-23,['RJ Scaringe']
27,SpaceX,2002-03-14,['Elon Musk']
28,TikTok,2016-09-01,['Zhang Yiming']

```

## 🧠 How It Works

### 1. **AI-Powered Analysis**

The system uses Google Gemini to analyze the entire essay and identify company mentions with their founding details.

### 2. **Smart Extraction**

The AI agent makes intelligent decisions about:

- Which text segments contain company information
- How to parse founder names from various formats
- How to handle incomplete date information

### 3. **Data Normalization**

- **Dates**: Converted to YYYY-MM-DD format (missing day/month default to 01)
- **Company Names**: Extracted as full official names
- **Founders**: Parsed into clean lists of individual names

### 4. **Output Generation**

Structured CSV output with consistent formatting for downstream processing.

## 🔧 Technical Implementation

### Key Components:

- **LangChain Integration**: Uses `ChatGoogleGenerativeAI` for AI processing
- **JSON Response Handling**: Robust parsing with markdown cleanup
- **Date Processing**: Smart normalization of various date formats
- **Error Handling**: Graceful degradation on parsing failures
- **Single API Call Strategy**: Efficient processing of entire documents

### Code Structure:

```python
# Main workflow
1. Load essay content
2. Create extraction prompt
3. Call Gemini API once
4. Parse JSON response
5. Generate CSV output
```

## 🎯 Assignment Requirements Met

✅ **LCEL Runnable Interface**: Uses LangChain's ChatGoogleGenerativeAI
✅ **Intelligent Agent**: AI makes decisions about data extraction
✅ **Text Parsing**: Processes essay content systematically
✅ **Data Extraction**: Extracts company names, dates, and founders
✅ **Date Normalization**: Handles incomplete dates with defaults
✅ **CSV Output**: Generates structured company_info.csv
✅ **Scalable Design**: Can process various document types

## 🚨 Notes

- The `company_info.csv` file is included in `.gitignore` to avoid committing generated data
- API key should never be committed to version control
- The system handles various date formats and company name variations
- Extraction quality depends on the clarity and structure of input text

## 📄 License

This project is part of an academic assignment demonstrating AI-powered data extraction techniques.

## 🆘 Troubleshooting

**Common Issues:**

1. **API Key Error**: Ensure your `.env` file contains a valid Google API key
2. **Import Error**: Install required packages with `pip install -r requirements.txt`
3. **Empty Output**: Check that essay_text.py contains the essay content
4. **JSON Parse Error**: The system includes error handling and will display raw output for debugging

**Getting Help:**

- Check that your Gemini API key is active and has sufficient quota
- Verify the essay content is properly formatted in essay_text.py
- Review the console output for any error messages
