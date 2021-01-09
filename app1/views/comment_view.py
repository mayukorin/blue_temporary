# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 12:39:35 2021

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
import os


class SimpleCommentRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        form = CommentUpdateForm()
        
        return render(request, 'comment/simple_comment/register.html', {'form': form, 'answer': answer})
    
    def post(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        form = CommentUpdateForm(request.POST)
        
        if not form.is_valid():
            
            return render(request, {'form': form, 'answer': answer})
        
        simple_comment = form.save(commit=False)
        simple_comment.created_at = timezone.now()
        simple_comment.updated_at = timezone.now()
        simple_comment.by = request.user
        simple_comment.answer = answer
        
        simple_comment.save()
        messages.success(request, 'コメントを投稿しました')
        
        return redirect('app1:answer_show', answer_id=answer_id)
    

simple_comment_register_view = SimpleCommentRegisterView.as_view()


class SimpleCommentUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, simple_comment_id, *args, **kwargs):
        
        simple_comment = Comment.objects.get(pk=simple_comment_id)
        
        form = CommentUpdateForm(instance=simple_comment)
        
        return render(request, 'comment/simple_comment/update.html', {'form': form, 'simple_comment': simple_comment})
    
    def post(self, request, simple_comment_id, *args, **kwargs):
        
        simple_comment = Comment.objects.get(pk=simple_comment_id)
        form = CommentUpdateForm(request.POST, instance=simple_comment)
        
        if not form.is_valid():
            
            return render(request, 'comment/simple_comment/update.html', {'form': form, 'simple_comment': simple_comment})
    
        simple_comment = form.save(commit=False)
        simple_comment.updated_at = timezone.now()
        simple_comment.save()
        
        messages.success(request, 'コメントの編集が完了しました')
        
        return redirect('app1:answer_show', answer_id=simple_comment.answer.id)
    
simple_comment_update_view = SimpleCommentUpdateView.as_view()


class SimpleCommentDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, simple_comment_id, *args, **kwargs):
        
        simple_comment = Comment.objects.get(pk=simple_comment_id)
        answer_id = simple_comment.answer.id
        simple_comment.delete()
        
        messages.success(request, 'コメントと写真を削除しました')
        
        return redirect('app1:answer_show', answer_id=answer_id)
  
    
simple_comment_delete_view = SimpleCommentDeleteView.as_view()


class OriginCommentUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, origin_comment_id, *args, **kwargs):
        
        origin_comment = Comment.objects.get(pk=origin_comment_id)
        
        form = CommentUpdateForm(instance=origin_comment)
        
        return render(request, 'comment/origin_comment/update.html', {'form': form, 'origin_comment': origin_comment})
    
    def post(self, request, origin_comment_id, *args, **kwargs):
        
        origin_comment = Comment.objects.get(pk=origin_comment_id)
        form = CommentUpdateForm(request.POST, instance=origin_comment)
        
        if not form.is_valid():
            
            return render(request, 'comment/origin_comment/update.html', {'form': form, 'origin_comment': origin_comment})
       
        origin_comment = form.save(commit=False)
        origin_comment.updated_at = timezone.now()
        origin_comment.save()
        
        messages.success(request, 'コメントの編集が完了しました')
        
        return redirect('app1:answer_show', answer_id=origin_comment.answer.id)
            
        
origin_comment_update_view = OriginCommentUpdateView.as_view()


class OriginCommentAndPhotoDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, origin_comment_id, *args, **kwargs):
        
        origin_comment = Comment.objects.get(pk=origin_comment_id)
        origin_photo_id = origin_comment.origin_photo.id
        answer_id = origin_comment.answer.id
        origin_comment.delete()
        
        photo = Photo.objects.get(pk=origin_photo_id)

        os.remove(str(photo.image))
        photo.image = ""
        photo.save()
        
        messages.success(request, 'コメントと写真を削除しました')
        
        return redirect('app1:answer_show', answer_id=answer_id)
  
    
origin_comment_and_photo_delete_view = OriginCommentAndPhotoDeleteView.as_view()


class ReplyCommentRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, photo_id, *args, **kwargs):
        
        photo = Photo.objects.get(pk=photo_id)
        form = CommentUpdateForm()
        
        return render(request, 'comment/reply_comment/register.html', {'form': form, 'photo': photo})
    
    def post(self, request, photo_id, *args, **kwargs):
        
        form = CommentUpdateForm(request.POST)
        photo = Photo.objects.get(pk=photo_id)
        
        if not form.is_valid():
            
            return render(request, 'comment/reply_comment/register.html', {'form': form, 'photo': photo})
        
        reply_comment = form.save(commit=False)
        created_at = timezone.now()
        reply_comment.created_at = created_at
        reply_comment.updated_at = created_at
        reply_comment.by = request.user
        reply_comment.answer = photo.answer
        reply_comment.photo = photo
        
        reply_comment.save()
        messages.success(request, 'コメントを追加しました')
        return redirect('app1:answer_show', answer_id=photo.answer.id)
    
reply_comment_register_view = ReplyCommentRegisterView.as_view()


class ReplyCommentUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, reply_comment_id, *args, **kwargs):
        
        reply_comment = Comment.objects.get(pk=reply_comment_id)
        form = CommentUpdateForm(instance=reply_comment)
        
        return render(request, 'comment/reply_comment/update.html', {'form': form, 'reply_comment': reply_comment})
    
    def post(self, request, reply_comment_id, *args, **kwargs):
        
        reply_comment = Comment.objects.get(pk=reply_comment_id)
        form = CommentUpdateForm(request.POST, instance=reply_comment)
        
        if not form.is_valid():
            
            return render(request, 'comment/reply_comment/update.html', {'form': form, 'reply_comment': reply_comment})
        
        reply_comment = form.save(commit=False)
        reply_comment.updated_at = timezone.now()
        
        reply_comment.save()
        messages.success(request, 'コメントの編集が完了しました')
        return redirect('app1:answer_show', answer_id=reply_comment.answer.id)

reply_comment_update_view = ReplyCommentUpdateView.as_view()


class ReplyCommentDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, reply_comment_id, *args, **kwargs):
        
        reply_comment = Comment.objects.get(pk=reply_comment_id)
        answer_id = reply_comment.answer.id
       
        reply_comment.delete()
        messages.success(request, 'コメントを削除しました')
        
        return redirect('app1:answer_show', answer_id=answer_id)
    
reply_comment_delete_view = ReplyCommentDeleteView.as_view()
