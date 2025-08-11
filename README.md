# Company Information Extraction System

A robust AI-powered system that leverages Google's Gemini API with LangChain's LCEL (LangChain Expression Language) and intelligent agents to extract essential company details from textual content and generates structured CSV output. This project demonstrates advanced agentic workflows with tools and paragraph-level processing.

## 🎯 Project Overview

This system analyzes essays or documents containing company information and automatically extracts:

- **Company Names** (Full official names)
- **Founding Dates** (Normalized to YYYY-MM-DD format)
- **Founders** (Complete list of founding members)

The system uses an **agentic workflow** that processes each paragraph individually, using **LCEL Runnable Interface** and **Tools** for intelligent extraction and data management.

In certain scenarios, the complete date information may not be available. To handle such cases:

- **If only the year is provided, default the date to January 1st of that year.** 
- **If the year and month are provided, default the date to the 1st day of the specified month.**

The extracted data is then exported to a clean, structured CSV file for further analysis or integration with other systems.

## 🚀 Features

- **LCEL Runnable Interface**: Uses LangChain's advanced chain composition
- **Intelligent Agent Workflow**: Tool-calling agents for smart data extraction  
- **Paragraph-by-Paragraph Processing**: Efficient individual paragraph analysis
- **Smart Date Normalization**: Converts various date formats to standardized YYYY-MM-DD
- **Tool-Based Architecture**: Uses `@tool` decorator for structured data saving
- **Robust Error Handling**: Graceful handling of API rate limits and failures
- **CSV Export**: Clean, structured output ready for analysis
- **Deduplication**: Automatic removal of duplicate company entries

## 📋 Requirements

```
langchain-google-genai
langchain-core
langchain
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
   pip install langchain-google-genai langchain-core langchain python-dotenv
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
├── main.py              # Main extraction script with LCEL and Tools
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

**Note**: The system may encounter rate limits on Gemini's free tier (15 requests/minute). It will automatically retry and continue processing.

## 📊 Expected Output

The system processes the provided essay and extracts **30 companies**. Here's a sample of the output:

```csv
S.N.,Company Name,Founded in,Founded by
1,The Coca-Cola Company,1886-05-08,['Dr. John Stith Pemberton']
2,Sony Corporation,1946-05-07,"['Masaru Ibuka', 'Akio Morita']"
3,McDonald's Corporation,1955-04-15,"['Ray Kroc', 'Richard McDonald', 'Maurice McDonald']"
4,Intel Corporation,1968-07-18,"['Robert Noyce', 'Gordon Moore']"
5,"Samsung Electronics Co., Ltd.",1969-01-13,['Lee Byung-chul']
...and 25 more companies
```

**Complete extraction includes**: Coca-Cola, Sony, McDonald's, Intel, Samsung, SAP, Microsoft, Apple, Oracle, NVIDIA, Amazon, Google, PayPal, Alibaba, SpaceX, LinkedIn, Tesla, Facebook, YouTube, Twitter, Spotify, Airbnb, Slack, Square, Block, Rivian, Stripe, Zoom, TikTok, and more.

## 🧠 How It Works

### 1. **LCEL Chain Architecture**

```python
# LCEL Runnable chain for paragraph processing
paragraph_processor = RunnableLambda(process_paragraph)
batch_processor = create_batch_processor()
```

### 2. **Tool-Based Extraction**

```python
@tool
def save_company_info(company_name: str, founding_date: str, founders: List[str]) -> str:
    """Tool to save extracted company information"""
```

### 3. **Agentic Workflow**

The system uses `create_tool_calling_agent` with:
- **Agent**: Makes intelligent decisions about data extraction
- **Tools**: Structured company data storage
- **Executor**: Manages the agent-tool interaction loop

### 4. **Paragraph-Level Processing**

1. **Split**: Essay divided into individual paragraphs
2. **Process**: Each paragraph analyzed by the agent
3. **Extract**: Agent calls tools to save company data
4. **Aggregate**: All extracted data combined and deduplicated

### 5. **Data Normalization**

- **Dates**: Converted to YYYY-MM-DD format (missing day/month default to 01)
- **Company Names**: Extracted as full official names
- **Founders**: Parsed into clean lists of individual names
- **Deduplication**: Removes duplicate companies based on name similarity

## 🔧 Technical Implementation

### Key Components:

- **LCEL Runnables**: `RunnableLambda` for custom processing logic
- **Tool Calling Agent**: `create_tool_calling_agent` for intelligent extraction
- **Agent Executor**: `AgentExecutor` for managing agent workflows
- **Tools**: `@tool` decorated functions for structured data operations
- **Prompt Templates**: `ChatPromptTemplate.from_messages` for agent instructions

### Code Architecture:

```python
# Advanced workflow with LCEL and Tools
1. Split essay into paragraphs (RunnableLambda)
2. Create tool-calling agent with extraction tools
3. Process each paragraph through agent executor
4. Agent calls save_company_info tool for each company found
5. Aggregate and deduplicate extracted data
6. Generate structured CSV output
```

## 🎯 Assignment Requirements Met

✅ **LCEL Runnable Interface**: Uses `RunnableLambda` and custom chain composition  
✅ **Tools and Tool Calling**: Implements `@tool` decorator and `create_tool_calling_agent`  
✅ **Agentic Workflow**: Uses `AgentExecutor` for intelligent processing  
✅ **Paragraph Processing**: Individual paragraph analysis as specified  
✅ **Data Extraction**: Extracts company names, dates, and founders systematically  
✅ **Date Normalization**: Handles incomplete dates with intelligent defaults  
✅ **CSV Output**: Generates structured company_info.csv  
✅ **Scalable Design**: Token-efficient paragraph-by-paragraph processing  

## 🚨 Notes

- **Rate Limiting**: Free tier has 15 requests/minute limit - system handles this automatically
- **Token Efficiency**: Paragraph processing optimizes token usage vs. single large API call
- **Agent Decisions**: AI agent intelligently decides when and how to extract company data
- **Tool Architecture**: Structured approach using LangChain's tool calling framework
- API key should never be committed to version control
- The system handles various date formats and company name variations

## 🆘 Troubleshooting

**Common Issues:**

1. **Rate Limit Errors**: Normal on free tier - system will retry automatically
2. **API Key Error**: Ensure your `.env` file contains a valid Google API key
3. **Import Error**: Install all required packages: `langchain-google-genai`, `langchain-core`, `langchain`
4. **Agent Scratchpad Error**: Ensure prompt template includes `{agent_scratchpad}` placeholder
5. **Empty Output**: Check that essay_text.py contains the essay content

**Getting Help:**

- Monitor console output for paragraph processing progress
- Check that your Gemini API key is active and has sufficient quota
- Verify the essay content is properly formatted in essay_text.py
- Review agent execution logs for extraction details

## 📄 License

This project is part of an academic assignment demonstrating advanced AI-powered data extraction techniques using LangChain's LCEL framework and intelligent agents.