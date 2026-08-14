from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    GENDER_CHOICES=[("M","Male"),("F","Female")]
    ACTIVITY_CHOICES=[
        ("1.2","Sedentary - little or no exercise"),
        ("1.375","Lightly active - 1 to 3 days/week"),
        ("1.55","Moderately active - 3 to 5 days/week"),
        ("1.725","Very active - 6 to 7 days/week"),
        ("1.9","Extra active - very hard exercise/physical job"),
    ]
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    name=models.CharField(max_length=100)
    age=models.PositiveIntegerField()
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES)
    height_cm=models.FloatField()
    weight_kg=models.FloatField()
    activity_level=models.CharField(max_length=10,choices=ACTIVITY_CHOICES,default="1.2")

    def __str__(self):
        return self.name

    def calculate_bmr(self):
        if self.gender=="M":
            return 66.47+(13.75*self.weight_kg)+(5.003*self.height_cm)-(6.755*self.age)
        return 655.1+(9.563*self.weight_kg)+(1.850*self.height_cm)-(4.676*self.age)

    def daily_calories(self):
        return self.calculate_bmr()*float(self.activity_level)

class CalorieEntry(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="calorie_entries")
    item_name=models.CharField(max_length=150)
    calories=models.PositiveIntegerField()
    consumed_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-consumed_at"]

    def __str__(self):
        return f"{self.item_name} - {self.calories} kcal"
