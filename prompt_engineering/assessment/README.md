# Assessment: AI Resume Parser

## Objective
Build a resume parsing pipeline that processes candidate resumes (PDF format) and extracts structured information into a local SQLite database using the provided prompt engineering framework.

## Required Extraction Fields

Your pipeline must extract the following fields **exactly** as specified:

- `name`: Candidate's full name.
- `email`: Contact email address.
- `phone_no`: Contact phone number.
- `experience_in_years`: Total professional experience in years (numeric).
- `skills`: A list of strings (e.g., ["Python", "Machine Learning", "Communication"]).
- `companies`: A list of objects with the following map:
    - `company_name`: Name of the organization.
    - `role`: Designation or job title.
    - `job_responsibilities`: Key tasks and achievements in that role.
- `projects`: A list of objects with the following map:
    - `project_name`: Title of the project.
    - `project_description`: Brief overview of what was built and tools used.

---

## Implementation Requirements

1.  **Text Extraction**: Use `pdfplumber` to extract text from the resumes.
2.  **Prompt Engineering**: Use the 7-component prompt framework (Role, Task, Context, Input, Format, Constraints, Examples) to ensure high-quality parsing.
3.  **Local Storage**:
    -   Store the structured data in a local SQLite database (`candidates.db`) with relational tables for companies and projects.
4.  **Batch Processing**: The script should handle multiple PDF files in a single run.

## Evaluation Criteria
-   **Field Accuracy**: Correct extraction of dates and numeric values (years).
-   **Schema Adherence**: Strict matching of the JSON field names provided above.
-   **Consistency**: Performance across different resume formats.
