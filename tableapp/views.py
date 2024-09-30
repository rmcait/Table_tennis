from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Table, WaitingList

previous_time_slot = None

def get_current_and_next_time_slot():
    time_slots = [
        "9時 ~ 11時", "11時 ~ 13時", "13時 ~ 15時",
        "15時 ~ 17時", "17時 ~ 19時", "19時 ~ 21時"
    ]
    now = datetime.now()

    # # ダミーデータ
    # now = datetime(2024, 9, 17, 13, 0, 0)

    current_time_slot = None
    next_time_slot = None

    # if 8 <= now.hour < 9:
    #     current_time_slot = '営業時間前'
    #     next_time_slot = time_slots[0]
    if 9 <= now.hour < 11:
        current_time_slot = time_slots[0]
        next_time_slot = time_slots[1]
    elif 11 <= now.hour < 13:
        current_time_slot = time_slots[1]
        next_time_slot = time_slots[2]
    elif 13 <= now.hour < 15:
        current_time_slot = time_slots[2]
        next_time_slot = time_slots[3]
    elif 15 <= now.hour < 17:
        current_time_slot = time_slots[3]
        next_time_slot = time_slots[4]
    elif 17 <= now.hour < 19:
        current_time_slot = time_slots[4]
        next_time_slot = time_slots[5]
    elif 19 <= now.hour < 21:
        current_time_slot = time_slots[5]
    elif  now.hour < 9 or 21 <= now.hour:
        current_time_slot = '営業時間前'
        next_time_slot  = time_slots[0]
        
    
        
        

    return current_time_slot, next_time_slot

@login_required
def employeefunc(request):

    current_time_slot, next_time_slot = get_current_and_next_time_slot()
    print(current_time_slot)
    print(next_time_slot)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # 現在の時間帯と次の時間帯を取得
        
    

        # 現在の時間帯の終了時間を計算
        now = datetime.now()
        slot_end_time = None
        if current_time_slot == "営業時間前":
            slot_end_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
        elif current_time_slot == "9時 ~ 11時":
            slot_end_time = now.replace(hour=11, minute=0, second=0, microsecond=0)
        elif current_time_slot == "11時 ~ 13時":
            slot_end_time = now.replace(hour=13, minute=0, second=0, microsecond=0)
        elif current_time_slot == "13時 ~ 15時":
            slot_end_time = now.replace(hour=15, minute=0, second=0, microsecond=0)
        elif current_time_slot == "15時 ~ 17時":
            slot_end_time = now.replace(hour=17, minute=0, second=0, microsecond=0)
        elif current_time_slot == "17時 ~ 19時":
            slot_end_time = now.replace(hour=19, minute=0, second=0, microsecond=0)


        # POST送信が有効かを判定
        can_post = slot_end_time and now >= (slot_end_time - timedelta(minutes=30))

        if form_type == 'next_status_change' and current_time_slot == "19時 ~ 21時":
            if now.hour >= 19:
                messages.error(request, "翌朝8時半以降に機能します")
                return redirect('employee')

        # 次の利用時間帯の予約
        if form_type == 'next_status_change':
            if not can_post:
                messages.error(request, "30分前以降でないと機能しません")
                return redirect('employee')  # 30分前でない場合、処理を中断

        # 現在の利用状況の変更
        if form_type == 'current_status_change':
            print(request.POST) 
            table_id = request.POST.get('table_id')
            table = Table.objects.get(id=table_id)
            table.is_occupied = not table.is_occupied
            table.save()

        # 次の利用時間帯の予約
        elif form_type == 'next_status_change':
            print(request.POST) 
            table_id = request.POST.get('table_id')
            table = Table.objects.get(id=table_id)

            # 現在の時間帯と次の時間帯を取得
            current_time_slot, next_time_slot = get_current_and_next_time_slot()


            try:
                waiting = WaitingList.objects.get(table=table)
                waiting.time_slot = next_time_slot  # 次の時間帯に更新
                waiting.next_is_occupied = not waiting.next_is_occupied
                waiting.save()
            except WaitingList.DoesNotExist:
                # 該当のテーブルがない場合は新規作成（ただし、今回は新しいオブジェクトが作成されないようにするので省略可）
                pass
    

        return redirect('employee')

    tables = Table.objects.all()
    waiting_list = WaitingList.objects.all()
    
    return render(request, 'employee.html', {
        'tables': tables,
        'waiting_list': waiting_list,
        'current_time_slot': current_time_slot,
        'next_time_slot': next_time_slot
    })

def update_waiting_list(current_time_slot, next_time_slot):
    # time_slot が current_time_slot でも next_time_slot でもないものをフィルタリング
    mismatched_waiting_lists = WaitingList.objects.exclude(time_slot=current_time_slot).exclude(time_slot=next_time_slot)
    
    # 該当するレコードを更新
    mismatched_waiting_lists.update(time_slot=next_time_slot, next_is_occupied=False)


def indexfunc(request):

    global previous_time_slot

    tables = Table.objects.all()  # すべての卓球台の状況を取得
    current_time_slot, next_time_slot = get_current_and_next_time_slot()
    print(f"Current time slot: {current_time_slot}")
    print(f"Previous time slot: {previous_time_slot}")
    print(f"Next time slot: {next_time_slot}")
    

    # 時間帯が切り替わった時にis_occupiedを空きにリセット
    if current_time_slot != previous_time_slot:
        for table in tables:
            table.is_occupied = False
            table.save()
    
    # 21時以降になったら待ち状況のリセット
        if  current_time_slot ==  "営業時間前" and previous_time_slot == "19時 ~ 21時" or previous_time_slot == None:
            waiting_non_lists = WaitingList.objects.all()
            for waiting_non_list in waiting_non_lists:
                waiting_non_list.time_slot = next_time_slot
                waiting_non_list.next_is_occupied = False
                waiting_non_list.save()

        # 現在の時間帯の予約を取得
        current_reservations = WaitingList.objects.filter(time_slot=current_time_slot)
        print(f"Reservations in current time slot: {current_reservations}")

        # next_is_occupiedがTrueのものを「利用中」に変更
        reservations_to_activate = current_reservations.filter(next_is_occupied=True)
        print(f"Reservations to activate: {reservations_to_activate}")
        
        # next_is_occupiedがTrueのものは「利用中」に変更
        for reservation in reservations_to_activate:
            reservation.table.is_occupied = True  # 利用中に変更
            reservation.table.save()

            # 次の時間帯に向けてリセット
            reservation.next_is_occupied = False
            reservation.time_slot = next_time_slot
            reservation.save()

        # next_is_occupiedがFalseのものは「空き」にリセット
        for reservation in current_reservations.filter(next_is_occupied=False):
            reservation.table.is_occupied = False  # 空きにリセット
            reservation.table.save()    

            # 次の時間帯に向けてtime_slotを更新
            reservation.time_slot = next_time_slot
            reservation.save()

        # update_waiting_list(current_time_slot, next_time_slot)

        previous_time_slot = current_time_slot

    # 次の時間帯の予約状況を取得して表示
    waiting_list = WaitingList.objects.all()


    return render(request, 'index.html', {
        'tables': tables,
        'current_time_slot': current_time_slot,
        'next_time_slot': next_time_slot,
        'waiting_list': waiting_list
    })
    
    

