"""
Streamlit UI - Educational Content Generator

A beautiful UI for generating educational content using AI agents.
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
)

# Custom CSS
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; max-width: 1200px; }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        color: #6b7280;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .pipeline-flow {
        background: linear-gradient(to right, #f0f9ff, #e0f2fe);
        border-radius: 12px;
        padding: 1rem 2rem;
        margin: 1.5rem 0;
        text-align: center;
    }
    
    .pipeline-step {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        margin: 0 0.5rem;
    }
    
    .step-generator { background: #dbeafe; color: #1e40af; }
    .step-reviewer { background: #fef3c7; color: #92400e; }
    .step-refine { background: #d1fae5; color: #065f46; }
    .step-arrow { color: #9ca3af; font-size: 1.5rem; }
    
    .mcq-card {
        background: #f9fafb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.75rem 0;
        border-left: 4px solid #667eea;
    }
    
    .feedback-item {
        background: #fef3c7;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #f59e0b;
    }
    
    .refined-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-pass {
        background: #d1fae5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
    }
    
    .status-fail {
        background: #fee2e2;
        color: #991b1b;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# Helper Functions
# ============================================================================

def display_content(content: dict, title: str, is_refined: bool = False):
    """Display generated educational content."""
    badge = '<span class="refined-badge">✨ REFINED</span>' if is_refined else ''
    st.markdown(f"### 📖 {title} {badge}", unsafe_allow_html=True)
    
    st.markdown("**Explanation:**")
    st.info(content["explanation"])
    
    st.markdown("**Multiple Choice Questions:**")
    for i, mcq in enumerate(content["mcqs"], 1):
        st.markdown(f"""
        <div class="mcq-card">
            <strong>Q{i}. {mcq['question']}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        for option in mcq["options"]:
            st.write(f"  {option}")
        
        st.success(f"✓ Correct Answer: {mcq['answer']}")


def display_review(review: dict):
    """Display reviewer feedback."""
    status = review["status"]
    status_class = "status-pass" if status == "pass" else "status-fail"
    status_icon = "✓" if status == "pass" else "✗"
    
    st.markdown(f"""
    ### 🔍 Review Result <span class="{status_class}">{status_icon} {status.upper()}</span>
    """, unsafe_allow_html=True)
    
    if review["feedback"]:
        st.markdown("**Feedback:**")
        for fb in review["feedback"]:
            st.warning(f"⚠️ {fb}")
    else:
        st.success("Content passed all quality checks!")


# ============================================================================
# Main Application
# ============================================================================

def main():
    # Header
    st.markdown('<h1 class="main-header">📚 Educational Content Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered content creation with automatic review and refinement</p>', unsafe_allow_html=True)
    
    # Pipeline visualization
    st.markdown("""
    <div class="pipeline-flow">
        <span class="pipeline-step step-generator">📝 Generator</span>
        <span class="step-arrow">→</span>
        <span class="pipeline-step step-reviewer">🔍 Reviewer</span>
        <span class="step-arrow">→</span>
        <span class="pipeline-step step-refine">✨ Refine (if needed)</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        grade = st.number_input("📊 Grade Level", min_value=1, max_value=12, value=4)
    
    with col2:
        topic = st.text_input("📖 Topic", placeholder="e.g., Types of angles, Photosynthesis...")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("🚀 Generate Content", type="primary", use_container_width=True, disabled=not topic)
    
    # Process and display results
    if generate_btn and topic:
        st.markdown("---")
        
        pipeline = EducationalContentPipeline()
        
        with st.status("🔄 Running AI Pipeline...", expanded=True) as status:
            st.write("📝 **Step 1:** Generator Agent creating content...")
            
            try:
                result = pipeline.run(grade=grade, topic=topic)
                
                st.write("🔍 **Step 2:** Reviewer Agent evaluating content...")
                
                if result.was_refined:
                    st.write("✨ **Step 3:** Refining content based on feedback...")
                
                status.update(label="✅ Pipeline Complete!", state="complete", expanded=False)
                
            except Exception as e:
                status.update(label="❌ Pipeline Failed", state="error")
                st.error(f"Error: {str(e)}")
                return
        
        # Display results
        st.markdown("## 📋 Results")
        
        with st.expander("📝 Initial Generation", expanded=True):
            display_content(result.initial_content, "Generated Content")
        
        with st.expander("🔍 Review Feedback", expanded=True):
            display_review(result.review_result)
        
        if result.was_refined and result.refined_content:
            with st.expander("✨ Refined Content", expanded=True):
                display_content(result.refined_content, "Refined Content", is_refined=True)
        
        # Summary metrics
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Grade Level", f"Grade {result.grade}")
        with col2:
            st.metric("Review Status", result.review_result["status"].upper())
        with col3:
            st.metric("Refinement", "Yes ✨" if result.was_refined else "Not needed ✓")
        
        # JSON export
        with st.expander("📥 Export JSON"):
            export_data = {
                "grade": result.grade,
                "topic": result.topic,
                "initial_content": result.initial_content,
                "review_result": result.review_result,
                "refined_content": result.refined_content,
                "was_refined": result.was_refined
            }
            st.json(export_data)
            st.download_button(
                "⬇️ Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"educational_content_{topic.replace(' ', '_')}.json",
                mime="application/json"
            )


if __name__ == "__main__":
    main()
