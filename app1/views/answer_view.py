# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 21:35:55 2021

@author: Mayuko
"""


from django.views import View
from app1.forms.answerForm import AnswerRegisterForm, AnswerUpdateForm
from app1.forms.causeTagForm import CauseTagRegisterFormSet, WithForPreviousCauseTagRegisterForm
from app1.forms.withForm import WithForPreviousCauseTagRegisterForm
from django.shortcuts import render, redirect
from app1.models.problem import Problem
from app1.models.photo import Photo
from app1.models.comment import Comment
from app1.models.answer import Answer
from app1.models.cause_tag import CauseTag
from app1.models.with_model import With
from app1.models.latest_with import LatestWith
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from app1.models.cause_tag import CauseTag
from app1.models.with_model import With
from app1.models.latest_with import LatestWith
from app1.models.section import Section


class AnswerRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, *args, **kwargs):
        
        problem = Problem.objects.get(pk=problem_id)
        
        form = AnswerRegisterForm()
        new_cause_tags_formset = CauseTagRegisterFormSet(queryset=CauseTag.objects.none())
        latest_withes = list(LatestWith.objects.filter(site_user__id=request.user.reference_user.id).filter(latest_with__overcome_flag=False).filter(problem__id=problem_id).order_by('-id').values())
        print(latest_withes)
        latest_withes = list(LatestWith.objects.filter(site_user__id=request.user.reference_user.id).filter(latest_with__overcome_flag=False).filter(problem__id=problem_id).order_by('-id'))
        print(latest_withes)
        with_for_previous_cause_tag_formset = forms.formset_factory(form=WithForPreviousCauseTagRegisterForm, extra=len(latest_withes))
        
       
        return render(request, 'answer/register.html', {'form': form, 'formset': new_cause_tags_formset, 'latest_withes': latest_withes, 'with_for_previous_cause_tag_formset': with_for_previous_cause_tag_formset, 'problem': problem})
    
    def post(self, request, problem_id, *args, **kwargs):
        
        
        form = AnswerRegisterForm(request.POST, request.FILES)
        new_cause_tags_formset = CauseTagRegisterFormSet(request.POST)
        problem = Problem.objects.get(pk=problem_id)
        
        latest_withes = list(LatestWith.objects.filter(site_user__id=request.user.reference_user.id).filter(latest_with__overcome_flag=False).filter(problem__id=problem_id).order_by('-id'))
        
        
        with_for_previous_cause_tag_formset_post = request.POST.copy()
        with_for_previous_cause_tag_formset_post['form-TOTAL_FORMS'] = len(latest_withes)
        with_for_previous_cause_tag_formset = forms.formset_factory(form=WithForPreviousCauseTagRegisterForm, extra=len(latest_withes))
        with_for_previous_cause_tag_formset = with_for_previous_cause_tag_formset(with_for_previous_cause_tag_formset_post)
        
        if not form.is_valid() or not new_cause_tags_formset.is_valid():
        
            
            return render(request, 'answer/register.html', {'form': form, 'formset': new_cause_tags_formset, 'latest_withes': latest_withes, 'with_for_previous_cause_tag_formset': with_for_previous_cause_tag_formset, 'problem': problem})
        
        print(type(form.cleaned_data['solve_plan_date']))
       
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
            
        if form.cleaned_data.get('solve_date') is not None:
            
            if not with_for_previous_cause_tag_formset.is_valid():
                
                print("with_for_previous_cause_tag_formsetは、原因タグに関する新しいwithのovercomeflag用のフォーム")
           
            
            new_withes = []
            for latest_with in latest_withes:
                
                with_model = With()
                with_model.site_user = request.user
                with_model.cause_tag = latest_with.cause_tag
                with_model.latest_with = latest_with
                with_model.answer = answer
                with_model.save()
                
                if latest_with.latest_with.answer.solve_date < answer.solve_date:
                    latest_with.latest_with = with_model
                    latest_with.save()
                
                new_withes.append(with_model)
               
            
            for count, with_for_previous_cause_tag_form in enumerate(with_for_previous_cause_tag_formset):
                
                
                new_withes[-1-count].overcome_flag = with_for_previous_cause_tag_form.cleaned_data['overcome_flag']
                new_withes[-1-count].save()
        
            for form in new_cause_tags_formset:
                
                if form.cleaned_data['content'] is not None:
                    
                    cause_tag = form.cause_tag_exist()
                    
                    if cause_tag is None:
                        
                        cause_tag = form.save(commit=True)
                        
                    
                    try:
                        latest_with = LatestWith.objects.get(problem__id=problem_id, site_user__id=request.user.reference_user.id, cause_tag__id=cause_tag.id)
                            
                    except ObjectDoesNotExist:
                        
                        
                        
                        latest_with = LatestWith()
                        latest_with.problem = problem
                        latest_with.site_user = request.user.reference_user
                        latest_with.cause_tag = cause_tag
                        latest_with.save()
                        
                   
                    if latest_with.latest_with is None or latest_with.latest_with.cause_tag.id not in [latest_with.cause_tag.id for latest_with in latest_withes]:
                        
                        with_model = With()
                        with_model.answer = answer
                        with_model.site_user = request.user
                        with_model.overcome_flag = False
                        with_model.cause_tag = cause_tag
                        with_model.latest_with = latest_with
                        with_model.save()
                        
                        if latest_with.latest_with is None or latest_with.latest_with.answer.solve_date < answer.solve_date:
                            
                            latest_with.latest_with = with_model
                            latest_with.save()
                        
            
            
        messages.success(request, "勉強記録を新規登録しました")  
        
        return redirect('app1:answer_list', problem_id=problem_id)
        
    
answer_register_view = AnswerRegisterView.as_view()


class AnswerUpdateView(LoginRequiredMixin, View):
    
    def get(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        form = AnswerUpdateForm(instance=answer)
        
        new_cause_tags_formset = CauseTagRegisterFormSet(queryset=CauseTag.objects.none())
     
        withes = list(With.objects.filter(answer__id=answer_id).filter(overcome_flag=False).order_by('-id'))
        withes_formset = forms.formset_factory(form=WithForPreviousCauseTagRegisterForm, extra=len(withes))
        
        return render(request, 'answer/update.html', {'form': form, 'answer': answer, 'formset': new_cause_tags_formset, 'withes': withes, 'withes_formset': withes_formset})
    
    def post(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        form = AnswerUpdateForm(request.POST, instance=answer)
        
        new_cause_tags_formset = CauseTagRegisterFormSet(request.POST)
        
        withes = list(With.objects.filter(answer__id=answer_id).filter(overcome_flag=False).order_by('-id'))
        withes_formset_post = request.POST.copy()
        withes_formset_post['form-TOTAL_FORMS'] = len(withes)
        withes_formset = forms.formset_factory(form=WithForPreviousCauseTagRegisterForm, extra=len(withes))
        withes_formset = withes_formset(withes_formset_post)
        
        if not form.is_valid() or not new_cause_tags_formset.is_valid():
            
            return render(request, 'answer/update.html', {'form': form, 'answer': answer, 'formset': new_cause_tags_formset, 'withes': withes, 'withes_formset': withes_formset})
        
        answer = form.save(commit=True)
        if not withes_formset.is_valid():
            
            print("with_for_previous_cause_tag_formsetは、原因タグに関する新しいwithのovercomeflag用のフォーム")
       
        
        if answer.solve_date is not None:
            
            for count, with_form in enumerate(withes_formset):
                
                withes[-1-count].overcome_flag = with_form.cleaned_data['overcome_flag']
                withes[-1-count].save()
                
            for form in new_cause_tags_formset:
                
                if form.cleaned_data['content'] is not None:
                    
                    cause_tag = form.cause_tag_exist()
                    
                    if cause_tag is None:
                        
                        cause_tag = form.save(commit=True)
                        
                    
                    try:
                        latest_with = LatestWith.objects.get(problem__id=answer.problem_id, site_user__id=request.user.reference_user.id, cause_tag__id=cause_tag.id)
                            
                    except ObjectDoesNotExist:
                        
                        latest_with = LatestWith()
                        latest_with.problem = answer.problem
                        latest_with.site_user = request.user.reference_user
                        latest_with.cause_tag = cause_tag
                        latest_with.save()
                        
                    if  latest_with.latest_with is None or latest_with.latest_with.cause_tag.id not in [with_model.cause_tag.id for with_model in withes]:
                        
                        
                       
                        try:
                            same_answer_and_cause_tag_with = With.objects.get(answer__id=answer.id, cause_tag__id=cause_tag.id)
                            with_model = same_answer_and_cause_tag_with
                            
                        except ObjectDoesNotExist:
                            
                            with_model = With()
                            with_model.answer = answer
                            with_model.site_user = request.user
                            with_model.cause_tag = cause_tag
                            with_model.latest_with = latest_with
                            with_model.save()
                            
                        with_model.overcome_flag = False
                        with_model.save()
                        
                        if latest_with.latest_with is None or latest_with.latest_with.answer.solve_date < answer.solve_date:
                            
                            latest_with.latest_with = with_model
                            latest_with.save()
                            
           
            
            
        messages.success(request, '勉強記録を更新しました')
        return redirect('app1:answer_show', answer_id=answer.id)
        

answer_update_view = AnswerUpdateView.as_view()


class AnswerToProblemListView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, *args, **kwargs):
        
        problem = Problem.objects.get(pk=problem_id)
        answers = Answer.objects.filter(problem__id=problem_id).filter(student=request.user.reference_user).order_by('solve_plan_date')
        
        return render(request, 'answer/list.html', {'answers': answers, 'problem': problem})
    
answer_to_problem_list_view = AnswerToProblemListView.as_view()


class AnswerAllListView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        
        answers = Answer.objects.filter(student=request.user.reference_user).order_by('solve_plan_date')
        
        return render(request, 'answer/all_list.html', {'answers': answers})

answer_all_list_view = AnswerAllListView.as_view()


class AnswerShowView(LoginRequiredMixin, View):
    
    def get(self, request, answer_id, *args, **kwargs):
        
        answer = Answer.objects.get(pk=answer_id)
        simple_comments = Comment.objects.filter(origin_photo=None).filter(photo=None).filter(answer__id=answer_id)
        
        withes = With.objects.values('cause_tag').annotate(max_id=Max('id'))
        print(answer.solve_date)
        
        return render(request, 'answer/show.html', {'answer': answer, 'simple_comments': simple_comments})
           
answer_show_view = AnswerShowView.as_view()

class AnswerWithCauseTagList(LoginRequiredMixin, View):

    def get(self, request, problem_id, cause_tag_id, *args, **kwargs):

        answer_list = Answer.objects.select_related('problem').filter(student__id=request.user.reference_user.id).filter(problem__id=problem_id).order_by('-solve_date').values('id', 'solve_date', 'correct_situation__id', 'problem__name', 'problem__problem_group__section__id', 'problem__problem_group__section__number', 'problem__problem_group__section__name')
        cause_tag = CauseTag.objects.get(pk=cause_tag_id)
        for answer in answer_list:
            try:
                with_model = With.objects.get(answer__id=answer['id'], cause_tag__id=cause_tag_id)
                answer['overcome_flag'] = with_model.overcome_flag

            except ObjectDoesNotExist:
                answer['overcome_flag'] = -1

        return render(request, 'answer/list_with_overcome.html', {'answer_list': answer_list, 'cause_tag': cause_tag})

answer_list_with_cause_tag_view = AnswerWithCauseTagList.as_view()
