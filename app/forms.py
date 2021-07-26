from django import forms

from .models import kanji, vocab, meanings, user_synonyms

class KanjiLessonForm(forms.ModelForm):

    class Meta:
        model = kanji
        fields = ('user_notes', )

class VocabLessonForm(forms.ModelForm):

    class Meta:
        model = vocab
        fields = ('user_notes', )

class MeaningSynonymsForm(forms.ModelForm):

    class Meta:
        model = user_synonyms
        fields = ('user_synonyms', )