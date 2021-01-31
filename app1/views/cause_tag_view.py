from django.views import View
from app1.forms.answerForm import AnswerRegisterForm, AnswerUpdateForm
from app1.forms.causeTagForm import CauseTagRegisterFormSet, WithForPreviousCauseTagRegisterForm
from app1.forms.withForm import WithForPreviousCauseTagRegisterForm
from django.shortcuts import render, redirect
from app1.models.problem import Problem
from app1.models.chapter import Chapter
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
from django.db.models import Max, Count
from app1.models.section import Section
from django.http import JsonResponse

class NotOvercomeCauseTagList(LoginRequiredMixin, View):

    def get(self, request, section_id, *args, **kwargs):

        queryset = LatestWith.objects.select_related().filter(site_user__id=request.user.reference_user.id).filter(latest_with__overcome_flag=False)
        overcome_queryset = LatestWith.objects.select_related().filter(site_user__id=request.user.reference_user.id).filter(latest_with__overcome_flag=True)
        section = None
        if section_id == 0:
            not_overcome_cause_tags = queryset.values('cause_tag__id', 'cause_tag__cause_type__id', 'cause_tag__content').annotate(total=Count('cause_tag'))
            overcome_cause_tags = overcome_queryset.values('cause_tag__id', 'cause_tag__cause_type__id', 'cause_tag__content').annotate(total=Count('cause_tag'))
        else:
            not_overcome_cause_tags = queryset.filter(problem__problem_group__section__id=section_id).values('cause_tag__id', 'cause_tag__cause_type__id', 'cause_tag__content').annotate(total=Count('cause_tag'))
            overcome_cause_tags = overcome_queryset.filter(problem__problem_group__section__id=section_id).values('cause_tag__id', 'cause_tag__cause_type__id', 'cause_tag__content').annotate(total=Count('cause_tag'))
            section = Section.objects.get(pk=section_id)

        return render(request, 'cause_tag/list.html', {'not_overcome_cause_tags': not_overcome_cause_tags, 'overcome_cause_tags': overcome_cause_tags, 'section': section})


cause_tag_list_view = NotOvercomeCauseTagList.as_view()

class CauseTagGraph(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        chapters = Chapter.objects.all()

        '''
        with_group_by_cause_tag_and_section = With.objects.select_related().filter(answer__student__id=request.user.reference_user.id).filter(latest_with__latest_with__overcome_flag=False).values('answer__problem__problem_group__section__id', 'cause_tag__cause_type__id').annotate(total=Count('cause_tag__cause_type__id'))
       
        sections = Section.objects.all().values()
        with_group_by_cause_tags = []
        
        for section in sections:
           
            cause_tag_by_section_dict = {str(d['cause_tag__cause_type__id']):d['total'] for d in with_group_by_cause_tag_and_section if d['answer__problem__problem_group__section__id'] == section['id']}
            print(cause_tag_by_section_dict)
            cause_tag_by_section_list = []
            for type_id in range(1, 4):
                total = cause_tag_by_section_dict.get(str(type_id))
                if total is None:
                    cause_tag_by_section_list.append(0)
                else:
                    cause_tag_by_section_list.append(total)
                
            print(cause_tag_by_section_list)
            with_group_by_cause_tags.extend(cause_tag_by_section_list)

        print(with_group_by_cause_tags)
        '''
        '''
        withes_group_by_cause_tag_type = With.objects.select_related().filter(answer__student__id=request.user.reference_user.id).filter(latest_with__latest_with__overcome_flag=False).filter(answer__problem__problem_group__section__id=section_id).values('cause_tag__cause_type__id').annotate(total=Count('cause_tag__cause_type__id'))
        withes_group_by_cause_tag_type_dict = {str(d['cause_tag__cause_type__id']):d['total'] for d in withes_group_by_cause_tag_type}
        print(withes_group_by_cause_tag_type_dict)
        withes_group_by_cause_tag_type_list = []
        for type_id in range(1, 4):
                total = withes_group_by_cause_tag_type_dict.get(str(type_id))
                if total is None:
                    withes_group_by_cause_tag_type_list.append(0)
                else:
                    withes_group_by_cause_tag_type_list.append(total)
        #overcome_withes = With.objects.select_related().filter(answer__student__id=request.user.reference_user.id).filter(latest_with__latest_with__overcome_flag=True).filter(answer__problem__problem_group__section__id=section_id).count()
        print(withes_group_by_cause_tag_type_list)
        
        sections = Section.objects.filter(chapter__id=chapter_id).values()
        withes_tag_count = {}
        for type_id in range(1, 4):
            withes_tag_count_by_type_id = []
            withes_by_section = With.objects.select_related().filter(answer__student__id=request.user.reference_user.id).filter(latest_with__latest_with__overcome_flag=False).filter(answer__problem__problem_group__section__chapter__id=chapter_id).filter(cause_tag__cause_type__id=type_id).values('answer__problem__problem_group__section__id').annotate(total=Count('answer__problem__problem_group__section__id'))
            withes_by_section_dict = {str(d['answer__problem__problem_group__section__id']):d['total'] for d in withes_by_section}
           
            for section in sections:
                if withes_by_section_dict.get(str(section['id'])) is None:
                    withes_tag_count_by_type_id.append(0)
                else:
                    withes_tag_count_by_type_id.append(withes_by_section_dict.get(str(section['id'])))
            
            withes_tag_count[type_id] = withes_tag_count_by_type_id
        '''
        return render(request, 'cause_tag/answer_with_cause_tag_graph.html', {'chapters': chapters})
       

cause_tag_graph = CauseTagGraph.as_view()

class WithesCount(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        chapter_id = request.GET['chapter_id']
        sections = Section.objects.filter(chapter__id=chapter_id).values()
        withes_tag_count = {}
        for type_id in range(1, 4):
            withes_tag_count_by_type_id = []
            withes_by_section = With.objects.select_related().filter(answer__student__id=request.user.reference_user.id).filter(latest_with__latest_with__overcome_flag=False).filter(answer__problem__problem_group__section__chapter__id=chapter_id).filter(cause_tag__cause_type__id=type_id).values('answer__problem__problem_group__section__id').annotate(total=Count('answer__problem__problem_group__section__id'))
            withes_by_section_dict = {str(d['answer__problem__problem_group__section__id']):d['total'] for d in withes_by_section}
           
            for section in sections:
                if withes_by_section_dict.get(str(section['id'])) is None:
                    withes_tag_count_by_type_id.append(0)
                else:
                    withes_tag_count_by_type_id.append(withes_by_section_dict.get(str(section['id'])))
            
            withes_tag_count[type_id] = withes_tag_count_by_type_id
        print(sections.count())
        sections_id = [section['id'] for section in sections]
        print(sections_id)
        sections_name = ['§'+str(section['number'])+section['name'] for section in sections]
        return JsonResponse({'withes_dict': withes_tag_count, 'sections_name': sections_name, 'sections_id': sections_id})
       

withes_count = WithesCount.as_view()

