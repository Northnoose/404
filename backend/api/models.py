# Tabeller av databasen i python objektformat. Må "Migrate" til database serveren for å initialisere databasen med disse tabellene.

from django.db import models
from django.db.models import JSONField  
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model  # Hent brukerens modell fra Django


class UserPermission(models.Model):                                                 # Rettigheter burde kansje endres/formateres på, evt lage liste med rettigheter?
    user_type = models.CharField(max_length=255, unique=True, primary_key=True)
    access_right_Tasks = models.BooleanField(default=False)       
    access_right_Modules = models.BooleanField(default=False)  
    access_right_Self = models.BooleanField(default=False)     
    access_right_other_users = models.BooleanField(default=False)                                
    edit_right_modules = models.BooleanField(default=False)
    edit_right_tasks = models.BooleanField(default=False)
    edit_right_user_premissions = models.BooleanField(default=False)
    edit_right_self = models.BooleanField(default=False)
    edit_right_other_user = models.BooleanField(default=False)
    delete_right_tasks = models.BooleanField(default=False)
    delete_right_modules = models.BooleanField(default=False)
    delete_right_self = models.BooleanField(default=False)
    delete_right_other_user = models.BooleanField(default=False)


    def __str__(self):
        return self.user_type


class User(AbstractUser):
    user_type = models.ForeignKey('UserPermission', on_delete=models.PROTECT)
    email = models.EmailField(unique=True) #Bruker AbstractUser fra Django, som automatisk hånderer passord og hasing. 

    def __str__(self):
        return self.user_name

class Task(models.Model):
    description = models.TextField()
    task_object = JSONField(null=True, blank=True)  

    def __str__(self):
        return self.description[:50] 


class Module(models.Model):
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE) 
    description = models.TextField()


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'task') 

class UserModule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'module') 

class UserProgression(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    progression_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Progression of {self.user.username}"

    
