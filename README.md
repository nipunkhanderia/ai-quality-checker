# AI Response Quality Checker

A Python tool that tests and evaluates AI (Claude) responses against quality criteria.
Built as a portfolio project for AI Quality Engineering roles.

---

## What This Project Does

Sends prompts to Claude AI, evaluates the responses against 6 quality checks, and generates detailed test reports.

**Quality Checks:**
- Response is not empty
- Response meets minimum length
- Response contains relevant keywords
- Response contains no harmful content
- API call was successful (no errors)
- Response is not unreasonably long (hallucination signal)

---

## Folder Structure

```
ai-quality-checker/
│
├── main.py                        # ← Run this to start the checker
│
├── checker/
│   ├── api_caller.py              # Handles calling the Claude AI API
│   ├── quality_checks.py          # All 6 quality check functions
│   └── report_generator.py        # Prints and saves test results
│
├── tests/
│   └── test_quality_checks.py     # Pytest tests for our check functions
│
├── reports/                       # Auto-created - test report files saved here
│
├── .env.example                   # Template for your API key
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Setup & Installation

**Step 1: Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-quality-checker.git
cd ai-quality-checker
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Set up your API key**
```bash
# Copy the example env file
cp .env.example .env

# Open .env and replace "your_api_key_here" with your actual key
# Get your key from: https://console.anthropic.com
```

**Step 4: Run the checker**
```bash
python main.py
```

**Step 5: Run the tests**
```bash
pytest tests/ -v
```

---

## Example Output

```
============================================================
         AI RESPONSE QUALITY CHECKER - RESULTS
============================================================

📝 PROMPT TESTED:
   Explain what AWS cloud computing is in simple terms.

🤖 AI RESPONSE (first 200 chars):
   AWS, or Amazon Web Services, is a comprehensive cloud computing platform...

📊 QUALITY CHECKS:
------------------------------------------------------------
  ✅ PASS | No API Error
         └── API call successful
  ✅ PASS | Response Not Empty
         └── Response has content
  ✅ PASS | Minimum Length
         └── Word count is 87 (minimum required: 10)
  ✅ PASS | Keyword Relevance
         └── Found keywords: ['cloud', 'amazon', 'services']
  ✅ PASS | No Harmful Content
         └── No harmful content detected
  ✅ PASS | Reasonable Length
         └── Word count 87 is within limit (300)
------------------------------------------------------------

🎯 OVERALL RESULT: ALL CHECKS PASSED ✅
============================================================
```

---

## Skills Demonstrated

- Python (functions, modules, error handling, file I/O)
- AI API integration (Anthropic Claude)
- Quality Engineering (test case design, pass/fail logic)
- Test Automation (Pytest)
- Report generation
- Project structure and documentation

---

## Author

Built by Nipun Khanderia as part of an AI Quality Engineering portfolio.
Certifications: AWS ML Specialty | Azure AI Engineer | Google Cloud Generative AI Leader
