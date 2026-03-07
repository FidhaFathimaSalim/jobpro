# 🚀 HireHub: Labor Hiring Management System (LHMS)

**HireHub** is a powerful and user-friendly platform designed to streamline labor recruitment, enhance decision-making, and optimize workforce management. Built with **Django**, **Scikit-Learn**, and **Google Gemini**, HireHub provides the tools needed to make informed hiring choices, foster a skilled workforce, and build professional identities.

---

## ✨ Features & Code Architecture

### 🎯 1. Skill Transformer (Job & Course Recommender)
- **Job Matching Algorithm:** Uses **TF-IDF Vectorization** and **Cosine Similarity** (`scikit-learn`) to compare a candidate's skills with required job skills, finding the top fitting roles from a CSV dataset (`job_dataset.csv`).
- **Course Recommendations:** Evaluates required skills taking advantage of **FuzzyWuzzy** string matching to fetch highly relevant online courses and training modules. Evaluates URLs and titles to deliver the most accurate self-improvement paths.
- **Skill Gap Analysis:** Highlights candidate skill mismatches and provides actionable upskilling advice.

### 🤖 2. HireBot
- **Intelligent Chatbot:** An embedded agent bridging dataset-based knowledge and Generative AI.
- **Data-Backed Fallbacks:** Before querying the LLM, the bot parses the custom dataset for course recommendations (`fuzz.partial_ratio`) or exact job openings using string matching.
- **LLM Integration:** Powered by **Google Generative AI (`gemini-1.5-flash`)**, HireBot steps in to fluidly answer general interview, skill-building, and professional growth questions via AJAX interactions.

### 📄 3. CareerForge (Resume Builder)
- **Comprehensive Profile Generation:** Enables users to build detailed ATS-friendly profiles, capturing educational history, technical/non-technical skills, language fluencies, and professional references.
- **CRUD Operations:** Candidates can Create, Read, Update, and Delete their Resumes/CVs seamlessly.
- **PDF Export:** Integrates **pdfkit** to convert user profiles dynamically into beautiful, exportable PDF documents.
- **Secure Authentication:** User accounts, logins, and private resume management handled via Django's secure authentication models.

---

## 🛠️ Tech Stack

- **Backend:** Python, Django 5.1
- **Database:** SQLite (default)
- **Machine Learning & NLP:** `scikit-learn`, `pandas`, `NumPy`, `fuzzywuzzy`, `joblib`
- **AI Integration:** Google Generative AI Python SDK
- **PDF Generation:** `pdfkit`
- **Frontend Utilities:** HTML/CSS Templates, AJAX for chatbot interactions

---

## ⚙️ Installation & Setup

Follow these steps to deploy and run the project locally.

### Prerequisites
- Python 3.8+
- `pip` package manager
- Virtual environment tool (`venv` recommended)
- [wkhtmltopdf](https://wkhtmltopdf.org/) (Required for `pdfkit` CV downloads)

### Step-by-Step Guide

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FidhaFathimaSalim/jobpro.git
   cd jobpro/hirehub
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv djvenv
   
   # Windows:
   djvenv\Scripts\activate
   
   # macOS/Linux:
   source djvenv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables Configuration:**
   Create a `.env` file in the `hirehub` directory (or export directly) to configure your AI credentials.
   *(Note: Set the `GEMINI_API_KEY` for the HireBot to enable its conversational features.)*
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional, for accessing the Admin DB):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application:**
   Open your web browser and navigate to `http://127.0.0.1:8000/`.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License.
