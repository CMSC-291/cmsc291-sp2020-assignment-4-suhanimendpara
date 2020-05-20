from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def add_question(request):
    question_text = request.POST['question_text']
    question = Question(question_text=question_text, pub_date=timezone.now())
    question.save()
    return HttpResponseRedirect(reverse('polls:index'))

def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question.id)
    if request.value == "Delete":
        question.delete()
    return HttpResponseRedirect(reverse('polls:index'))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_text = request.POST['choice_text']
    choice = Choice(question=question, choice_text=choice_text)
    choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    question = get_object_or_404(Question, pk=choice.question.id)
    if request.method == "POST":
        choice.delete()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
