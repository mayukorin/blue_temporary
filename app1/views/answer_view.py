# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:35:55 2021

@author: Mayuko
"""


from django.views import View
from app1.forms.answerForm import AnswerRegisterForm, AnswerUpdateForm
from django.shortcuts import render, redirect
from app1.models.problem import Problem
from app1.models.photo import Photo
from app1.models.comment import Comment
from app1.models.answer import Answer
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class AnswerRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, *args, **kwargs):
        
        form = AnswerRegisterForm()
        problem = Problem.objects.get(pk=problem_id)
       
        return render(request, 'answer/register.html', {'form': form, 'problem': problem})
    
    def post(self, request, problem_id, *args, **kwargs):
        
        form = AnswerRegisterForm(request.POST, request.FILES)
        
        if not form.is_valid():
            
            return render(request, 'answer/register.html', {'form': form, 'problem_id': problem_id})
        
        problem = Problem.objects.get(pk=problem_id)
        answer = form.save(commit=False)
        answer.problem = problem
        answer.student = request.user.reference_user
        answer.save()
        
        photo = None
       
        if form.cleaned_data['photo'] is not None:
            
            photo = Photo()
            
            photo.image = form.cleaned_data['photo']
            photo.answer = answer
            photo.upload_by = request.user
            photo.save()
            
        if form.cleaned_data['comment'] != "" or form.cleaned_data['photo'] is not None:
            
            comment = Comment()
            
            comment.comment = form.cleaned_data['comment']
            comment.by = request.user
            comment.answer = answer
            current_time = timezone.now()
            comment.created_at = current_time
            comment.updated_at = current_time
            comment.origin_photo = photo
            
            comment.save()
            
        messages.success(request, "勉強記録を新規登録しました")     
        return redirect('app1:answer_list', problem_id=problem_id)
        
    
answer_register_view = AnswerRegisterView.as_view()


class AnswerUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        form = AnswerUpdateForm(instance=answer)
        
        return render(request, 'answer/update.html', {'form': form, 'answer': answer})
    
    def post(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        form = AnswerUpdateForm(request.POST, instance=answer)
        
        if not form.is_valid():
            
            return render(request, 'answer/update.html', {'form': form, 'answer': answer})
        
        form.save(commit=True)
        messages.success(request, '勉強記録を更新しました')
        return redirect('app1:answer_show', answer_id=answer.id)
        

answer_update_view = AnswerUpdateView.as_view()


class AnswerListView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, *args, **kwargs):
        
        problem = Problem.objects.get(pk=problem_id)
        answers = Answer.objects.filter(problem__id=problem_id).filter(student=request.user.reference_user).order_by('solve_plan_date')
        
        return render(request, 'answer/list.html', {'answers': answers, 'problem': problem})
    
answer_list_view = AnswerListView.as_view()


class AnswerShowView(LoginRequiredMixin, View):
    
    def get(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        row_comments = Comment.objects.filter(origin_photo=None).filter(photo=None).filter(answer__student=request.user.reference_user)
       
        return render(request, 'answer/show.html', {'answer': answer, 'row_comments': row_comments})
    
answer_show_view = AnswerShowView.as_view()