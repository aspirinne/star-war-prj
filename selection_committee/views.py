from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseNotFound
from .forms import YounglingForm
from .models import *
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

# Start page with choice
def selection_committee(request):
    return render(request, 'selection_committee/index.html')


# registration form for youngling
def youngling(request):
    if request.method == 'POST':
        younglingform = YounglingForm(request.POST)
        if younglingform.is_valid():
            young = younglingform.save()
            return redirect('selection_committee:before', young_id=young.id)
    else:
        younglingform = YounglingForm()
    return render(request, 'selection_committee/youngling_edit.html', {'younglingform': younglingform})


# Creating of thr Personal Test for Youngling
def before_testing(request, young_id):
    # get the random order from model.Order
    order = Order.objects.all().order_by('?').first()
    personal_test = Test()
    personal_test.orders_code_id = order.id
    personal_test.youngling_id = young_id
    personal_test.save()
    # Select of 3 random question from model.Question
    questions_list = Question.objects.all().order_by('?')[:3]
    for quest in questions_list:
        answer = QAns()
        answer.test_id = personal_test.id
        answer.question_id = quest.id
        answer.save()
    return redirect('selection_committee:testing', personal_test_id=personal_test.id)


# Answering for test
def testing(request, personal_test_id):
    try:
        qs = QAns.objects.filter(test_id=personal_test_id).prefetch_related('question')
        if request.method == 'POST':
            for quest in qs:
                quest.answer = request.POST[str(quest.id)]
                # ans = request.POST[str(quest.id)]
                # if ans == 'None':
                #     quest.answer = None
                # elif ans == 'True':
                #     quest.answer = True
                # else:
                #     quest.answer = False
                quest.save()
            return render(request, 'selection_committee/index.html')
        else:
            personal_test = Test.objects.get(id=personal_test_id)
            return render(request, 'selection_committee/answering.html', {'qs': qs, 'personal_test': personal_test})
    except QAns.DoesNotExist:
        return HttpResponseNotFound('<h2>Question not found</h2>')


def jedies(request):
    all_jedies = Jedi.objects.all()
    if request.method == 'POST':
        selected_jedi_id = request.POST['jedi_selecter']
        return redirect('selection_committee:j_y_choosing', selected_jedi_id=selected_jedi_id)
    else:
        return render(request, 'selection_committee/jedies.html', {'all_jedies': all_jedies})


def j_y_choosing(request, selected_jedi_id):
    jedi = Jedi.objects.get(id=selected_jedi_id)
    younglings = Youngling.objects.filter(planet_habitat=jedi.planet_stud, teacher__isnull=True)
    if request.method == 'POST':
        try:
            selected_padawan = request.POST['id_checked']
        except KeyError:
            selected_padawan = None
        if selected_padawan is not None:
            padawan = Youngling.objects.get(id=selected_padawan)
            padawan.teacher_id = selected_jedi_id
            subject = padawan.name
            message = 'Congratulations! ' + padawan.teacher.name + ' will teach you!'
            adress = padawan.email
            padawan.save()
            send_mail(subject, message, settings.EMAIL_HOST_USER, [adress])
        return render(request, 'selection_committee/index.html')
    else:
        return render(request, 'selection_committee/padawan_select.html', {'younglings': younglings})
