from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # ── CLIENT ─────────────────────────────────────────
    path('', views.index_view, name='index'),
    path('movies/', views.movie_list_view, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail_view, name='movie_detail'),
    path('coming/', views.coming_view, name='coming'),
    path('newsletter/', views.newsletter_view, name='newsletter'),
    path('chair/', views.chair_view, name='chair'),
    path('payment/', views.payment_view, name='payment'),
    path('confirm/', views.confirm_view, name='confirm'),

    # ── AUTH ────────────────────────────────────────────
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    # ── ADMIN PANEL ─────────────────────────────────────
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),

    # Movies
    path('admin-panel/movies/', admin_views.admin_movies, name='admin_movies'),
    path('admin-panel/movies/create/', admin_views.admin_create_movie, name='admin_create_movie'),
    path('admin-panel/movies/<int:movie_id>/edit/', admin_views.admin_edit_movie, name='admin_edit_movie'),
    path('admin-panel/movies/<int:movie_id>/delete/', admin_views.admin_delete_movie, name='admin_delete_movie'),

    # Rooms
    path('admin-panel/rooms/', admin_views.admin_rooms, name='admin_rooms'),
    path('admin-panel/rooms/create/', admin_views.admin_create_room, name='admin_create_room'),
    path('admin-panel/rooms/<int:room_id>/edit/', admin_views.admin_edit_room, name='admin_edit_room'),
    path('admin-panel/rooms/<int:room_id>/delete/', admin_views.admin_delete_room, name='admin_delete_room'),

    # Shows
    path('admin-panel/shows/', admin_views.admin_shows, name='admin_shows'),
    path('admin-panel/shows/create/', admin_views.admin_create_show, name='admin_create_show'),
    path('admin-panel/shows/<int:show_id>/edit/', admin_views.admin_edit_show, name='admin_edit_show'),
    path('admin-panel/shows/<int:show_id>/delete/', admin_views.admin_delete_show, name='admin_delete_show'),

    # Bills
    path('admin-panel/bills/', admin_views.admin_bills, name='admin_bills'),
    path('admin-panel/bills/<int:bill_id>/edit/', admin_views.admin_edit_bill, name='admin_edit_bill'),
    path('admin-panel/bills/<int:bill_id>/delete/', admin_views.admin_delete_bill, name='admin_delete_bill'),

    # Users
    path('admin-panel/users/', admin_views.admin_users, name='admin_users'),
    path('admin-panel/users/create/', admin_views.admin_create_user, name='admin_create_user'),
    path('admin-panel/users/<int:user_id>/edit/', admin_views.admin_edit_user, name='admin_edit_user'),
    path('admin-panel/users/<int:user_id>/delete/', admin_views.admin_delete_user, name='admin_delete_user'),

    # Genres (The Loai)
    path('admin-panel/genres/', admin_views.admin_genres, name='admin_genres'),
    path('admin-panel/genres/create/', admin_views.admin_create_genre, name='admin_create_genre'),
    path('admin-panel/genres/<int:genre_id>/edit/', admin_views.admin_edit_genre, name='admin_edit_genre'),
    path('admin-panel/genres/<int:genre_id>/delete/', admin_views.admin_delete_genre, name='admin_delete_genre'),
]
