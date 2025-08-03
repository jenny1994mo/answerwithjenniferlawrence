from django.db import models
from django.contrib.auth.models import User 
from django_countries.fields import CountryField

class Profile(models.Model): 
    ROLE_CHOICES = (('client', 'Client'), ('hustler', 'Hustler'),) 
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES) 
    
    def __str__(self): return f"{self.user.username} - {self.role}" 
    
class Question(models.Model): 
    question_number = models.CharField(max_length=255)
    question_text = models.CharField(max_length=255) 
    option_a = models.CharField(max_length=255) 
    option_b = models.CharField(max_length=255) 
    option_c = models.CharField(max_length=255) 
    option_d = models.CharField(max_length=255) 
    correct_option = models.CharField( max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')] ) 
    def __str__(self): 
        return self.question_number 
        
class QuizResult(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    score = models.IntegerField(default=0) 
    total_questions = models.IntegerField(default=0) 
    date_taken = models.DateTimeField(auto_now_add=True) 
    def __str__(self): 
        return f"{self.user.username} - Score: {self.score}/{self.total_questions * 10}" 


class FrontCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')  # stored in MEDIA_ROOT/images/
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
   

class BackCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')  # stored in MEDIA_ROOT/images/
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class UserPaymentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    country = CountryField()
    score = models.IntegerField(default=0) 

