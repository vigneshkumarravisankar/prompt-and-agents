# AI Research Paper Parser

## Objective
Build a research paper parsing pipeline that processes academic papers (PDF format) and extracts structured information into a local SQLite database using the provided prompt engineering framework.

---

# Required Extraction Fields

Your pipeline must extract the following fields **exactly** as specified:

- `paper_title`: Title of the research paper.
- `authors`: A list of author names.
- `abstract`: Abstract section of the paper.
- `keywords`: A list of keywords/topics.
- `publication_year`: Year of publication (numeric).
- `research_domain`: Domain/category of the paper (e.g., NLP, Computer Vision, Healthcare AI).
- `methodologies`: A list of techniques, models, or algorithms used.
- `datasets_used`: A list of datasets mentioned in the paper.
- `results_summary`: Summary of the results and findings.
- `references_count`: Total number of references/citations in the paper.
- `sections`: A list of objects with the following map:
    - `section_name`: Name of the section.
    - `section_summary`: Brief summary of the section.
- `authors_affiliations`: A list of objects with the following map:
    - `author_name`: Name of the author.
    - `affiliation`: University/Organization name.

---

# Implementation Requirements

## 1. Text Extraction
Use `pdfplumber` to extract text from the research papers.

## 2. Prompt Engineering
Use the 7-component prompt framework:

1. Role  
2. Task  
3. Context  
4. Input  
5. Format  
6. Constraints  
7. Examples  

The framework should ensure high-quality and consistent parsing.

## 3. Local Storage
Store the structured data in a local SQLite database named:

```bash
research_papers.db