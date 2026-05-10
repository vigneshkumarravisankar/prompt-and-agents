# Prompt Engineering Guide: Invoice Parsing

This guide compares a "Bad" vs. "Good" prompt for extracting data from invoices using LLMs like Gemini.

---

## ❌ The Bad Prompt
A bad prompt is often too brief, lacks structure, and doesn't define the output format strictly.

**Example:**
> "Extract the data from this invoice text: [text]"

### Why it's bad:
1.  **No Role**: The AI doesn't know its specialized context.
2.  **Vague Output**: It might return a bulleted list, a long paragraph, or a different JSON structure every time.
3.  **Missing Constraints**: It might include conversational filler like "Sure, here is the data..." which breaks automated pipelines.
4.  **No Examples**: The model might misinterpret currency symbols or date formats without guidance.

---

## ✅ The Good Prompt (Current Implementation)
A good prompt uses the **formal framework** (Persona, Task, Context, etc.) to ensure reliability.

**Components:**
1.  **Role/Persona**: *Senior Financial Data Analyst.* (Tells the AI to be precise).
2.  **Task**: *Extract data into a clean JSON format.* (Defines the 1 objective).
3.  **Context**: *Automated accounts payable pipeline.* (Explains WHY accuracy matters).
4.  **Input Data**: *Clearly delimited OCR text.* (Prevents the model from getting confused by noise).
5.  **Output Format**: *Strict JSON Schema.* (Ensures code can read the output).
6.  **Constraints**: *No preamble, numeric totals.* (Prevents common formatting errors).
7.  **Examples**: *Few-shot logic.* (Demonstrates the expected behavior).

---

## Conclusion
By using a structured prompt with comments (as seen in `invoice_parser.py`), we achieve:
- **Consistency**: The same invoice produces the same JSON structure every time.
- **Reliability**: Fewer "hallucinations" of data in missing fields.
- **Automation-Ready**: The output can be piped directly into a database without manual cleaning.
