from django.views import View
from app1.models.problem_group import Problem_group
from app1.models.problem import Problem
from app1.models.subject import Subject
from app1.models.by import By
from app1.models.by_comment import ByComment
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from app1.forms.problemForm import SearchForm
from app1.forms.byCommentForm import ByCommentUpdateForm
from django.db.models import Count
from app1.models.evaluation_tag import EvaluationTag
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from config.settings.base import EVALUATION_TAG_AGREE, EVALUATION_TAG_DISAGREE, EVALUATION_TAG_NO_OPINION
from django.utils import timezone


class ByCommentUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, by_comment_id, *args, **kwargs):
        
        by_comment = ByComment.objects.get(pk=by_comment_id)
        form = ByCommentUpdateForm(instance=by_comment)
        
        return render(request, 'by_comment/update.html', {'form': form, 'by_comment': by_comment})
    
    def post(self, request, by_comment_id, *args, **kwargs):
        
        by_comment = ByComment.objects.get(pk=by_comment_id)
        form = ByCommentUpdateForm(request.POST, instance=by_comment)
        
        if not form.is_valid():
            
            return render(request, 'by_comment/update.html', {'form': form, 'by_comment': by_comment})
        
        new_by_comment = form.save(commit=False)
        new_by_comment.updated_at = timezone.now()
        
        new_by_comment.save()
        
        messages.success(request, 'コメント内容を更新しました')
        
        return redirect('app1:by_comment_list', problem_id=by_comment.by.problem.id, evaluation_tag_id=by_comment.by.evaluation_tag.id, evaluation_tag_content=by_comment.by.evaluation_tag.content, evaluation_tag_type=by_comment.by.evaluation_tag.evaluation_type.id)
    
    
by_comment_update_view = ByCommentUpdateView.as_view()


class ByCommentDeleteView(LoginRequiredMixin, View):
    
    def post(self, request, by_comment_id, *args, **kwargs):
        
        by_comment = ByComment.objects.get(pk=by_comment_id)
        problem_id = by_comment.by.problem.id
        evaluation_tag_id = by_comment.by.evaluation_tag.id
        evaluation_tag_content = by_comment.by.evaluation_tag.content
        evaluation_tag_type = by_comment.by.evaluation_tag.evaluation_type.id
        by_comment.delete()
        
        messages.success(request, 'コメントを削除しました')
        
        return redirect('app1:by_comment_list', problem_id=problem_id, evaluation_tag_id=evaluation_tag_id, evaluation_tag_content=evaluation_tag_content, evaluation_tag_type=evaluation_tag_type)

by_comment_delete_view = ByCommentDeleteView.as_view()

class ByCommentRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, evaluation_tag_id, evaluation_tag_content, evaluation_tag_type, *args, **kwargs):
        
        form = ByCommentUpdateForm()
        
        problem = Problem.objects.get(pk=problem_id)
        
        context = {
            'problem': problem,
            'evaluation_tag_id': evaluation_tag_id,
            'evaluation_tag_content': evaluation_tag_content,
            'evaluation_tag_type': evaluation_tag_type,
            'form': form,
            }
        
        
        
        return render(request, 'by_comment/register.html', context)
    
    def post(self, request, problem_id, evaluation_tag_id, evaluation_tag_content, evaluation_tag_type, *args, **kwargs):
        
        problem = Problem.objects.get(pk=problem_id)
        form = ByCommentUpdateForm(request.POST)
        
        
        
        if not form.is_valid():
            context = {
            'problem': problem,
            'evaluation_tag_id': evaluation_tag_id,
            'evaluation_tag_content': evaluation_tag_content,
            'evaluation_tag_type': evaluation_tag_type,
            'form': form,
            }
            
            return render(request, 'by_comment/register.html', context)
        
        by_comment = form.save(commit=False)
        my_by = By.objects.get(problem__id=problem_id, evaluation_tag__id=evaluation_tag_id, site_user__id=request.user.id)
        by_comment.by = my_by
        by_comment.created_at = timezone.now()
        by_comment.updated_at = by_comment.created_at
        
        by_comment.save()
        
        messages.success(request, 'コメントを作成しました')
        
        return redirect('app1:by_comment_list', problem_id=problem_id, evaluation_tag_id=evaluation_tag_id, evaluation_tag_content=evaluation_tag_content, evaluation_tag_type=evaluation_tag_type)
    
by_comment_register_view = ByCommentRegisterView.as_view()