from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields import CharField, TextField, IntegerField, ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField

import unittest
import sys


class TestModels(unittest.TestCase):
    def test_import(self):
        import qa.models


class TestProfile(unittest.TestCase):
    def test_profile(self):
        from qa.models import Profile
        try:
            avatar = Profile._meta.get_field('avatar')
        except FieldDoesNotExist:
            assert False, "avatar field does not exist in Profile model"
        assert isinstance(avatar, ImageField), "avatar field is not ImageField"


class TestQuestion(unittest.TestCase):
    def test_question(self):
        from qa.models import Question
        try:
            title = Question._meta.get_field('title')
        except FieldDoesNotExist:
            assert False, "title field does not exist in Question model"
        assert isinstance(title, CharField), "title field is not CharField"
        try:
            text = Question._meta.get_field('text')
        except FieldDoesNotExist:
            assert False, "text field does not exist in Question model"
        assert isinstance(text, TextField), "text field is not TextField"
        try:
            added_at = Question._meta.get_field('added_at')
        except FieldDoesNotExist:
            assert False, "added_at field does not exist in Question model"
        assert isinstance(text, DateField) or isinstance(added_at, DateField), "added_at field is not DateTimeField"
        try:
            rating = Question._meta.get_field('rating')
        except FieldDoesNotExist:
            assert False, "rating field does not exist in Question model"
        assert isinstance(rating, IntegerField), "text field is not IntegerField"
        try:
            author = Question._meta.get_field('author')
        except FieldDoesNotExist:
            assert False, "author field does not exist in Question model"
        assert isinstance(author, ForeignKey), "author field is not ForeignKey"
        assert author.related_field.model == User, "author field does not refer User model"


class TestAnswer(unittest.TestCase):
    def test_answer(self):
        from qa.models import Answer
        try:
            text = Answer._meta.get_field('text')
        except FieldDoesNotExist:
            assert False, "text field does not exist in Answer model"
        assert isinstance(text, TextField), "text field is not TextField"
        try:
            question = Answer._meta.get_field('question')
        except FieldDoesNotExist:
            assert False, "question field does not exist in Answer model"
        assert isinstance(question, ForeignKey), "question field is not ForeignKey"
        assert author.related_field.model == Question, "question field does not refer Question model"
        try:
            added_at = Answer._meta.get_field('added_at')
        except FieldDoesNotExist:
            assert False, "added_at field does not exist in Answer model"
        assert isinstance(text, DateField) or isinstance(added_at, DateField), "added_at field is not DateTimeField"
        try:
            author = Answer._meta.get_field('author')
        except FieldDoesNotExist:
            assert False, "author field does not exist in Answer model"
        assert isinstance(author, ForeignKey), "author field is not ForeignKey"
        assert author.related_field.model == User, "author field does not refer User model"


suite = unittest.TestLoader().loadTestsFromTestCase(globals().get(sys.argv[1]))
unittest.TextTestRunner(verbosity=0).run(suite)
