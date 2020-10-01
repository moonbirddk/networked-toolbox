from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404

from .forms import FeedbackForm
# Create your views here.

@login_required
def send_feedback(request): 
    form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.cleaned_data['sender']=request.user
            instance = form.save(commit=False)
            instance.sender = request.user
            instance.save()
            
        
            messages.success(request, "Thank you for your Feedback!")
            return redirect('homepage')

    context = {'form': form}
    return render(request, 'feedback/add_feedback.html', context)