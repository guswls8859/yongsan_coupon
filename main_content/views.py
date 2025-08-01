import datetime

from django.shortcuts import render, HttpResponse
from main_content.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.db.models import Count
from django.shortcuts import get_object_or_404
import random
import string


# Create your views here.
def main_page(request):
    content = {}
    return render(request, 'index.html', content)

def icool_page(request):
    content = {}
    return render(request, 'icool_index.html', content)

def coopon(request, coopon_id):
    coopon_content = Coopon.objects.get(number=coopon_id)
    content = {'coopon': coopon_content}
    return render(request, 'main.html', content)

def coopon_icool(request, coopon_id):
    coopon_content = Coopon_icool.objects.get(number=coopon_id)
    content = {'coopon': coopon_content}
    return render(request, 'icool_main.html', content)

@csrf_exempt  # 개발 중일 경우. 운영 환경에선 CSRF 설정 필요.
def coopon_use(request, coopon_id):
    if request.method == 'POST':
        try:
            coopon = Coopon.objects.get(number=coopon_id)
            coopon.activate = True
            coopon.save()
            return JsonResponse({'success': True, 'message': f'{coopon_id}번 쿠폰이 활성화되었습니다.'})
        except Coopon.DoesNotExist:
            return JsonResponse({'success': False, 'message': '해당 쿠폰을 찾을 수 없습니다.'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'POST 요청만 허용됩니다.'}, status=405)


@csrf_exempt  # 개발 중일 경우. 운영 환경에선 CSRF 설정 필요.
def coopon_icool_use(request, coopon_id):
    if request.method == 'POST':
        try:
            coopon = Coopon_icool.objects.get(number=coopon_id)
            coopon.activate = True
            coopon.usetime = datetime.datetime.now()
            coopon.save()
            return JsonResponse({'success': True, 'message': f'{coopon_id}번 쿠폰이 활성화되었습니다.'})
        except Coopon.DoesNotExist:
            return JsonResponse({'success': False, 'message': '해당 쿠폰을 찾을 수 없습니다.'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'POST 요청만 허용됩니다.'}, status=405)


# 6자리 숫자 난수 생성 함수
def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def generate_unique_numbers(request):
    # 엑셀 파일 경로
    excel_file_path = 'static/coo_phone_data.xlsx'

    # 엑셀 파일 읽기
    df = pd.read_excel(excel_file_path)

    # A열 (첫 번째 열) 값 → 두 번째 행부터 (헤더 제외)
    a_column_values = df.iloc[1:, 0].tolist()

    # 1️⃣ 현재 DB에 있는 number(코드) 다 가져오기 → 중복 방지
    existing_codes = set(Coopon_icool.objects.values_list('number', flat=True))

    # 2️⃣ 새로운 코드들도 여기 저장해서 중복 방지
    new_codes = set()

    # 반복 저장
    for phone in a_column_values:
        # 빈값 skip
        if pd.isna(phone):
            continue

        # 중복되지 않는 코드 생성
        while True:
            random_code = generate_random_code()
            if random_code not in existing_codes and random_code not in new_codes:
                break  # 중복 없으면 탈출

        # DB 저장
        Coopon_icool.objects.create(
            phone=phone,
            number=random_code,
            activate=False,
            edittime=datetime.datetime.now()
        )

        # 사용한 코드 set 에 추가
        new_codes.add(random_code)

        print(f'Inserted: {phone} / Code: {random_code}')

    return HttpResponse("중복 없는 코드로 DB 저장 완료!")


def clean_phone_numbers(request):
    coopons = Coopon.objects.all()
    duplicate_count = 0
    update_count = 0

    for co in coopons:
        original = co.phone_number

        # None 이거나 빈 값이면 skip
        if not original:
            continue

        # 1️⃣ 하이픈 제거
        cleaned = original.replace('-', '').strip()

        # 2️⃣ 처음이 0으로 시작하지 않으면 0 추가
        if not cleaned.startswith('0'):
            cleaned = '0' + cleaned

        # 3️⃣ 중복 여부 체크 (자기 자신은 제외)
        if Coopon.objects.exclude(pk=co.pk).filter(phone_number=cleaned).exists():
            print(f'Skipping duplicate: {cleaned} (original: {original})')
            duplicate_count += 1
            continue

        # 기존 값과 다른 경우에만 업데이트
        if co.phone_number != cleaned:
            print(f'Updating: {original} → {cleaned}')
            co.phone_number = cleaned
            co.save()
            update_count += 1

    return HttpResponse(
        f"전화번호 정리 완료! 업데이트 {update_count}건, 중복으로 skip {duplicate_count}건"
    )

def wndqhrghkrdls(request):
    # 1️⃣ phone_number 별로 그룹화해서 개수 세기
    duplicates = (
        Coopon.objects.values('phone_number')
        .annotate(count=Count('id'))
        .filter(count__gt=1)
    )

    delete_count = 0

    for dup in duplicates:
        phone_number = dup['phone_number']

        # 2️⃣ 해당 번호 가진 row 모두 가져오기 (id 순 정렬)
        coo_list = Coopon.objects.filter(phone_number=phone_number).order_by('id')

        # 3️⃣ 첫 번째(최신 것) 하나 남기고 나머지 삭제
        coo_to_keep = coo_list.first()
        coo_to_delete = coo_list.exclude(pk=coo_to_keep.pk)

        count = coo_to_delete.count()
        delete_count += count

        coo_to_delete.delete()

        print(f'중복 번호 {phone_number}: {count}개 삭제 (keep id={coo_to_keep.id})')

    return HttpResponse(f'중복 phone_number 정리 완료! 삭제된 row 수: {delete_count}개')

def excel_make(request):
    from django.utils.timezone import is_aware

    # 데이터 가져오기
    qs = Coopon_icool.objects.all().values()

    # datetime 필드에서 tz 제거
    cleaned_data = []
    for item in qs:
        for field in ['edittime', 'usetime']:
            dt = item.get(field)
            if dt and is_aware(dt):
                item[field] = dt.replace(tzinfo=None)
        cleaned_data.append(item)

    # DataFrame 생성 후 엑셀로 저장
    df = pd.DataFrame(cleaned_data)
    df.to_excel('coopon_icool_export.xlsx', index=False)

    return HttpResponse(f'엑셀 저장 완료! →')

def phone_num_ch(request):
    coo = Coopon.objects.all()

    for phone in coo:
        original = phone.phone_number

        # None 또는 빈 값 skip
        if not original or len(original) < 10:
            continue

        # 하이픈 제거
        cleaned = original.replace('-', '')

        # 포맷 변경 (가정: 01012345678 형식)
        if len(cleaned) == 11:  # 010xxxxxxxx
            formatted = f'{cleaned[:3]}-{cleaned[3:7]}-{cleaned[7:]}'
        elif len(cleaned) == 10:  # 02xxxxxxxx 또는 011xxxxxxxx
            formatted = f'{cleaned[:3]}-{cleaned[3:6]}-{cleaned[6:]}'
        else:
            # 포맷을 만들 수 없는 경우 skip
            continue

        # 변경된 경우 저장
        if phone.phone_number != formatted:
            print(f'Updating: {original} → {formatted}')
            phone.phone_number = formatted
            phone.save()

    # ✅ 모든 Coopon → DataFrame 으로 변환
    coopon_data = Coopon.objects.all().values('phone_number', 'number', 'activate')

    df = pd.DataFrame(list(coopon_data))

    # ✅ 엑셀로 저장
    output_path = 'static/coopon_export.xlsx'
    df.to_excel(output_path, index=False)

    return HttpResponse(f'번호 변경 및 엑셀 저장 완료! → {output_path}')


def data_upload(request):
    # ✅ 엑셀 파일 경로 (경로는 필요에 따라 수정 가능)
    excel_file_path = 'static/coupons.xlsx'

    # ✅ 엑셀 파일 읽기
    df = pd.read_excel(excel_file_path)

    # ✅ DataFrame 확인 (컬럼명 출력)
    print(df.columns)

    # ✅ 컬럼명이 아래와 같다고 가정
    # phone_number / number / activate

    insert_count = 0
    update_count = 0

    for index, row in df.iterrows():
        phone_number = row['phone_number']
        number = row['number']
        activate = row['activate']

        # ✅ 이미 number(고유번호)가 DB 에 있으면 update
        coopon, created = Coopon.objects.update_or_create(
            number=number,  # 기준 필드
            defaults={
                'phone_number': phone_number,
                'activate': activate
            }
        )

        if created:
            insert_count += 1
            print(f'Inserted: {number} / {phone_number}')
        else:
            update_count += 1
            print(f'Updated: {number} / {phone_number}')

    return HttpResponse(f'엑셀 → DB 저장 완료! (신규 {insert_count}개, 업데이트 {update_count}개)')


def test_data_set(request):
    # NMik88
    coopon = Coopon.objects.get(phone_number='010-4168-9819')
    coopon.activate = False
    coopon.save()
    return HttpResponse('업로드 완료')


def use_data(request):
    coupon = Coopon.objects.filter(activate=True).order_by('id')
    for test in coupon:
        print(test.phone_number)
    return HttpResponse(coupon)

def sms_sends(request):
    data = {}
    return render()