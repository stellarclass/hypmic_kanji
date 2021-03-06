from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.core.signals import request_started
from django.dispatch import receiver

from django.utils import timezone

from .models import kanji, vocab, meanings, readings, source, examples
from .forms import KanjiLessonForm, VocabLessonForm, MeaningSynonymsForm

import ebisu

# Create your views here.

def lesson_page(request):
    # TBD: add in a view when there is nothing to learn
    # maybe make a pre-view page
    # if kanji is available, elif vocab, else nothing
    # when updating the models, can probably trim down some of this code/the forms
    # most of the stuff can be put into the learning state

    # TO DO:
    # filter by source, so we can select different sources to learn from
    # order by learning order?

    kanji_lesson = kanji.objects.filter(have_learned=False)
    if kanji_lesson.exists():
        kanji_lesson = kanji_lesson.first()
        meaning = meanings.objects.filter(Q(kanji__item=kanji_lesson))
        reading = readings.objects.filter(Q(kanji__item=kanji_lesson))
        if request.method == "POST":
            user_syn_form = MeaningSynonymsForm(request.POST)
            kanji_form = KanjiLessonForm(request.POST, instance=kanji_lesson)
            if user_syn_form.is_valid() and kanji_form.is_valid():
                user_syn = user_syn_form.save(commit=False)
                user_syn.kanji = kanji_lesson
                user_syn.save()
                kanji_form = kanji_form.save(commit=False)
                kanji_form.have_learned = True
                kanji_form.date_learned = timezone.now()
                kanji_form.date_last_reviewed = timezone.now()
                kanji_form.save()
                return HttpResponseRedirect(reverse('lesson_page'))
        else:
            user_syn_form = MeaningSynonymsForm()
            kanji_form = KanjiLessonForm(instance=kanji_lesson)
        return render(request, 'app/lesson.html', {'lesson': kanji_lesson, 'meaning': meaning, 'reading': reading,
                                                   'user_syn_form': user_syn_form, 'item_form': kanji_form})
    vocab_lesson = vocab.objects.filter(
        linked_kanji__have_learned=True,
        have_learned=False,
    )
    if vocab_lesson.exists():
        vocab_lesson = vocab_lesson.first()
        meaning = meanings.objects.filter(Q(vocab__item=vocab_lesson))
        reading = readings.objects.filter(Q(vocab__item=vocab_lesson))
        if request.method == "POST":
            user_syn_form = MeaningSynonymsForm(request.POST)
            vocab_form = VocabLessonForm(request.POST, instance=vocab_lesson)
            if user_syn_form.is_valid() and vocab_form.is_valid():
                user_syn = user_syn_form.save(commit=False)
                user_syn.vocab = vocab_lesson
                user_syn.save()
                vocab_form = vocab_form.save(commit=False)
                vocab_form.have_learned = True
                vocab_form.date_learned = timezone.now()
                vocab_form.date_last_reviewed = timezone.now()
                vocab_form.save()
                return HttpResponseRedirect(reverse('lesson_page'))
        else:
            user_syn_form = MeaningSynonymsForm()
            vocab_form = VocabLessonForm(instance=vocab_lesson)
        return render(request, 'app/lesson.html', {'lesson': vocab_lesson, 'meaning': meaning, 'reading': reading,
                                                       'user_syn_form': user_syn_form, 'item_form': vocab_form})

    return render(request, 'app/lesson.html', {})

# update review recall every time the review page is accessed
# probably move this to a pre-review page so it only does it once every session?
# otherwise if this grows, it'll start to become very slow thanks to the loops
@receiver(request_started)
def callback(sender, environ, **kwargs):
    if environ['PATH_INFO'] == '/review/':
        print('Reviews Updating')
        from datetime import timedelta
        from django.utils import timezone

        now = timezone.now()
        oneHour = timedelta(hours=1)

        for kanji_review in kanji.objects.filter(have_learned=True):
            kanji_review.recall_prob = ebisu.predictRecall(
                (kanji_review.alpha, kanji_review.beta, kanji_review.half_life),
                (now - kanji_review.date_last_reviewed) / oneHour,
                exact=True)
            kanji_review.save(update_fields=['recall_prob'])

        for vocab_review in vocab.objects.filter(have_learned=True):
            vocab_review.recall_prob = ebisu.predictRecall(
                (vocab_review.alpha, vocab_review.beta, vocab_review.half_life),
                (now - vocab_review.date_last_reviewed) / oneHour,
                exact=True)
            vocab_review.save(update_fields=['recall_prob'])

def review_page(request):
    # TBD: add in a view when there is nothing to review
    # need to update recall probs for each item before we run the reviews - should this be a "pre-view" somewhere?

    kanji_review = kanji.objects.filter(have_learned=True).order_by('recall_prob').last()
    vocab_review = vocab.objects.filter(have_learned=True).order_by('recall_prob').last()

    if not kanji_review and not vocab_review:
        # no reviews available
        return render(request, 'app/review.html', {})

    elif not kanji_review:
        # go straight into vocab review
        review = vocab_review

    elif not vocab_review:
        # go straight into kanji review
        review = kanji_review

    # if both available, pick whichever one is lower in recall
    elif kanji_review.recall_prob > vocab_review.recall_prob:
        review = vocab_review

    else:
        review = kanji_review

    meaning = meanings.objects.filter(Q(kanji__item=review) | Q(vocab__item=review))
    reading = readings.objects.filter(Q(kanji__item=review) | Q(vocab__item=review))

    return render(request, 'app/review.html', {'review': review, 'meaning': meaning, 'reading': reading})

def main_page(request):
    return render(request, 'app/main.html', {})