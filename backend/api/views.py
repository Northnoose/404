from datetime import timedelta
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from .models import UserProgression
from .models import Module
from .models import UserQuizScore
from .models import UserPermission, User, QuizBlokkOppgave, UserScore, Rewards, UserRewards, UserProgression, Module, UserQuizScore, FriendRequest, Friendship
from django.utils import timezone
import re
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.db import models
from django.contrib.auth import get_user_model
from .models import Friendship
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages



User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """A custom user creation form that extends Django's UserCreationForm with additional email validation and password requirements."""
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    email = forms.EmailField(required=True, help_text="En gyldig e-postadresse er påkrevd.")

    def clean_email(self):
        """Clean and validate the email field."""
        email = self.cleaned_data.get('email')
        return email
    
    
    def clean_password2(self):
        """Validate that the password meets complexity requirements."""
        password = self.cleaned_data.get("password2")
        
        if len(password) < 8:
            forms.ValidationError("Passordet må være minst 8 tegn langt.")
        
        if not re.search(r'[A-Z]', password):
            forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn.")
        
        if not re.search(r'\d', password):
            forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn")
        
        if not re.search(r'[@$!%*?&]', password):
            forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn")
        
        return password


def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

def login_view(request):
    """Handle user login authentication."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not user.has_seen_tutorial:
                request.session['show_tutorial'] = True
            return redirect('profile')
        else:
            messages.error(request, 'Ugyldig brukernavn eller passord.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    """Handle new user registration."""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Brukernavnet finnes allerede.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Bruker opprettet! Logg inn.')
            return redirect('login')
    return render(request, 'register.html')



@login_required
def profile(request):
    """Display user profile with progression, rewards, and friend information."""
    show_tutorial = request.session.pop('show_tutorial', False)
    if 'user_id' in request.GET and request.GET['user_id'] != str(request.user.id):
        viewed_user = get_object_or_404(User, id=request.GET['user_id'])
    else:
        viewed_user = request.user

    try:
        progression = UserProgression.objects.get(user=viewed_user)
    except UserProgression.DoesNotExist:
        progression = None

    def get_user_skill_level(score):
        if score <= 10:
            return 'beginner'
        elif score <= 25:
            return 'intermediate'
        else:
            return 'advanced'

    user_level = None
    if progression:
        user_level = get_user_skill_level(progression.progression_score)

    user_rewards = UserRewards.objects.filter(user=viewed_user)

    friends = User.objects.filter(
        id__in=Friendship.objects.filter(user1=request.user).values('user2')
    )

    pending_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status='pending'
    )

    already_friends = Friendship.objects.filter(
        Q(user1=request.user, user2=viewed_user) |
        Q(user1=viewed_user, user2=request.user)
    ).exists()

    request_sent = FriendRequest.objects.filter(
        sender=request.user,
        receiver=viewed_user,
        status='pending'
    ).exists()

    context = {
        'user': viewed_user,
        'progression': progression,
        'user_level': user_level,
        'user_rewards': user_rewards,
        'friends': friends,
        'pending_requests_count': pending_requests.count(),
        'already_friends': already_friends,
        'request_sent': request_sent,
        'show_tutorial': show_tutorial
    }
    return render(request, 'profile.html', context)





class EditProfileForm(forms.ModelForm):
    """Form for editing user profile information."""
    class Meta:
        model = User
        fields = ['username', 'email']

@login_required
def edit_profile(request):
    """Handle profile editing form submission."""
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profilen din ble oppdatert.")
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'editprofile.html', {'form': form})



@login_required
def module_overview(request):
    """Display overview of available learning modules based on user skill level."""
    user_progress, _ = UserProgression.objects.get_or_create(user=request.user)

    def get_user_skill_level(score):
        if score <= 8:
            return 'beginner'
        elif score <= 16:
            return 'intermediate'
        else:
            return 'advanced'

    skill_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
    user_level = get_user_skill_level(user_progress.progression_score)

    modules_info = [
    {
        "title": "Grunnleggende Quiz",
        "description": "Lær det helt grunnleggende om koding og test deg selv med en enkel quiz med flervalgsspørsmål.",
        "url_name": "python_lesson",
        "difficulty": "beginner"
    },
    {
        "title": "Drag and Drop-oppgaver",
        "description": "Utforsk koding på en interaktiv måte ved å dra og slippe kodeblokker på riktig plass.",
        "url_name": "drag_and_drop_lesson",
        "difficulty": "intermediate"
    },
    {
        "title": "Blokkbasert Koding",
        "description": "Sett sammen kodeblokker som representerer handlinger, løkker og betingelser for å lage små programmer.",
        "url_name": "blokkbasert_instruksjoner",
        "difficulty": "advanced"
    },
    {
        "title": "OOP Quiz",
        "description": "Test dine kunnskaper i objektorientert programmering. Passer for viderekomne brukere.",
        "url_name": "oop_quiz",
        "difficulty": "advanced"
    },
]


    for module in modules_info:
        module["is_above_user_level"] = skill_order[module["difficulty"]] > skill_order[user_level]

    return render(request, 'modules_overview.html', {
        'modules_info': modules_info,
        'user_level': user_level
    })


def python_lesson_view(request):
    return render (request, 'lesson_python.html')

QUIZ_QUESTIONS = [
    {
        "question": "Hva er riktig måte å skrive en print-setning i Python?",
        "choices": [
            "echo('Hello')",
            "System.out.println('Hello')",
            "print('Hello')",
            "console.log('Hello')"
        ],
        "correct": 2,  # Index 2: "print('Hello')"
        "explanation": "I Python bruker du print('Hello') for å skrive ut tekst."
    },
    {
        "question": "Hvilket nøkkelord definerer en funksjon i Python?",
        "choices": [
            "function",
            "func",
            "def",
            "lambda"
        ],
        "correct": 2,  # Index 2: "def"
        "explanation": "Funksjoner defineres med 'def' i Python."
    },
    
]

@login_required
def python_quiz_view(request):
    """Handle Python quiz submission and display results."""
    if request.method == "POST":
        correct_count = 0
        feedback = []

        
        QUIZ_QUESTIONS = [
            {
                "question": "Hva er riktig måte å skrive en print-setning i Python?",
                "choices": ["echo('Hello')", "System.out.println('Hello')", "print('Hello')", "console.log('Hello')"],
                "correct": 2,
                "explanation": "I Python bruker du print('Hello') for å skrive ut tekst."
            },
            {
                "question": "Hvilket nøkkelord definerer en funksjon i Python?",
                "choices": ["function", "func", "def", "lambda"],
                "correct": 2,
                "explanation": "Funksjoner defineres med 'def' i Python."
            },
            {
                "question": "Hvilken setning skriver 'Hello World' til konsollen?",
                "choices": ["echo \"Hello World\"", "printf(\"Hello World\")", "console.log(\"Hello World\")", "print(\"Hello World!\")"],
                "correct": 3,
                "explanation": "I Python er print(\"Hello World!\") riktig."
            }
        ]

       
        for i, question in enumerate(QUIZ_QUESTIONS):
            chosen_str = request.POST.get(f'answer_{i}', None)
            chosen = int(chosen_str) if chosen_str is not None else -1
            is_correct = (chosen == question["correct"])

            if is_correct:
                correct_count += 1

            feedback.append({
                "question": question["question"],
                "chosen_answer": question["choices"][chosen] if 0 <= chosen < len(question["choices"]) else "Ingen svar",
                "correct_answer": question["choices"][question["correct"]],
                "is_correct": is_correct,
                "explanation": question["explanation"] if not is_correct else ""
            })

        
        context = {
            "feedback": feedback,
            "correct_count": correct_count,
            "total": len(QUIZ_QUESTIONS),
        }
        return render(request, 'quiz_python_result.html', context)

    
    return render(request, 'quiz_python.html')

def python_quiz_result_view(request):
    """Display Python quiz results and update user progression."""
    QUIZ_QUESTIONS = [
        {
            "question": "Hva er riktig måte å skrive en print-setning i Python?",
            "choices": ["echo('Hello')", "System.out.println('Hello')", "print('Hello')", "console.log('Hello')"],
            "correct": 2,
            "explanation": "I Python bruker du print('Hello') for å skrive ut tekst."
        },
        {
            "question": "Hvilket nøkkelord definerer en funksjon i Python?",
            "choices": ["function", "func", "def", "lambda"],
            "correct": 2,
            "explanation": "Funksjoner defineres med 'def' i Python."
        },
        {
            "question": "Hvilken setning skriver 'Hello World' til konsollen?",
            "choices": ["echo \"Hello World\"", "printf(\"Hello World\")", "console.log(\"Hello World\")", "print(\"Hello World!\")"],
            "correct": 3,
            "explanation": "I Python er print(\"Hello World!\") riktig."
        }
    ]

    answers = []
    feedback = []
    correct_count = 0

    for i, question in enumerate(QUIZ_QUESTIONS):
        chosen_str = request.GET.get(f'answer_{i}', "")
        try:
            chosen = int(chosen_str)
        except ValueError:
            chosen = -1

        is_correct = (chosen == question["correct"])
        if is_correct:
            correct_count += 1

        feedback.append({
            "question": question["question"],
            "chosen_answer": question["choices"][chosen] if 0 <= chosen < len(question["choices"]) else "Ingen svar",
            "correct_answer": question["choices"][question["correct"]],
            "is_correct": is_correct,
            "explanation": question["explanation"] if not is_correct else ""
        })

    if request.user.is_authenticated:
        user_progression, created = UserProgression.objects.get_or_create(user=request.user)
        user_progression.progression_score += correct_count
        user_progression.save()

    context = {
        "feedback": feedback,
        "correct_count": correct_count,
        "total": len(QUIZ_QUESTIONS),
    }
    
    messages.success(request, f"Du fikk {correct_count} av {len(QUIZ_QUESTIONS)} riktige!")
    
    return render(request, "quiz_python_result.html", context)

def drag_and_drop_lesson_view(request):
    return render(request, 'drag_and_drop_lesson.html')

def drag_and_drop_exercise_view(request):
    return render(request,'drag_and_drop_exercise.html')

def blokkbasert_instruksjoner(request):
    return render(request, 'blokkbasert_instruksjoner.html')

@login_required
def blokkbasert_koding(request):
    return render(request, 'block_coding.html')

def lesson_oop_view(request):
    return render(request, 'lesson_oop.html')


@login_required
def drag_and_drop_result_view(request):
    """
    Evaluates the results of a drag-and-drop exercise, compares the user's answers to the correct answers,
    provides feedback, and updates the user's progression score and quiz performance.
    """

    dropzone_data = [
        {
            "question": "Setning 1 – if-setning",
            "correct_answer": "if x > 10:",
            "explanation": "Du må starte med en if-setning for å sjekke om x er større enn 10."
        },
        {
            "question": "Setning 1 – else",
            "correct_answer": "else:",
            "explanation": "Else brukes til å definere hva som skal skje dersom betingelsen i if-setningen ikke er oppfylt."
        },
        {
            "question": "Setning 2 – x = 7",
            "correct_answer": "x = 7",
            "explanation": "Denne linjen definerer variabelen x med verdien 7."
        },
        {
            "question": "Setning 2 – print (x er større enn 10)",
            "correct_answer": "print('x er større enn 10')",
            "explanation": "Denne linjen skriver ut at x er større enn 10 hvis betingelsen er oppfylt."
        },
        {
            "question": "Setning 2 – print (x er 10 eller mindre)",
            "correct_answer": "print('x er 10 eller mindre')",
            "explanation": "Denne linjen skriver ut at x er 10 eller mindre hvis betingelsen ikke er oppfylt."
        },
    ]

    correct_count = 0
    feedback = []

    # Loop through all the dropzones (questions), and check the user's answers from the GET parameters
    for i, dz in enumerate(dropzone_data):
        user_answer = request.GET.get(f'answer_{i}', "").strip()
        is_correct = (user_answer == dz["correct_answer"])
        if is_correct:
            correct_count += 1

        feedback.append({
            "question": dz["question"],
            "chosen_answer": user_answer if user_answer else "Ingen svar",
            "correct_answer": dz["correct_answer"],
            "is_correct": is_correct,
            "explanation": dz["explanation"] if not is_correct else ""
        })

    total = len(dropzone_data)

     # If the user is authenticated, update their progression score and quiz performance
    if request.user.is_authenticated:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_obj = request.user
        if not isinstance(user_obj, User):
            user_obj = User.objects.get(username=user_obj)
        user_progression, created = UserProgression.objects.get_or_create(user=user_obj)
        user_progression.progression_score += correct_count
        user_progression.save()

        quiz_name = "drag_and_drop"
        user_quiz, created = UserQuizScore.objects.get_or_create(user=user_obj, quiz_name=quiz_name)
        user_quiz.attempts += 1
        user_quiz.score = correct_count
        if correct_count > user_quiz.best_score:
            user_quiz.best_score = correct_count
        user_quiz.save()

    context = {
        "feedback": feedback,
        "correct_count": correct_count,
        "total": total,
    }
    
    messages.success(request, f"Du fikk {correct_count} av {total} riktige!")
    
    return render(request, "drag_and_drop_result.html", context)



@login_required
def blokkbasert_koding_result_view(request):
    """Evaluate block-based coding exercise and display results."""
    points_earned = 10  # Replace with actual logic to calculate points

    # Update the user's progression score
    if request.user.is_authenticated:
        user_progression, created = UserProgression.objects.get_or_create(user=request.user)
        user_progression.progression_score += points_earned
        user_progression.save()

    # Prepare context for the result page
    context = {
        "points_earned": points_earned,
        "total_points": user_progression.progression_score if request.user.is_authenticated else 0,
    }
    
    messages.success(request, f"Du tjente {points_earned} poeng! Totalt: {user_progression.progression_score}")

    return render(request, 'blokkbasert_koding_result.html', context)

def scoreboard(request):
    """Display user scoreboard ranked by progression scores."""
    user_progressions = UserProgression.objects.all().order_by('-progression_score')
    return render(request, 'scoreboard.html', {'user_progressions': user_progressions})


def is_admin(user):
    """Check if user belongs to Administrators group."""
    return user.groups.filter(name='Administratorer').exists()

@user_passes_test(is_admin)
def admin_dashboard(request):
    """Display admin dashboard with all users."""
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})


@login_required
def send_friend_request(request, user_id):
    """Send friend request to specified user."""
    receiver = get_object_or_404(User, id=user_id)
    
    if FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
        messages.error(request, "Venneforespørsel allerede sendt!")
    else:
        FriendRequest.objects.create(sender=request.user, receiver=receiver, status='pending')
        messages.success(request, "Venneforespørsel sendt!")
    
    return redirect('profile')

@login_required
def accept_friend_request(request, request_id):
    """Accept incoming friend request."""
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)

    if friend_request.status == 'pending':
        Friendship.objects.get_or_create(user1=friend_request.sender, user2=friend_request.receiver)
        Friendship.objects.get_or_create(user1=friend_request.receiver, user2=friend_request.sender)

        FriendRequest.objects.filter(
            Q(sender=friend_request.sender, receiver=friend_request.receiver) |
            Q(sender=friend_request.receiver, receiver=friend_request.sender)
        ).delete()

        messages.success(request, f"Du og {friend_request.sender.username} er nå venner!")
        return redirect('friend_requests')

    return redirect('friend_requests')


@login_required
def reject_friend_request(request, request_id):
    """Reject incoming friend request."""
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    
    if friend_request.status == 'pending':
        friend_request.status = 'rejected'
        friend_request.save()
        messages.success(request, f"Du har avslått forespørselen fra {friend_request.sender.username}.")
    
    return redirect('friend_requests')

@login_required
def friend_requests(request):
    """Display pending friend requests."""
    received_requests = FriendRequest.objects.filter(
        receiver=request.user,
        status='pending'
    ).select_related('sender')
    
    FriendRequest.objects.filter(
        receiver=request.user,
        status='pending',
        created_at__lt=timezone.now() - timedelta(days=30)
    ).delete()
    
    return render(request, 'friend_requests.html', {
        'received_requests': received_requests
    })

@login_required
def remove_friend(request, friendship_id):
    """Remove friend relationship."""
    friendship = get_object_or_404(Friendship, id=friendship_id)
    
    if request.user in [friendship.user1, friendship.user2]:
        friendship.delete()
        messages.success(request, "Venn fjernet")
    else:
        messages.error(request, "Ingen tilgang")
    
    return redirect('profile')


@login_required
def user_search(request):
    """Search for users by username."""
    query = request.GET.get('q', '')
    users = User.objects.exclude(id=request.user.id)
    
    if query:
        users = users.filter(
            Q(username__icontains=query) 
        )
    
    existing_friends = request.user.friends.all()
    pending_requests = FriendRequest.objects.filter(
        sender=request.user,
        status='pending'
    ).values_list('receiver_id', flat=True)
    
    users = users.exclude(
        Q(id__in=existing_friends.values_list('id', flat=True)) |
        Q(id__in=pending_requests)
    )
    
    return render(request, 'user_search.html', {
        'users': users,
        'query': query
    })
    
@login_required
def friend_progression(request):
    """Display friends' progression scores."""
    friend_ids = Friendship.objects.filter(user1=request.user).values_list('user2', flat=True)

    friends = User.objects.filter(id__in=friend_ids).select_related('userprogression')

    friends = sorted(
        friends,
        key=lambda f: f.userprogression.progression_score if hasattr(f, 'userprogression') else 0,
        reverse=True
    )

    context = {
        'friends': friends,
    }
    return render(request, 'friend_progression.html', context)

def oop_quiz_view(request):
    return render(request, 'quiz_oop.html')

@login_required
def oop_quiz_result_view(request):
    """
    Evaluates the user's answers to the Object-Oriented Programming (OOP) quiz, provides feedback on each question,
    updates the user's progression score if authenticated, and displays the results on a quiz result page.

    This view retrieves the user's answers from the GET parameters, compares them with the correct answers, 
    calculates the number of correct answers, and generates feedback for each question. If the user is authenticated, 
    their progression score is updated based on the quiz performance.

    """
    answers = []
    feedback = []
    correct_count = 0

    for i, question in enumerate(OOP_QUIZ_QUESTIONS):
        chosen_str = request.GET.get(f'answer_{i}', "")
        try:
            chosen = int(chosen_str)
        except ValueError:
            chosen = -1

        is_correct = (chosen == question["correct"])
        if is_correct:
            correct_count += 1

        feedback.append({
            "question": question["question"],
            "chosen_answer": question["choices"][chosen] if 0 <= chosen < len(question["choices"]) else "Ingen svar",
            "correct_answer": question["choices"][question["correct"]],
            "is_correct": is_correct,
            "explanation": question["explanation"] if not is_correct else ""
        })

    
    if request.user.is_authenticated:
        user_progression, _ = UserProgression.objects.get_or_create(user=request.user)
        user_progression.progression_score += correct_count
        user_progression.save()

    context = {
        "feedback": feedback,
        "correct_count": correct_count,
        "total": len(OOP_QUIZ_QUESTIONS),
    }
    
    messages.success(request, f"Du fikk {correct_count} av {len(OOP_QUIZ_QUESTIONS)} riktige!")

    return render(request, "quiz_oop_result.html", context)


OOP_QUIZ_QUESTIONS = [
    {
        "question": "Hva er et objekt i objektorientert programmering?",
        "choices": [
            "En funksjon som returnerer en verdi",
            "En instans av en klasse",
            "En loopstruktur",
            "En datatype"
        ],
        "correct": 1,
        "explanation": "Et objekt er en instans av en klasse, med egne attributter og metoder."
    },
    {
        "question": "Hva gjør nøkkelordet `self` i Python-klasser?",
        "choices": [
            "Refererer til en global variabel",
            "Er navnet på klassen",
            "Refererer til instansen av klassen",
            "Importerer klassen"
        ],
        "correct": 2,
        "explanation": "`self` refererer til det aktuelle objektet/instansen."
    },
    {
        "question": "Hva er arv i objektorientert programmering?",
        "choices": [
            "En metode som lager nye objekter",
            "Evnen til å dele data mellom funksjoner",
            "En mekanisme der en klasse arver egenskaper fra en annen klasse",
            "En prosess for å slette objekter"
        ],
        "correct": 2,
        "explanation": "Arv lar en klasse overta attributter og metoder fra en annen klasse."
    },
    {
    "question": "Hva er polymorfisme i objektorientert programmering?",
    "choices": [
        "Evnen til å endre verdier i objekter",
        "Muligheten for én funksjon å ha ulike former",
        "Å bruke flere klasser i én fil",
        "Å slette objekter dynamisk"
    ],
    "correct": 1,
    "explanation": "Polymorfisme betyr at en metode eller funksjon kan ha forskjellige former, avhengig av hvilken klasse som bruker den."
}


    
]

@login_required
def mark_tutorial_seen(request):
    """Mark tutorial as seen for current user."""
    if request.method == 'POST':
        user = request.user
        user.has_seen_tutorial = True
        user.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)



