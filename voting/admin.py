from django.contrib import admin
from .models import Vote, VoteOption, UserVote

admin.site.register(Vote)
admin.site.register(VoteOption)
admin.site.register(UserVote)
