# 🏥 AutoFiller: LLM-Based Medical Record Redaction Validation

🤖 AutoFiller is a tool that uses Large Language Models (LLMs) to fill in redacted medical records, specifically designed to work with datasets like MIMIC-IV-note. The primary purpose is to acquire validation and testing data for LLM redaction systems by generating realistic mock Personal Identifiable Information (PII) for redacted fields.

## 🔧 How It Works

The project leverages the Groq API with the Llama model to intelligently fill in redacted portions of medical records (marked with "___") with plausible synthetic PII. This creates realistic test data that can be used to validate and improve medical record redaction systems without compromising actual patient privacy. 🔒

The system maintains the original document format while replacing redacted fields with contextually appropriate mock data, making it ideal for:
- 🧪 Testing redaction algorithms
- 📊 Training redaction models
- ✅ Validating anonymization processes
- 📋 Creating synthetic datasets for research

## ⚙️ Setup

### Prerequisites
- 🐍 Python 3.7+
- 🔑 Groq API key

### Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🚀 Usage Modes

### 1. Manual Mode

For processing individual redacted records manually:

1. **Create input file**: Create a file named `redact.txt` in the project root directory
2. **Add redacted content**: Input your redacted medical records into `redact.txt` (with redacted fields marked as "___")
3. **Run the script**:
   ```bash
   python manual.py
   ```
4. **Output**: All filled results will be saved in `manual_output.json` in the `outputs/` directory

**Example `redact.txt` content:**
```
Patient Name: ___ ___
Date of Birth: ___
Medical Record Number: ___
```

### 2. Automatic Mode

For batch processing of CSV datasets:

1. **Open the Jupyter notebook**: `main.ipynb`
2. **Review and adjust**: Examine the notebook code and make necessary adjustments for your specific CSV structure
3. **Configure data source**: Update the notebook to point to your CSV file containing redacted medical records
4. **Run the notebook**: Execute the cells to automatically process each row's redacted fields

**Important**: Please carefully review the notebook code and make appropriate modifications based on your specific dataset structure before running.

## File Structure

- `filler.py`: Core LLM filling functionality using Groq API
- `manual.py`: Manual mode script for single document processing
- `main.ipynb`: Jupyter notebook for automatic batch processing
- `requirements.txt`: Python dependencies
- `redact.txt`: Input file for manual mode (user-created)
- `outputs/`: Directory containing processed results

## Output Format

The system returns results in JSON format containing both the filled and original redacted text:

```json
{
  "filled": "Patient Name: John-Smith",
  "redacted": "Patient Name: ___ ___"
}
```

## Notes

- The LLM is configured to maintain original document formatting
- Filled information uses single words or hyphen-connected phrases
- All outputs preserve the original redacted text for comparison
- The system is designed specifically for medical record contexts

## Security & Privacy

This tool is intended for research and validation purposes only. It generates synthetic data and should not be used with actual patient information without proper ethical approval and data protection measures. 