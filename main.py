import os
import csv
import json
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from essay_text import essay

# Load API key
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)

# Global storage for extracted companies
extracted_companies = []

@tool
def save_company_info(company_name: str, founding_date: str, founders: List[str]) -> str:
    """
    Tool to save extracted company information.
    
    Args:
        company_name: Name of the company
        founding_date: Founding date in YYYY-MM-DD format
        founders: List of founder names
    
    Returns:
        Confirmation message
    """
    global extracted_companies
    
    # Validate and format the date
    formatted_date = format_date(founding_date)
    
    company_info = {
        "company_name": company_name,
        "founding_date": formatted_date,
        "founders": founders
    }
    
    extracted_companies.append(company_info)
    return f"Successfully saved company: {company_name}"

def format_date(date_str: str) -> str:
    """Format date according to assignment requirements"""
    # Remove any extra spaces and normalize
    date_str = date_str.strip()
    
    # Handle different date formats
    if re.match(r'^\d{4}$', date_str):  # Only year
        return f"{date_str}-01-01"
    elif re.match(r'^\d{4}-\d{2}$', date_str):  # Year and month
        return f"{date_str}-01"
    elif re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):  # Full date
        return date_str
    else:
        # Try to extract year from various formats
        year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if year_match:
            return f"{year_match.group()}-01-01"
        return "1900-01-01"  # Fallback

def split_into_paragraphs(text: str) -> List[str]:
    """Split essay into individual paragraphs"""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

# Create extraction prompt template
extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at extracting company information from text paragraphs.

Analyze the given paragraph and extract ALL company information mentioned. For each company found, use the save_company_info tool.

Rules:
1. Extract company names exactly as mentioned
2. For founding dates:
   - If only year provided: use YYYY-01-01
   - If year and month: use YYYY-MM-01  
   - If full date: use YYYY-MM-DD
3. Extract all founders mentioned as a list
4. Call save_company_info tool for EACH company found
5. If no companies found, respond with "No companies found in this paragraph"
"""),
    ("human", "Paragraph to analyze:\n{paragraph}"),
    ("placeholder", "{agent_scratchpad}")
])

# Create the LCEL chain for paragraph processing
def process_paragraph(paragraph: str) -> str:
    """LCEL Runnable to process a single paragraph"""
    
    # Create agent with tools
    tools = [save_company_info]
    agent = create_tool_calling_agent(llm, tools, extraction_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    
    try:
        result = agent_executor.invoke({"paragraph": paragraph})
        return result.get("output", "Processed paragraph")
    except Exception as e:
        print(f"Error processing paragraph: {e}")
        return "Error processing paragraph"

# Create LCEL Runnable chain
paragraph_processor = RunnableLambda(process_paragraph)

# Batch processing chain using LCEL
def create_batch_processor():
    """Create LCEL chain for batch processing paragraphs"""
    
    def split_and_process(essay_text: str) -> List[str]:
        paragraphs = split_into_paragraphs(essay_text)
        print(f"Processing {len(paragraphs)} paragraphs...")
        
        results = []
        for i, paragraph in enumerate(paragraphs, 1):
            if len(paragraph) > 50:  # Only process substantial paragraphs
                print(f"Processing paragraph {i}/{len(paragraphs)}...")
                result = paragraph_processor.invoke(paragraph)
                results.append(result)
        
        return results
    
    return RunnableLambda(split_and_process)

# Create and run the processing chain
def main():
    global extracted_companies
    extracted_companies = []  # Reset
    
    print("🚀 Starting company extraction using LCEL and Tools...")
    
    # Create the batch processor chain
    batch_processor = create_batch_processor()
    
    # Process the essay
    results = batch_processor.invoke(essay)
    
    print(f"\n✅ Extraction complete! Found {len(extracted_companies)} companies.")
    
    # Remove duplicates based on company name
    unique_companies = []
    seen_names = set()
    
    for company in extracted_companies:
        name_lower = company["company_name"].lower().strip()
        if name_lower not in seen_names:
            seen_names.add(name_lower)
            unique_companies.append(company)
    
    print(f"📊 After deduplication: {len(unique_companies)} unique companies.")
    
    # Generate CSV
    generate_csv(unique_companies)

def generate_csv(companies: List[Dict[str, Any]]):
    """Generate CSV file with extracted company data"""
    
    # Prepare CSV rows
    rows = []
    for i, company in enumerate(companies, start=1):
        # Format founders as string representation of list
        founders_str = str(company["founders"]) if isinstance(company["founders"], list) else f"['{company['founders']}']"
        
        rows.append([
            i,
            company["company_name"],
            company["founding_date"],
            founders_str
        ])
    
    # Sort by founding date for better organization
    rows.sort(key=lambda x: x[2])  # Sort by founding date
    
    # Re-number after sorting
    for i, row in enumerate(rows, start=1):
        row[0] = i
    
    # Save CSV
    filename = "company_info.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["S.N.", "Company Name", "Founded in", "Founded by"])
        writer.writerows(rows)
    
    print(f"📄 {filename} created successfully!")
    print(f"📈 Total companies extracted: {len(rows)}")
    
    # Print first few entries for verification
    print("\n📋 Sample entries:")
    print("S.N. | Company Name | Founded in | Founded by")
    print("-" * 60)
    for row in rows[:5]:  # Show first 5
        founders = row[3][:50] + "..." if len(row[3]) > 50 else row[3]
        print(f"{row[0]:4} | {row[1][:20]:20} | {row[2]:10} | {founders}")
    
    if len(rows) > 5:
        print(f"... and {len(rows) - 5} more companies")

if __name__ == "__main__":
    main()