
# AutoGen Web Scraper Builder (AWS Bedrock + Playwright)

This project automates the creation of Playwright-based web-scraping scripts using **AutoGen**, **AWS Bedrock (Anthropic Claude)**, and **Autogen Agents** such as WebSurfer, CoderAgent, and Executor.
The system generates a scraping script entirely through LLM-driven interactions, saves it to disk, and prepares it for execution.

---

## ✅ Features

* **Automatic Playwright Script Generation** via Claude 3 Sonnet (AWS Bedrock)
* **Interactive Multi-Agent Workflow**:

  * **WebSurfer** → Navigates real websites
  * **CoderAgent** → Writes final Playwright scripts
  * **Executor** → Saves generated code
* **Local Command Execution** via `LocalCommandLineCodeExecutor`
* **Configurable AWS Bedrock Authentication**
* **Proxy Support** for Playwright browser automation
* **Customizable Search Query**
* **Graceful Error Handling** with fallback simulated data
* Output script is stored in `scraping_output/`

---

## 📁 Project Structure

```
project/
│
├── scraping_output/          # Auto-generated scripts saved here
├── autogen_scraper.py        # The AutoGen orchestration script (your provided script)
└── README.md                 # Documentation
```

---

## 🚀 How It Works

The script orchestrates a coordinated multi-agent conversation:

### **1. CoderAgent**

* Writes a standalone Playwright script named `ky_scraper.py`
* Ensures:

  * Correct filename in first line (`# filename: ky_scraper.py`)
  * Proxy setup
  * Custom User-Agent
  * Website navigation and scraping logic
  * Error-handling fallback

### **2. WebSurfer**

* Opens real web pages
* Inspects DOM, clicks buttons, extracts selectors

### **3. Executor**

* Writes the generated script to `scraping_output/`
* Returns `"TERMINATE"` when done

---

## 📦 Requirements

Install dependencies:

```bash
pip install autogen-agentchat autogen-core autogen-ext playwright
```

Install Playwright browsers:

```bash
playwright install
```

---

## 🔧 Configuration

Update these values in the script:

```python
aws_access_key = "aws-access-key-here"
aws_secret_key = "aws-access-secret-here"
aws_region = "aws-region-here"
model_id = "model-id-here"
aws_session_token = "aws-session-token-here"
```

Update business search string:

```python
BUSINESS_TO_SEARCH = "KENTUCKY FRIED CHICKEN"
```

---

## ▶️ How to Run

Run the main orchestration script:

```bash
python3 autogen_scraper.py
```

The system will:

1. Start Autogen GroupChat
2. Generate the Playwright scraper
3. Save it as:

```
scraping_output/ky_scraper.py
```

---

## 🧩 Output: What the Generated Script Does

The resulting Playwright script:

✅ Opens browser with proxy
✅ Sets a realistic User-Agent
✅ Navigates to Kentucky business search portal
✅ Searches for `"KENTUCKY FRIED CHICKEN"`
✅ Clicks the correct business link
✅ Extracts the details table
✅ Prints all extracted data
✅ Falls back to simulated output on error

---

## ✅ Example Output Location

```
scraping_output/
└── ky_scraper.py
```

---

## ⚠️ Notes

* This project requires valid AWS Bedrock credentials.
* The WebSurfer agent may open browser windows unless `headless=True` is set.
* Running AutoGen agents consumes API credits on AWS.

---

