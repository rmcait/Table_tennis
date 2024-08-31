from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.
from .models import Table


def indexfunc(request):
    tables = Table.objects.all()  # すべての卓球台の状況を取得
    now = datetime.now()

    

    # 時間帯を設定
    time_slots = [
        "9時 ~ 11時", "11時 ~ 13時", "13時 ~15時",
        "15時 ~ 17時", "17時 ~ 19時", "19時 ~ 21時"
    ]

    # 現在の時間に基づいて表示する時間帯を決定
    current_time_slot = None
    if 9 <= now.hour < 11:
        current_time_slot = time_slots[0]
    elif 11 <= now.hour < 13:
        current_time_slot = time_slots[1]
    elif 13 <= now.hour < 15:
        current_time_slot = time_slots[2]
    elif 15 <= now.hour < 17:
        current_time_slot = time_slots[3]
    elif 17 <= now.hour < 19:
        current_time_slot = time_slots[4]
    elif 19 <= now.hour < 21:
        current_time_slot = time_slots[5]

    return render(request, 'index.html', {
        'tables': tables,
        'current_time_slot': current_time_slot
    })
    
    

@login_required
def employeefunc(request):
    if request.method == 'POST':
        # 卓球台の利用状況を更新する
        table_id = request.POST.get('table_id')
        table = Table.objects.get(id=table_id)
        table.is_occupied = not table.is_occupied  # 状況を反転させる
        table.save()
        return redirect('employee')

    # 現在の卓球台の状況を取得
    tables = Table.objects.all()
    return render(request, 'employee.html', {'tables': tables})

