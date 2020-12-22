# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 13:27:13 2020

@author: Mayuko
"""
from django.views import View
from app1.models.chapter import Chapter,Subject
from django.shortcuts import render
from django.db import connection
from django.db.models import Count

class ChapterListView(View):
    
    def get(self,request,*args,**kwargs):
        
        chapters = Chapter.objects.all()
        subjects = Subject.objects.all()
        
        with connection.cursor() as cursor:
            
            cursor.execute("select s.*,group_concat(c.name) from app1_subject as s left join app1_chapter as c on s.id = c.subject_id group by s.id")
            chap = cursor.fetchall()
            chap2 = list(cursor.fetchall())
            
            tup = ((1,2,3),(2,3,4),(3,4,5))
            #print(list(tup))
        #for c in chap2:
            #print(c)
        for c in chap:
            
            if c[2] != None:
                cc = tuple(c[2].split(','))
                
                c += cc
            #print(c)
        #print(chap)
        
        group_by_chapters = Chapter.objects.select_related().values('subject__name').annotate(total=Count('subject'))
        print(group_by_chapters)
        
        return render(request,'chapter/chapter_list.html',{'chapters':chapters,'chap':chap,'subjects':subjects,'names':group_by_chapters})
    
    
    
    
    
chapter_list = ChapterListView.as_view()