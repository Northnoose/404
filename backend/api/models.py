# Tabeller av databasen i python objektformat. Må "Migrate" til database serveren for å initialisere databasen med disse tabellene.

from django.db import models
from django.db.models import JSONField  
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class UserPermission(models.Model):                                                 
    """
    Defines a user role and the specific access, edit, and delete permissions 
    the role grants within the system.
    """
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
    """
    Custom user model extending Django's AbstractUser.
    Includes user type (role), email, and tutorial tracking.
    """
    user_type = models.ForeignKey('UserPermission', on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(unique=True) 
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)  
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True) 
    has_seen_tutorial = models.BooleanField(default=False) 

    def __str__(self):
        return self.username

class Task(models.Model):
    """
    Represents a single programming task or challenge.
    Includes task description, difficulty, and optional JSON object.
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Nybegynner'),
        ('intermediate', 'Viderekommen'),
        ('advanced', 'Avansert'),
    ]

    description = models.TextField()
    task_object = JSONField(null=True, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')

    def __str__(self):
        return self.description[:50]
 

class Module(models.Model):
    """
    Represents a learning module containing a single task.
    """
    tasks = models.ForeignKey(Task, on_delete=models.CASCADE) 

class QuizBlokkOppgave(models.Model):
    """
    Represents a quiz block (a type of task) within a module, 
    including quiz-specific JSON data.
    """
    task_id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    description = models.TextField()
    quiz_blokk_data = models.JSONField()

    def __str__(self):
        return str(self.task_id)
    
    
class UserScore(models.Model):
    """
    Tracks user performance on individual quiz block tasks.
    Stores scores, attempts, and completion status.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(QuizBlokkOppgave, on_delete=models.CASCADE)
    oppgave_name = models.CharField(max_length=255) 
    score = models.IntegerField()
    best_score = models.IntegerField()
    finished = models.BooleanField()
    attempts = models.IntegerField()
    last_attempt = models.DateTimeField()

    class Meta:
        unique_together = (('user', 'task'),) 

    def __str__(self):
        return f"{self.user.username} - {self.task.task_id}"


class UserProgression(models.Model):
    """
    Stores the progression score of a user.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    progression_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Progression of {self.user.username}"


class UserQuizScore(models.Model):
    """
    Tracks user's scores on named quizzes (not tied to a specific task).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=100)  
    score = models.IntegerField(default=0)         
    best_score = models.IntegerField(default=0)    
    attempts = models.IntegerField(default=0)      
    last_attempt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz_name}: {self.best_score}"

class Rewards(models.Model):
    """
    Represents a reward that can be earned by users through points.
    """
    reward_id = models.AutoField(primary_key=True)
    description = models.TextField()
    points_required = models.IntegerField()

    def __str__(self):
        return str(self.reward_id)

class UserRewards(models.Model):
    """
    Tracks which users have received which rewards and when.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    reward = models.ForeignKey(Rewards, on_delete=models.CASCADE) 
    date_awarded = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = (('user', 'reward'),) 


    def __str__(self):
        return f"{self.user.username} - {self.reward.description}"


    
class FriendRequest(models.Model):
    """
    Represents a friend request between users.
    Tracks status (pending, accepted, rejected) and timestamp.
    """
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver') 

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username} ({self.status})"

class Friendship(models.Model):
    """
    Represents an established friendship between two users.
    """
    user1 = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2') 

    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username}"
