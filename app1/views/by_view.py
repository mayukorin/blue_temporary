from django.views import View
from app1.models.problem_group import Problem_group
from app1.models.problem import Problem
from app1.models.subject import Subject
from app1.models.by import By
from app1.models.by_comment import ByComment
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from app1.models.evaluation_tag import EvaluationTag
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from config.settings.base import EVALUATION_TAG_AGREE, EVALUATION_TAG_DISAGREE, EVALUATION_TAG_NO_OPINION
#from app1.forms.ByForm import ByCommentRegisterForm

class ByRegisterView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, evaluation_tag_id, evaluation_tag_content, evaluation_tag_type, my_by_status, good_flag, *args, **kwargs):
        
        if my_by_status == EVALUATION_TAG_NO_OPINION:
            by = By()
            evaluation_tag = EvaluationTag.objects.get(pk=evaluation_tag_id)
            problem = Problem.objects.get(pk=problem_id)
            by.evaluation_tag = evaluation_tag
            by.site_user = request.user
            by.problem = problem
            by.good_flag = (good_flag == 1)
            
            by.save()
            
        else:
            my_by = By.objects.get(problem__id=problem_id, evaluation_tag__id=evaluation_tag_id, site_user__id=request.user.id)
            my_by.good_flag = (good_flag == 1)
            my_by.save()
        
        
        
        return redirect('app1:by_comment_list', problem_id=problem_id, evaluation_tag_id=evaluation_tag_id, evaluation_tag_content=evaluation_tag_content, evaluation_tag_type=evaluation_tag_type)
        
by_register_view = ByRegisterView.as_view()

class ByCommentListView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, evaluation_tag_id, evaluation_tag_content, evaluation_tag_type, *args, **kwargs):
        
        good_byes_count =  By.objects.filter(problem__id=problem_id).filter(evaluation_tag__id=evaluation_tag_id).filter(good_flag=True).count()
        bad_byes_count = By.objects.filter(problem__id=problem_id).filter(evaluation_tag__id=evaluation_tag_id).filter(good_flag=False).count()
        problem = Problem.objects.get(pk=problem_id)
        
        try:
                site_user_by = By.objects.get(problem__id=problem_id, evaluation_tag__id=evaluation_tag_id, site_user__id=request.user.id)
                
                if site_user_by.good_flag is True:
                
                    my_by_status = EVALUATION_TAG_AGREE
                        
                else:
                    my_by_status = EVALUATION_TAG_DISAGREE
                
        except ObjectDoesNotExist:
            
            my_by_status = EVALUATION_TAG_NO_OPINION
            
        
        by_comments = ByComment.objects.filter(by__evaluation_tag__id=evaluation_tag_id).filter(by__problem__id=problem_id)
        
        context = {
            'problem': problem,
            'evaluation_tag_id': evaluation_tag_id,
            'evaluation_tag_content': evaluation_tag_content,
            'evaluation_tag_type': evaluation_tag_type,
            'good_byes_count': good_byes_count,
            'bad_byes_count': bad_byes_count,
            'my_by_status': my_by_status,
            'by_comments': by_comments,
            }
        return render(request, 'by/comment_list.html', context)
       
        
        
by_comment_list_view = ByCommentListView.as_view()