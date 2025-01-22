from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ImageForm, PasswordChangeForm
from .models import Image, PasswordResetToken, Wishlist
import uuid
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required



@login_required
def home(request):
    # Get the search query from GET request
    search_query = request.GET.get('search', '')
    
    # Filter images by the logged-in user
    img = Image.objects.filter(user=request.user)

    # If there's a search query, filter images based on title
    if search_query:
        img = img.filter(title__icontains=search_query)  # Case-insensitive match

    # Image form handling for image upload
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save image with the current user
            image = form.save(commit=False)
            image.user = request.user  # Assign the logged-in user to the image
            image.save()
            messages.success(request, 'Image uploaded successfully!')
            form = ImageForm()  # Clear the form after saving

    return render(request, 'home.html', {'img': img, 'form': form, 'search_query': search_query})


# Image detail - Show the image only if it belongs to the logged-in user
@login_required
def image_detail(request, id):
    img = get_object_or_404(Image, id=id, user=request.user)  # Ensure the image belongs to the logged-in user
    return render(request, 'image_detail.html', {'img': img})

# Delete image - Only allow the image owner to delete it
@login_required
def delete_image(request, id):
    img = get_object_or_404(Image, id=id, user=request.user)  # Ensure the image belongs to the logged-in user
    if request.method == 'POST':
        img.delete()
        messages.success(request, 'Image deleted successfully!')
        return redirect('home')
    return render(request, 'delete_image.html', {'img': img})

# Update image - Only allow the image owner to update it
@login_required
def update_image(request, id):
    img = get_object_or_404(Image, id=id, user=request.user)  # Ensure the image belongs to the logged-in user
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=img)
        if form.is_valid():
            form.save()
            messages.success(request, 'Image updated successfully!')
            return redirect('image_detail', id=img.id)
    else:
        form = ImageForm(instance=img)
    return render(request, 'update_image.html', {'form': form, 'img': img})

# logout
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# change password
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]

            # Check if the old password is correct
            if not request.user.check_password(old_password):
                form.add_error("old_password", "Old password is incorrect.")
            else:
                # Set the new password
                request.user.set_password(new_password)
                request.user.save()

                # Update the session to prevent user from logging out
                update_session_auth_hash(request, request.user)

                messages.success(request, "Your password has been updated.")
                return redirect("login")  # Redirect to a profile page or wherever you want
    else:
        form = PasswordChangeForm()

    return render(request, "change_password.html", {"form": form})

# signup
def signup_view(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Password match validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('/signup')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/signup')

        # Optionally, you can check if the email is unique as well
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('/signup')

        try:
            # Create the user
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email  # Saving the email as well
            )
            user.set_password(password)  # Make sure password is hashed
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('/login/')
        except IntegrityError as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('/signup/')

    return render(request, 'signup.html')

# login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')


def request_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            token = str(uuid.uuid4())  # Generate unique token
            PasswordResetToken.objects.create(user=user, token=token)

            reset_link = f"http://127.0.0.1:8000/reset-password/{token}/"
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return render(request, "password_reset_sent.html")

    return render(request, "password_reset_form.html")

def reset_password(request, token):
    reset_token = PasswordResetToken.objects.filter(token=token).first()

    if not reset_token:
        return render(request, "invalid_token.html")

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            reset_token.user.password = make_password(new_password)
            reset_token.user.save()
            reset_token.delete()  # Remove used token
            return render(request, "password_reset_success.html")

    return render(request, "password_reset_confirm.html", {"token": token})

@login_required
def add_to_wishlist(request, image_id):
    """User can add an image to their wishlist"""
    image = get_object_or_404(Image, id=image_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, image=image)
    
    if created:
        messages.success(request, "Image added to your wishlist!")
    else:
        messages.info(request, "This image is already in your wishlist.")
    
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, image_id):
    """User can remove an image from their wishlist"""
    image = get_object_or_404(Image, id=image_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, image=image)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, "Image removed from your wishlist.")
    
    return redirect('wishlist')

@login_required
def wishlist_view(request):
    """Display all wishlist images of the logged-in user"""
    wishlist_images = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_images': wishlist_images})