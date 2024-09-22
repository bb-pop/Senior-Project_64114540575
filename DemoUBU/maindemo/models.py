from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    image = models.ImageField(upload_to='Item_images/', blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    max_borrow_time = models.PositiveIntegerField(default=60, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=50, null=True, default="user@ubu.ac.th")
    id_student = models.CharField(max_length=11, null=True)
    faculty = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class BorrowRecord(models.Model):
    STATUS_CHOICES = (
        ('waiting', 'รออนุมัติ'),
        ('borrowing', 'กำลังยืม'),
        ('returned', 'คืนแล้ว'),
        ('cancel' , 'ยกเลิก'),
        ('notreturn','ไม่คืนของ'),
    )
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="อุปกรณ์")
    borrower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="ผู้ยืม")
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name="วันที่ยืม")
    return_date = models.DateTimeField(null=True, blank=True, verbose_name="วันที่คืน")
    quantity = models.PositiveIntegerField(default=1, verbose_name="จำนวนที่ยืม")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="สถานะ")
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.borrow_date:
            self.borrow_date = timezone.now()

        if not self.return_date:
            self.return_date = self.borrow_date + timezone.timedelta(minutes=self.item.max_borrow_time)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.borrower.id_student} borrows {self.item.name}"