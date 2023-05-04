# 
from django.shortcuts import render

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from crm.models import Employee
from rest_framework import serializers
from rest_framework.decorators import action

class EmployeeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Employee
        fields="__all__"

class EmployeesView(ViewSet):
  

    def list(self,request,*args,**kwargs):
        qs=Employee.objects.all()       

        if "department" in request.query_params:
            dept=request.query_params.get("department")
            qs=qs.filter(department=dept)
        
        if "salary" in request.query_params:
            sal=request.query_params.get("salary")
            qs=qs.filter(salary=sal)

        if "salary_gt" in request.query_params:
            sal=request.query_params.get("salary_gt")
            qs=qs.filter(salary__gte=sal)
             

       
        serializer=EmployeeSerializer(qs,many=True)       
      
        return Response(data=serializer.data)
    
    def create(self,request,*args,**kwargs):
        # serialization
        serializer=EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
      
    #localhost:8000/api/employees/3/
    def retrieve(self,request,*args,**kwargs):
      
      id=kwargs.get("pk")
      qs=Employee.objects.get(id=id)
      serializer=EmployeeSerializer(qs)
      return Response(data=serializer.data)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        emp_obj=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(instance=emp_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        # form=EmployeeForm(instance=emp_obj,data=request.POST)
       
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Employee.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")
    
    @action(methods=["get"],detail=False)   
    def all_departments(self,request,*args,**kwargs):
        qs=Employee.objects.all().values_list("department",flat=True).distinct()
        return Response(data=qs)
    
# localhost:8000/products/?category="electronics"
# get


# localhost:8000/api/cakes/falvours/
# get


# localhost:8000/api/cakes/?flavour=chklt

# localhost:8000/api/cakes/?shape=round

