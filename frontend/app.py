"""
Streamlit UI - Educational Content Generator

A beautiful, theme-aware UI with interactive MCQ quizzes.
"""

import streamlit as st
import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))
from pipeline import EducationalContentPipeline


# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="Educational Content Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# Theme-Aware CSS (Dark/Light Mode)
# ============================================================================

st.markdown("""
<style>
    /* ===== CSS Variables for Theme Support ===== */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-color: #10b981;
        --error-color: #ef4444;
        --warning-color: #f59e0b;
    }
    
    /* ===== Base Styles ===== */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }
    
    /* ===== Header Styles ===== */
    .main-header {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        text-align: center;
        font-size: 1.15rem;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    /* ===== Pipeline Flow ===== */
    .pipeline-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    
    /* Light mode */
    @media (prefers-color-scheme: light) {
        .pipeline-container { background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); }
        .card { background: #ffffff; border: 1px solid #e5e7eb; }
        .mcq-card { background: #f8fafc; border-left: 4px solid #667eea; }
        .mcq-option { background: #f1f5f9; border: 2px solid #e2e8f0; }
        .mcq-option:hover { background: #e2e8f0; border-color: #667eea; }
        .mcq-correct { background: #d1fae5 !important; border-color: #10b981 !important; }
        .mcq-incorrect { background: #fee2e2 !important; border-color: #ef4444 !important; }
        .feedback-card { background: #fffbeb; border-left: 4px solid #f59e0b; }
    }
    
    /* Dark mode */
    @media (prefers-color-scheme: dark) {
        .pipeline-container { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); }
        .card { background: #1e293b; border: 1px solid #334155; }
        .mcq-card { background: #1e293b; border-left: 4px solid #818cf8; }
        .mcq-option { background: #334155; border: 2px solid #475569; color: #f1f5f9; }
        .mcq-option:hover { background: #475569; border-color: #818cf8; }
        .mcq-correct { background: #064e3b !important; border-color: #10b981 !important; }
        .mcq-incorrect { background: #7f1d1d !important; border-color: #ef4444 !important; }
        .feedback-card { background: #451a03; border-left: 4px solid #f59e0b; }
    }
    
    /* Streamlit dark mode override */
    [data-theme="dark"] .pipeline-container,
    .stApp[data-theme="dark"] .pipeline-container { 
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
    }
    
    .pipeline-step {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.25rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: transform 0.2s ease;
    }
    
    .pipeline-step:hover { transform: translateY(-2px); }
    
    .step-generator { background: #dbeafe; color: #1e40af; }
    .step-reviewer { background: #fef3c7; color: #92400e; }
    .step-refine { background: #d1fae5; color: #065f46; }
    .step-arrow { font-size: 1.5rem; opacity: 0.5; }
    
    /* ===== Card Styles ===== */
    .card {
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.2s ease;
    }
    
    .card:hover { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* ===== MCQ Styles ===== */
    .mcq-card {
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .mcq-question {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    
    .mcq-options-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
    }
    
    @media (max-width: 768px) {
        .mcq-options-grid { grid-template-columns: 1fr; }
    }
    
    .mcq-option {
        padding: 0.875rem 1rem;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .mcq-option.selected { border-color: #667eea; background: rgba(102, 126, 234, 0.1); }
    
    /* ===== Status Badges ===== */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .badge-pass { background: #d1fae5; color: #065f46; }
    .badge-fail { background: #fee2e2; color: #991b1b; }
    .badge-refined { 
        background: var(--primary-gradient); 
        color: white; 
        font-size: 0.75rem;
    }
    
    /* ===== Feedback Styles ===== */
    .feedback-card {
        border-radius: 10px;
        padding: 0.875rem 1rem;
        margin: 0.5rem 0;
    }
    
    /* ===== Score Display ===== */
    .score-display {
        text-align: center;
        padding: 1.5rem;
        border-radius: 16px;
        background: var(--primary-gradient);
        color: white;
        margin: 1rem 0;
    }
    
    .score-number {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1;
    }
    
    .score-label {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* ===== Animations ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-in { animation: fadeIn 0.4s ease-out; }
    
    /* ===== Button Overrides ===== */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        transition: transform 0.2s ease !important;
    }
    
    .stButton > button:hover { transform: translateY(-2px); }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# Session State Initialization
# ============================================================================

if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'result' not in st.session_state:
    st.session_state.result = None


# ============================================================================
# Helper Functions
# ============================================================================

def reset_quiz():
    """Reset quiz state for new content."""
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False


def display_interactive_mcq(mcqs: list, prefix: str = ""):
    """Display interactive MCQ quiz with answer selection."""
    
    total = len(mcqs)
    correct_count = 0
    
    for i, mcq in enumerate(mcqs):
        key = f"{prefix}_q{i}"
        
        st.markdown(f"""
        <div class="mcq-card animate-in" style="animation-delay: {i * 0.1}s">
            <div class="mcq-question">Q{i + 1}. {mcq['question']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Extract correct answer letter
        correct_answer = mcq['answer'].strip().upper()
        if len(correct_answer) > 1:
            correct_answer = correct_answer[0]
        
        # Create columns for options
        cols = st.columns(2)
        
        for j, option in enumerate(mcq['options']):
            option_letter = chr(65 + j)  # A, B, C, D
            col = cols[j % 2]
            
            with col:
                # Determine button state
                is_selected = st.session_state.quiz_answers.get(key) == option_letter
                is_correct = option_letter == correct_answer
                
                if st.session_state.quiz_submitted:
                    if is_correct:
                        st.success(f"✓ {option}")
                        if is_selected:
                            correct_count += 1
                    elif is_selected and not is_correct:
                        st.error(f"✗ {option}")
                    else:
                        st.write(f"　{option}")
                else:
                    # Show as selectable buttons
                    btn_type = "primary" if is_selected else "secondary"
                    if st.button(
                        f"{'● ' if is_selected else '○ '}{option}",
                        key=f"{key}_{option_letter}",
                        use_container_width=True,
                        type=btn_type
                    ):
                        st.session_state.quiz_answers[key] = option_letter
                        st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    return correct_count if st.session_state.quiz_submitted else None


def display_content_with_quiz(content: dict, title: str, is_refined: bool = False, key_prefix: str = "main"):
    """Display generated content with interactive quiz."""
    
    badge = '<span class="badge badge-refined">✨ REFINED</span>' if is_refined else ''
    
    st.markdown(f"""
    <div class="card animate-in">
        <div class="card-title">📖 {title} {badge}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Explanation section
    st.markdown("### 📝 Explanation")
    st.info(content["explanation"])
    
    # MCQ section
    st.markdown("### 🎯 Quiz - Test Your Knowledge")
    st.caption("Select your answers for each question, then click 'Check Answers' to see your score!")
    
    # Display interactive MCQs
    score = display_interactive_mcq(content["mcqs"], prefix=key_prefix)
    
    # Submit/Reset buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if not st.session_state.quiz_submitted:
            all_answered = all(
                f"{key_prefix}_q{i}" in st.session_state.quiz_answers 
                for i in range(len(content["mcqs"]))
            )
            
            if st.button(
                "✅ Check Answers", 
                use_container_width=True, 
                type="primary",
                disabled=not all_answered
            ):
                st.session_state.quiz_submitted = True
                st.rerun()
            
            if not all_answered:
                st.caption("Answer all questions to check your score")
        else:
            if st.button("🔄 Try Again", use_container_width=True):
                reset_quiz()
                st.rerun()
    
    # Show score if submitted
    if st.session_state.quiz_submitted and score is not None:
        total = len(content["mcqs"])
        percentage = int((score / total) * 100)
        
        if percentage >= 80:
            emoji = "🎉"
            message = "Excellent!"
        elif percentage >= 60:
            emoji = "👍"
            message = "Good job!"
        else:
            emoji = "📚"
            message = "Keep learning!"
        
        st.markdown(f"""
        <div class="score-display animate-in">
            <div class="score-number">{score}/{total}</div>
            <div class="score-label">{emoji} {message} - {percentage}% correct</div>
        </div>
        """, unsafe_allow_html=True)


def display_review(review: dict):
    """Display reviewer feedback."""
    status = review["status"]
    is_pass = status == "pass"
    
    badge_class = "badge-pass" if is_pass else "badge-fail"
    icon = "✓" if is_pass else "✗"
    
    st.markdown(f"""
    <div class="card animate-in">
        <div class="card-title">
            🔍 Review Result 
            <span class="badge {badge_class}">{icon} {status.upper()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if review["feedback"]:
        st.markdown("**Feedback from AI Reviewer:**")
        for fb in review["feedback"]:
            st.markdown(f"""
            <div class="feedback-card animate-in">⚠️ {fb}</div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Content passed all quality checks!")


# ============================================================================
# Main Application
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 Educational Content Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered content creation with automatic review and interactive quizzes</p>', unsafe_allow_html=True)
    
    # Pipeline visualization
    st.markdown("""
    <div class="pipeline-container">
        <div class="pipeline-step step-generator">📝 Generator</div>
        <span class="step-arrow">→</span>
        <div class="pipeline-step step-reviewer">🔍 Reviewer</div>
        <span class="step-arrow">→</span>
        <div class="pipeline-step step-refine">✨ Refine</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form
    st.markdown("---")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        grade = st.selectbox(
            "📊 Grade Level",
            options=list(range(1, 13)),
            index=3,
            help="Select student grade level (1-12)"
        )
    
    with col2:
        topic = st.text_input(
            "📖 Topic",
            placeholder="Enter a topic... (e.g., Types of angles, Photosynthesis, Fractions)",
            help="Enter the educational topic to generate content for"
        )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button(
            "🚀 Generate Content",
            type="primary",
            use_container_width=True,
            disabled=not topic
        )
    
    # Process and display results
    if generate_btn and topic:
        reset_quiz()
        st.session_state.result = None
        st.markdown("---")
        
        pipeline = EducationalContentPipeline()
        
        with st.status("🔄 Running AI Pipeline...", expanded=True) as status:
            st.write("📝 **Step 1:** Generator Agent creating content...")
            
            try:
                result = pipeline.run(grade=grade, topic=topic)
                st.session_state.result = result
                
                st.write("🔍 **Step 2:** Reviewer Agent evaluating content...")
                
                if result.was_refined:
                    st.write("✨ **Step 3:** Refining content based on feedback...")
                
                status.update(label="✅ Pipeline Complete!", state="complete", expanded=False)
                
            except Exception as e:
                status.update(label="❌ Pipeline Failed", state="error")
                st.error(f"Error: {str(e)}")
                return
    
    # Display results if available
    if st.session_state.result:
        result = st.session_state.result
        
        st.markdown("## 📋 Results")
        
        # Create tabs for different views
        if result.was_refined and result.refined_content:
            tab1, tab2, tab3 = st.tabs(["✨ Final Content", "📝 Initial Draft", "🔍 Review"])
            
            with tab1:
                display_content_with_quiz(
                    result.refined_content, 
                    "Refined Content", 
                    is_refined=True,
                    key_prefix="refined"
                )
            
            with tab2:
                st.markdown("""
                <div class="card">
                    <div class="card-title">📝 Initial Generation</div>
                </div>
                """, unsafe_allow_html=True)
                st.info(result.initial_content["explanation"])
                
                st.markdown("**Original MCQs:**")
                for i, mcq in enumerate(result.initial_content["mcqs"], 1):
                    st.markdown(f"**Q{i}.** {mcq['question']}")
                    for opt in mcq["options"]:
                        st.write(f"  {opt}")
                    st.write(f"  ✓ Answer: {mcq['answer']}")
            
            with tab3:
                display_review(result.review_result)
        else:
            tab1, tab2 = st.tabs(["📖 Content & Quiz", "🔍 Review"])
            
            with tab1:
                display_content_with_quiz(
                    result.initial_content, 
                    "Generated Content",
                    key_prefix="main"
                )
            
            with tab2:
                display_review(result.review_result)
        
        # Summary metrics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Grade", f"Grade {result.grade}")
        with col2:
            st.metric("📚 Topic", result.topic[:20] + "..." if len(result.topic) > 20 else result.topic)
        with col3:
            status_icon = "✅" if result.review_result["status"] == "pass" else "⚠️"
            st.metric("🔍 Review", f"{status_icon} {result.review_result['status'].upper()}")
        with col4:
            st.metric("✨ Refined", "Yes" if result.was_refined else "No")
        
        # Export section
        with st.expander("📥 Export Data"):
            export_data = {
                "grade": result.grade,
                "topic": result.topic,
                "initial_content": result.initial_content,
                "review_result": result.review_result,
                "refined_content": result.refined_content,
                "was_refined": result.was_refined
            }
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.json(export_data)
            with col2:
                st.download_button(
                    "⬇️ Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"edu_content_{topic.replace(' ', '_')}.json",
                    mime="application/json",
                    use_container_width=True
                )


if __name__ == "__main__":
    main()
