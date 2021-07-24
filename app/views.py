from django.shortcuts import render
from django.db.models import Q

from .models import kanji, vocab, meanings, readings, source, examples

from itertools import chain
import random

# Create your views here.

def lesson_page(request):
    kanji_lesson = kanji.objects.filter(have_learned=False)
    vocab_lesson = vocab.objects.filter(
        linked_kanji__have_learned=True,
        have_learned=False,
    )

    lesson_list = list(chain(kanji_lesson, vocab_lesson))
    lesson = random.choice(lesson_list)

    meaning = meanings.objects.filter(Q(kanji__item=lesson) | Q(vocab__item=lesson))
    reading = readings.objects.filter(Q(kanji__item=lesson) | Q(vocab__item=lesson))

    return render(request, 'app/lesson.html', {'lesson': lesson, 'meaning': meaning, 'reading': reading})

def review_page(request):
    return render(request, 'app/review.html', {})

def main_page(request):
    return render(request, 'app/main.html', {})