from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from .models import UserProgression  # Importer UserProgression-modellen
from .models import Module
from .models import UserQuizScore
from django.utils import timezone
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    email = forms.EmailField(required=True, help_text="En gyldig e-postadresse er påkrevd.")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
    
    
    def clean_password2(self):
        password = self.cleaned_data.get("password2")
        
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn.")
        
        if not re.search(r'\d', password):
            raise forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn")
        
        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("Passordet må inneholde minst én stor bokstav, minst ett tall og ett spesialtegn")
        
        return password


def home(request):
    return render(request, 'home.html')
    
def about(request):
    return render(request, 'about.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            # feil melding ved ugyldig innlogg
            messages.error(request, 'Invalid username or password.')
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'register.html', { 'form': form})



@login_required
def profile(request):
    try:
        progression = UserProgression.objects.get(user=request.user)  # Henter brukerens progresjon
    except UserProgression.DoesNotExist:
        progression = None  # Hvis ingen progresjonsdata finnes, settes det til None

    return render(request, 'profile.html', {'progression': progression})

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'editprofile.html', {'form': form})



def module_overview(request):
    # Hent alle moduler fra databasen
    modules = Module.objects.all()
    context = {'modules': modules}
    return render(request, 'modules_overview.html', context)

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

    context = {
        "feedback": feedback,
        "correct_count": correct_count,
        "total": len(QUIZ_QUESTIONS),
    }
    return render(request, "quiz_python_result.html", context)



def blokkbasert_instruksjoner(request):
    return render(request, 'blokkbasert_instruksjoner.html')

# View for blokkbasert koding
@login_required
def blokkbasert_koding(request):
    return render(request, 'block_coding.html')  # Renders the 'block_coding.html' template