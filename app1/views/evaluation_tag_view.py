# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 16:19:44 2021

@author: Mayuko
"""


from django.views import View
from app1.forms.evaluationTagForm import EvaluationTagRegisterForm
from django.shortcuts import render, redirect
from app1.models.problem import Problem
from app1.models.photo import Photo
from app1.models.comment import Comment
from app1.models.answer import Answer
from app1.models.by import By
from app1.models.by_comment import ByComment
from app1.models.evaluation_tag import EvaluationTag
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone


class EvaluationTagRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, *args, **kwargs):
        
        problem = Problem.objects.get(pk=problem_id)
        
        context = {'form': EvaluationTagRegisterForm(request.user.id, problem_id), 'problem': problem}
        
        return render(request, 'evaluation_tag/register.html', context)
    
    
    def post(self, request, problem_id, *args, **kwargs):
        
        form = EvaluationTagRegisterForm(request.user.id, problem_id, request.POST)
        problem = Problem.objects.get(pk=problem_id)
        
        if not form.is_valid():
            
            return render(request, 'evaluation_tag/register.html', {'form': form, 'problem': problem})

        evaluation_tag = form.evaluation_tag_exist()
        
        if evaluation_tag is None:
          
            evaluation_tag = form.save(commit=True)
            
        by = By()
        by.evaluation_tag = evaluation_tag
        by.site_user = request.user
        by.problem = problem
        by.good_flag = True
        by.save()
        if form.cleaned_data['comment'] != '':
            by_comment = ByComment()
            by_comment.content = form.cleaned_data['comment']
            by_comment.by = by
            by_comment.created_at = timezone.now()
            by_comment.updated_at =by_comment.created_at
            
            by_comment.save()
        
       
        
        messages.success(request, '評価タグを登録しました')
          
        return redirect('app1:problem_show', problem_id=problem.id)
        

evaluation_tag_register_view = EvaluationTagRegisterView.as_view() 


class EvaluationTagSuggestView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        
        keyword = request.GET.get('keyword')
    
        if keyword:
            
            evaluation_tag_list = [{'pk': ev.pk, 'content': ev.content, 'type_id': ev.evaluation_type.id } for ev in EvaluationTag.objects.filter(content__icontains=keyword)]
            
        else:
            
            evaluation_tag_list = []
        
        
        return JsonResponse({'object_list': evaluation_tag_list})


evaluation_tag_suggest_view = EvaluationTagSuggestView.as_view()


class EvaluationTagReleaseView(LoginRequiredMixin, View):
    
    def post(self, request, problem_id, evaluation_tag_id, *args, **kwargs):
        
        
        all_by_count = By.objects.filter(evaluation_tag__id=evaluation_tag_id).count()
        
        if all_by_count != 1:
            
            my_by = By.objects.get(problem__id=problem_id, evaluation_tag__id=evaluation_tag_id, site_user__id=request.user.id)
            my_by.delete()
            
        else:
            evaluation_tag = EvaluationTag.objects.get(pk=evaluation_tag_id)
            evaluation_tag.delete()
            
        messages.success(request, '自分の評価タグを解除しました')
        
        return redirect('app1:problem_show', problem_id=problem_id)
        

evaluation_tag_release_view = EvaluationTagReleaseView.as_view()
        