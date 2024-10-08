import os
import tempfile
import imghdr
import markdown
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpRequest
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash-002")

def index(request: HttpRequest):
    cover_letter = None
    if request.method == 'POST':
        resume = request.FILES['resume'].read()
        open_position = request.FILES['open_position'].read()
        try:
            cover_letter = generate_cover_letter(resume, open_position, request.POST.get('language', 'Bahasa Indonesia'))
        except Exception as e:
            cover_letter = f"An error occurred: {e}"

    if cover_letter:
        cover_letter = markdown.markdown(cover_letter)

    return render(request, 'coverletter/index.html', {'cover_letter': cover_letter})

def _upload_resume(resume: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(resume)
        temp_file_path = temp_file.name
    pdf_resume = genai.upload_file(temp_file_path)

    return pdf_resume, temp_file_path

def _upload_open_position(open_position: bytes):
    # 1. Determine image type
    image_type = imghdr.what(None, h=open_position) 
    if not image_type:
        return "Error: Invalid image format. Please provide a valid image file."
    extension = "." + image_type

    # 2. Create temporary file with correct extension
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
        temp_file.write(open_position)
        temp_file_path = temp_file.name

    uploaded_open_position = genai.upload_file(temp_file_path)

    return uploaded_open_position, temp_file_path

def generate_cover_letter(resume: bytes, open_position: bytes, language: str) -> str:
    try:
        pdf_resume, pdf_resume_path = _upload_resume(resume)
        open_position, open_position_path = _upload_open_position(open_position)

        prompt = f'''
Imagine you're scrolling through Instagram and come across an intriguing job posting that aligns perfectly with your career aspirations. Craft a professional email to the HR department expressing your enthusiasm and detailing how your skills, as outlined in your resume, make you an ideal candidate for this role. Consider how you can articulate your unique strengths without referring to details that aren't explicitly provided in the job listing and resume. Also, make sure your language in {language} to mirrors the tone and language of the job listing. How will you ensure that your message stands out among potential applicants? Don't explain your response.
'''

        response = model.generate_content([prompt, pdf_resume, open_position])

        # delete from local storage and cloud
        os.remove(pdf_resume_path)
        os.remove(open_position_path)
        pdf_resume.delete()
        open_position.delete()

        prompt = f'''
Please format this in markdown

{response.text}
'''

        response = model.generate_content([prompt])

        return response.text
    except Exception as e:
        return f"Something error. Please try again. {e}"

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})