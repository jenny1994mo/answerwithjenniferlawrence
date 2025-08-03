from django.contrib import admin
from .models import Profile, Question, QuizResult,FrontCard, BackCard,UserPaymentInfo

# Register your models here.
admin.site.register(Profile)

admin.site.register(Question)

admin.site.register(QuizResult)

admin.site.register(FrontCard)

admin.site.register(BackCard)

admin.site.register(UserPaymentInfo)



