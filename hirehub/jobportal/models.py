from django.db import models

class Profile(models.Model):
    # Profile
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(max_length=2000)

    # Education
    school = models.CharField(max_length=200)
    school_gpa = models.FloatField(blank=True, null=True)
    school_joined_year = models.CharField(max_length=5, blank=True, null=True)
    school_left_year = models.CharField(max_length=5, blank=True, null=True)
    college = models.CharField(max_length=200)
    college_gpa = models.FloatField(blank=True, null=True)
    stream = models.CharField(max_length=20, choices=[('Science', 'Science'), ('Management', 'Management'), ('Humanities', 'Humanities')])
    college_joined_year = models.CharField(max_length=5, blank=True, null=True)
    college_left_year = models.CharField(max_length=5, blank=True, null=True)
    university = models.CharField(max_length=200)
    university_gpa = models.FloatField(blank=True, null=True)
    university_faculty = models.CharField(max_length=200)
    university_joined_year = models.CharField(max_length=5, blank=True, null=True)
    university_left_year = models.CharField(max_length=5, blank=True, null=True)

    # Skills
    technical_skills = models.CharField(max_length=2000, blank=True, null=True)
    nontechnical_skills = models.CharField(max_length=2000, blank=True, null=True)

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

class Project(models.Model):
    profile = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    project = models.CharField(max_length=200)
    project_description = models.TextField()
    project_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.project

class Certificate(models.Model):
    profile = models.ForeignKey(Profile, related_name='certificates', on_delete=models.CASCADE)
    certificate= models.CharField(max_length=200)
    certificate_description = models.TextField()

    def __str__(self):
        return self.certificate

class Language(models.Model):
    profile = models.ForeignKey(Profile, related_name='languages', on_delete=models.CASCADE)
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language