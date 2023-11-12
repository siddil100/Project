from django.shortcuts import render
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.contrib.auth.models import User

from django.core.mail import send_mail

from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest

from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist



@never_cache
@login_required(login_url='accounts:login')
def myadminview(request):
    # Get the filter criteria
    # Get the filter criteria
    filter_name = request.GET.get('name', 'all')  # Default to 'all'
    filter_status = request.GET.get('status', 'all')  # Default to 'all'
    filter_gender = request.GET.get('gender', 'all')  # Default to 'all'

    # Get all users
    users = User.objects.filter(is_superuser=False)

    # Apply filters based on the criteria
    if filter_name != 'all':
        users = users.filter(username__istartswith=filter_name)  # Filter by name

    if filter_status == 'active':
        users = users.filter(is_active=True)  # Filter by active status
    elif filter_status == 'inactive':
        users = users.filter(is_active=False)  # Filter by inactive status

    if filter_gender == 'male':
        users = users.filter(personaldetails__gender='male')  # Filter by male gender
    elif filter_gender == 'female':
        users = users.filter(personaldetails__gender='female')  # Filter by female gender

    # Define the number of users to display per page
    per_page = 10
    paginator = Paginator(users, per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        suspension_reason = request.POST.get('suspension_reason')  # Get the selected suspension reason

        if user_id:
            try:
                user = User.objects.get(id=user_id)

                if user.is_active:
                    # If the user is active, suspend them and save the suspension reason
                    user.is_active = False
                    user.suspension_reason = suspension_reason
                    user.save()

                    # Send an email with the suspension reason
                    subject = 'Your Account is Suspended'
                    message = f'Hello {user.username}, your account has been suspended by the admin due to the following reason: {suspension_reason}. If you feel there is something wrong, please contact us at dreamwedofficials@gmail.com.'
                    from_email = 'dreamwedofficials@gmail.com'  # Replace with your admin email
                    recipient_list = [user.email]

                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                else:
                    # Handle unsuspension if needed
                    user.is_active = True
                    user.suspension_reason = ""
                    user.save()
            except User.DoesNotExist:
                # Handle the case where the user is not found
                pass
            

    return render(request, 'myadmin/myadmin.html', {'users': page})

from matrimony.models import*
from django.shortcuts import render, get_object_or_404

def aadharsusview(request):
    # Get the filter criteria
    filter_name = request.GET.get('name', 'all')  # Default to 'all'
    filter_gender = request.GET.get('gender', 'all')  # Default to 'all'
    filter_aadhar_valid = request.GET.get('aadhar_valid', 'all')  # Default to 'all'

    # Get all users
    users = User.objects.filter(is_superuser=False)

    # Apply filters based on the criteria
    if filter_name != 'all':
        users = users.filter(username__istartswith=filter_name)  # Filter by name

    if filter_gender == 'male':
        users = users.filter(personaldetails__gender='male')  # Filter by male gender
    elif filter_gender == 'female':
        users = users.filter(personaldetails__gender='female')  # Filter by female gender

    if filter_aadhar_valid == 'valid':
        users = users.filter(personaldetails__aadhar_valid=True)  # Filter by valid Aadhar
    elif filter_aadhar_valid == 'invalid':
        users = users.filter(personaldetails__aadhar_valid=False)  # Filter by invalid Aadhar

    # Define the number of users to display per page
    per_page = 10
    paginator = Paginator(users, per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        suspension_reason = request.POST.get('suspension_reason')  # Get the selected suspension reason

        if user_id:
            user = get_object_or_404(User, id=user_id)

            if user.is_active:
                try:
                    personal_details = PersonalDetails.objects.get(user=user)
                    
                    # Toggle the value of aadhar_valid
                    personal_details.update_aadhar_valid(not personal_details.aadhar_valid)

                    # Save the suspension reason
                    user.suspension_reason = suspension_reason
                    user.save()

                    print(f"Toggling Aadhar Valid for User ID: {user_id}")
                    print(f"Suspension Reason: {suspension_reason}")
                    print(f"User Aadhar Valid: {personal_details.aadhar_valid}")

                except ObjectDoesNotExist:
                    print(f"PersonalDetails not found for User ID: {user_id}")
            else:
                # If the user is not active, clear suspension_reason
                user.suspension_reason = ""
                user.save()

                try:
                    personal_details = PersonalDetails.objects.get(user=user)
                    personal_details.update_aadhar_valid(True)  # Set aadhar_valid to True
                    print(f"Unsuspending User ID: {user_id}")
                    print(f"User Aadhar Valid: {personal_details.aadhar_valid}")
                except ObjectDoesNotExist:
                    print(f"PersonalDetails not found for User ID: {user_id}")
        else:
            return HttpResponseBadRequest("Invalid user_id in the request.")

    return render(request, 'myadmin/aadharsus.html', {'users': page})




from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse
from io import BytesIO
from django.shortcuts import get_object_or_404
from matrimony.models import  PersonalDetails, EducationalDetails, EmploymentDetails, LocationDetails

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse
from io import BytesIO
from django.shortcuts import get_object_or_404
from matrimony.models import PersonalDetails, EducationalDetails, EmploymentDetails, LocationDetails
from datetime import datetime

def generate_pdf(request, user_id):
    user = get_object_or_404(User, id=user_id)
    personal_details = get_object_or_404(PersonalDetails, user=user)
    educational_details = get_object_or_404(EducationalDetails, user=user)
    employment_details = get_object_or_404(EmploymentDetails, user=user)
    location_details = get_object_or_404(LocationDetails, user=user)

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a BytesIO buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object using the BytesIO buffer
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Add content to the PDF
    pdf.setFont("Helvetica-Bold", 20)  # Set font size and style for "DreamWed.com"
    pdf.drawCentredString(300, 750, "DreamWed.com")

    pdf.setFont("Helvetica", 10)  # Set font size for date and time

    # Add profile picture to the PDF (top right corner)
    profile_image_path = personal_details.profile_image.path
    pdf.drawImage(ImageReader(profile_image_path), 450, 680, width=100, height=100)

    # Draw the date and time on the right side, below the image
    pdf.drawString(450, 660, f"Generated on: {current_datetime}")

    pdf.setFont("Helvetica-Bold", 16)  # Set font to bold for heading

    pdf.drawString(100, 730, f"{personal_details.first_name}'s Details")

    
    # Display personal details
    pdf.setFont("Helvetica", 12)  # Reset font to normal for personal details
    pdf.drawString(100, 690, f"First Name: {personal_details.first_name}")
    pdf.drawString(100, 675, f"Middle Name: {personal_details.middle_name}")
    pdf.drawString(100, 660, f"Last Name: {personal_details.last_name}")
    pdf.drawString(100, 645, f"Gender: {personal_details.gender}")
    pdf.drawString(100, 630, f"Birth Place: {personal_details.birth_place}")

    hobbies = ", ".join(hobby.name for hobby in personal_details.hobbies.all())
    pdf.drawString(100, 615, f"Hobbies: {hobbies if hobbies else 'Not available'}")

    # Display educational details (bold)
    pdf.setFont("Helvetica-Bold", 12)  # Set font to bold
    pdf.drawString(100, 580, "Educational Details")
    pdf.setFont("Helvetica", 10)  # Reset font to normal

    pdf.drawString(100, 565, f"Highest Qualification: {educational_details.highest_qualification}")
    pdf.drawString(100, 550, f"UG Degree: {educational_details.ug_degree}")
    pdf.drawString(100, 535, f"PG Degree: {educational_details.pg_degree}")

    # Display employment details (bold)
    pdf.setFont("Helvetica-Bold", 12)  # Set font to bold
    pdf.drawString(100, 505, "Employment Details")
    pdf.setFont("Helvetica", 10)  # Reset font to normal

    pdf.drawString(100, 490, f"Employment Status: {employment_details.employment_status}")
    pdf.drawString(100, 475, f"Occupation: {employment_details.occupation}")
    pdf.drawString(100, 460, f"Employer of: {employment_details.employerof}")

    # Display location details (bold)
    pdf.setFont("Helvetica-Bold", 12)  # Set font to bold
    pdf.drawString(100, 430, "Location Details")
    pdf.setFont("Helvetica", 10)  # Reset font to normal

    pdf.drawString(100, 415, f"Current City: {location_details.current_city}")
    pdf.drawString(100, 400, f"Current State: {location_details.current_state}")
    pdf.drawString(100, 385, f"Current Pin Code: {location_details.current_pin_code}")

    # Save the PDF object cleanly and finish the buffer
    pdf.showPage()
    pdf.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')











