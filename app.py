import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import google.generativeai as genai
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="WealthWise AI",
    page_icon="💸",
    layout="wide"
)

# --- LOAD CUSTOM CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file '{file_name}' not found. Please create it for custom styling.")

local_css("style.css")

# --- API KEY and MODEL CONFIGURATION ---
api_key = st.secrets["GOOGLE_API_KEY"]

def get_gemini_response(prompt):
    if not api_key:
        st.error("Please enter your API Key to generate insights.")
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# --- SHARED SESSION STATE INITIALIZATION ---
if 'financial_plan' not in st.session_state:
    st.session_state.financial_plan = {}
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help with your plan today?"}]
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Welcome"

# --- HEADER / NAVIGATION MENU ---
st.markdown('<div class="fixed-header">', unsafe_allow_html=True)

options = ["Welcome", "💰 Goal Planner", "🤖 AI Advisor", "👥 Team Details"]
icons = ['house', 'cash-coin', 'robot', 'people-fill']
default_index = options.index(st.session_state.selected_page)

selected = option_menu(
    menu_title=None,
    options=options,
    icons=icons,
    orientation="horizontal",
    default_index=default_index,
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#0d6efd"},
    }
)

st.markdown('</div>', unsafe_allow_html=True)


if st.session_state.selected_page != selected:
    st.session_state.selected_page = selected
    st.rerun()

# --- PAGE DEFINITIONS (Functions) ---

def page_welcome():
    st.title("Welcome to WealthWise AI 💸")
    st.header("Your Personal Financial Goal & Investment Copilot")
    st.write("---")
    st.markdown("""
    **WealthWise AI** is a powerful tool designed to help you plan, track, and achieve your financial dreams.
    Use the header menu above to navigate between the different sections of the application.
    """)

def page_goal_planner():
    st.title("💰 Financial Goal Planner")
    st.write("Define your financial goals and see a projection of your investments.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your Financial Goal")
        goal_name = st.text_input("Goal Name", st.session_state.financial_plan.get('goal_name', "Retirement Fund"))
        target_amount = st.number_input("Target Amount (₹)", min_value=100000, value=st.session_state.financial_plan.get('target_amount', 10000000), step=50000)
        timeline = st.slider("Timeline (Years)", min_value=1, max_value=50, value=st.session_state.financial_plan.get('timeline', 20))
    with col2:
        st.subheader("Your Investment Plan")
        initial_investment = st.number_input("Initial Investment (₹)", min_value=0, value=st.session_state.financial_plan.get('initial_investment', 50000), step=10000)
        monthly_contribution = st.number_input("Monthly Contribution (₹)", min_value=0, value=st.session_state.financial_plan.get('monthly_contribution', 15000), step=1000)
        risk_profile = st.selectbox("Risk Profile", ["Conservative (6%)", "Moderate (9%)", "Aggressive (12%)"])

    if st.button("📈 Project My Wealth"):
        rate_str = risk_profile.split('(')[1].replace('%)', '')
        annual_rate = float(rate_str) / 100
        years = np.arange(0, timeline + 1)
        future_values = []
        for year in years:
            fv_initial = initial_investment * ((1 + annual_rate) ** year)
            fv_monthly = monthly_contribution * 12 * ((((1 + annual_rate) ** year) - 1) / annual_rate) if annual_rate > 0 else monthly_contribution * 12 * year
            future_values.append(fv_initial + fv_monthly)
        
        st.session_state.financial_plan = {
            'goal_name': goal_name, 'target_amount': target_amount, 'timeline': timeline,
            'initial_investment': initial_investment, 'monthly_contribution': monthly_contribution,
            'risk_profile': risk_profile, 'annual_rate': annual_rate, 'years': years.tolist(),
            'future_values': future_values, 'final_value': future_values[-1]
        }
        if 'ai_insights' in st.session_state.financial_plan:
            del st.session_state.financial_plan['ai_insights']
    
    if 'future_values' in st.session_state.financial_plan:
        plan = st.session_state.financial_plan
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=plan['years'], y=plan['future_values'], mode='lines+markers', name='Projected Growth'))
        fig.add_hline(y=plan['target_amount'], line_dash="dash", annotation_text="Target Amount")
        fig.update_layout(title=f"Projection for '{plan['goal_name']}'", xaxis_title="Years", yaxis_title="Value (₹)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🤖 AI-Powered Strategy & Insights")
        if st.button("Generate AI Strategy"):
            final_value, target_amount = plan['final_value'], plan['target_amount']
            shortfall_surplus = final_value - target_amount
            prompt = f"Analyze this financial plan: Goal='{plan['goal_name']}', Target=₹{target_amount:,}, Timeline={plan['timeline']} years. Projected value is ₹{final_value:,.2f}, resulting in a {'shortfall' if shortfall_surplus < 0 else 'surplus'} of ₹{abs(shortfall_surplus):,.2f}. Provide: 1. AI Insights summary. 2. Budgeting Suggestions. 3. Investment Strategy. 4. Risk Analysis."
            with st.spinner("Generating strategy..."):
                ai_insights = get_gemini_response(prompt)
                if ai_insights:
                    st.session_state.financial_plan['ai_insights'] = ai_insights
        
        if 'ai_insights' in st.session_state.financial_plan:
            st.markdown(st.session_state.financial_plan['ai_insights'])

def page_ai_advisor():
    st.title("🤖 AI Financial Advisor")
    st.write("Ask questions about your financial plan or general finance topics.")

    st.sidebar.markdown("---")
    if st.sidebar.button("Clear Entire Chat History", key="clear_chat"):
        st.session_state["messages"] = [{"role": "assistant", "content": "Chat history cleared. How can I help you?"}]
        st.rerun()

    if not st.session_state.get('financial_plan'):
        st.info("Please create a financial plan in the '💰 Goal Planner' page first.")
        st.stop()
    
    with st.expander("Show My Current Financial Plan Summary", expanded=True):
        plan = st.session_state.financial_plan
        st.markdown(f"""
        - **Goal:** {plan.get('goal_name', 'N/A')}
        - **Target:** ₹{plan.get('target_amount', 0):,}
        - **Timeline:** {plan.get('timeline', 0)} years
        - **Monthly Contribution:** ₹{plan.get('monthly_contribution', 0):,}
        - **Projected Final Value:** ₹{plan.get('final_value', 0):,.2f}
        """)

    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            col1, col2 = st.columns([10, 1])
            with col1:
                st.chat_message("user").write(msg["content"])
            with col2:
                if idx + 1 < len(st.session_state.messages) and st.session_state.messages[idx+1]["role"] == "assistant":
                    if st.button("🗑️", key=f"delete_{idx}", help="Delete this question and its answer"):
                        st.session_state.messages.pop(idx + 1)
                        st.session_state.messages.pop(idx)
                        st.rerun()
        else:
            st.chat_message("assistant").write(msg["content"])

    if prompt := st.chat_input():
        if not api_key:
            st.info("Please add your API Key to chat.")
            st.stop()
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        plan = st.session_state.financial_plan
        plan_context = f"Context: User's goal is '{plan.get('goal_name', 'N/A')}' with a target of ₹{plan.get('target_amount', 0):,} over {plan.get('timeline', 0)} years. Their projected final value is ₹{plan.get('final_value', 0):,.2f}."
        full_prompt = f"You are a helpful AI Financial Advisor. {plan_context}. Answer the user's question: '{prompt}'"
        
        with st.spinner("Thinking..."):
            response = get_gemini_response(full_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

def page_team_details():
    st.title("Our Team")
    st.write("---")
    
    team_members = {
        "Aviral Srivastava": "202408001", "Ayush Pal": "202408002", "Sakshi Naresh Joshi": "202403022",
        "Saraiya Meet Hareshbhai": "202403023", "Saumyadip Das": "202403024", "Saurabh Madhukar Shelar": "202403025",
        "Shubham Nirmal Daga": "202403026", "Sudharshana Kumar D": "202403027", "Viraj Dnyaneshwar Takale": "202403029",
        "Vishal Soni": "202403030"
    }

    member_list = list(team_members.items())
    for i in range(0, len(member_list), 2):
        col1, col2 = st.columns(2)
        if i < len(member_list):
            with col1:
                st.info(f"**{member_list[i][0]}**\n\nID: {member_list[i][1]}")
        if i + 1 < len(member_list):
            with col2:
                st.info(f"**{member_list[i+1][0]}**\n\nID: {member_list[i+1][1]}")

# --- ROUTING LOGIC ---
if st.session_state.selected_page == "Welcome":
    page_welcome()
elif st.session_state.selected_page == "💰 Goal Planner":
    page_goal_planner()
elif st.session_state.selected_page == "🤖 AI Advisor":
    page_ai_advisor()
elif st.session_state.selected_page == "👥 Team Details":
    page_team_details()

# --- FOOTER ---
footer_text = "Copyright © 2025 — Group 50, IIM Mumbai. All Rights Reserved."

st.markdown(f'<div class="footer">{footer_text}</div>', unsafe_allow_html=True)




