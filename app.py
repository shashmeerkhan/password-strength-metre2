import streamlit as st
import re
import string

def check_password_strength(password):
    """Calculate password strength based on length, complexity, and patterns"""
    score = 0
    feedback = []
    
    # Check length
    if len(password) == 0:
        return 0, ["Please enter a password"]
    elif len(password) < 8:
        feedback.append("Password is too short. Use at least 8 characters.")
    elif len(password) >= 12:
        score += 1
    
    # Check for lowercase
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Include lowercase letters (a-z)")
    
    # Check for uppercase
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Include uppercase letters (A-Z)")
    
    # Check for numbers
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Include numbers (0-9)")
    
    # Check for special characters
    special_chars = set(string.punctuation)
    if any(c in special_chars for c in password):
        score += 1
    else:
        feedback.append("Include special characters (e.g., !@#$%)")
    
    # Check for common patterns
    if re.search(r'12345|qwerty|password|admin', password.lower()):
        score -= 1
        feedback.append("Avoid common patterns and words")
    
    # Check for repeating characters
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        feedback.append("Avoid repeating characters (e.g., 'aaa')")
    
    # Normalize score to 0-4 range
    score = max(0, min(score, 4))
    
    return score, feedback

# Page configuration
st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .password-meter {
        margin: 20px 0;
        height: 10px;
        border-radius: 5px;
        background-color: #ddd;
        position: relative;
    }
    .meter-fill {
        height: 100%;
        border-radius: 5px;
        transition: width 0.5s ease-in-out;
    }
    .very-weak { background-color: #ff4d4d; }
    .weak { background-color: #ffa64d; }
    .moderate { background-color: #ffff4d; }
    .strong { background-color: #4dff4d; }
    .very-strong { background-color: #1a8cff; }
    .feedback-item {
        padding: 5px 10px;
        margin: 5px 0;
        border-radius: 4px;
        background-color: #f0f0f0;
        border-left: 3px solid #ff4d4d;
    }
    .header-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<div class="header-container"><h1>🔒 Password Strength Meter</h1></div>', unsafe_allow_html=True)
st.write("Enter a password to check its security strength")
st.markdown(
    "<div style='color: blue; font-size: 20px;'>Created by Shahmeer Khan</div>",
    unsafe_allow_html=True
)

# Password input
password = st.text_input("Enter password", type="password")

if password:
    # Calculate strength
    score, feedback = check_password_strength(password)
    
    # Determine strength level
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    strength_class = ["very-weak", "weak", "moderate", "strong", "very-strong"]
    
    # Display strength meter
    st.markdown(f"""
    <div class="password-meter">
        <div class="meter-fill {strength_class[score]}" style="width: {(score + 1) * 20}%;"></div>
    </div>
    <h3>{strength_levels[score]}</h3>
    """, unsafe_allow_html=True)
    
    # Display feedback
    if feedback:
        st.subheader("Suggestions to improve:")
        for tip in feedback:
            st.markdown(f'<div class="feedback-item">{tip}</div>', unsafe_allow_html=True)
    
    # Password info
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Password length: {len(password)} characters")
    with col2:
        if score >= 3:
            st.success("This password meets basic security standards.")
        else:
            st.warning("This password doesn't meet recommended security standards.")

# Password tips
with st.expander("Password Security Tips"):
    st.markdown("""
    * Use at least 12 characters
    * Mix uppercase and lowercase letters
    * Include numbers and special characters
    * Avoid common patterns and dictionary words
    * Use a unique password for each account
    * Consider using a password manager
    """)

# Footer
st.markdown("---")
st.markdown("This password strength checker evaluates your password locally and securely.")