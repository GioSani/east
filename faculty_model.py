from django.db import models

class Curriculum(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    courses = models.ManyToManyField('Course', through='CurriculumCourse')

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    credit_hours = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

class CurriculumCourse(models.Model):
    curriculum = models.ForeignKey('Curriculum', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()
    is_elective = models.BooleanField(default=False)



from django.db import models

class IntegratedCurriculum(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    modules = models.ManyToManyField('Module', through='CurriculumModule')

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    credit_hours = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.name

class Component(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CurriculumModule(models.Model):
    curriculum = models.ForeignKey(IntegratedCurriculum, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.curriculum} - {self.module}"