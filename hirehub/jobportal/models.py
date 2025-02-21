from django.db import models

# Create your models here.
class Profile(models.Model):
    #Profile
    full_name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    phone=models.CharField(max_length=15)
    address= models.CharField(max_length=200, blank=True, null=True)
    summary=models.TextField(max_length=2000)

    #Education
    #school
    school=models.CharField(max_length=200)
    school_gpa=models.FloatField(blank=True, null=True)
    school_joined_year= models.CharField(max_length=5,blank=True, null=True)
    school_left_year=models.CharField(max_length=5,blank=True, null=True)
    #college
    college=models.CharField(max_length=200)
    college_gpa=models.FloatField(blank=True, null=True)
    stream= models.CharField(max_length=20,choices=[('Science','Science'),('Management','Management'),('Humanities','Humanities')])
    college_joined_year= models.CharField(max_length=5,blank=True, null=True)
    college_left_year= models.CharField(max_length=5,blank=True, null=True)
    #University
    university=models.CharField(max_length=200)
    university_gpa=models.FloatField(blank=True, null=True)
    university_faculty=models.CharField(max_length=200)
    university_joined_year= models.CharField(max_length=5,blank=True, null=True)
    university_left_year= models.CharField(max_length=5,blank=True, null=True)

    # #Experience
    # #current_company
    # current_company=models.CharField(max_length=200,blank=True, null=True)
    # current_position=models.CharField(max_length=200,blank=True, null=True)
    # current_work_description=models.TextField(blank=True, null=True)
    # current_joined_date= models.DateField(blank=True, null=True)
    # #previous_company
    # previous_company=models.CharField(max_length=200,blank=True, null=True)
    # previous_position=models.CharField(max_length=200,blank=True, null=True)
    # previous_work_description=models.TextField(blank=True, null=True)
    # previous_joined_date= models.DateField(blank=True, null=True)
    # previous_left_date=models.DateField(blank=True, null=True)

    #Projects
    project= models.CharField(max_length=100,blank=True, null=True)
    project_description=models.TextField(blank=True, null=True)
    project_link=models.CharField(max_length=100,blank=True, null=True)
    # project_two= models.CharField(max_length=100,blank=True, null=True)
    # project_two_description=models.TextField(blank=True, null=True)
    # project_three= models.CharField(max_length=100,blank=True, null=True)
    # project_three_description=models.TextField(blank=True, null=True)

    #skills
    technical_skills=models.CharField(max_length=2000,blank=True, null=True)
    nontechnical_skills=models.CharField(max_length=2000,blank=True, null=True)

    #language
    language= models.CharField(max_length=2000,blank=True, null=True)

    #reference
    reference_name= models.CharField(max_length=200,blank=True, null=True)
    reference_position= models.CharField(max_length=200,blank=True, null=True)
    reference_organization= models.CharField(max_length=200,blank=True, null=True)
    reference_email=models.EmailField(max_length=200, blank=True, null=True)
    reference_phone=models.CharField(max_length=15,blank=True, null=True)

    #time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.full_name
    
    