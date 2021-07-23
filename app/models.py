from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import timedelta
import ebisu

class commonLearning(models.Model):
    #user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    have_learned = models.BinaryField(default=False)
    order_of_learning = models.PositiveIntegerField()
    item = models.TextField()
    date_learned = models.DateTimeField(blank=True, null=True)
    date_last_reviewed = models.DateTimeField(blank=True, null=True)
    recall_prob = models.FloatField()

    class Meta:
        abstract = True

    def learn(self):
        self.date_learned = timezone.now()
        self.date_last_reviewed = timezone.now()
        self.save()

    def review(self, bayes_model, quiz_result):
        self.recall_prob = ebisu.updateRecall([bayes_model.alpha, bayes_model.beta, bayes_model.half_life],
                                              quiz_result, 1,
                                              (timezone.now() - self.date_last_reviewed)/timedelta()hours=1)
        self.date_last_reviewed = timezone.now()
        self.save()

    def __str__(self):
        return self.item_learned

class kanji(commonLearning):

class vocab(commonLearning):
    linked_kanji = models.ManyToManyField(kanji)

class meanings(models.Model):
    item = models.ForeignKey(commonLearning, on_delete=models.DO_NOTHING)
    meanings = models.TextField()

    def __str__(self):
        return self.meanings

class readings(models.Model):
    readings = models.TextField()

    def __str__(self):
        return self.readings

class bayes_model(models.Model):
    item = models.OneToOneField(commonLearning, on_delete=models.CASCADE)
    alpha = models.FloatField(default = 4.0)
    beta = models.FloatField(default = 4.0)
    half_life = models.FloatField(default = 24.0)

    def __str__(self):
        return 'Current model for %s: [%s, %s, %s]' % (self.)