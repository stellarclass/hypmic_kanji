from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

"""class user(models.Model):
    pass

class learningState(models.Model):
    # user-specific details
    #user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_notes = models.TextField(blank=True, null=True)

    # linking to the item to be learned
    kanji = models.ForeignKey(kanji, blank=True, null=True, on_delete=models.DO_NOTHING)
    vocab = models.ForeignKey(vocab, blank=True, null=True, on_delete=models.DO_NOTHING)

    # details about when item was learned
    have_learned = models.BooleanField(default=False)
    date_learned = models.DateTimeField(blank=True, null=True)

    # details about reviewing
    date_last_reviewed = models.DateTimeField(blank=True, null=True)
    recall_prob = models.FloatField(blank=True, null=True)
    alpha = models.FloatField(default=4.0)
    beta = models.FloatField(default=4.0)
    half_life = models.FloatField(default=24.0)

    # properties for linking to item to be learned (kanji or vocab)
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
            raise ValueError("obj parameter must be an object of Kanji or Vocab class")"""

class commonLearning(models.Model):
    # TBD: change name of class, remove items that have been moved to learning state
    have_learned = models.BooleanField(default=False)
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
    kanji = models.ForeignKey(kanji, blank=True, null=True, on_delete=models.DO_NOTHING)
    vocab = models.ForeignKey(vocab, blank=True, null=True, on_delete=models.DO_NOTHING)
    meanings = models.TextField()

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

class user_synonyms(models.Model):
    # maybe link this to learn state
    kanji = models.ForeignKey(kanji, blank=True, null=True, on_delete=models.DO_NOTHING)
    vocab = models.ForeignKey(vocab, blank=True, null=True, on_delete=models.DO_NOTHING)
    user_synonyms = models.TextField()

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

class readings(models.Model):
    kanji = models.ForeignKey(kanji, blank=True, null=True, on_delete=models.DO_NOTHING)
    vocab = models.ForeignKey(vocab, blank=True, null=True, on_delete=models.DO_NOTHING)
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

class source(models.Model):
    # model for where the kanji/vocab are found (e.g. which songs, etc.)
    item_source = models.TextField()
    kanji = models.ManyToManyField(kanji, blank=True)
    vocab = models.ManyToManyField(vocab, blank=True)

class examples(models.Model):
    # model for sample/context sentences (e.g. lyrics)
    example_sentence = models.TextField()
    source = models.ForeignKey(source, on_delete=models.DO_NOTHING)
    # vocab = models.ManyToManyField(vocab)
    # instead of manually linking vocab, can probably do a filter on the contents?
