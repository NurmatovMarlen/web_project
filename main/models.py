from django.db import models

class Category(models.Model):
    slug=models.SlugField(primary_key=True,max_length=50)
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='categories',blank=True,null=True)
    parent=models.ForeignKey('self',related_name='children',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f'{self.parent}->{self.name}'
        return self.name


    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False

class Student(models.Model):
    student_name=models.CharField(max_length=255)
    description=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='students')
    posted_date=models.DateField()

    def __str__(self):
        return self.student_name

    @property
    def get_image(self):
        return self.images.first()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail',kwargs={'pk':self.pk})

class Image(models.Model):
    image=models.ImageField(upload_to='students')
    student=models.ForeignKey(Student,on_delete=models.CASCADE,related_name='images')

    def __str__(self):
        return self.image.url
