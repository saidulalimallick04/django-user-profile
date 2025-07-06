from django.shortcuts import render,redirect,resolve_url
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from cloudinary.uploader import destroy

from .models import OtpData
from .utils import *
# Create your views here.

User = get_user_model()

def create_account(request):
    if request.method == 'POST':
        try:
            data = request.POST     # Accept data from Front-End.[JSON]
            
            Username = data.get('nickname')
            First_Name = data.get('first-name')
            Last_Name = data.get('last-name')
            Email = data.get('email-address')
            DoB = data.get('dob')
            
            Password = data.get('password')
            Confirm_Password = data.get('confirm-password')
            
        except:
            messages.error(request,"Unable Fetch data in backend // Give Proper input!!")   # Handle Error if cannot accept data from front-end.
            return redirect(resolve_url('create_account_page'))
        
        if Password !=Confirm_Password:     # Check Password and Conform password.[Will removed in future by Frontend]
            messages.error(request, 'Both Password & Confirm Password should be same!!')
            return redirect(resolve_url('create_account_page'))
        
        if User.objects.filter(email=Email).exists():       # Check if the email is already exist in database.[Will removed in future by Frontend]
            messages.error(request, 'Email address already exixt. Try again with other one.')
            return redirect(resolve_url('create_account_page'))
        try:        # Trying to create a new record in database/new user.
            new_user=User()
            new_user.email = Email
            
            new_user.first_name = First_Name
            new_user.last_name = Last_Name
            
            new_user.date_of_birth = DoB
            new_user.set_password(Password)
            new_user.save()
            
            
            try:
                User.objects.filter(email = Email).update(username = Username)  # Handle if username already exist.[Will removed in future by Frontend]
            except:
                messages.warning(request, message='Username already exist!! Other fields updated except username.')
            
            
            current_user = authenticate(email = Email, password = Password)
            login(request, user=current_user)       # Auto login when account created.
            messages.success(request, message='Login Successfull!!')
            return redirect(resolve_url('landing_page'))
            
        except Exception as e:      # Handle error during creation, possiblely database errors.
            print("Error!!",e)
            messages.error(request, e)
            return redirect(resolve_url('create_account_page'))
        
    else:
        
        return render(request, 'users/create_account_page.html')        # Simply load the account creation page
#----------------------------------------------------------------------------------------------------------

def login_account(request):
    
    next_url = request.GET.get('next','/')  # Store the next path where user wants to go/access or homepage.
    
    if request.method == 'POST':
        data = request.POST     # Accept login inputs from front-end.
        
        email_address = data.get('login-identifier')
        input_password = data.get('login-password')
        
        if User.objects.filter(email = email_address).exists() is None:    # Check if account exist or not.
            messages.error(request, 'No Account Found!!')
            return redirect(resolve_url('login_account_page'))
        
        current_user = authenticate(email = email_address, password = input_password)   # authencate user with email, password.
        
        if current_user is None:        # If Password is wrong!!
            messages.error(request, 'Invalid Credintial!!')
            return redirect(resolve_url('login_account_page'))

        login(request, user=current_user)
        messages.success(request, message='Login Successfull!!')
        
        return redirect(next_url)     # if any next url present other-wise homepage.
    
    else:
        return render(request, 'users/login_account_page.html')     #Load the Login page.
# ----------------------------------------------------------------------------------------------

@login_required(login_url='/login')     # if anyone wants to go profile paage then he  needs to be an authencated user.
def user_profile(request):  
    
    return render(request, 'users/user_profile_page.html')      # User Profile page


#-------------------------------------------------------------------------------------------------
def verify_profile(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        
        input_otp = data.get('OTP')
        real_otp = OtpData.objects.values_list(('otp'),flat=True).get(email = request.user.email)
        if input_otp == real_otp:
            print("verified>>>>>>>>>>>>>>")
            User.objects.filter(uid = request.user.uid).update(is_verified = True)
            messages.success(request, 'Account is now Verified!!')
            return redirect(resolve_url('user_profile_page'))
        else:
            messages.error(request, 'Invalid OTP!! Try Again!!')
            print("Invalid OTP!!")
            context = {
                'user_email_address': request.user.email
            }
            return render(request, 'users/otp_submit_page.html',context=context)
    else:
        
        send_otp_code(request.user.email)
        messages.info(request, "Check Your Mail-Box emails. if can't found check spam emails.")
        context = {
            'user_email_address': request.user.email
        }
        return render(request, 'users/otp_submit_page.html',context=context)
#-----------------------------------------------------------------------------------------------

# Login Required for logout process.
@login_required(login_url='/login')
def logout_account(request):
    logout(request)     # Remove authencation and login
    return redirect(resolve_url('login_account_page'))      #Then return login page.


#-------------------------------------------------------------------------------------------------

@login_required(login_url='/login')
def edit_profile(request):
    if request.method == 'POST':
        try:
            data = request.POST     # accept possible edited data from front end.
            
            Username = data.get('username')
            First_Name = data.get('first-name')
            Last_Name = data.get('last-name')
            DoB = data.get('dob')
            
        except:                     # Handle error 
            messages.error("Something went wrong!! Unable to catch data from front-end.")
            return redirect(resolve_url('edit_profile_page'))

        try:
            current_user = User.objects.get(email = request.user.email)     # Fetch User object to update.
            
            current_user.first_name = First_Name
            current_user.last_name = Last_Name
            current_user.date_of_birth = DoB
            try:
                current_user.username = Username    # handle if username already exist.
            except:
                messages.warning(request, message='Username already exist!! Other fields updated except username.')
            current_user.save()
            
            messages.success(request, message='Profile update Successfull!!')
            return redirect(resolve_url('user_profile_page'))
            

        except Exception as e:
            print("Backend ---X---> Database")
            print("Error!!",e)
            messages.error(request, e)
            return redirect(resolve_url('edit_profile_page'))
        
    else:
        return render(request, 'users/edit_account_page.html')


#-------------------------------------------------------------------------------------------------

@login_required(login_url='/login') 
def upload_profile_image(request):      # Upload user image
    if request.method == 'POST':
        data_file = request.FILES       # Accepts media files.

        try:
            current_user = User.objects.get(uid = request.user.uid)     # Fetch current user.
            if current_user.profile_image:
                old_public_id = current_user.profile_image.public_id    # Fetch old user profile data to destroy/free occupied spaces.
                print(old_public_id)
            
            current_user.profile_image = data_file.get('profile-picture')
            current_user.save(update_fields=["profile_image"])      # Only update profile_image field.
            
            messages.success(request,"Profile Image Updated.")
            try:
                destroy(public_id= old_public_id)       # Delete/destroy/free spaces of previous profile image.
            except Exception as e:
                print(f"Destroy failed!! {e}")
            
            return redirect(resolve_url('user_profile_page'))
        
        except Exception as e:
            messages.error(request, 'Something Went wrong!! Try again!!')
            return redirect(resolve_url('upload_profile_image_page'))
        
    else:
        
        return render(request, 'users/upload_profile_image_page.html')


#-------------------------------------------------------------------------------------------------


@login_required(login_url='/login')
def edit_email(request):
    if request.method == 'POST':    
        data = request.POST
        New_Email = data.get('new-email')
        Varification_Password = data.get('current-password')
        
        if New_Email == request.user.email:
            messages.error(request, 'Email already Exist!!, Try again with other one.')
            return redirect(resolve_url('edit_email_page'))
        
        if authenticate(email = request.user.email, password = Varification_Password):
            try:
                User.objects.filter(email = request.user.email).update(email = New_Email)
                
                messages.success(request, 'Email Update Successful.')
                return redirect(resolve_url('user_profile_page'))
            except:
                messages.error(request, 'Email already Exist!!, Try again with other one.')
                return redirect(resolve_url('edit_email_page'))
        else: 
            messages.error(request, 'In-currenct Password!! Try again!!')
            return redirect(resolve_url('edit_email_page'))

    else:
        return render(request, 'users/edit_email_address.html')


#-------------------------------------------------------------------------------------------------



@login_required(login_url='/login')
def edit_password(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        Varification_Password = data.get('current-password')
        New_Password = data.get('new-password')
        Confirm_Password = data.get('confirm-password')
        
        if authenticate(email = request.user.email, password = Varification_Password ):
            current_user = User.objects.get(email = request.user.email)
            current_user.set_password(New_Password)
            current_user.save()
            return redirect(resolve_url('user_profile_page'))
        else:
            messages.error("Invalid Password!! Try again")
    else:
        
        return render(request, 'users/edit_password_page.html')


#-------------------------------------------------------------------------------------------------

# When user forget password
def forget_password(request):
    if request.method == 'POST':
        if 'email-submit' in request.POST:
            data = request.POST
            input_email = data.get('email-address')
            
            print(data)
            if User.objects.filter(email = input_email).exists():
                # Send Email with otp
                send_otp_code(input_email)
                messages.info(request, 'Check your mail. If uou can\'t find mail see spam mails.')
                context = {
                    "user_email_address": input_email
                }
                return render(request, 'users/otp_submit_page.html', context=context)
            else:
                messages.info(request, 'Email is not found with any account.')
                return redirect(resolve_url('forget_password_page'))
            

        elif 'OTP-submit'and 'OTP' in request.POST:
            data = request.POST
            input_email = data.get('email-address')
            input_otp = data.get('OTP')
            try:
                real_otp = OtpData.objects.values_list(('otp'), flat=True).get(email = input_email)
            except Exception as e:
                messages.error(request, 'internal error!! Try again!!')
                context = {
                    "user_email_address": input_email
                }
                print("Internal Error",e)
                return render(request, 'users/otp_submit_page.html', context=context)
            
            if input_otp == real_otp:
                
                #SEnd mail with temp password
                print("OTP Successful")
                OtpData.objects.get(email = input_email).delete()
                messages.success(request, 'OTP validate Sucessfully. You got a temporary password in registered email.')
                return redirect(resolve_url('login_account_page'))

        else: 
            messages.error(request, "Page data manupulated Possibly!! Try again!!")
            return redirect(resolve_url('forget_password_page'))
    else:
        return render(request, 'users/forget_password_email_page.html')

#-------------------------------------------------------------------------------------------------

def forget_email(request):
    if request.method == 'POST':
        
        data = request.POST
        Username = data.get('nickname')
        Dob = data.get('dob')
        try:
            the_user_email = User.objects.values_list(('email'), flat=True).get(username = Username, date_of_birth = Dob) 
            
            if the_user_email:
                messages.info(request, f"Account Found!! Email: {the_user_email}")
                print(f"Email: {the_user_email}")
                return redirect(resolve_url('login_account_page'))
            else:
                messages.error(request, "No Account Found.")
                return redirect(resolve_url('forget_email_page'))
        except:
            messages.info("Something Went Wrong!! Try again!!")
    else:
        return render(request, 'users/forget_email_page.html')

#-------------------------------------------------------------------------------------------------

@login_required(login_url='/login')

def delete_account(request):
    try:
        requested_user = User.objects.get(email = request.user.email)
        image_public_id = requested_user.profile_image.public_id
        requested_user.delete()
        try:
            destroy(image_public_id)
        except:
            print('Destroy Failed!!')
        
        messages.info(request, 'Account deleted Sucessfully!!')
        return redirect(resolve_url('landing_page'))
    except:
        messages.error('Request Failed!! Try Again Later.')
        return redirect(resolve_url('user_profile_page'))
    

#-------------------------------------------------------------------------------------------------
