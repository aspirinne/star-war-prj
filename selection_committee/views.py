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
    """
    View function for Start Page.
    :param request:
    :return: start page (selection_committee/index.html)
    """
    return render(request, 'selection_committee/index.html')


# registration form for youngling
def youngling(request):
    """
    View function for Youngling's registration page with form.
    :param request:
    :return: GET: registration page; POST: redirect to selection_committee:before with this registered youngling's ID.
    """
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
    """
    Function what make and save personal test by the random questions and random order for registered youngling.
    :param request:
    :param young_id: ID of registered youngling, who will answer this test.
    :return: redirect to selection_committee:testing and generated Test's ID.
    """
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
    """
    View function for answering page, where youngling answer the questions from his personal test.
    :param request:
    :param personal_test_id: ID of test, what was generated for this youngling.
    :return: GET: youngling's answering page; POST: start page.
    """
    try:
        qs = QAns.objects.filter(test_id=personal_test_id).prefetch_related('question')
    except QAns.DoesNotExist:
        return HttpResponseNotFound('<h2>Question not found</h2>')
    else:
        if request.method == 'POST':
            for quest in qs:
                answers_selecter_name = str(quest.id)
                quest.answer = request.POST[answers_selecter_name]
                quest.save()
            return render(request, 'selection_committee/index.html')
        else:
            personal_test = Test.objects.get(id=personal_test_id)
            return render(request, 'selection_committee/answering.html', {'qs': qs, 'personal_test': personal_test})


def jedies(request):
    """
    View function for page where jedi chose himself from the list.
    :param request:
    :return: GET: page with all jedies list; POST: redirect to selection_committee:j_y_choosing with selected jedi's ID.
    """
    all_jedies = Jedi.objects.all()
    if request.method == 'POST':
        selected_jedi_id = request.POST['jedi_selecter']
        return redirect('selection_committee:j_y_choosing', selected_jedi_id=selected_jedi_id)
    else:
        return render(request, 'selection_committee/jedies.html', {'all_jedies': all_jedies})


def j_y_choosing(request, selected_jedi_id):
    """
    View function for page, where jedi can see younglings without teacher from his planet and their answers for personal test.
    Based on answers he can choose youngling, who become his apprentice. And message will be sent for this youngling.
    :param request:
    :param selected_jedi_id: ID of jedi, who watch this page.
    :return: GET: page with younglings; POST: start page
    """
    jedi = Jedi.objects.get(id=selected_jedi_id)
    younglings = Youngling.objects.filter(planet_habitat=jedi.planet_stud, teacher__isnull=True)
    if request.method == 'POST':
        try:
            selected_padawan = request.POST['id_checked']
        except KeyError:
            print('He does not want to get new student')
        else:
            padawan = Youngling.objects.get(id=selected_padawan)
            padawan.teacher_id = selected_jedi_id
            subject = padawan.name
            message = 'Congratulations! ' + padawan.teacher.name + ' will teach you!'
            adress = padawan.email
            padawan.save()
            send_mail(subject, message, settings.EMAIL_HOST_USER, [adress])
        finally:
            return render(request, 'selection_committee/index.html')
    else:
        return render(request, 'selection_committee/padawan_select.html', {'younglings': younglings})
