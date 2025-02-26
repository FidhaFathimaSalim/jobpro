from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    link = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Profile(models.Model):
    # Profile
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(max_length=2000)

    # Education
    # School
    school = models.CharField(max_length=200)
    school_gpa = models.FloatField(blank=True, null=True)
    school_joined_year = models.CharField(max_length=5, blank=True, null=True)
    school_left_year = models.CharField(max_length=5, blank=True, null=True)
    # College
    college = models.CharField(max_length=200)
    college_gpa = models.FloatField(blank=True, null=True)
    stream = models.CharField(max_length=20, choices=[('Science', 'Science'), ('Management', 'Management'), ('Humanities', 'Humanities')])
    college_joined_year = models.CharField(max_length=5, blank=True, null=True)
    college_left_year = models.CharField(max_length=5, blank=True, null=True)
    # University
    university = models.CharField(max_length=200)
    university_gpa = models.FloatField(blank=True, null=True)
    university_faculty = models.CharField(max_length=200)
    university_joined_year = models.CharField(max_length=5, blank=True, null=True)
    university_left_year = models.CharField(max_length=5, blank=True, null=True)

    # Projects
    projects = models.ManyToManyField(Project, blank=True)

    # Skills
    technical_skills = models.CharField(max_length=2000, blank=True, null=True)
    nontechnical_skills = models.CharField(max_length=2000, blank=True, null=True)

    # Languages
    languages = models.ManyToManyField(Language, blank=True)

    # Reference
    reference_name = models.CharField(max_length=200, blank=True, null=True)
    reference_position = models.CharField(max_length=200, blank=True, null=True)
    reference_organization = models.CharField(max_length=200, blank=True, null=True)
    reference_email = models.EmailField(max_length=200, blank=True, null=True)
    reference_phone = models.CharField(max_length=15, blank=True, null=True)

    # Time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name