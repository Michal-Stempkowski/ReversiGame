from django.db import models


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text


class PlayerAIRecord(models.Model):
    name = models.CharField(max_length=200, default='human_player')


class GameBoardRecord(models.Model):
    player1_AI = models.ForeignKey(PlayerAIRecord, related_name='player1')
    player2_AI = models.ForeignKey(PlayerAIRecord, related_name='player2')
    game_state = models.CharField(max_length=200)
    board_size = models.IntegerField(default=8)
    board = models.CharField(max_length=200)
