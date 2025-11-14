import streamlit as st
import os
from pathlib import Path
import PyPDF2
import docx
from io import BytesIO
from typing import List, Dict
import json

# Try to import OpenAI (works with both old and new versions)
try:
    from openai import OpenAI
    OPENAI_NEW = True
except ImportError:
    try:
        import openai
        OPENAI_NEW = False
    except ImportError:
        OPENAI_NEW = None

# Page configuration
st.set_page_config(
    page_title="MCQ Generator",
    page_icon="📝",
    layout="wide"
)

# PWA Support - Inject manifest and service worker
# Note: PWA features work best when deployed as a web app
try:
    import streamlit.components.v1 as components
    # Inject PWA manifest
    st.markdown("""
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#1f77b4">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="MCQ Generator">
    """, unsafe_allow_html=True)
except:
    pass  # PWA files not required for basic functionality

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .question-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .answer-option {
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        background-color: white;
    }
    .explanation {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        font-style: italic;
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_docx(file) -> str:
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def extract_text_from_file(uploaded_file) -> str:
    """Extract text from uploaded file based on file type"""
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension in ['.docx', '.doc']:
        return extract_text_from_docx(uploaded_file)
    elif file_extension == '.txt':
        return str(uploaded_file.read(), "utf-8")
    else:
        st.error(f"Unsupported file type: {file_extension}")
        return ""

def generate_mcq_with_ai(text: str, num_questions: int, api_key: str) -> List[Dict]:
    """Generate MCQ questions using OpenAI API"""
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar")
        return []
    
    if OPENAI_NEW is None:
        st.error("OpenAI library not installed. Please run: pip install openai")
        return []
    
    try:
        # Initialize OpenAI client
        if OPENAI_NEW:
            client = OpenAI(api_key=api_key)
        else:
            openai.api_key = api_key
        
        # Split text into chunks if too long
        max_chunk_length = 3000
        chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
        
        all_questions = []
        
        for chunk in chunks[:3]:  # Limit to first 3 chunks to avoid too many API calls
            prompt = f"""Generate {num_questions} multiple choice questions (MCQ) based on the following text. 
For each question, provide:
1. The question text
2. Four answer options (A, B, C, D)
3. The correct answer (A, B, C, or D)
4. A brief explanation (2-3 sentences) for why the answer is correct

Format the response as JSON with this structure:
{{
    "questions": [
        {{
            "question": "Question text here?",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "A",
            "explanation": "Brief explanation here"
        }}
    ]
}}

Text content:
{chunk}

Generate exactly {num_questions} questions. Return only valid JSON."""

            # Use appropriate API call based on OpenAI version
            if OPENAI_NEW:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert educator who creates high-quality multiple choice questions. Always return valid JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                response_text = response.choices[0].message.content.strip()
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert educator who creates high-quality multiple choice questions. Always return valid JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                response_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                # Remove markdown code blocks if present
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                data = json.loads(response_text)
                if "questions" in data:
                    all_questions.extend(data["questions"])
            except json.JSONDecodeError:
                st.warning("Failed to parse AI response. Using fallback method.")
                # Fallback: create simple questions
                all_questions.extend(generate_simple_questions(chunk, num_questions))
        
        return all_questions[:num_questions]
    
    except Exception as e:
        st.error(f"Error generating questions: {str(e)}")
        # Fallback to simple question generation
        return generate_simple_questions(text, num_questions)

def generate_simple_questions(text: str, num_questions: int) -> List[Dict]:
    """Fallback method to generate simple questions without AI"""
    sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 50]
    
    questions = []
    for i, sentence in enumerate(sentences[:num_questions]):
        if len(sentence) > 100:
            # Create a simple fill-in-the-blank question
            words = sentence.split()
            if len(words) > 10:
                blank_idx = len(words) // 2
                correct_word = words[blank_idx]
                question_text = " ".join(words[:blank_idx]) + " _____ " + " ".join(words[blank_idx+1:])
                
                questions.append({
                    "question": f"Complete the sentence: {question_text}",
                    "options": {
                        "A": correct_word,
                        "B": "different",
                        "C": "another",
                        "D": "similar"
                    },
                    "correct_answer": "A",
                    "explanation": f"This is based on the original text: {sentence[:100]}..."
                })
    
    return questions

def display_question(question: Dict, index: int):
    """Display a single MCQ question with options and explanation"""
    st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
    st.markdown(f"### Question {index + 1}")
    st.markdown(f"**{question['question']}**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display options
    for option, text in question['options'].items():
        is_correct = option == question['correct_answer']
        color = "#28a745" if is_correct else "#6c757d"
        st.markdown(f'<div class="answer-option"><strong style="color: {color};">{option}.</strong> {text}</div>', 
                   unsafe_allow_html=True)
    
    # Display explanation
    st.markdown(f'<div class="explanation"><strong>Explanation:</strong> {question["explanation"]}</div>', 
               unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

def main():
    st.markdown('<h1 class="main-header">📝 MCQ Question Generator</h1>', unsafe_allow_html=True)
    st.markdown("### Upload your study material and generate multiple choice questions with explanations!")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to generate AI-powered questions",
            value=st.session_state.api_key
        )
        st.session_state.api_key = api_key
        
        if not api_key:
            st.info("💡 You can get an API key from https://platform.openai.com/api-keys")
        
        st.markdown("---")
        
        # Number of questions
        num_questions = st.slider(
            "Number of Questions",
            min_value=1,
            max_value=20,
            value=5,
            help="Select how many questions you want to generate"
        )
        
        st.markdown("---")
        
        # File upload
        st.header("📄 Upload File")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt', 'docx', 'doc'],
            help="Upload PDF, TXT, or DOCX file containing your study material"
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            
            # Extract text
            with st.spinner("Reading file content..."):
                text_content = extract_text_from_file(uploaded_file)
            
            if text_content:
                st.info(f"📊 Extracted {len(text_content)} characters from the file")
                
                # Show preview
                with st.expander("📖 Preview Content (first 500 characters)"):
                    st.text(text_content[:500] + "...")
                
                # Generate questions button
                if st.button("🚀 Generate Questions", type="primary", use_container_width=True):
                    if not api_key:
                        st.warning("⚠️ Please enter your OpenAI API key in the sidebar to generate AI-powered questions.")
                        st.info("Using simple question generation method instead...")
                        with st.spinner("Generating questions..."):
                            questions = generate_simple_questions(text_content, num_questions)
                    else:
                        with st.spinner("🤖 Generating questions with AI..."):
                            questions = generate_mcq_with_ai(text_content, num_questions, api_key)
                    
                    if questions:
                        st.session_state.questions = questions
                        st.success(f"✅ Generated {len(questions)} questions!")
                    else:
                        st.error("❌ Failed to generate questions. Please try again.")
        
        else:
            st.info("👆 Please upload a file to get started")
            st.markdown("""
            ### How to use:
            1. **Upload a file** (PDF, TXT, or DOCX) containing your study material
            2. **Enter your OpenAI API key** in the sidebar (optional but recommended)
            3. **Select number of questions** you want to generate
            4. **Click "Generate Questions"** button
            5. Review the questions with explanations below
            """)
    
    # Display questions
    if st.session_state.questions:
        st.markdown("---")
        st.header("📋 Generated Questions")
        
        for idx, question in enumerate(st.session_state.questions):
            display_question(question, idx)
        
        # Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            questions_json = json.dumps(st.session_state.questions, indent=2)
            st.download_button(
                label="📥 Download Questions (JSON)",
                data=questions_json,
                file_name="mcq_questions.json",
                mime="application/json",
                use_container_width=True
            )

if __name__ == "__main__":
    main()

