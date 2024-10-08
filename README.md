## LetterCraft: Resume-to-Cover Letter Generator

**Automatically generate tailored cover letters from your resume and job descriptions.**

LetterCraft simplifies the job application process by automatically generating personalized cover letters. Upload your resume (PDF) and a screenshot of the job description (Image), and LetterCraft will handle the rest.

**Features:**

-   **Resume Parsing:**  Extracts key information from your resume to customize your cover letter.
-   **Job Description Analysis:**  Identifies relevant keywords and phrases from the job posting to highlight your skills and experience.
-   **Tailored Content Generation:**  Creates a unique and compelling cover letter that matches your qualifications with the job requirements.

**How to Use:**

1.  **Clone the repository:**  `git clone https://github.com/hafizhlf/resume-to-coverletter`
    
2.  **Install dependencies:**  `pip install -r requirements.txt`
    
3.  **Set up environment variables:**
    
    Create a  `.env`  file in the root directory and add the following:
    
    ```text
    DJANGO_SECRET_KEY=your_secret_key
    HOST=your_host_address
    GEMINI_API_KEY=your_gemini_api_key 
    ```
    
4.  **Run the application:**  `python manage.py runserver`
    
5.  **Access the web interface:**  Open your browser and navigate to the provided host address.
    
**Technologies Used:**

-   Python
-   Django
-   Google Gemini

**License:**

This project is licensed under the GPL-3.0 License - see the  [LICENSE](LICENSE)  file for details.

**Contribute:**

Contributions are welcome! Please open an issue or submit a pull request.

**Disclaimer:**

This project is under development and may not be perfect. Use at your own discretion.