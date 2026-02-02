"""
Flask Web Application for AI-Powered Job Application Agent
Run on localhost for web interface
"""

import os
import sys
import json
import re
from flask import Flask, render_template, request, jsonify, send_file, flash
from dotenv import load_dotenv

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

# Import our modular components
from utils.deepseek_client import DeepSeekClient
from utils.document_builder import DocumentBuilder
from utils.match_calculator import MatchCalculator
from agents.job_analyzer import JobAnalyzer
from agents.cv_customizer import CVCustomizer
from agents.cover_letter_generator import CoverLetterGenerator

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Global variables for initialized components
client = None
builder = None
match_calculator = None
job_analyzer = None
cv_customizer = None
cover_letter_generator = None

def initialize_components():
    """Initialize all AI components."""
    global client, builder, match_calculator, job_analyzer, cv_customizer, cover_letter_generator
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
    
    client = DeepSeekClient(api_key=api_key)
    builder = DocumentBuilder()
    match_calculator = MatchCalculator()
    job_analyzer = JobAnalyzer(client)
    cv_customizer = CVCustomizer(client)
    cover_letter_generator = CoverLetterGenerator(client)

def load_profile(path: str = "data/master_profile.json") -> dict:
    """Load the master profile JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Profile file not found at {path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in {path}")

def sanitize_filename(name: str) -> str:
    """Sanitize filename for Windows."""
    return re.sub(r'[<>:"/\\|?*]', '', name).strip().replace(' ', '_')

@app.route('/')
def index():
    """Main page."""
    try:
        profile = load_profile()
        # Use redesigned template if available, fallback to original
        try:
            return render_template('index_redesigned.html', profile=profile)
        except:
            return render_template('index.html', profile=profile)
    except Exception as e:
        flash(f"Error loading profile: {str(e)}", "error")
        try:
            return render_template('index_redesigned.html', profile=None)
        except:
            return render_template('index.html', profile=None)

@app.route('/api/process', methods=['POST'])
def process_job():
    """Process job description and generate CV/cover letter."""
    try:
        data = request.json
        job_description = data.get('job_description', '').strip()
        
        if not job_description or len(job_description) < 50:
            return jsonify({
                'success': False,
                'error': 'Job description is too short. Please provide at least 50 characters.'
            }), 400
        
        # Initialize components if not already done
        if client is None:
            initialize_components()
        
        # Load profile
        profile = load_profile()
        
        # Analyze job
        analysis = job_analyzer.analyze(job_description)
        role_title = analysis.get('role_info', {}).get('title', 'Unknown Role')
        company = analysis.get('role_info', {}).get('company', 'Unknown Company')
        
        # Calculate match score
        match_data = match_calculator.calculate_match_score(profile, analysis)
        
        # Customize CV
        customized_cv = cv_customizer.customize(profile, analysis)
        
        # Generate cover letter
        cover_letter_text = cover_letter_generator.generate(profile, analysis)
        
        # Generate documents
        os.makedirs("output", exist_ok=True)
        safe_title = sanitize_filename(role_title)
        safe_company = sanitize_filename(company)
        
        cv_filename = f"output/CV_{safe_company}_{safe_title}.docx"
        cl_filename = f"output/CL_{safe_company}_{safe_title}.docx"
        
        # Create documents (reuse builder but create new instances for each)
        cv_builder = DocumentBuilder()
        cv_builder.create_cv(customized_cv, cv_filename)
        
        cl_builder = DocumentBuilder()
        cl_builder.create_cover_letter(cover_letter_text, profile, cl_filename)
        
        return jsonify({
            'success': True,
            'role_title': role_title,
            'company': company,
            'match_score': match_data,
            'cv_file': cv_filename,
            'cover_letter_file': cl_filename,
            'analysis': analysis
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Configuration error: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Processing error: {str(e)}'
        }), 500

@app.route('/api/download/<path:filename>')
def download_file(filename):
    """Download generated files."""
    try:
        # Security: only allow files from output directory
        if not filename.startswith('output/'):
            return jsonify({'error': 'Invalid file path'}), 403
        
        file_path = filename
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile', methods=['GET'])
def get_profile():
    """Get current profile."""
    try:
        profile = load_profile()
        return jsonify({'success': True, 'profile': profile})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize components on startup
    try:
        initialize_components()
        print("✅ All components initialized successfully")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize components: {e}")
        print("💡 Make sure DEEPSEEK_API_KEY is set in .env file")
    
    print("\n🚀 Starting Flask web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
