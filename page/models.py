from django.db import models
# [코드 추가] settings.py의 객체를 불러올 수 있도록 설정
from django.conf import settings

# Create your models here.
class Posting(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # [코드 추가] 작성자를 저장하는 필드 추가
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='postings',null=True,blank = True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name='comment_list')
    content = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    # [코드 추가] 작성자를 저장하는 필드 추가
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments',null=True, blank = True)
