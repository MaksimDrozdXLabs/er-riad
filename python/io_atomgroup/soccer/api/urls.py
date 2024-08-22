from django.urls import include, path, re_path

urlpatterns = [
    path(
        r'leaderboard',
        include('python.io_atomgroup.soccer.leaderboard.urls'),
        name='leaderboard',
    )
]
