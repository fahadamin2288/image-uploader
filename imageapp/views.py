from django.shortcuts import render, get_object_or_404, redirect
from .forms import ImageForm
from .models import Image

def home(request):
    form = ImageForm()
    img = Image.objects.all()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ImageForm()

    return render(request, 'home.html', {'img': img, 'form': form})


def image_detail(request, id):
    img = get_object_or_404(Image, id=id)
    return render(request, 'image_detail.html', {'img': img})

def delete_image(request, id):
    img = get_object_or_404(Image, id=id)
    if request.method == 'POST':
        img.delete()
        return redirect('home')
    return render(request, 'delete_image.html', {'img': img})

def update_image(request, id):
    img = get_object_or_404(Image, id=id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=img)
        if form.is_valid():
            form.save()
            return redirect('image_detail', id=img.id)
    else:
        form = ImageForm(instance=img)
    return render(request, 'update_image.html', {'form': form, 'img': img})
