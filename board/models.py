from datetime import datetime

from django.db import models
from member.models import Member

# Create your models here.
# on_delete : CASCADE, Do_NOTHING
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10)
    member = models.ForeignKey(Member, related_name='board',
                               on_delete=models.CASCADE)
    regdate = models.DateTimeField(default=datetime.now)
    views = models.IntegerField(default=0)
    contents = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'board'
        ordering= ['-regdate']

    def __str__(self):
        return self.title
