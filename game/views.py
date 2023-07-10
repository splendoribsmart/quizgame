from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Level, Subject, Quiz, Question, Choice, Answer, Point
from .forms import SubjectSelectionForm

@login_required
def subject_selection_view(request):
    if request.method == 'POST':
        form = SubjectSelectionForm(request.POST)
        if form.is_valid():
            selected_subject = form.cleaned_data['subject']
            levels = Level.objects.filter(subject=selected_subject)
            context = {'levels': levels}
            return render(request, 'level_selection.html', context)
    else:
        form = SubjectSelectionForm()
    
    context = {'form': form}
    return render(request, 'subject_selection.html', context)

@login_required
def level_selection_view(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    levels = Level.objects.filter(subject=subject)
    context = {'subject': subject, 'levels': levels}
    return render(request, 'level_selection.html', context)

# def level_selection_view(request, subject_id):
#     subject = get_object_or_404(Subject, pk=subject_id)
#     levels = Level.objects.filter(subject=subject)
#     quizzes = Quiz.objects.filter(level__subject=subject)
#     context = {'subject': subject, 'levels': levels, 'quizzes': quizzes}
#     return render(request, 'level_selection.html', context)
# def level_selection_view(request, level_id):
#     level = Level.objects.get(pk=level_id)
#     quizzes = Quiz.objects.filter(level=level)
#     context = {'level': level, 'quizzes': quizzes}
#     return render(request, 'level_selection.html', context)

@login_required
def level_detail_view(request, level_id):
    level = get_object_or_404(Level, pk=level_id)
    quizzes = Quiz.objects.filter(level=level)
    context = {'level': level, 'quizzes': quizzes}
    return render(request, 'level_detail.html', context)

@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.question_set.all()
    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'quiz.html', context)
# def quiz_view(request, quiz_id):
#     quiz = Quiz.objects.get(pk=quiz_id)
#     questions = Question.objects.filter(quiz=quiz)
#     context = {'quiz': quiz, 'questions': questions}
#     return render(request, 'quiz.html', context)

@login_required
def submit_quiz_view(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = Choice.objects.get(pk=selected_choice_id)
                if selected_choice.is_correct:
                    correct_answers += 1
                    # You can implement further logic here to update scores, etc.
                    # ...

        # Calculate and update user's score for the level
        user = request.user
        level = quiz.level
        point, created = Point.objects.get_or_create(user=user, level=level)
        point.score = (correct_answers / total_questions) * 100
        point.save()

        return redirect('quiz_result', point_id=point.id)

@login_required
def quiz_result_view(request, point_id):
    point = Point.objects.get(pk=point_id)
    context = {'point': point}
    return render(request, 'quiz_result.html', context)
