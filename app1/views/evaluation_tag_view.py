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
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class EvaluationTagRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, *args, **kwargs):
        
        problem = Problem.objects.get(pk=problem_id)
        
        context = {'form': EvaluationTagRegisterForm(), 'problem': problem}
        
        return render(request, 'evaluation_tag/register.html', context)
    
    
    def post(self, request, problem_id, *args, **kwargs):
        
        form = EvaluationTagRegisterForm(request.POST)
        problem = Problem.objects.get(pk=problem_id)
        
        if not form.is_valid():
            
            return render(request, 'evaluation_tag/register.html', {'form': form, 'problem': problem})
    
        print('cc:'+form.cleaned_data['content'])
        evaluation_tag = form.evaluation_tag_exist()
        
        if evaluation_tag is None:
          
            evaluation_tag = form.save(commit=True)
            
        by = By()
        by.evaluation_tag = evaluation_tag
        by.site_user = request.user
        by.problem = problem
        
        by.save()
        
        messages.success(request, '評価タグを登録しました')
          
        return redirect('app1:problem_show', problem_id=problem.id)
        

evaluation_tag_register_view = EvaluationTagRegisterView.as_view() 