# AI-Powered Job Application Agent 🚀

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](https://github.com/Ismail-2001/AI-Job-Application-Agent)

An intelligent, multi-agent system that automatically analyzes job descriptions and generates ATS-optimized, customized CVs and cover letters tailored to each application.

## ✨ Features

- **🔍 Intelligent Job Analysis**: Extracts requirements, skills, and keywords from job descriptions
- **🎨 Smart CV Customization**: Automatically tailors your CV to match job requirements
- **📄 Professional Document Generation**: Creates ATS-friendly DOCX files ready for submission
- **✍️ Cover Letter Generation**: Generates personalized cover letters matching job requirements
- **📊 Match Score Analysis**: Calculates compatibility score between your profile and job requirements
- **🎯 ATS Optimization**: 95%+ compatibility with Applicant Tracking Systems
- **🌐 Web Interface**: Beautiful, responsive web UI for easy access
- **⚡ Production-Ready**: Enterprise-grade code with comprehensive error handling

## 🏗️ Architecture

This project follows a **multi-agent architecture**:

```
Job Description → JobAnalyzer → CVCustomizer → CoverLetterGenerator → DocumentBuilder → Customized CV + Cover Letter
```

### Components

1. **JobAnalyzer** (`agents/job_analyzer.py`)
   - Analyzes job descriptions
   - Extracts requirements, skills, and keywords
   - Identifies ATS keywords with exact capitalization

2. **CVCustomizer** (`agents/cv_customizer.py`)
   - Tailors master profile to job requirements
   - Uses STAR method for achievement quantification
   - Optimizes keyword density for ATS

3. **CoverLetterGenerator** (`agents/cover_letter_generator.py`)
   - Generates personalized cover letters
   - Connects candidate value to job needs
   - Professional yet personable tone

4. **DocumentBuilder** (`utils/document_builder.py`)
   - Generates professional DOCX documents
   - ATS-compatible formatting
   - Clean, standard structure

5. **MatchCalculator** (`utils/match_calculator.py`)
   - Calculates profile-to-job compatibility
   - Provides detailed breakdown
   - Generates actionable recommendations

## 📋 Prerequisites

- Python 3.10 or higher
- DeepSeek API key ([Get one here](https://platform.deepseek.com/))
- All dependencies from `requirements.txt`

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Ismail-2001/AI-Job-Application-Agent.git
cd AI-Job-Application-Agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

**Note**: Never commit your `.env` file to version control!

### 4. Update Your Profile

Edit `data/master_profile.json` with your information:

```json
{
  "personal_info": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "phone": "+1 555-0123",
    "linkedin": "linkedin.com/in/yourprofile",
    "location": "Your City, State"
  },
  "summary": "Your professional summary...",
  "skills": {
    "Languages": ["Python", "JavaScript"],
    "Frameworks": ["Django", "React"],
    "Tools": ["AWS", "Docker"]
  },
  "experience": [
    {
      "company": "Company Name",
      "title": "Your Title",
      "dates": "2020 - Present",
      "location": "City, State",
      "responsibilities": [
        "Achievement 1 with metrics",
        "Achievement 2 with metrics"
      ]
    }
  ],
  "education": [
    {
      "school": "University Name",
      "degree": "Your Degree",
      "dates": "2014 - 2018"
    }
  ]
}
```

### 5. Run the Application

#### Option A: Web Interface (Recommended) 🌐

```bash
python app.py
```

Then open your browser and go to: **http://localhost:5000**

#### Option B: Command Line Interface 💻

```bash
python main.py
```

Follow the prompts to paste your job description.

## 📁 Project Structure

```
AI-Job-Application-Agent/
├── main.py                          # CLI entry point
├── app.py                           # Flask web application
├── requirements.txt                 # Python dependencies
├── .env                             # API keys (create this)
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── agents/
│   ├── __init__.py
│   ├── job_analyzer.py             # Job analysis agent
│   ├── cv_customizer.py            # CV customization agent
│   └── cover_letter_generator.py   # Cover letter generator
├── utils/
│   ├── __init__.py
│   ├── deepseek_client.py          # DeepSeek API wrapper
│   ├── gemini_client.py            # Gemini API wrapper (alternative)
│   ├── document_builder.py         # DOCX generation
│   └── match_calculator.py         # Match score calculator
├── data/
│   └── master_profile.json         # Your professional profile
├── templates/
│   ├── index.html                  # Web interface template
│   └── index_redesigned.html       # Premium redesigned template
└── output/                         # Generated documents
```

## 🎯 Usage Example

### Web Interface

1. Start the server: `python app.py`
2. Open http://localhost:5000
3. Paste a job description
4. Click "Analyze & Generate CV"
5. Wait 20-30 seconds
6. Download your customized CV and cover letter

### Command Line

```bash
$ python main.py

🚀 AI-Powered Job Application Agent Initializing...

📂 Loading master profile...
✅ Loaded profile for Your Name

📋 Paste the Job Description below (Press Ctrl+Z/D then Enter when done):
[Paste job description]
^Z

🔍 Phase 1: Analyzing Job Description...
✅ Job Analyzed: Senior Python Developer at FutureTech AI

📊 Calculating Match Score...
🎯 Overall Match Score: 85/100

🎨 Phase 2: Customizing CV...
✅ CV content customized for ATS optimization.

✍️  Phase 3: Writing Cover Letter...
✅ Cover letter generated.

📄 Phase 4: Generating Documents...
✅ Document saved to: output/CV_FutureTech_AI_Senior_Python_Developer.docx
✅ Cover Letter saved to: output/CL_FutureTech_AI_Senior_Python_Developer.docx

✨ SUCCESS! Your customized CV and cover letter are ready!
```

## 🔧 Configuration

### Using Google Gemini Instead

If you prefer to use Google Gemini API:

1. Update `main.py` or `app.py` to import `GeminiClient` instead of `DeepSeekClient`
2. Set `GOOGLE_API_KEY` in your `.env` file
3. Install `google-generativeai`: `pip install google-generativeai`

### Temperature Settings

The system uses optimized temperature settings:
- **0.1**: Job analysis (structured extraction)
- **0.5**: CV customization (balanced creativity)
- **0.7**: Cover letter generation (creative but professional)

## 🎓 Best Practices

### ATS Optimization Tips

1. **Use Exact Keywords**: The system preserves exact capitalization from job descriptions
2. **Quantify Achievements**: Use the STAR method (Situation, Task, Action, Result)
3. **Standard Headers**: The system uses ATS-friendly section headers
4. **No Graphics**: Documents are text-only for maximum compatibility

### Profile Tips

- **Be Specific**: Include metrics, percentages, and numbers in your achievements
- **Update Regularly**: Keep your `master_profile.json` current
- **Use Keywords**: Include industry-standard terms in your skills

## 🐛 Troubleshooting

### API Key Issues

```
❌ Error: DEEPSEEK_API_KEY not found in environment variables.
```

**Solution**: Create a `.env` file with your API key.

### JSON Parse Errors

```
❌ JSON Decode Error: ...
```

**Solution**: The system includes automatic retry logic. If errors persist, check your API key and internet connection.

### Profile Not Found

```
❌ Error: Profile file not found at data/master_profile.json
```

**Solution**: Ensure `data/master_profile.json` exists and is properly formatted JSON.

## 📚 Documentation

- **`DESIGN_SYSTEM.md`**: Complete design system documentation
- **`DESIGN_IMPLEMENTATION_GUIDE.md`**: Design implementation guide
- **`TECHNICAL_AUDIT_REPORT.md`**: Comprehensive technical audit
- **`IMPLEMENTATION_PLAN.md`**: Development roadmap
- **`SYSTEM_PROMPT_FOR_IDE.md`**: AI assistant system prompts

## 🛠️ Development

### Code Quality Standards

- ✅ Type hints throughout
- ✅ Comprehensive docstrings
- ✅ Error handling with retry logic
- ✅ PEP 8 compliant
- ✅ Production-ready code

### Testing

Run the system verification script:

```bash
python test_system.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [DeepSeek AI](https://platform.deepseek.com/)
- Document generation with [python-docx](https://python-docx.readthedocs.io/)
- Web framework: [Flask](https://flask.palletsprojects.com/)

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the documentation files
3. Open an issue on GitHub

## 🚀 Roadmap

- [ ] User authentication system
- [ ] Database for job history
- [ ] Batch processing for multiple jobs
- [ ] LinkedIn profile optimization
- [ ] Interview preparation questions
- [ ] A/B testing for CV versions

---

**Built with ❤️ for job seekers who want to stand out**

⭐ If you find this project helpful, please give it a star!
