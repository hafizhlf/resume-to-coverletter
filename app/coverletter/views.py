import os
import tempfile
import imghdr
import markdown
from django.shortcuts import render
from django.http import HttpRequest
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-002")

def index(request: HttpRequest):
    return render(request, 'coverletter/index.html')

def coverletter(request: HttpRequest):
    cover_letter = None
    if request.method == 'POST':
        resume = request.FILES['resume']
        open_position = request.FILES['open_position']
        try:
            cover_letter = generate_cover_letter(resume, open_position, request.POST.get('language', 'Bahasa Indonesia'))
        except Exception as e:
            cover_letter = f"An error occurred: {e}"

    if cover_letter:
        cover_letter = markdown.markdown(cover_letter)

    return render(request, 'coverletter/coverletter.html', {'cover_letter': cover_letter})

def get_file_extension(file_to_upload):
    # Get the name of the uploaded file
    file_name = file_to_upload.name
    # Split the file name and get the extension
    _, file_extension = os.path.splitext(file_name)
    return file_extension

def _upload_file(file_to_upload):
    suffix = get_file_extension(file_to_upload)
    with tempfile.NamedTemporaryFile(delete=True, suffix=suffix) as temp_file:
        temp_file.write(file_to_upload.read())
        uploaded_file = genai.upload_file(temp_file.name)

    return uploaded_file

def generate_cover_letter(resume: bytes, open_position: bytes, language: str) -> str:
    try:
        pdf_resume = _upload_file(resume)
        open_position = _upload_file(open_position)

        prompt = f'''
Imagine you're scrolling through Instagram and come across an intriguing job posting that aligns perfectly with your career aspirations. Craft a professional email to the HR department expressing your enthusiasm and detailing how your skills, as outlined in your resume, make you an ideal candidate for this role. Consider how you can articulate your unique strengths without referring to details that aren't explicitly provided in the job listing and resume. Also, make sure your language in {language} to mirrors the tone and language of the job listing. How will you ensure that your message stands out among potential applicants? Don't explain your response.
'''

        response = model.generate_content([prompt, pdf_resume, open_position])

        # Delete files from the cloud, as they have already been removed locally after the upload
        pdf_resume.delete()
        open_position.delete()

        prompt = f'''
Format this in Markdown

{response.text}
'''

        response = model.generate_content([prompt])

        return response.text
    except Exception as e:
        return f"Something error. Please try again. {e}"
