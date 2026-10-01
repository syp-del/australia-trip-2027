#!/usr/bin/env python3
"""New guide spots collected 2026-10-01 (Korean-review research + user picks). Writes extra.json."""
import json
from pathlib import Path

R, C = "추천", "검토필요"
CITY = "시티 · 서큘러키 · 달링하버"
CITYF = "시티 · 서큘러키 · 차이나타운"
EAST = "본다이 · 쿠지 · 클로벨리"
WATS = "왓슨스베이 · 발모랄"
SURRY = "서리힐스 · 달링허스트"
WEST = "시드니 서부 · 올림픽파크"
GLEBE = "글리브 · 레드펀"
BM = "블루마운틴"
PS = "포트스테판 · 뉴캐슬"
CC = "센트럴코스트 · 헌터밸리"
SOUTH = "로열내셔널파크 · 울런공"
KIAMA = "키아마 · 게링공"
JB = "저비스베이"
NB = "노던비치 · 팜비치"
MCBD = "멜버른 · CBD 레인웨이"
MCBDF = "멜버른 · CBD"
MSB = "멜버른 · 사우스뱅크"
MCARL = "멜버른 · 칼튼 · 파크빌"
MCARLF = "멜버른 · 칼튼(리틀이탈리아)"
MSTK = "멜버른 · 세인트킬다 · 브라이튼"
MNEAR = "멜버른 · 근교"
MMORN = "멜버른 · 모닝턴반도"
B = "https://blog.naver.com/"

# (id, kind, region, icon, title, sub|sig, desc, q, tags, badge, hours, closed, price, note, src)
ROWS = [
 # ---- user picks
 ("runbarangaroo","place",CITY,"i-bridge2","바랑가루역~오페라하우스 러닝코스","편도 약 3.5km · 평지","바랑가루 리저브 → 월시베이 부두 → 하버브리지 아래(도스포인트) → 서큘러키 → 오페라하우스. 해안 산책로만 따라가면 돼서 길 잃을 일이 없어요.","Barangaroo Reserve Sydney",["조깅","노을","무료"],R,"상시 개방","","무료","한여름엔 해 뜨기 직후나 해질녘에. 돌아올 땐 서큘러키에서 전철·라이트레일.",""),
 ("walkabout","place",CC,"i-roo","워크어바웃 야생동물 보호구역","칼가 · 시드니에서 약 1시간","캥거루·왈라비·에뮤가 풀려 있는 숲속 보호구역. 레인저 프로그램이 입장료에 포함.","Walkabout Wildlife Sanctuary Calga",["동물","렌터카"],C,"매일 09:30~17:00","","성인 A$45 · 어린이(3~11) A$30","한국인 후기를 찾지 못해 검토필요. 차 없이는 가기 어려워요.","https://walkaboutpark.com.au/opening-hours-prices/"),
 ("hydepark","place",CITY,"i-leaf","하이드 파크","숙소에서 도보 5분","세인트메리 대성당과 아치볼드 분수가 있는 도심 공원. 오스트레일리안 뮤지엄·쿡+필립 수영장과 붙어 있어요.","Hyde Park Sydney",["산책","무료"],R,"상시 개방","","무료","",""),
 ("bbqbronte","place",EAST,"i-bbq","브론테 공원 무료 바베큐","해변 바로 뒤 잔디공원","전기 바베큐 그릴과 피크닉 테이블, 놀이터가 해변 뒤 공원에 모여 있어요. 무료 락풀(브론테 배스)과 묶기 좋아요.","Bronte Park BBQ",["무료","바베큐","수영"],R,"상시 개방","","무료","주말 점심엔 자리 경쟁이 심해 오전에 도착. 그릴 닦을 키친타월·호일 지참.",""),
 ("bbqclovelly","place",EAST,"i-bbq","클로벨리 무료 바베큐","해변 산책로 옆","클로벨리비치 북쪽 산책로와 남쪽(번독 파크 쪽)에 무료 바베큐 시설. 잔잔한 만에서 수영 후 바로 구워먹기.","Clovelly Beach BBQ",["무료","바베큐","수영"],R,"상시 개방","","무료","",""),
 ("bbqshelly","place","맨리","i-bbq","셸리비치 무료 바베큐","맨리에서 도보 15분","셸리비치 뒤편 그늘에 무료 바베큐와 테이블. 얕고 잔잔해 아이들 물놀이와 같이 하기 좋아요.","Shelly Beach Manly BBQ",["무료","바베큐","수영"],R,"상시 개방","","무료","",""),
 ("bbqpirrama","place",CITY,"i-bbq","피라마 파크 무료 바베큐","피어몬트 · 물놀이 분수","하버 옆 공원에 무료 바베큐, 놀이터, 여름철 물놀이 분수가 한자리에. 숙소에서 가장 가까운 바베큐 후보.","Pirrama Park Pyrmont",["무료","바베큐","물놀이"],R,"상시 개방","","무료","피쉬마켓에서 장봐서 가기 좋은 위치.",""),
 ("bbqglebe","place",GLEBE,"i-bbq","바이센테니얼 파크(글리브) 무료 바베큐","블랙와틀베이 해안","안작브리지가 보이는 잔디공원. 무료 바베큐와 놀이터, 해안 산책로.","Bicentennial Park Glebe",["무료","바베큐"],R,"상시 개방","","무료","",""),
 # ---- Sydney city A
 ("cookphillip","place",CITY,"i-wave","쿡+필립 파크 수영장","숙소 도보권 실내풀","하이드파크 옆 실내 수영장. 키즈·레저풀과 파도풀이 있어 비 오거나 너무 더운 날 해변 대안.","Cook + Phillip Park Pool Sydney",["수영","실내"],R,"매일 06:00~20:00","","성인 A$9.10 · 어린이 A$5.90 · 가족 A$21.20","수건·세면도구 지참. 파도 가동 시간은 확인 필요.",B+"gae2deuk/224157647065"),
 ("gunyama","place","파라마타 · 알렉산드리아","i-wave","군야마 파크 아쿠아틱 센터","제틀랜드 · 그린스퀘어","실내풀·야외 50m·야외 키즈풀을 갖춘 신축 시설. 옆 쇼핑몰에 콜스가 있어요.","Gunyama Park Aquatic and Recreation Centre",["수영"],R,"06:00~20:00","","성인 약 A$9.10 · 가족 약 A$22.50","16시 이후엔 수영 강습으로 붐벼요.",B+"everkyj0228/224136482060"),
 ("sopaquatic","place",WEST,"i-wave","시드니 올림픽 파크 아쿠아틱 센터","실내 미니 워터파크","슬라이드·유수풀·키즈 스플래시존이 있는 실내 수영장. 물이 따뜻하고 가족 탈의실이 있어요.","Sydney Olympic Park Aquatic Centre",["수영","실내"],R,"평일 05:00~20:00 · 주말 06:00~19:00","","성인 A$10 · 어린이 A$7.60","슬라이드는 오후에만 가동, 시간표가 날마다 달라요. 키 제한 확인 필요.",B+"mumin113/224151699730"),
 ("abcpool","place",CITY,"i-wave","앤드류 보이 찰튼 풀","보타닉가든 옆 야외풀","울루물루 만과 군함이 내려다보이는 야외 수영장. Mrs Macquaries Point 노을 산책과 묶기 좋아요.","Andrew (Boy) Charlton Pool",["수영","뷰"],R,"미확인 — 방문 전 확인","","미확인","그늘이 없어 오전이나 늦은 오후에. 얕은 키즈풀 유무 확인 필요.",B+"bje1993/224129176909"),
 ("princealfredpool","place","서리힐스 · 센트럴","i-wave","프린스 알프레드 파크 수영장","센트럴역 옆 야외 50m","잔디 언덕에 둘러싸인 야외풀. 랩 위주라 부모님 운동 수영에 좋아요.","Prince Alfred Park Pool Surry Hills",["수영"],R,"미확인 — 방문 전 확인","","약 A$8","",B+"filledwith_happiness/224340819885"),
 ("brontebaths","place",EAST,"i-wave","브론테 비치 & 브론테 배스","무료 해수 락풀","본다이~쿠지 산책로 중간. 무료 락풀과 탈의실·샤워가 있어 아이스버그 대신 가는 곳.","Bronte Baths",["수영","무료"],R,"상시 개방","","무료","락풀 수심 1~2m로 생각보다 깊어요. 해변 쪽은 파도가 있는 서핑 비치.",B+"sw16ja17/224075215973"),
 ("sharkbeach","place",WATS,"i-wave","샤크 비치 (닐슨 파크)","그물 쳐진 잔잔한 하버 비치","파도가 거의 없고 수영 구역에 그물이 있어요. 그늘과 피크닉 공간이 넉넉한 현지 가족 명소.","Shark Beach Nielsen Park Vaucluse",["수영","가족추천","피크닉"],R,"상시 개방","","무료","더운 주말엔 일찍. 버스 접근, 주차 적음.",B+"robinsblog/224109392917"),
 ("campcove","place",WATS,"i-wave","캠프 코브","왓슨스베이 페리에서 도보","파도가 잔잔하고 모래가 고운 작은 하버 비치. 더 갭·도일스와 한 코스.","Camp Cove Beach Watsons Bay",["수영","페리"],R,"상시 개방","","무료","그늘이 거의 없어 래시가드·파라솔 준비.",B+"superbein9/224273393945"),
 ("ausmuseum","place",CITY,"i-palette","오스트레일리안 뮤지엄","무료 · 공룡과 고래 뼈","하이드파크 옆 자연사박물관. 입구에서 탐험 지도를 주고 화석 발굴 체험존이 있어요.","Australian Museum Sydney",["실내","무료","우천대비"],R,"매일 10:00~17:00","","상설 무료 (특별전 유료)","한낮 더위 피하기 좋은 2~3시간 코스.",B+"llalla_nana/224424143523"),
 ("maritime","place",CITY,"i-ferris","호주 국립 해양박물관","실제 잠수함·구축함 탑승","달링하버. 잠수함과 군함에 직접 들어가 보는 게 아이들 하이라이트.","Australian National Maritime Museum",["실내","체험"],R,"10:00~16:00","","가족권 약 A$89","함정 탑승은 키 90cm 이상. 잠수함은 정원 제한이 있어 도착하자마자 확인.",B+"dearsoja/224366661712"),
 ("observatoryhill","place",CITY,"i-sunset","옵저버토리 힐 공원","하버브리지 뷰 노을 피크닉","한국인 블로그에서 가장 많이 꼽히는 노을 명소. 잔디에 돗자리 펴고 브리지를 바라봐요.","Observatory Hill Park Sydney",["노을","피크닉","무료"],R,"상시 개방","","무료","2월 일몰은 20시 무렵. 한 시간 전엔 자리 잡기.",B+"aes2ong/224340532441"),
 ("rbgsydney","place",CITY,"i-leaf","로열 보타닉 가든 시드니","오페라하우스 뷰 잔디밭","하버를 낀 정원. 잔디 피크닉과 부모님 조깅 코스로 좋아요.","Royal Botanic Garden Sydney",["피크닉","조깅","무료"],R,"매일 07:00~일몰 무렵","","무료","매점이 적어 물을 챙기고 그늘 자리 잡기.",B+"millitory/224426344203"),
 ("operatour","place",CITY,"i-opera","오페라하우스 한국어 내부 투어","약 30분","한국어 가이드로 내부를 짧게 둘러보는 투어. 아이들이 안에 들어가 보고 싶어할 때.","Sydney Opera House",["실내","예약"],R,"투어 시간표 확인 필요","","1인 약 3.9만원","사전 예약 필수.",B+"zorba-lim/224374073398"),
 ("towereye","place",CITY,"i-bridge2","시드니 타워 아이","250m 전망대","웨스트필드 위 전망대. 숙소에서 걸어갈 수 있는 실내 코스.","Sydney Tower Eye",["실내","전망"],R,"매일 10:00~19:00 무렵 (입장 마감 18:00)","","1인 약 3.2만원","2월엔 입장 마감이 일몰보다 일러 노을은 못 봐요.",B+"jamjma98/224324336926"),
 ("rocksmarket","place",CITY,"i-cart","록스 마켓","주말 수공예·푸드 마켓","수제 기념품과 먹거리 노점. 장본 뒤 오페라하우스 뷰 피크닉으로 이어가요.","The Rocks Markets",["마켓","주말"],R,"토·일 10:00~17:00","월화수목금","입장 무료","여행 중 2/13(토)·2/14(일)만 가능.",B+"secondlifehere/224416519824"),
 ("paddys","place",CITY,"i-bag","패디스 마켓","숙소 옆 기념품 시장","코알라 인형·비치타월·열쇠고리를 대량으로 사는 곳. 실내라 더운 날도 편해요.","Paddy's Markets Haymarket",["쇼핑","기념품"],R,"수~일 10:00~18:00","월화","입장 무료","가격 평은 갈려요. 여러 가게 비교 후 구매.",B+"kyj3248/224420352231"),
 ("qvb","place",CITY,"i-bag","퀸 빅토리아 빌딩 (QVB)","고풍스러운 쇼핑 아케이드","시계탑과 스테인드글라스가 볼거리. 어그·판도라·T2 매장.","Queen Victoria Building",["쇼핑","실내"],R,"월~수·금·토 09:00~18:00 · 목 09:00~21:00 · 일 11:00~17:00","","입장 무료","",B+"yu_boo/224356722005"),
 ("glebemarket","place",GLEBE,"i-cart","글리브 마켓","토요일 빈티지 플리마켓","노점 200여 개의 로컬 벼룩시장. 시드니대·캐리지웍스와 묶는 코스.","Glebe Markets",["마켓","토요일"],R,"토 10:00~16:00","월화수목금일","입장 무료","여행 중 2/13(토)만 가능. 야외라 덥고 아이들 흥미는 낮을 수 있어요.",B+"ebeblog/224268954102"),
 ("carriageworks","place",GLEBE,"i-cart","캐리지웍스 파머스 마켓","토요일 오전 파머스마켓","굴·페이스트리·A.P 베이커리 노점. 주말 마켓 중 꼭 가야 할 곳으로 꼽혀요.","Carriageworks Farmers Market",["마켓","토요일"],R,"토 08:00~13:00","월화수목금일","입장 무료","여행 중 2/13(토)만 가능. 오후엔 이미 끝나요.","https://carriageworks.com.au/visit/"),
 ("alfies","food",CITYF,"i-ribs","Alfie's","가성비 설로인 스테이크","4-6 Bligh St. 한국인 블로그에서 요즘 가장 많이 보이는 설로인 스테이크집. 만 18세 이상만 입장.","Alfie's Bligh Street Sydney",[],C,"월~토 12:00~24:00","일","스테이크 약 A$39~42","바 형태라 아이 입장 가능 여부 확인 필요. 예약 시 카드 등록, 노쇼 A$75.",B+"aga_bao_daily/224310587605"),
 ("macelleria","food","본다이","i-ribs","Macelleria 본다이","정육점에서 고른 고기를 구워줌","Campbell Parade. 진열대에서 부위를 고르면 그릴에 구워주는 캐주얼 스테이크. 고구마 웨지 추천.","Macelleria Bondi",[],R,"본다이점 미확인 (뉴타운점 매일 12:00~22:00)","","1인 약 A$40~60","예약 없이 가능. 본다이 해변 날 점심으로.",B+"robinsblog/224393472877"),
 ("meatwine","food",CITYF,"i-ribs","The Meat & Wine Co 바랑가루","스테이크 런치 코스","런치 3코스 약 $55. 캥거루 스테이크도 있어요. 대가족 식사 후기가 있는 곳.","The Meat & Wine Co Barangaroo",[],R,"미확인 — 방문 전 확인","","런치 3코스 약 A$55","예약 권장. 런치가 가성비.",B+"yu_boo/224419010891"),
 ("pancakesrocks","food",CITYF,"i-croissant","Pancakes on the Rocks","팬케이크 · 립","더 록스의 오래된 한국인 단골집. 양이 많아 나눠 먹기.","Pancakes on the Rocks The Rocks",[],R,"일~목 07:30~24:00 · 금·토 07:30~02:00","","미확인","평은 갈리는 편. 아이 메뉴는 무난.",B+"y00n_59/224336183124"),
 ("elements","food",CITYF,"i-ribs","Elements Bar and Grill 월시베이","스테이크 익스프레스 런치","유튜버 쯔양 방문 후 유명해진 곳. 마리나 뷰 야외석.","Elements Bar and Grill Walsh Bay",[],R,"미확인 — 방문 전 확인","","미확인","한국에서 미리 예약하는 편. 아이 동반 적합 여부 확인 필요.",B+"leeeeeee_life/224421118580"),
 ("singleo","food",SURRY,"i-coffee","Single O 서리힐스","시드니 3대 커피 · 브런치","60-64 Reservoir St. 커피와 음식 모두 평이 좋아요.","Single O Surry Hills",[],R,"월~금 07:00~15:30 · 토·일 08:00~15:00","","미확인","좁고 붐벼요. 예약 불가, 오픈 시간에 가기.",B+"lemonade_99/224421846632"),
 ("gumption","food",CITYF,"i-coffee","Gumption by Coffee Alchemy","시드니 3대 커피 · 플랫화이트","스트랜드 아케이드 안. 세 곳 중 가장 시내 중심.","Gumption by Coffee Alchemy",[],R,"월~금 08:00~16:30 · 토 10:00~15:45 · 일 10:00~14:45","","미확인","좌석이 거의 없는 테이크아웃 위주.",B+"qwqwqw1644/224373153173"),
 ("apbakery","food",SURRY,"i-croissant","A.P Bakery (A.P House)","크루아상 샌드위치 · 아몬드 크루아상","L2/80 Commonwealth St 루프탑. 한국인 빵지순례 1순위.","A.P House Surry Hills",[],R,"매일 07:30~15:00","","미확인","줄이 길고 비싸다는 평이 공통.",B+"ddohh12/224412199752"),
 ("lode","food",SURRY,"i-croissant","Lode Pies & Pastries","와규 파이 · 피스타치오 페이스트리","487 Crown St. 파인다이닝 셰프들이 만든 베이커리.","Lode Pies & Pastries Surry Hills",[],R,"매일 08:00~15:00 (2023년 기준)","","미확인","",B+"dds05053/224355322915"),
 ("theeca","food",SURRY,"i-croissant","Theeca","대왕 팬케이크 브런치","1 Burton St. 손님 절반이 한국인이라는 요즘 가장 유명한 브런치.","Theeca Darlinghurst",[],R,"07:30~15:00 (목~일 저녁 영업 여부 미확인)","","미확인","팬케이크는 호불호가 크게 갈려요. 오픈런 필요.",B+"hyoji_joy/224353270088"),
 ("messina","food",CITYF,"i-honey","Gelato Messina","젤라또","서큘러키·마틴플레이스·달링스퀘어·본다이 등. 시드니 젤라또의 기본값.","Gelato Messina Circular Quay",[],R,"일~목 12:00~22:00 · 금·토 12:00~23:00 (서큘러키점)","","2스쿱 A$8.90","야외석은 갈매기 주의.",B+"jinnimong/224417666979"),
 ("yochi","food",CITYF,"i-honey","Yo-Chi","셀프 프로즌 요거트","무게로 계산하는 요거트 아이스크림. 아이들이 직접 토핑을 담아요.","Yo-Chi George Street Sydney",[],R,"미확인 — 방문 전 확인","","무게당 계산","밤 10시에도 줄이 있지만 금방 빠져요.",B+"qhfk0710/224339576579"),
 ("anita","food","맨리","i-honey","Anita Gelato 맨리","젤라또 · 피스타치오","46-48 The Corso. 맨리 가는 날 들르기 좋아요.","Anita Gelato Manly",[],R,"미확인 — 방문 전 확인","","미확인","줄이 길어요.",B+"nayeong95/224338052977"),
 # ---- Sydney city B
 ("wildplay","place","패딩턴 · 센테니얼파크","i-leaf","이안 포터 와일드 플레이 가든","센테니얼파크 안 자연 놀이터","물놀이가 되는 자연형 놀이터. 한국인 가족 후기는 좋지만 2023~25년 글이에요.","Ian Potter Children's WILD PLAY Garden",["놀이터","물놀이","무료"],C,"미확인 — 방문 전 확인","","무료","운영 요일·시간 확인 필요.",B+"tabo4515/223760559054"),
 ("murrayrose","place",WATS,"i-wave","머레이 로즈 풀 (레드리프)","더블베이 무료 하버 수영장","그물로 둘러싼 잔잔한 하버풀과 보드워크. 현지인 비밀 장소로 소개돼요.","Murray Rose Pool Double Bay",["수영","무료"],C,"상시 개방","","무료","한국인 후기 3건 정도로 적어요.",B+"nojamsydney/224282012945"),
 ("blaxland","place",WEST,"i-ferris","블랙스랜드 리버사이드 파크","올림픽파크 대형 무료 놀이터","시드니 최대급 놀이터. 물놀이 시설 가동 여부는 확인되지 않았어요.","Blaxland Riverside Park",["놀이터","무료"],C,"상시 개방","","무료","후기 1건(유아 대상). CBD에서 20km 이상.",B+"narara_rara/224375674890"),
 ("birkenhead","place",WEST,"i-bag","버켄헤드 포인트 아울렛","드러모인 · 120여 매장","시내에서 가장 가까운 아울렛. 평은 갈려요.","Birkenhead Point Brand Outlet",["쇼핑"],C,"대략 10:00~17:30 (요일별 상이)","","","아이들 흥미는 낮아요.",B+"matjip32/224309742553"),
 ("bills","food",SURRY,"i-croissant","bills 서리힐스","리코타 핫케이크","핫케이크 약 $33. 한국 블로그는 대부분 서울 지점 글이라 시드니점 후기는 적어요.","bills Surry Hills",[],C,"미확인 — 방문 전 확인","","핫케이크 약 A$33","피크 시간 대기.",B+"y00n_59/224404601906"),
 ("reubenhills","food",SURRY,"i-coffee","Reuben Hills","브런치 · 커피","평은 좋지만 서리힐스 카페가 이미 많고 메뉴가 어른 취향.","Reuben Hills Surry Hills",[],C,"월~금 07:00~15:30 · 토·일 07:30~15:30","","미확인","항상 대기.",B+"bubn33/224272481385"),
 ("flyingbear","food","밀슨스포인트 · 커리빌리","i-coffee","The Flying Bear","커리빌리 물가 브런치","밀슨 파크 옆. 블로그에 인용된 구글 평점은 3.9.","The Flying Bear Kirribilli",[],C,"미확인 (블로그마다 다름)","","미확인","야외석 햇볕이 강해요. 노스 시드니 올림픽 풀 가는 날 후보.",B+"unnnnn_/224166197920"),
 ("lunesydney","food",CITYF,"i-croissant","Lune Croissanterie 시드니","크루아상","마틴플레이스 인근. 멜버른 본점이 이미 리스트에 있어요.","Lune Croissanterie Sydney",[],C,"미확인 — 방문 전 확인","","플레인 A$8 · 아몬드 A$12.50","멜버른을 안 가면 여기서.",B+"freehkkty/224244412984"),
 ("rivareno","food",CITYF,"i-honey","RivaReno Gelato","젤라또 · 피스타치오","바랑가루 등. 한 비교 글에서 1위였지만 후기 수는 적어요.","RivaReno Gelato Barangaroo",[],C,"미확인 — 방문 전 확인","","미확인","",B+"garie2885/224413305981"),
 ("harrys","food",CITYF,"i-ribs","Harry's Cafe de Wheels","타이거 파이 · 핫도그","울루물루의 오래된 파이 수레. 맛보다 명물로 들르는 곳.","Harry's Cafe de Wheels Woolloomooloo",[],C,"일~목 09:00~22:00 · 금 09:00~23:30 · 토 10:00~23:30","","미확인","야외 벤치에서 먹어야 해요.",B+"applemanggu/223785966738"),
 ("bettys","food",CITYF,"i-ribs","Betty's Burgers","버거 · 프로즌 커스터드","44 Market St 등. 아이들 한 끼로 무난한 체인.","Betty's Burgers Sydney CBD",[],C,"월~목 10:30~21:00 (그 외 미확인)","","버거 A$13.90 · 감자튀김 A$4.90","한국인 평은 미지근해요.",B+"rlawnwn__/224281453242"),
 ("operabar","food",CITYF,"i-sunset","Opera Bar","오페라하우스 아래 노을 한 잔","노을·야경 명소로 추천되지만 바예요.","Opera Bar Sydney",[],C,"미확인 — 방문 전 확인","","미확인","아이 입장 가능 시간 확인 필요. 매우 붐벼요.",B+"jungsonlove/224378615069"),
 ("theeight","food",CITYF,"i-noodle","The Eight","헤이마켓 얌차","카트 딤섬. 큰 홀이라 아이 동반에 편한 형식.","The Eight Modern Chinese Restaurant Haymarket",[],C,"미확인 — 방문 전 확인","","미확인","한국인 후기 1건.",B+"hl429/224380307968"),
 # ---- Sydney surrounds A
 ("scenicworld","place",BM,"i-train","시닉월드","레일웨이 · 스카이웨이 · 케이블웨이","블루마운틴 한국인 투어의 기본 코스. 타는 것 위주라 아이들이 덜 힘들어요.","Scenic World Katoomba",["전망","체험"],R,"평일 10:00~16:00 · 주말 09:00~17:00","","패스 약 A$35~57","시드니에서 약 2시간. 기차+버스나 투어로 차 없이 가능.",B+"billroad/224392654462"),
 ("echopoint","place",BM,"i-bridge2","에코포인트 & 세자매봉","블루마운틴 대표 전망대","평평하고 난간이 있는 전망대. 짧게 보고 가는 사진 명소.","Echo Point Lookout Three Sisters Katoomba",["전망","무료"],R,"상시 개방","","무료 (주차비 미확인)","",B+"sparklinglife/224364274486"),
 ("leura","place",BM,"i-leaf","로라마을","아기자기한 점심 마을","한국인 투어의 점심 정차지. 짧은 산책과 젤라또.","Leura Mall Leura NSW",["마을","산책"],R,"가게 대부분 17:00 무렵 마감","","무료","",B+"ebeblog/224268102286"),
 ("cafesana","food",BM,"i-noodle","Cafe Sana 로라","한국인 운영 · 비빔밥·불고기 덮밥","5/146 Leura Mall. 브런치 메뉴 옆에 한식이 있어 아이들 한 끼로 편해요.","Cafe Sana Leura",[],R,"08:30~16:00 무렵 (블로그마다 다름)","","미확인","",B+"hyun_ab_/224382989670"),
 ("josophans","food",BM,"i-honey","Josophan's Fine Chocolates","젤라또 · 초콜릿","로라마을에서 유명한 디저트 가게.","Josophan's Fine Chocolates Leura",[],R,"미확인 — 방문 전 확인","","미확인","",B+"joy3345/224406549212"),
 ("yellowdeli","food",BM,"i-ribs","The Yellow Deli","샌드위치 · 호빗집 인테리어","214 Katoomba St. 투어 가이드 추천 식당. 인테리어를 아이들이 좋아해요.","The Yellow Deli Katoomba",[],R,"일~목 10:00~22:00 · 금 10:00~16:00","토","미확인","토요일 휴무. 종교 공동체가 운영.",B+"maejiness/224221553573"),
 ("featherdale","place",BM,"i-koala","페더데일 야생동물공원","코알라 사진 · 캥거루 먹이주기","블루마운틴 가는 길 둔사이드. 쿼카도 있어요. 1.5~2시간이면 충분.","Featherdale Sydney Wildlife Park",["동물","체험"],R,"매일 08:00~17:00","","성인 A$42 · 어린이 A$28","더우니 8시 오픈에 맞춰 가기.",B+"chahyunin/224359418091"),
 ("bmsunsettour","place",BM,"i-sunset","블루마운틴 선셋 + 별보기 투어","한인 투어 · 오후 출발","페더데일 → 세자매봉 → 선셋 포인트 → 저녁 → 별 관측. 후기가 매우 많아요.","Blue Mountains Three Sisters",["투어","노을"],R,"오후 출발 · 밤 늦게 복귀","","1인 약 5.1만~7.5만원","2월 일몰이 19:50 무렵이라 복귀가 매우 늦어요. 일정에 링컨스락이 있으면 폐쇄 여부 확인.",B+"yoongzang/224417759503"),
 ("pstour","place",PS,"i-car","포트스테판 데이투어","한인 투어 · 돌고래+모래썰매","블루마운틴 다음으로 후기가 많은 당일 투어. 아이 동반 추천 글이 많아요.","Port Stephens Nelson Bay",["투어","동물"],R,"07:00 출발 · 편도 2.5시간","","1인 약 11.9만~17만원","긴 하루예요. 옵션을 줄이는 게 낫다는 엄마 후기가 있어요.",B+"pink0223/224426736450"),
 ("stockton","place",PS,"i-sun","스톡턴 모래언덕 모래썰매","사막과 바다가 만나는 곳","포트스테판 후기의 하이라이트. 애나베이 비루비 비치에서 4WD로 올라가요.","Birubi Beach sandboarding Anna Bay",["체험"],R,"업체별 상이 — 확인 필요","","미확인","그늘이 없고 모래가 뜨거워요. 양말·운동화 필수, 이른 시간에.",B+"sparklinglife/224390396943"),
 ("nelsonbay","place",PS,"i-wave","넬슨베이 돌핀크루즈","야생 돌고래 · 약 1.5시간","연중 돌고래를 볼 수 있는 잔잔한 만 크루즈.","Nelson Bay dolphin cruise d'Albora Marina",["동물","크루즈"],R,"업체·시간표 확인 필요","","미확인","",B+"aqua79440/224413866923"),
 ("oakvale","place",PS,"i-farm","오크베일 와일드라이프 파크","농장형 동물원 · 물놀이장","코알라 만지기, 왈라비·농장 동물 먹이주기. 스플래시 베이 물놀이장이 있어요.","Oakvale Wildlife Park Salt Ash",["동물","물놀이"],R,"매일 10:00~17:00 (입장 마감 16:00)","","미확인","투어가 아니면 차 필요.",B+"ssohee0726/224270081219"),
 ("symbio","place",SOUTH,"i-koala","심비오 와일드라이프 파크","한적한 동물원 + 무료 스플래시 파크","타롱가보다 좋았다는 후기가 있는 곳. 캥거루가 풀려 있고 쿼카 체험, 물놀이장·그늘 놀이터 포함.","Symbio Wildlife Park Helensburgh",["동물","물놀이","렌터카"],R,"매일 09:30~17:00","","성인 약 A$42 · 어린이 약 A$27 (2023년)","시드니에서 약 1시간, 차가 사실상 필요. 와타몰라·씨클리프 브릿지와 한 코스.",B+"nanusam1104/222971771182"),
 ("wattamolla","place",SOUTH,"i-wave","와타몰라 비치 & 라군","로열내셔널파크","한쪽은 라군, 한쪽은 바다. 얕고 잔잔한 라군이 아이들 물놀이에 좋아요.","Wattamolla Beach Royal National Park",["수영","피크닉","렌터카"],R,"공원 게이트 07:00~20:30","","차량 입장료 약 A$12","안전요원 없음. 더운 날엔 주차장이 차서 게이트를 닫기도 해요.",B+"mjlove373/224151824686"),
 ("seacliff","place",SOUTH,"i-bridge2","씨클리프 브릿지 & 볼드힐 전망대","남부해안 드라이브 첫 정차지","바다 위 다리와 행글라이더가 뜨는 전망대.","Bald Hill Lookout Stanwell Park",["전망","무료","렌터카"],R,"상시 개방","","무료","다리 보도는 그늘이 없어 한낮은 피하기.",B+"leeeeeee_life/224407222275"),
 ("nantien","place",SOUTH,"i-leaf","남천사 (Nan Tien Temple)","남반구 최대 불교 사원","울런공 투어 단골 코스. 45~60분의 조용한 정차지.","Nan Tien Temple Berkeley",["무료"],R,"화~일 09:00~17:00","월","무료","월요일 휴무. 단정한 복장.",B+"insmeer/224054280989"),
 ("kiamablowhole","place",KIAMA,"i-wave","키아마 블로우홀 & 등대","바닷물이 솟구치는 바위 구멍","난간 있는 전망대와 넓은 잔디. 기차로도 갈 수 있어요.","Kiama Blowhole",["전망","무료"],R,"상시 개방","","무료","남동 너울이 있어야 크게 솟구쳐요. 잔잔한 날엔 밋밋.",B+"nojamsydney/224392434844"),
 ("pennywhistlers","food",KIAMA,"i-coffee","Penny Whistlers","키아마 바다 뷰 브런치","5/31 Shoalhaven St. 항구 잔디가 내려다보이는 발코니.","Penny Whistlers Kiama",[],R,"일~수 07:00~15:00 · 목~토 07:00~22:00 무렵","","미확인","",B+"nojamsydney/224409472809"),
 ("southcoasttour","place",KIAMA,"i-car","남부해안 데이투어","한인 투어 · 볼드힐~게로아~키아마","포트스테판보다 이동이 짧은 당일 투어. 수영 시간은 없어요.","Sea Cliff Bridge Clifton",["투어"],R,"07:50 달링하버 출발","","성인 약 8.9만~9.4만원 (점심 별도)","최소 4명 출발.",B+"kjrang2/224420742437"),
 ("hyams","place",JB,"i-wave","하이암스 비치","세상에서 가장 하얀 모래","잔잔한 만이라 아이들 수영에 좋아요. 시드니에서 3시간이라 당일보다 1박 코스.","Hyams Beach NSW",["수영","렌터카"],R,"상시 개방","","무료","주차장이 작아 일찍. 그늘 없음, 2월 안전요원 여부 미확인.",B+"jenn_seoul/223902592989"),
 ("fivelittlepigs","food",JB,"i-coffee","5 Little Pigs","허스키슨 브런치","64-66 Owen St. 저비스베이 한국인 브런치 단골.","5 Little Pigs Huskisson",[],R,"미확인 — 방문 전 확인","","미확인","만석이 잦아요.",B+"myena_/224115683899"),
 ("palmbeach","place",NB,"i-sunset","팜비치 & 배런조이 등대","두 바다가 만나는 풍경","등대까지 1km 완만한 오르막. 아이와도 갈 만하다는 후기.","Barrenjoey Lighthouse Palm Beach",["전망","수영","렌터카"],R,"상시 개방","","무료","그늘이 없어 이른 아침이나 늦은 오후에. 피트워터 쪽이 잔잔해요.",B+"nojamsydney"),
 # ---- Sydney surrounds B
 ("kiamarockpool","place",KIAMA,"i-wave","키아마 락풀","블로우홀 옆 무료 해수풀","잔디와 화장실이 옆에 있는 바다 수영장.","Kiama Rock Pool Blowhole Point",["수영","무료"],C,"상시 개방","","무료","한국인 후기 1건. 안전요원 없음.",B+"nojamsydney/224392434844"),
 ("kiamafish","food",KIAMA,"i-ribs","키아마 항구 피시앤칩스","항구 앞 여러 가게","후기는 여럿이지만 가게 이름과 영업 여부를 확인하지 못했어요.","fish and chips Kiama harbour",[],C,"미확인 — 방문 전 확인","","미확인","",B+"leeeeeee_life/224408418005"),
 ("gerroaclub","food",KIAMA,"i-ribs","Gerroa Boat Fisherman's Club","세븐마일 비치 오션뷰 클럽","뷰가 환상적이라는 후기 1건. 키즈 메뉴 있음.","Gerroa Boat Fisherman's Club",[],C,"미확인 — 방문 전 확인","","미확인","클럽이라 입구에서 방문자 등록.",B+"psynara82/224404200227"),
 ("berrydonut","food",KIAMA,"i-honey","Berry Donut Van","1974년부터 시나몬 도넛","베리 마을의 명물 도넛 트럭.","Berry Donut Van Berry NSW",[],C,"미확인 — 방문 전 확인","","미확인","대기가 길다는 후기. 한국인 글 2~3건.",B+"robinsblog/223934572155"),
 ("jbdolphin","place",JB,"i-wave","저비스베이 돌핀크루즈","허스키슨 출발","한국인 근거가 패키지 투어 후기뿐이에요.","Jervis Bay dolphin cruise Huskisson",["동물","크루즈"],C,"업체·시간표 확인 필요","","미확인","",B+"mini_pink_moon/224423440508"),
 ("irukandji","place",PS,"i-wave","이루칸지 샤크 & 레이 인카운터","가오리·작은 상어 먹이주기","얕은 풀에 들어가 가오리에게 먹이를 줘요. 일부 실내라 덥거나 비 오는 날 대안.","Irukandji Shark and Ray Encounters Anna Bay",["동물","체험"],C,"매일 09:00~17:00","","성인 A$41 · 어린이 A$25","후기가 투어사 블로그 위주예요.",B+"kqlcsk551/223282014135"),
 ("reptilepark","place",CC,"i-roo","오스트레일리안 렙타일 파크","캥거루 먹이주기 · 파충류 쇼","서머스비. 피크닉·바베큐 공간 있음.","Australian Reptile Park Somersby",["동물","렌터카"],C,"09:00~17:00 (운영 요일 확인 필요)","","성인 A$49.99 · 어린이 A$32.99 · 가족 A$149.99","한국인 글 3건, 거주자 위주.",B+"evergreeneducation/223738396307"),
 ("terrigal","place",CC,"i-wave","테리갈 비치","센트럴코스트 해변 마을","카페와 피시앤칩스가 있는 타운 비치.","Terrigal Beach",["수영","렌터카"],C,"상시 개방","","무료","거주자 글 3건. 평일 안전요원 여부 미확인.",B+"sydney2seoul/224176194459"),
 ("pelican","place",CC,"i-farm","디 엔트런스 펠리칸 먹이주기","무료 · 15:30","펠리칸 광장에서 하는 먹이주기 행사.","Pelican Plaza The Entrance",["동물","무료","렌터카"],C,"15:30 (요일 확인 필요)","","무료","학기 중엔 수·토·일만이라는 글과 매일이라는 안내가 엇갈려요.",B+"blackruby_au/224297789456"),
 ("calmsley","place",WEST,"i-farm","캄슬리 힐 시티팜","젖 짜기 · 아기 염소 먹이주기","애보츠버리. 1시간이면 충분한 체험 농장. 코알라도 있어요.","Calmsley Hill City Farm",["동물","체험"],C,"평일 ~15:00 · 주말 ~16:00 (개장 시간 미확인)","","성인 A$34.50","한국인 후기 1건(최근, 긍정).",B+"sammyplace/224418890932"),
 ("hvgardens","place",CC,"i-leaf","헌터밸리 가든","동화 정원 · 아쿠아 골프","포콜빈. 와이너리 지역에서 아이들이 갈 만한 곳.","Hunter Valley Gardens Pokolbin",["정원","렌터카"],C,"매일 09:00~17:00 (입장 마감 16:00)","","미확인","2월엔 매우 더워요. 아이 관련 한국인 글 2건.","https://sydney2023.tistory.com/198"),
 ("newcastlebaths","place",PS,"i-wave","뉴캐슬·미어웨더 오션배스","대형 무료 해수 수영장","남반구 최대급 해수풀. 시드니에서 2시간 넘게 걸려요.","Merewether Ocean Baths",["수영","무료"],C,"청소일·개방 여부 확인 필요","","무료","수영보다 구경 위주 글이 많아요.",B+"hype_life/224277745926"),
 ("wollongonglight","place",SOUTH,"i-bridge2","울런공 등대 & 노스비치","플래그스태프 힐","울런공 일정의 잠깐 들르는 정차지.","Flagstaff Hill Lighthouse Wollongong",["전망","무료"],C,"상시 개방","","무료","스쳐가는 언급뿐이에요.",B+"soul21002/224276217834"),
 ("bilpin","place",BM,"i-farm","빌핀 과일농장","과일 따기 · 애플파이","직접 따는 과일 농장. 2월에 뭘 딸 수 있는지 확인 필요.","Bilpin Fruit Bowl",["체험","렌터카"],C,"평일 운영 여부 확인 필요","","미확인","한국인 글은 2020~21년 유학원 글.",B+"sydneykokos1/222043117447"),
 ("leuraeats","food",BM,"i-pizza","로라마을 기타 식당","Pizza Sublime · Leura Gourmet · Gia · Polar Bear","각 1~2건의 후기. 영업 여부 미확인.","Leura Mall restaurants",[],C,"미확인 — 방문 전 확인","","미확인","",B+"inyourlove2000/224382370503"),
 ("nelsonbayeats","food",PS,"i-ribs","넬슨베이 식당","Hog's Breath Cafe · Nero's Gelato","관광지 식당가. 각 1건의 후기.","Nelson Bay restaurants",[],C,"미확인 — 방문 전 확인","","미확인","",B+"sparklinglife/224390396943"),
 ("glenworth","place",CC,"i-farm","글렌워스 밸리 승마","센트럴코스트 승마 체험","최소 연령·가격·더위 운영 방침 미확인.","Glenworth Valley Outdoor Adventures",["체험","렌터카"],C,"미확인 — 방문 전 확인","","미확인","한국인 글 대부분 오래됨.",B+"sanglee7942"),
 ("sydneyzoo","place",WEST,"i-roo","시드니 주","번가리비 · 서부 시드니","아이들이 제일 좋아했다는 글이 있지만 후기가 적어요.","Sydney Zoo Bungarribee",["동물"],C,"미확인 — 방문 전 확인","","미확인","",B+"jenkim0516/224383112446"),
 # ---- Melbourne A
 ("qvm","place",MCBD,"i-cart","퀸 빅토리아 마켓","기념품 · 과일 · 핫 잼 도넛","한국인 필수 코스. 대부분 지붕 있는 구역이고 여름 체리·망고가 좋아요.","Queen Victoria Market Melbourne",["마켓","장보기"],R,"화·목·금 06:00~15:00 · 토 06:00~16:00 · 일 09:00~16:00","월수","입장 무료","월·수 휴무. 여행 중엔 2/14(일)·2/16(화)·2/18(목). 수요일 밤 서머 나이트마켓은 시즌 확인.",B+"jack0hee/224406582626"),
 ("donutkitchen","food",MCBDF,"i-honey","American Doughnut Kitchen","퀸빅토리아마켓 핫 잼 도넛","마켓 안 도넛 밴. 갓 튀긴 잼 도넛.","American Doughnut Kitchen Queen Victoria Market",[],R,"화·목·금 07:00~15:00 · 토·일 07:00~16:00","월수","10개 약 A$20","마켓 휴무일엔 쉬어요.",B+"solar7153/224365809918"),
 ("southmelbmarket","place",MSB,"i-cart","사우스 멜버른 마켓","더 깔끔한 로컬 마켓","퀸빅보다 유럽 느낌이라는 평. 굴·딤심, 아가테 크루아상.","South Melbourne Market",["마켓","장보기"],R,"수 08:00~16:00 · 금 08:00~17:00 · 토·일 08:00~16:00","월화목","입장 무료","여행 중엔 2/14(일)·2/17(수)만.",B+"smjd22/224353456608"),
 ("agathe","food","멜버른 · 사우스멜버른","i-croissant","Agathé Pâtisserie","아몬드·판단 크루아상","사우스 멜버른 마켓 안. 아몬드 크루아상 1위로 꼽혀요.","Agathé Pâtisserie South Melbourne Market",[],R,"마켓 운영일 (수·금·토·일)","월화목","미확인","피크엔 줄.",B+"melbebe/224319198324"),
 ("marketlane","food",MCBDF,"i-coffee","Market Lane Coffee","멜버른 3대 커피 · 라떼","462 Queen St, 퀸빅 옆. 마켓이 쉬는 날에도 열어요.","Market Lane Coffee Queen Street Melbourne",[],R,"월·수 08:00~15:00 · 화·목·금 08:00~17:00 · 토 07:00~17:00 · 일 08:00~17:00","","커피 약 A$5~6","서서 마시는 테이크아웃 위주.",B+"iammj_blog/224428098515"),
 ("patricia","food",MCBDF,"i-coffee","Patricia Coffee Brewers","멜버른 3대 커피 · 플랫화이트","493-495 Little Bourke St. 좌석 없는 스탠딩 바.","Patricia Coffee Brewers Melbourne",[],R,"월~금 07:00~16:00","토일","커피 약 A$5~6","주말 휴무.",B+"kaheee2/224398553352"),
 ("dukes","food",MCBDF,"i-coffee","Dukes Coffee Roasters","커피 · 드립백 선물","247 Flinders Lane. 드립백·원두가 선물로 인기.","Dukes Coffee Roasters Flinders Lane",[],R,"월~금 07:00~16:30 · 토 08:00~17:00","일","커피 약 A$4.5~6","일요일 휴무.",B+"simvely-/224402963516"),
 ("higherground","food",MCBDF,"i-croissant","Higher Ground","리코타 핫케이크 브런치","650 Little Bourke St. 옛 발전소를 개조한 높은 천장. 넓어서 가족 동반에 편해요.","Higher Ground Melbourne",[],R,"월·화 07:00~16:00 · 수~금 07:00~22:00 · 토 08:00~22:00 · 일 08:00~16:00","","메인 약 A$25~35","주말 브런치는 대기. 예약 가능.",B+"jack0hee/224337375573"),
 ("hectors","food",MCBDF,"i-ribs","Hector's Deli","토스트 샌드위치","430 Little Collins St. 버섯 멜트가 인기. 투어 전 아침이나 공원 피크닉용.","Hector's Deli Melbourne CBD",[],R,"매일 07:00~15:00","","샌드위치 약 A$15~20","테이크아웃 위주. 호불호가 갈려요.",B+"dojaki05/224351058234"),
 ("bricklane","food",MCBDF,"i-croissant","Brick Lane","멜버른 3대 브런치","33 Guildford Lane.","Brick Lane Guildford Lane Melbourne",[],R,"이른 오후 마감 (정확한 시간 미확인)","","미확인","맛있지만 비싸다는 평.",B+"wltjs29_/224407771361"),
 ("bakemono","food",MCBDF,"i-croissant","Bakemono Bakers","일본풍 크루아상","Drewery Lane. 룬과 비교되는 베이커리.","Bakemono Bakers Melbourne",[],R,"월~금 07:30~15:00 · 토·일 08:30~15:00","","미확인","늦으면 품절.",B+"afternoon_200104/224369802793"),
 ("piccolina","food",MCBDF,"i-honey","Piccolina Gelateria","젤라또","디그레이브스 스트리트 등. 피다피포와 함께 가장 많이 나오는 젤라또.","Piccolina Gelateria Degraves Street",[],R,"매일 12:00~23:00 (디그레이브스점)","","약 A$7~10","저녁엔 줄.",B+"dazdada/224416721426"),
 ("goodmeasure","food",MCARLF,"i-coffee","Good Measure","몽블랑 커피","193 Lygon St. 라이곤 스트리트·멜버른 뮤지엄과 묶기.","Good Measure Carlton",[],R,"월~금 07:30~15:30 · 토·일 08:00~15:30","","미확인","밤엔 바로 운영.",B+"cosqls/224386619139"),
 ("universal","food",MCARLF,"i-pizza","Universal Restaurant","가성비 파르마 · 파스타","139-141 Lygon St. 양 많고 저렴한 로컬 맛집.","Universal Restaurant Lygon Street Carlton",[],R,"일~목 11:00~23:00 · 금·토 11:00~23:30","","미확인","가족 동반에 편한 캐주얼 식당.",B+"dojaki05/224351012363"),
 ("tipo00","food",MCBDF,"i-pizza","Tipo 00","파스타 바","361 Little Bourke St. 멜버른 맛집 리스트 상위.","Tipo 00 Melbourne",[],R,"월~토 11:30~21:30","일","파스타 약 A$35~45","예약 사실상 필수. 일요일 휴무.",B+"solar7153/224350428381"),
 ("meatwinemel","food",MCBDF,"i-ribs","The Meat & Wine Co 사우스뱅크","야라강변 스테이크","Freshwater Place. 런치 세트가 가성비.","The Meat & Wine Co Southbank",[],R,"일~목 12:00~22:00 · 금·토 12:00~23:00","","런치 2코스 A$39 · 3코스 A$49","",B+"jack0hee/224387540075"),
 ("ngv","place",MSB,"i-palette","빅토리아 국립미술관 (NGV)","무료 · 키즈카페 같은 미술관","입구 물의 벽을 아이들이 좋아해요. 안내데스크에서 어린이 활동지를 줘요.","NGV International Melbourne",["실내","무료","우천대비"],R,"매일 10:00~17:00","","상설 무료 (특별전 유료)","",B+"kaheee2/224398553352"),
 ("rbgmelb","place",MSB,"i-leaf","로열 보타닉 가든 멜버른","피크닉 · 탠 트랙 조깅","한국인 피크닉 글이 많은 정원. 이안 포터 어린이 정원에 물놀이 요소가 있어요.","Royal Botanic Gardens Victoria Melbourne Gardens",["피크닉","조깅","무료"],R,"매일 07:30~일몰","","무료","어린이 정원은 학기 중 수~일만 열어 2/15(월)·2/16(화)엔 못 들어가요.",B+"honeymory/223844393261"),
 ("carltongardens","place",MCARL,"i-ferris","칼튼 가든 놀이터","멜버른 뮤지엄 옆","박물관 뒤 아이들을 풀어놓는 곳. 그늘나무가 많아요.","Carlton Gardens Playground Melbourne",["놀이터","무료"],R,"상시 개방","","무료","",B+"silverlight71/223748932612"),
 ("fedsquare","place",MCBD,"i-opera","페더레이션 광장 & 야라강변","무료 트램 구역","플린더스역 맞은편 광장과 강변 산책로. 도착 첫날 저녁 산책용.","Federation Square Melbourne",["산책","무료"],R,"상시 개방","","무료","",""),
 ("stkildabeach","place",MSTK,"i-sunset","세인트 킬다 비치 & 피어 펭귄","노을 · 야생 리틀펭귄","가장 많이 꼽히는 노을 명소. 잔잔한 만 해변과 놀이터.","St Kilda Pier penguin viewing",["노을","동물","수영"],R,"해변 상시 · 펭귄은 일몰 후","","무료","펭귄 관람은 무료지만 예약제(매주 화 10시 오픈, 금방 마감). 못 봤다는 후기도 있어요.",B+"kimsk960104/224069742581"),
 ("brighton","place",MSTK,"i-wave","브라이튼 비치 배싱 박스","알록달록 오두막","미들 브라이튼역에서 도보. 얕은 만이라 수영도 가능.","Brighton Bathing Boxes",["전망","수영","무료"],R,"상시 개방","","무료","그늘이 거의 없고 바람 부는 날은 추워요.",B+"thepantryjournal/224397051920"),
 ("phillipisland","place",MNEAR,"i-koala","필립 아일랜드 펭귄 퍼레이드","야생 리틀펭귄 · 데이투어","여행 하이라이트로 꼽히는 코스. 한인 투어는 퍼핑빌리·브라이튼·문릿과 묶어요.","Phillip Island Penguin Parade",["동물","투어","예약"],R,"펭귄은 2월 20:30 무렵 · 숙소 복귀 자정 무렵","","일반석 성인 A$34 · 어린이 A$17 · 가족 A$85","사전 예약 필수. 펭귄 촬영 금지, 겉옷 챙기기.",B+"rim2042/224413616361"),
 ("moonlit","place",MMORN,"i-roo","문릿 생추어리","캥거루·왈라비 먹이주기","모닝턴반도 초입. 7세·4세 아이 부모의 좋은 후기가 있어요.","Moonlit Sanctuary Wildlife Conservation Park",["동물","체험"],R,"매일 09:30~16:00","","성인 A$37 · 어린이 A$19","차 없이는 투어로. 야외라 더운 날 힘들어요.",B+"eoteot11/224405066221"),
 ("msac","place",MSTK,"i-wave","MSAC 수영장","알버트파크 · 실내 파도풀","당일권으로 들어가는 대형 수영장. 가족 탈의실, 실내 파도풀, 야외 50m.","Melbourne Sports and Aquatic Centre",["수영","실내"],R,"월~금 05:30~22:00 · 토 05:30~20:00 · 일 07:00~20:00","","성인 A$8.50 · 어린이 A$5.80 · 가족 A$21.40 (2024년)","파도풀은 평일 16~20시. 슬라이드는 운영 안 한다는 글. 랩풀은 깊어요.",B+"seowonsfamily/224362024351"),
 # ---- Melbourne B
 ("geelong","place",MNEAR,"i-wave","질롱 이스턴 비치","무료 어린이 풀 · 해수욕장","기차로 1시간. 2월 초 37도 날 아이와 다녀와 좋았다는 후기.","Eastern Beach Reserve Geelong",["수영","무료","물놀이"],C,"상시 개방 (안전요원 10:00~17:00, 시즌 확인)","","무료","거의 하루가 걸려요.",B+"silverlight71/223756400087"),
 ("lunaparkmel","place",MSTK,"i-ferris","루나 파크 멜버른","1912년 목조 롤러코스터","세인트킬다. 바다가 보이는 코스터.","Luna Park Melbourne",["놀이공원"],C,"학기 중 토·일 11:00~18:00","월화수목금","미확인","여행 중엔 2/14(일)만 가능.",B+"trip_dhmom/224401895060"),
 ("babubudan","food",MCBDF,"i-coffee","Brother Baba Budan","커피","Little Bourke St. 세븐시즈 자매점.","Brother Baba Budan",[],C,"월~수 07:00~17:00 · 목·금 07:00~18:00 · 토·일 08:00~18:00","","미확인","좌석 적음. 라떼가 쓰다는 후기.",""),
 ("maxhardware","food",MCBDF,"i-pizza","Max on Hardware","캥거루 스테이크 · 피자·파스타","54-58 Hardware Lane.","Max on Hardware Melbourne",[],C,"매일 12:00~23:00","","미확인","평이 갈려요. 아이들은 피자·파스타.",B+"o0o_522/224352543769"),
 ("dragonhotpot","food",MCBDF,"i-noodle","Dragon Hot Pot","마라탕","러셀 스트리트점 추천. 한국인에게 인기지만 매워요.","Dragon Hot Pot Russell Street Melbourne",[],C,"미확인 — 방문 전 확인","","미확인","안 매운 국물 선택 가능 여부 확인.",B+"bubn33/224264761458"),
 ("bykorea","food",MCBDF,"i-noodle","By Korea","한식당","구글 4.6이라는 블로그 인용. 주소·영업 여부 미확인.","By Korea Melbourne",[],C,"미확인 — 방문 전 확인","","미확인","",B+"fleetgogo/224354368027"),
 ("pinkflake","food","멜버른 · 사우스멜버른","i-ribs","Pink Flake Fish & Chips","세인트킬다 피시앤칩스","노을 보기 전 들르는 곳. 한국인 글 2건.","Pink Flake Fish and Chips St Kilda",[],C,"미확인 — 방문 전 확인","","미확인","장기 휴업 후 재개했다는 정보, 영업 확인.",B+"iammj_blog/224412390664"),
 ("librarydock","place",MCBD,"i-palette","라이브러리 앳 더 독","도클랜드 무료 실내 키즈 공간","하버 뷰 도서관과 놀이터. 장기 체류 가족 글 위주.","Library at the Dock",["실내","무료"],C,"미확인 (안내마다 다름)","","무료","",B+"leesungmingo/224155648236"),
 ("gimlet","food",MCBDF,"i-ribs","Gimlet at Cavendish House","파인다이닝","평은 매우 좋지만 비싸고 어른 분위기.","Gimlet at Cavendish House",[],C,"미확인 — 방문 전 확인","","미확인","예약 필수. 아이 동반엔 맞지 않아요.",B+"dbtjfghk3199/224345100009"),
]

out = []
for r in ROWS:
    (i, kind, region, icon, title, sub, desc, q, tags, badge, hours, closed, price, note, src) = r
    d = {"id": i, "kind": kind, "region": region, "icon": icon, "title": title,
         ("sub" if kind == "place" else "sig"): sub, "desc": desc, "q": q, "badge": badge,
         "hours": hours, "closed": list(closed), "price": price, "note": note, "src": src,
         "verified": "blog" if "blog.naver" in src or "tistory" in src else ("official" if src else "")}
    if kind == "place":
        d["tags"] = tags
    out.append(d)
ids = [d["id"] for d in out]
assert len(ids) == len(set(ids)), [x for x in ids if ids.count(x) > 1]
Path(__file__).with_name("extra.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(len(out), "items", sum(d["kind"] == "place" for d in out), "places", sum(d["kind"] == "food" for d in out), "food")
