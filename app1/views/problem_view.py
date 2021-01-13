from django.views import View
from app1.models.problem_group import Problem_group
from app1.models.problem import Problem
from app1.models.subject import Subject
from app1.models.by import By
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from app1.forms.problemForm import SearchForm
from django.db.models import Count


class ProblemListView(LoginRequiredMixin, View):
    
    def get(self, request, problem_group_id, *args, **kwargs):
        
        problems = Problem.objects.filter(problem_group__id=problem_group_id)
        problem_group = Problem_group.objects.get(pk=problem_group_id)
        
        return render(request, 'problem/list.html', {'problems': problems, 'problem_group': problem_group})


problem_list_view = ProblemListView.as_view()


class ProblemSearchView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        
        context = {'form': SearchForm()}
        
        return render(request, 'problem/search.html', context)
    
    def post(self, request, *args, **kwargs):
        
        form = SearchForm(request.POST)
        
        if not form.is_valid():
            return render(request, 'problem/search.html', {'form': form})
        
        subject_id = form.cleaned_data['subject']
        from_page = form.cleaned_data['from_page']
        to_page = form.cleaned_data['to_page']
        from_problem_number = form.cleaned_data['from_problem_number']
        to_problem_number = form.cleaned_data['to_problem_number']
        exercise_flag = form.cleaned_data['exercise_flag']
        difficulty = form.cleaned_data['difficulty']
        
        queryset = Problem.objects.all()
        
        subject = None
        
        if subject_id != '0':
            
            queryset = queryset.filter(problem_group__section__chapter__subject__id=subject_id)
            subject = Subject.objects.get(pk=subject_id)
            
        if from_page is not None and to_page is not None:
            
            true_from_page = min(from_page, to_page)
            
            true_to_page = max(from_page, to_page)
            
            queryset = queryset.filter(page__gte=true_from_page).filter(page__lte=true_to_page)
            
        elif from_page is not None:
            
            queryset = queryset.filter(page__gte=from_page)
            
        elif to_page is not None:
            
            queryset = queryset.filter(page__lte=to_page)
            
        if exercise_flag:
            
            queryset = queryset.filter(problem_group__name='EXERCISE')
        
        else:
            
            if from_problem_number is not None and to_problem_number is not None:
            
                true_from_problem_number = min(from_problem_number, to_problem_number)
                
                true_to_problem_number = max(from_problem_number, to_problem_number)
                
                queryset = queryset.filter(problem_group__number__gte=true_from_problem_number).filter(problem_group__number__lte=true_to_problem_number)
            
            elif from_problem_number is not None:
                
                queryset = queryset.filter(problem_group__number__gte=from_problem_number)
                
            elif to_problem_number is not None:
                
                queryset = queryset.filter(problem_group__number__lte=to_problem_number)
                
        if difficulty != '0':
            
            queryset = queryset.filter(difficulty=difficulty)
        
        problems = queryset
        
        return render(request, 'problem/result.html', {'problems': problems, 'subject': subject, 'from_page': from_page, 'to_page': to_page, 'from_problem_number': from_problem_number, 'to_problem_number': to_problem_number, 'exercise_flag': exercise_flag, 'difficulty': difficulty})

problem_search_view = ProblemSearchView.as_view()


class ProblemShowView(LoginRequiredMixin, View):
    
    def get(self, request, problem_id, *args, **kwargs):
        
        problem = Problem.objects.get(pk=problem_id)
        evaluations = By.objects.select_related().filter(problem=problem).values('evaluation_tag', 'evaluation_tag__content', 'evaluation_tag__evaluation_type__id').annotate(total=Count('evaluation_tag'))
        print(evaluations)
        return render(request, 'problem/show.html', {'problem': problem, 'evaluations': evaluations})
    
    
problem_show_view = ProblemShowView.as_view()