# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 18:08:25 2021

@author: Mayuko
"""
from django.views import View
from app1.forms.commentForm import CommentUpdateForm
from django.shortcuts import render, redirect
from app1.models.problem import Problem
from app1.models.photo import Photo
from app1.models.comment import Comment
from app1.models.answer import Answer
from app1.models.correct_situation import CorrectSituation
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from app1.forms.photoForm import PhotoRegisterForm


class PhotoRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        form = PhotoRegisterForm()
        
        return render(request, 'photo/register.html', {'form': form, 'answer': answer})
    
    def post(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        form = PhotoRegisterForm(request.POST, request.FILES)
        
        if not form.is_valid():
            
            return render(request, 'photo/register.html', {'form': form, 'answer': answer})
        
        photo = form.save(commit=False)
        photo.answer = answer
        photo.upload_by = request.user
        created_at = timezone.now()
        
        photo.save()
            
        origin_comment = Comment()
        
        origin_comment.comment = form.cleaned_data['comment']
        origin_comment.by = request.user
        origin_comment.answer = answer
        created_at = timezone.now()
        origin_comment.created_at = created_at
        origin_comment.updated_at = created_at
        origin_comment.origin_photo = photo
        
        origin_comment.save()
        
        messages.success(request, '写真の登録が完了しました')
        return redirect('app1:answer_show', answer_id=answer_id)
    

photo_register_view = PhotoRegisterView.as_view()
