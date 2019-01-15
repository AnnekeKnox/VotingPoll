from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question
from django.http import Http404
from django.urls import reverse
from django.views import generic

# Create your views here.

class DayofDeadView(generic.DetailView):
    template_name = 'votingpoll/dayOftheDead.html'
    model = Question

class HalloweenView(generic.DetailView):
    template_name = 'votingpoll/halloween.html'
    model = Question

class IndexView(generic.ListView):
    template_name = 'votingpoll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'votingpoll/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'votingpoll/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        
        return render(request, 'votingpoll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
       
        return HttpResponseRedirect(reverse('votingpoll:results', args=(question.id,)))