# WealthWise AI: A Personal Financial Goal & Investment Copilot 💸

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([https://wealthwise-ai.streamlit.app/(https://wealthwise-ai.streamlit.app/))

**WealthWise AI** is a powerful, multi-page dashboard built with Streamlit and powered by Google's Gemini AI. It helps users plan, track, and achieve their financial goals by combining traditional financial forecasting with personalized, AI-generated strategies.

This project was developed for the "Gen AI for Business" course at IIM Mumbai.

## ✨ Key Features

* **Interactive Goal Planner:** Set long-term financial goals (like retirement or a down payment), input your investment plan, and visualize your projected wealth growth with an interactive Plotly chart.
* **AI-Powered Strategy:** Receive personalized insights and actionable advice on your financial plan. The AI analyzes your trajectory and suggests improvements to your budgeting, investment strategy, and risk management.
* **Context-Aware AI Advisor:** Chat with an AI that understands your financial plan. Ask specific questions about your goals or general finance topics and get tailored answers.
* **Professional UI:** Features a clean, multi-page interface with a fixed header and footer, custom styling, and full chat management features (clear history, delete individual turns).

## 🚀 Live Demo

You can access the live, deployed version of the application here:

**[https://wealthwise-ai.streamlit.app/](https://wealthwise-ai.streamlit.app/)**

*(Note: Replace the URL above with your actual Streamlit Community Cloud app URL after deployment.)*

## 📸 Screenshot

Here's a look at the Financial Goal Planner in action:

![WealthWise AI Screenshot]<img width="1893" height="949" alt="Image" src="https://github.com/user-attachments/assets/fbd60257-7428-4690-a80f-c8801298d51e" />

*(Note: You should upload your own screenshot, for example to a site like [Imgur](https://imgur.com/upload), and replace the URL above.)*

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Streamlit Option Menu
* **Backend & Logic:** Python
* **Data Visualization:** Plotly
* **AI & NLP:** Google Generative AI (Gemini 1.5 Flash)

## ⚙️ Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    * Create a folder named `.streamlit` in your project's root directory.
    * Inside the `.streamlit` folder, create a file named `secrets.toml`.
    * Add your Google AI API key to the `secrets.toml` file in the following format:
        ```toml
        # .streamlit/secrets.toml
        GOOGLE_API_KEY = "YOUR_SECRET_GOOGLE_AI_API_KEY"
        ```

5.  **Run the application:**
    ```sh
    streamlit run app.py
    ```
    The application should now be running in your web browser.
