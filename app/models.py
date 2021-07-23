from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class commonLearning(models.Model):
    #user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    have_learned = models.BinaryField(default=False)
    order_of_learning = models.PositiveIntegerField()
    item = models.TextField()
    date_learned = models.DateTimeField(blank=True, null=True)
    date_last_reviewed = models.DateTimeField(blank=True, null=True)
    recall_prob = models.FloatField(blank=True, null=True)
    alpha = models.FloatField(default = 4.0)
    beta = models.FloatField(default = 4.0)
    half_life = models.FloatField(default = 24.0)
    user_notes = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.item

class kanji(commonLearning):
    pass

class vocab(commonLearning):
    linked_kanji = models.ManyToManyField(kanji)

class meanings(models.Model):
    kanji = models.ForeignKey(kanji, on_delete=models.DO_NOTHING)
    vocab = models.ForeignKey(vocab, on_delete=models.DO_NOTHING)
    meanings = models.TextField()
    user_synonyms = models.TextField(blank=True, null=True)

    @property
    def type_of_item(self):
        return self.kanji or self.vocab

    @type_of_item.setter
    def type_of_item(self, obj):
        if type(obj) == kanji:
            self.kanji = obj
            self.vocab = None
        elif type(obj) == vocab:
            self.vocab = obj
            self.kanji = None
        else:
            raise ValueError("obj parameter must be an object of Kanji or Vocab class")

    def __str__(self):
        return 'Meaning(s) are %s' % (self.meanings)

class readings(models.Model):
    kanji = models.ForeignKey(kanji, on_delete=models.DO_NOTHING)
    vocab = models.ForeignKey(vocab, on_delete=models.DO_NOTHING)
    readings = models.TextField()

    @property
    def type_of_item(self):
        return self.kanji or self.vocab

    @type_of_item.setter
    def type_of_item(self, obj):
        if type(obj) == kanji:
            self.kanji = obj
            self.vocab = None
        elif type(obj) == vocab:
            self.vocab = obj
            self.kanji = None
        else:
            raise ValueError("obj parameter must be an object of Kanji or Vocab class")

    def __str__(self):
        return 'Reading(s) are %s' % (self.readings)
