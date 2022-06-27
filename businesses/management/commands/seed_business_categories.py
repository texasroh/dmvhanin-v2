from businesses.models import Category, SubCategory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    categories = (
        {
            "name": "식당",
            "slug": "restaurant",
            "subcategories": [
                {"name": "한식", "slug": "korean"},
                {"name": "일식", "slug": "japanese"},
                {"name": "중식", "slug": "chinese"},
                {"name": "카페", "slug": "cafeteria"},
                {"name": "제빵/제과", "slug": "bakery"},
                {"name": "떡집/캐더링", "slug": "rice-cake-catering"},
                {"name": "기타", "slug": "etc"},
            ],
        },
        {
            "name": "식품점",
            "slug": "grocery",
            "subcategories": [
                {"name": "식품점", "slug": "grocery"},
            ],
        },
        {
            "name": "병원/약국",
            "slug": "hospital-pharmacy",
            "subcategories": [
                {"name": "의료원", "slug": "medical"},
                {"name": "내과", "slug": "medicine"},
                {"name": "물리재활/언어치료/통증", "slug": "therpy"},
                {"name": "발전문", "slug": "foot"},
                {"name": "방사선과", "slug": "radiology"},
                {"name": "비뇨기과", "slug": "urology"},
                {"name": "산부인과", "slug": "obstetrics-gynecology"},
                {"name": "성형외과", "slug": "plastic-surgery"},
                {"name": "소아과", "slug": "pediatrics"},
                {"name": "수의과", "slug": "veterinary"},
                {"name": "신경/흉곽외과", "slug": "neuro-thoracic-surgery"},
                {"name": "안과", "slug": "ophthalmology"},
                {"name": "검안과", "slug": "optometry"},
                {"name": "외과", "slug": "surgery"},
                {"name": "이비인후과", "slug": "otorhinolaryngology"},
                {"name": "정신과", "slug": "psychiatry"},
                {"name": "정형외과", "slug": "orthopedics"},
                {"name": "피부과", "slug": "dermatology"},
                {"name": "척추신경", "slug": "spinal-nerve"},
                {"name": "치과", "slug": "dentist"},
                {"name": "치과기공/재료", "slug": "dental-technician-material"},
                {"name": "한의원", "slug": "oriental-medicine-clinic"},
                {"name": "모발이식/탈모관리", "slug": "hair-transplant-loss-management"},
                {"name": "동물병원", "slug": "animal-hospital"},
                {"name": "약국", "slug": "pharmacy"},
                {"name": "양로원", "slug": "nursing-home"},
                {"name": "안경", "slug": "glasses"},
            ],
        },
        {
            "name": "학교/학원/튜터",
            "slug": "academy",
            "subcategories": [
                {"name": "노인학교", "slug": "senior-school"},
                {"name": "불교대학/한의대학", "slug": "buddhist-oriental-medicine"},
                {"name": "신학대학", "slug": "seminary"},
                {"name": "일반대학", "slug": "university"},
                {"name": "한글학교", "slug": "korean"},
                {"name": "꽃꽃이학원", "slug": "florist"},
                {"name": "영어학원", "slug": "english"},
                {"name": "예능학원", "slug": "entertainment"},
                {"name": "운전학원", "slug": "driving"},
                {"name": "유치원", "slug": "kindergarden"},
                {"name": "유학원", "slug": "abroad"},
                {"name": "종합학원", "slug": "general"},
                {"name": "종합학원/학자금", "slug": "general-fund"},
                {"name": "직업기술학원", "slug": "job-skill"},
                {"name": "컴퓨터학원", "slug": "computer"},
                {"name": "태권도", "slug": "taekwondo"},
                {"name": "골프레슨/미니골프/연습장/용품", "slug": "golf"},
            ],
        },
        {
            "name": "미용/뷰티",
            "slug": "beauty",
            "subcategories": [
                {"name": "화장품", "slug": "cosmetics"},
                {"name": "미용실/이발", "slug": "salon-barber"},
                {"name": "피부관리/체형관리", "slug": "skin-body-care"},
                {"name": "동물미용센터", "slug": "animal-beauty"},
                {"name": "미용재료", "slug": "tool-ingredients"},
            ],
        },
        {
            "name": "변호사/회계사",
            "slug": "lawyer-accountant",
            "subcategories": [
                {"name": "변호사", "slug": "lawyer"},
                {"name": "회계/공인회계사", "slug": "cpa"},
                {"name": "회계/공인세무사", "slug": "certified-tax-accountant"},
                {"name": "회계/회계사무소", "slug": "accounting"},
            ],
        },
        {
            "name": "은행/보험",
            "slug": "finance",
            "subcategories": [
                {"name": "보험", "slug": "insurance"},
                {"name": "융자", "slug": "loan"},
                {"name": "은행/금융기관", "slug": "bank"},
                {"name": "증권/투자", "slug": "investment"},
                {"name": "송금", "slug": "transfer"},
            ],
        },
        {
            "name": "부동산",
            "slug": "real-estate",
            "subcategories": [
                {"name": "부동산", "slug": "real-estate"},
                {"name": "부동산감정", "slug": "inspection"},
                {"name": "부동산타이틀회사", "slug": "title"},
            ],
        },
        {
            "name": "자동차",
            "slug": "car",
            "subcategories": [
                {"name": "매매", "slug": "trading"},
                {"name": "세차장", "slug": "car-wash"},
                {"name": "정비/바디샵", "slug": "maintenence-body-shop"},
                {"name": "토잉서비스", "slug": "towing"},
            ],
        },
        {
            "name": "여행/숙박/택시",
            "slug": "travel-lodgment-taxi",
            "subcategories": [
                {"name": "여행사", "slug": "travel-agency"},
                {"name": "관광버스/택시", "slug": "tour-bus-taxi"},
            ],
        },
        {
            "name": "생활편의",
            "slug": "convenience",
            "subcategories": [
                {"name": "운송/이삿짐", "slug": "moving"},
                {"name": "노래방/당구장/PC방/민화방/기원", "slug": "entertainment"},
                {"name": "스파/지압", "slug": "spa-acupressure"},
                {"name": "보청기", "slug": "hearing"},
                {"name": "인터넷서비스", "slug": "Internet"},
                {"name": "전기공사", "slug": "electrical-work"},
                {"name": "정수기", "slug": "water-filter"},
                {"name": "정원/조경", "slug": "garden-landscape"},
                {"name": "컴퓨터", "slug": "computer"},
                {"name": "커튼/인테리어", "slug": "curtain-tnterior"},
                {"name": "카펫", "slug": "carpet"},
                {"name": "피아노조율", "slug": "piano-tuning"},
                {"name": "홈케어", "slug": "homecare"},
                {"name": "스포츠", "slug": "sports"},
                {"name": "청소/제설", "slug": "cleaning-snow-removal"},
                {"name": "잔디기계/수리", "slug": "lawn-machinery-repair"},
                {"name": "전자판매/수리", "slug": "electronic-sales-repair"},
                {"name": "전화서비스", "slug": "telephone"},
                {"name": "페인트", "slug": "paint"},
                {"name": "플러밍", "slug": "plumming"},
            ],
        },
        {
            "name": "기타",
            "slug": "etc",
            "subcategories": [
                {"name": "건축/건설", "slug": "consturction"},
                {"name": "건강제품", "slug": "healthy-food"},
                {"name": "가구제작/판매/수리", "slug": "furniture"},
                {"name": "간판", "slug": "sign"},
                {"name": "결혼서비스/폐백", "slug": "wedding"},
                {"name": "고물상", "slug": "antique"},
                {"name": "광고대행/디자인", "slug": "sign-design"},
                {"name": "구두수선", "slug": "shoe-repair"},
                {"name": "꽃집", "slug": "florist"},
                {"name": "냉동/히팅", "slug": "freeze-heating"},
                {"name": "농장", "slug": "farm"},
                {"name": "도난방지", "slug": "anti-theft"},
                {"name": "도매/수입/잡화", "slug": "wholesale-import-miscellaneous-goods"},
                {"name": "도매/식품", "slug": "wholesale-grocery"},
                {"name": "물판매", "slug": "water-sale"},
                {"name": "번역/통역", "slug": "translation"},
                {"name": "보석", "slug": "jewel"},
                {"name": "봉제", "slug": "plush"},
                {"name": "사무기", "slug": "office-equipment"},
                {"name": "사진관/비디오촬영", "slug": "photo-studio-video-shoot"},
                {"name": "상담", "slug": "consulting"},
                {"name": "서점", "slug": "bookstore"},
                {"name": "선물센터", "slug": "gift-center"},
                {"name": "세탁장비", "slug": "laundry-equipment"},
                {"name": "소독", "slug": "disinfection"},
                {"name": "식당장비", "slug": "restaurant-equipment"},
                {"name": "소방장비", "slug": "firefighting-equipment"},
                {"name": "악기", "slug": "instrument"},
                {"name": "방송/신문/잡지", "slug": "broadcast-newspaper-magazine"},
                {"name": "연회장", "slug": "banquet-hall"},
                {"name": "열쇠", "slug": "key"},
                {"name": "운명철학/신점", "slug": "destiny-philosophy"},
                {"name": "유리", "slug": "glass"},
                {"name": "의류/가죽/모피/무스탕", "slug": "clothing-leather-fur-mustang"},
                {"name": "의류/양복", "slug": "clothing-suit-men"},
                {"name": "의류/양장", "slug": "clothing-suit-women"},
                {"name": "의류/웨딩", "slug": "clothing-wedding"},
                {"name": "의류/유니폼", "slug": "uniform-cloth"},
                {"name": "의류/한복", "slug": "clothing-korean"},
                {"name": "의류도매", "slug": "clothing-wholesale"},
                {"name": "이민", "slug": "immigrant"},
                {"name": "인쇄소", "slug": "print"},
                {"name": "장의사/묘지", "slug": "undertaker-cemetery"},
                {"name": "전당포", "slug": "pawn-shop"},
                {"name": "조명기구", "slug": "light"},
                {"name": "철공소", "slug": "iron-work"},
                {"name": "철물점", "slug": "hardware-store"},
                {"name": "카드서비스", "slug": "card-service"},
                {"name": "크레딧교정", "slug": "credit-correction"},
                {"name": "탐정", "slug": "detective"},
                {"name": "트로피", "slug": "trophy"},
                {"name": "행사/이벤트", "slug": "event"},
                {"name": "화랑/액자", "slug": "gallery-frame"},
            ],
        },
    )

    def handle(self, *args, **kwargs):
        for category in self.categories:
            cat, _ = Category.objects.get_or_create(
                name=category["name"], slug=category["slug"]
            )
            for subcategory in category["subcategories"]:
                SubCategory.objects.get_or_create(
                    name=subcategory["name"], slug=subcategory["slug"], category=cat
                )
                # sub = SubCategory(
                #     name=subcategory["name"], slug=subcategory["slug"], category=cat
                # )
                # sub.save()
