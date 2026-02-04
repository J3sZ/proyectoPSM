from django.db import models

# Create your models here.
class Career(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    career = models.ForeignKey('Career', on_delete=models.CASCADE)
    UC = models.IntegerField()
    HT = models.IntegerField()
    HP = models.IntegerField()
    HL = models.IntegerField()
    TH = models.IntegerField()
    semester = models.IntegerField()
    #auto relacion para prelaciones(se requiere pasar otros subjects antes)
    prerequisites = models.ManyToManyField('self', through='Prerequisite', related_name='required_by', symmetrical=False)

    def __str__(self):
        return self.name    
    

class Prerequisite(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='main_subject')
    prerequisite = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='prerequisite_subject')
    class Meta:
        unique_together = ('subject', 'prerequisite')