from datetime import timedelta
import datetime
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import logout
from maindemo.models import BorrowRecord, Item, UserProfile
from maindemo.forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .forms import UserProfileForm
from django.db.models import F
from .forms import DateRangeForm
import pandas as pd
from django.http import HttpResponse
from django.db.models import Count


#User


def home(request):
    if request.user.is_authenticated: 
        return redirect('/index')  
    return render(request, "user/home.html")

@login_required 
@receiver(user_logged_in)
def create_or_update_user_profile_on_login(sender, user, **kwargs):
    UserProfile.objects.get_or_create(user=user)
    
@login_required
def edit_user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'user/edit_profile.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def index(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, "user/index.html", context)

@login_required
def detail(request, id):
    it = Item.objects.get(pk=id)
    context = {
        'it': it,
    }
    return render(request, 'user/item_detail.html', context)

@login_required
def confirm(request, id):
    item = get_object_or_404(Item, pk=id)
    # current_time = timezone.localtime(timezone.now()).time()
    # start_time = datetime.time(14, 0) 
    # end_time = datetime.time(20, 0)  

    # if not start_time <= current_time <= end_time:
    #     return redirect('index')

    existing_borrow = BorrowRecord.objects.filter(borrower=request.user.userprofile, status__in=['waiting', 'borrowing', 'notreturn']).exists()
    if existing_borrow:
        return redirect('index')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if item.quantity >= quantity:
            borrow_record = BorrowRecord(
                item=item,
                borrower=request.user.userprofile,
                quantity=quantity,
                status='waiting'
            )
            
            try:
                borrow_record.save()
                
                item.quantity = F('quantity') - quantity
                item.save()
                item.refresh_from_db()
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Not enough items available to borrow.")
        
        return redirect('history')
    else:
        return render(request, 'user/confirm.html', {'it': item, 'id': item.id})

@login_required
def history(request):
    user_profile = request.user.userprofile
    borrow_records = BorrowRecord.objects.filter(borrower=user_profile).order_by('-borrow_date')

    return render(request, 'user/history.html', {'borrow_records': borrow_records})

@login_required
def cancel_borrow(request, record_id):
    record = get_object_or_404(BorrowRecord, id=record_id, borrower=request.user.userprofile, status='waiting')
    record.status = 'cancel'
    record.save()

    record.item.quantity += record.quantity
    record.item.save()

    return redirect('history')

@login_required
def check_and_cancel_borrows(request):
    now = timezone.now()
    ten_minutes_ago = now - timedelta(minutes=10)
    records_to_cancel = BorrowRecord.objects.filter(status='waiting', borrow_date__lte=ten_minutes_ago)

    count = 0
    for record in records_to_cancel:
        record.status = 'cancel'
        record.save()
        record.item.quantity += record.quantity
        record.item.save()
        count += 1

    return redirect('/')

@login_required
def contact(request):
    return render(request, "user/contact.html")

@login_required
def rules(request):
    return render(request, "user/rules.html")


#Admin


@login_required
def check_and_cancel_admin(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    now = timezone.now()
    ten_minutes_ago = now - timedelta(minutes=10)
    records_to_cancel = BorrowRecord.objects.filter(status='waiting', borrow_date__lte=ten_minutes_ago)

    count = 0
    for record in records_to_cancel:
        record.status = 'cancel'
        record.save()
        record.item.quantity += record.quantity
        record.item.save()
        count += 1
        
    return redirect('index_admin')

@login_required
def index_admin(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, "admin/index-admin.html", context)

@login_required
def create(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('index_admin')
    else:
        form = ItemForm()
    context = {
        'form': form
    }
    return render(request, "admin/create.html", context)

@login_required
def edit(request, id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    it = Item.objects.get(pk=id)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=it)
        if form.is_valid():
            form.save()
            return redirect('index_admin')
    else:
        form = ItemForm(instance=it)
    
    context = {
        'it': it,
        'form': form
    }
    return render(request, 'admin/edit.html', context)

@login_required  
def delete(request,id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    it = Item.objects.get(pk=id)
    it.delete()
    return redirect('index_admin')

@login_required
def approve_admin(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    borrow_records = BorrowRecord.objects.filter(status='waiting')
    return render(request, 'admin/approve-borrow.html', {'borrow_records': borrow_records})

@login_required
def reject(request, record_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    borrow_record = get_object_or_404(BorrowRecord, pk=record_id)

    if borrow_record.status == 'waiting' and request.user.has_perm('maindemo.change_borrowrecord'):
        borrow_record.status = 'cancel'
        borrow_record.save()
        borrow_record.item.quantity += borrow_record.quantity
        borrow_record.item.save()

    return redirect('approve_admin')

@login_required
def approve_borrow(request, record_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    borrow_record = get_object_or_404(BorrowRecord, pk=record_id)

    if borrow_record.status == 'waiting' and request.user.has_perm('maindemo.change_borrowrecord'):
        borrow_record.status = 'borrowing'
        borrow_record.save()

    return redirect('approve_admin')

@login_required
def return_item(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    borrowing_records = BorrowRecord.objects.filter(status='borrowing').order_by('-borrow_date')
    return render(request, 'admin/return_item.html', {'borrow_records': borrowing_records})

@login_required
def confirm_return(request, record_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    borrow_record = get_object_or_404(BorrowRecord, pk=record_id, status='borrowing')
    borrow_record.status = 'returned'
    borrow_record.return_date = timezone.now()  
    borrow_record.save()

    item = borrow_record.item
    item.quantity += borrow_record.quantity
    item.save()

    return redirect('return_item')

@login_required
def not_returned(request, record_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')

    borrow_record = get_object_or_404(BorrowRecord, pk=record_id, status='borrowing')
    borrow_record.status = 'notreturn'
    borrow_record.save()

    return redirect('return_item') 

@login_required
def noreturn_admin(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    borrow_records = BorrowRecord.objects.filter(status='notreturn')
    return render(request, 'admin/noretrun-admin.html', {'borrow_records': borrow_records})

@login_required
def confirm_noreturn(request, record_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    borrow_record = get_object_or_404(BorrowRecord, pk=record_id, status='notreturn')
    borrow_record.status = 'returned'
    borrow_record.return_date = timezone.now()  
    borrow_record.save()

    item = borrow_record.item
    item.quantity += borrow_record.quantity
    item.save()

    return redirect('noreturn_admin')

@login_required
def dashboard(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('/')
    
    items = Item.objects.all()
    form = DateRangeForm(request.GET or None)
    records = BorrowRecord.objects.all()

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        item_id = request.GET.get('item_id')
        
        if start_date and end_date:
            records = records.filter(borrow_date__gte=start_date, borrow_date__lte=end_date)
        if item_id:
            records = records.filter(item__id=item_id)
            
    total_borrows = records.count()

    top_items = records.values('item__name').annotate(total=Count('id')).order_by('-total')[:3]

    top_faculties = records.values('borrower__faculty').annotate(total=Count('id')).order_by('-total')[:3]

    if 'export' in request.GET and records.exists():
        response = export_records_to_excel(records)
        return response

    context = {
        'form': form,
        'records': records,
        'items': items,
        'total_borrows': total_borrows,
        'top_items': top_items,
        'top_faculties': top_faculties
    }
    return render(request, 'admin/dashboard.html', context)

def export_records_to_excel(records):
    data = []
    for i, record in enumerate(records, start=1):
        if record.status in ['cancel', 'ยกเลิก', 'notreturn', 'ไม่คืนของ']:
            return_date = '-'
            return_time = '-'
        else:
            return_date = record.return_date.strftime('%d/%m/%Y') if record.return_date else '-'
            return_time = record.return_date.strftime('%H:%M') if record.return_date else '-'

        row = {
            'ลำดับ': i,
            'ชื่ออุปกรณ์': record.item.name,
            'จำนวน': record.quantity,
            'คณะ': record.borrower.faculty,
            'รหัสนักศึกษา': record.borrower.id_student,
            'วันที่ยืม ว/ด/ป': record.borrow_date.strftime('%d/%m/%Y') if record.borrow_date else '',
            'เวลาที่ยืม': record.borrow_date.strftime('%H:%M') if record.borrow_date else '',
            'วันที่ที่คืน ว/ด/ป': return_date,
            'เวลาที่คืน': return_time,
            'สถานะ': record.get_status_display()
        }
        data.append(row)

    df = pd.DataFrame(data)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="records_export.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response
