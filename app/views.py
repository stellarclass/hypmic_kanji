from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import kanji, vocab, meanings, readings, source, examples
from .forms import KanjiLessonForm, VocabLessonForm, MeaningSynonymsForm

from itertools import chain
import random

# Create your views here.

def lesson_page(request):
    # TBD: add in a view when there is nothing to learn
    kanji_lesson = kanji.objects.filter(have_learned=False)
    vocab_lesson = vocab.objects.filter(
        linked_kanji__have_learned=True,
        have_learned=False,
    )

    # can't randomize lesson like this - impacts writing to the db
    lesson_list = list(chain(kanji_lesson, vocab_lesson))
    lesson = random.choice(lesson_list)

    meaning = meanings.objects.filter(Q(kanji__item=lesson) | Q(vocab__item=lesson))
    reading = readings.objects.filter(Q(kanji__item=lesson) | Q(vocab__item=lesson))

    #user_syn = get_object_or_404(meaning)
    item_learned = get_object_or_404(kanji.objects.filter(Q(item=lesson)))
    if request.method == "POST":
        user_syn_form = MeaningSynonymsForm(request.POST)
        kanji_form = KanjiLessonForm(request.POST, instance=item_learned)
        if user_syn_form.is_valid() and kanji_form.is_valid():
            user_syn = user_syn_form.save(commit=False)
            user_syn.kanji = item_learned
            user_syn.save()
            kanji_form = kanji_form.save(commit=False)
            kanji_form.have_learned = True
            kanji_form.save()
            return HttpResponseRedirect(reverse('lesson_page'))
    else:
        user_syn_form = MeaningSynonymsForm()
        kanji_form = KanjiLessonForm(instance=item_learned)

    return render(request, 'app/lesson.html', {'lesson': lesson, 'meaning': meaning, 'reading': reading,
                                               'user_syn_form': user_syn_form, 'kanji_form': kanji_form})

def learn_lesson(request, item):
    if item.linked_kanji:
        vocab.have_learned=True
        vocab.save()
    else:
        kanji.have_learned=True
        kanji.save()
    return HttpResponseRedirect(reverse('lesson_page'))

def review_page(request):
    # TBD: add in a view when there is nothing to review
    kanji_review = kanji.objects.filter(have_learned=True)
    vocab_review = vocab.objects.filter(have_learned=True)

    review_list = list(chain(kanji_review, vocab_review))
    review = random.choice(review_list)

    meaning = meanings.objects.filter(Q(kanji__item=review) | Q(vocab__item=review))
    reading = readings.objects.filter(Q(kanji__item=review) | Q(vocab__item=review))

    return render(request, 'app/review.html', {'review': review, 'meaning': meaning, 'reading': reading})

def main_page(request):
    return render(request, 'app/main.html', {})