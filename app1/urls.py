
"""
Created on Sat Dec 19 13:50:53 2020

@author: Mayuko
"""


from django.urls import path
from . import views


app_name = 'app1'

urlpatterns = [
    
    path('', views.chapter_view.chapter_list, name='chapter_list'),
    path('siteUser/register', views.siteUser_view.siteUser_register, name='siteUser_register'),
    path('siteUser/logout', views.siteUser_view.siteUser_logout, name='siteUser_logout'),
    path('siteUser/login', views.siteUser_view.siteUser_login, name='siteUser_login'),
    path('siteUser/reference_user/login', views.siteUser_view.reference_user_login_view, name='reference_user_login'),
    path('siteUser/reference_user/logout', views.siteUser_view.reference_user_logout_view, name='reference_user_logout'),
    path('chapter/list', views.chapter_view.chapter_list, name='chapter_list'),
    path('section/list/<int:chapter_id>/', views.section_view.section_list_view, name='section_list'),
    path('problem_group/list/<int:section_id>/', views.problem_group_view.problem_group_list_view, name='problem_group_list'),
    path('problem/list/<int:problem_group_id>/', views.problem_view.problem_list_view, name='problem_list'),
    path('problem/search', views.problem_view.problem_search_view, name='problem_search'),
    path('problem/show/<int:problem_id>/', views.problem_view.problem_show_view, name='problem_show'),
    path('problem/problem_list_with_cause_tag/<int:cause_tag_id>/<int:section_id>/', views.problem_view.problem_list_with_cause_tag_view, name='problem_list_with_cause_tag'),
    path('answer/register/<int:problem_id>/', views.answer_view.answer_register_view, name='answer_register'),
    path('answer/update/<int:answer_id>/', views.answer_view.answer_update_view, name='answer_update'),
    path('answer/list/<int:problem_id>/', views.answer_view.answer_to_problem_list_view, name='answer_list'),
    path('ansewr/list_with_overcome/<int:problem_id>/<int:cause_tag_id>/', views.answer_view.answer_list_with_cause_tag_view, name='answer_list_with_cause_tag'),
    path('answer/all_list/', views.answer_view.answer_all_list_view, name='answer_all_list'),
    path('answer/show/<int:answer_id>/', views.answer_view.answer_show_view, name='answer_show'),
    path('comment/simple_comment/register/<int:answer_id>/', views.comment_view.simple_comment_register_view, name='simple_comment_register'),
    path('comment/reply_comment/register/<int:photo_id>', views.comment_view.reply_comment_register_view, name='reply_comment_register'),
    path('comment/simple_comment/update/<int:simple_comment_id>/', views.comment_view.simple_comment_update_view, name='simple_comment_update'),
    path('comment/origin_comment/update/<int:origin_comment_id>/', views.comment_view.origin_comment_update_view, name='origin_comment_update'),
    path('comment/reply_comment/update/<int:reply_comment_id>/', views.comment_view.reply_comment_update_view, name='reply_comment_update'),
    path('comment/simple_comment/delete/<int:simple_comment_id>/', views.comment_view.simple_comment_delete_view, name='simple_comment_delete'),
    path('comment/origin_comment/delete/<int:origin_comment_id>/', views.comment_view.origin_comment_and_photo_delete_view, name='origin_comment_and_photo_delete'),
    path('comment/reply_comment/delete/<int:reply_comment_id>/', views.comment_view.reply_comment_delete_view, name='reply_comment_delete'),
    path('photo/register/<int:answer_id>/', views.photo_view.photo_register_view, name='photo_register'),
    path('evaluation/register/<int:problem_id>/', views.evaluation_tag_view.evaluation_tag_register_view, name='evaluation_tag_register'),
    path('evaluation/suggest/', views.evaluation_tag_view.evaluation_tag_suggest_view, name='evaluation_tag_suggest'),
    path('evaluation/release/<int:problem_id>/<int:evaluation_tag_id>/', views.evaluation_tag_view.evaluation_tag_release_view, name='evaluation_tag_release'), 
    path('evaluation/search/', views.evaluation_tag_view.evaluation_tag_search_view, name='evaluation_tag_search'),
    path('by/register/<int:problem_id>/<int:evaluation_tag_id>/<str:evaluation_tag_content>/<int:evaluation_tag_type>/<int:my_by_status>/<int:good_flag>/', views.by_view.by_register_view, name='by_register'),
    path('by/comment_list/<int:problem_id>/<int:evaluation_tag_id>/<str:evaluation_tag_content>/<int:evaluation_tag_type>/', views.by_view.by_comment_list_view, name='by_comment_list'),
    path('by_comment/update/<int:by_comment_id>/', views.by_comment_view.by_comment_update_view, name='by_comment_update'),
    path('by_comment/delete/<int:by_comment_id>/', views.by_comment_view.by_comment_delete_view, name='by_comment_delete'),
    path('by/comment_register/<int:problem_id>/<int:evaluation_tag_id>/<str:evaluation_tag_content>/<int:evaluation_tag_type>/', views.by_comment_view.by_comment_register_view, name='by_comment_register'),
    path('cause_tag/list/<int:section_id>/', views.cause_tag_view.cause_tag_list_view, name='cause_tag_list'),
    path('cause_tag/graph/', views.cause_tag_view.cause_tag_graph, name='cause_tag_graph'),
    path('cause_tag/withes_count/', views.cause_tag_view.withes_count, name='withes_count'),
    
]