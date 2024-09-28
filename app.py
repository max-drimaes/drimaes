import streamlit as st

# 문서별로 결재 라인 유형 분류
document_types = {
    "A유형": [],
    "B유형": ['휴가신청서', '국내출장 신청서'],
    "C유형": ['국내출장 결과보고 및 정산신청서', '휴일대체근무신청서', '경조사비용 신청서'],
    "D유형": ['시간외근로 사전신청서', '시간외근로 결과보고서', '근태취소신청서'],
    "E유형": ['입금품의', '거래처등록신청서', '선급정산신청서'],
    "F유형": ['품의서', '계약품의서', '해외출장 신청서'],
    "G유형": [
        '지출승인요청서(법인카드)',
        '구매(용역)요청서-계좌이체/법인카드',
        '지급품의(정기/수시/기타)_세금계산서',
        '선급금신청서',
        '교육 신청서',
        '교육결과보고서',
        '경비청구신청서(개인카드, 영수증)'
    ],
    "H유형": [
        '지출승인요청서(법인카드)',
        '구매(용역)요청서-계좌이체/법인카드',
        '지급품의(정기/수시/기타)_세금계산서',
        '선급금신청서',
        '교육 신청서',
        '교육결과보고서',
        '세금계산서 발행요청서',
        '경비청구신청서(개인카드, 영수증)'
    ],
    "공문서": ['공문서'],
    "회원가입완료보고서": ['회원가입완료보고서'],
    "협회가입신청서": ['협회가입신청서']
}

# 금액 입력이 필요한 문서 목록 (거래처등록신청서 제거)
documents_requiring_amount = [
    '입금품의',
    # '거래처등록신청서',  # 제거됨
    '선급정산신청서',
    '지출승인요청서(법인카드)',
    '구매(용역)요청서-계좌이체/법인카드',
    '지급품의(정기/수시/기타)_세금계산서',
    '선급금신청서',
    '교육 신청서',
    '교육결과보고서',
    '경비청구신청서(개인카드, 영수증)',
    '외화송금신청서'
]

# 1000 단위로 쉼표 추가 함수
def format_number_with_commas(number):
    try:
        number = int(number)
        return f"{number:,}"
    except (ValueError, TypeError):
        return ""

# 문서 목록 중복 제거 함수
def remove_duplicates(doc_list):
    return list(dict.fromkeys(doc_list))

# 문서 목록 가져오기
def get_all_documents():
    all_documents = []
    for docs in document_types.values():
        all_documents.extend(docs)
    return sorted(remove_duplicates(all_documents))

# 센터 및 팀 정보
team_dict = {
    'Alliance 센터': ['기술개발', '기술제휴', '마케팅', '사업개발'],
    'Design 센터': ['팀 없음'],
    '선행 R&D 센터': ['솔루션개발', 'CTIO'],
    '전장 R&D 센터': ['HW설계', '임베디드SW설계', '제어기SW설계']
}

# 리더십 매칭 정보
leadership_matching = {
    'Alliance 센터': '아이언맨',
    '선행 R&D 센터': '중앙기술연구소장',
    '전장 R&D 센터': '중앙기술연구소장',
    'Design 센터': '중앙기술연구소장'
}

# 센터장 이름 매칭
center_heads = {
    'Alliance 센터': 'Alliance 센터장',
    'Design 센터': 'Design 센터장',
    '선행 R&D 센터': '선행 R&D 센터장',
    '전장 R&D 센터': '전장 R&D 센터장',
}

# 역할 목록 기본값 (팀원, 팀장)
default_roles = ['팀원', '팀장']

# HR&GA 팀 합의 필요한 문서
hr_documents = [
    '휴가신청서',
    '국내출장 신청서',
    '시간외근로 사전신청서',
    '시간외근로 결과보고서',
    '근태취소신청서',
    '휴일대체근무신청서',
    '공문서',
    '해외출장 신청서',
    '교육 신청서',
    '교육결과보고서'
]

# Finance 팀 합의 필요한 문서
finance_documents = [
    '국내출장 결과보고 및 정산신청서',
    '경조사비용 신청서',
    '입금품의',
    '세금계산서 발행요청서',
    '거래처등록신청서',
    '경비청구신청서(개인카드, 영수증)',
    '지출승인요청서(법인카드)',
    '지급품의(정기/수시/기타)_세금계산서',
    '선급금신청서',
    '선급정산신청서',
    '외화송금신청서'
]

# 중앙기술연구소장과 선행 R&D 센터장이 동일인물인지 여부
def is_same_person(role1, role2):
    same_person_roles = [('중앙기술연구소장', '선행 R&D 센터장')]
    return (role1, role2) in same_person_roles or (role2, role1) in same_person_roles

# 결재 라인 생성 함수
def generate_approval_line(selected_center, selected_team, selected_role, selected_document, amount):
    # 중앙기술연구소 소속 여부 확인
    cri_centers = ['선행 R&D 센터', '전장 R&D 센터', 'Design 센터']
    is_cri_member = selected_center in cri_centers

    # 결재 라인 초기화
    approval_line = []
    approver_set = set()

    order = 1  # order 변수 초기화

    # 결재자 및 합의자 지정 함수
    def add_approver_if_not_exists(approver):
        nonlocal order
        if approver and approver not in approver_set:
            approval_line.append((order, '결재', approver))
            approver_set.add(approver)
            order += 1

    def add_agreement_if_not_exists(agreer):
        nonlocal order
        if agreer and agreer not in approver_set:
            approval_line.append((order, '합의', agreer))
            approver_set.add(agreer)
            order += 1

    # 센터장 결정
    center_head = center_heads.get(selected_center, f"{selected_center.replace(' 센터', '')} 센터장")

    # 만약 center_head와 '중앙기술연구소장'이 동일인물인지 여부
    if is_same_person(center_head, '중앙기술연구소장'):
        center_head = '중앙기술연구소장'

    # 차상위 결재자 결정
    def get_next_approver():
        if selected_role == '팀원':
            if selected_team != '팀 없음':
                return f"{selected_team} 팀장"
            else:
                return center_head
        elif selected_role == '팀장':
            return center_head
        else:
            return '아이언맨'

    # 리더십 매칭 결재자 결정
    def get_leadership_matching():
        return leadership_matching.get(selected_center, '아이언맨')

    # 합의자 결정 (HR&GA 또는 Finance 팀원)
    def get_agreement_team():
        if selected_document in hr_documents:
            return 'HR&GA 팀원'
        elif selected_document in finance_documents:
            return 'Finance 팀원'
        else:
            return None

    # 문서 유형 가져오기
    document_type = None
    for dtype, docs in document_types.items():
        if selected_document in docs:
            document_type = dtype
            break

    # 금액 조건에 따른 문서 유형 조정
    if selected_document in ['교육 신청서', '교육결과보고서']:
        if amount >= 1000000:
            document_type = "H유형"
        else:
            document_type = "G유형"
    elif selected_document in ['지출승인요청서(법인카드)', '경비청구신청서(개인카드, 영수증)']:
        if amount >= 500000:
            document_type = "H유형"
        else:
            document_type = "G유형"
    elif selected_document in ['구매(용역)요청서-계좌이체/법인카드', '선급금신청서', '지급품의(정기/수시/기타)_세금계산서']:
        if amount >= 3000000:
            document_type = "H유형"
        else:
            document_type = "G유형"

    # 결재 라인 생성 로직
    def process_approval_line():
        nonlocal order

        next_approver = get_next_approver()
        leadership = get_leadership_matching()
        agreement_team = get_agreement_team()
        gwp_center_head = 'GWP 센터장'

        # '협회가입신청서'에 대한 특수 로직 적용
        if selected_document == '협회가입신청서':
            # 제공된 조건에 따라 결재 라인 생성
            if not is_cri_member:
                # 중앙기술연구소 외부
                if selected_role == '팀원':
                    add_approver_if_not_exists(next_approver)  # 팀장
                    add_approver_if_not_exists(center_head)  # 해당 센터장
                    add_agreement_if_not_exists('해그리드')     # 전략실(해그리드)
                    add_agreement_if_not_exists(gwp_center_head)
                    add_approver_if_not_exists('중앙기술연구소장')  # 중앙기술연구소장으로 변경
                    add_approver_if_not_exists('아이언맨')
                elif selected_role == '팀장':
                    add_approver_if_not_exists(center_head)
                    add_agreement_if_not_exists('해그리드')
                    add_agreement_if_not_exists(gwp_center_head)
                    add_approver_if_not_exists('중앙기술연구소장')  # 중앙기술연구소장으로 변경
                    add_approver_if_not_exists('아이언맨')
            else:
                # 중앙기술연구소 소속
                if selected_role == '팀원':
                    add_approver_if_not_exists(next_approver)  # 팀장
                    add_approver_if_not_exists(center_head)
                    add_approver_if_not_exists('중앙기술연구소장')  # 중앙기술연구소장 추가
                    add_agreement_if_not_exists('해그리드')
                    add_agreement_if_not_exists(gwp_center_head)
                    add_approver_if_not_exists('아이언맨')
                elif selected_role == '팀장':
                    add_approver_if_not_exists(center_head)
                    add_approver_if_not_exists('중앙기술연구소장')  # 중앙기술연구소장 추가
                    add_agreement_if_not_exists('해그리드')
                    add_agreement_if_not_exists(gwp_center_head)
                    add_approver_if_not_exists('아이언맨')
        else:
            # 기존 로직 유지
            # 각 문서 유형에 따른 결재 라인 생성

            if document_type == 'A유형':
                add_approver_if_not_exists(next_approver)

            elif document_type == 'B유형':
                add_approver_if_not_exists(next_approver)
                if agreement_team:
                    add_agreement_if_not_exists(agreement_team)
                add_agreement_if_not_exists(gwp_center_head)

            elif document_type == 'C유형':
                if selected_role == '팀원':
                    add_approver_if_not_exists(next_approver)
                    add_approver_if_not_exists(center_head)
                elif selected_role == '팀장':
                    add_approver_if_not_exists(center_head)
                if agreement_team:
                    add_agreement_if_not_exists(agreement_team)
                add_agreement_if_not_exists(gwp_center_head)

            elif document_type == 'D유형':
                if selected_role == '팀원':
                    add_approver_if_not_exists(next_approver)
                elif selected_role == '팀장':
                    add_approver_if_not_exists(center_head)
                if agreement_team:
                    add_agreement_if_not_exists(agreement_team)
                add_agreement_if_not_exists(gwp_center_head)

            elif document_type == 'E유형':
                if selected_role == '팀원':
                    add_approver_if_not_exists(next_approver)
                    add_approver_if_not_exists(center_head)
                elif selected_role == '팀장':
                    add_approver_if_not_exists(center_head)
                if agreement_team:
                    add_agreement_if_not_exists(agreement_team)

            elif document_type in ['F유형', 'H유형', '공문서']:
                if selected_role == '팀원':
                    add_approver_if_not_exists(next_approver)
                    add_approver_if_not_exists(center_head)
                elif selected_role == '팀장':
                    add_approver_if_not_exists(center_head)
                if selected_center in ['Design 센터', '전장 R&D 센터']:
                    add_approver_if_not_exists('중앙기술연구소장')  # 센터장 뒤에 중앙기술연구소장 추가
                if agreement_team:
                    add_agreement_if_not_exists(agreement_team)
                add_agreement_if_not_exists(gwp_center_head)
                if is_cri_member:
                    add_approver_if_not_exists('중앙기술연구소장')  # 전략실장 대신 중앙기술연구소장
                add_approver_if_not_exists('아이언맨')

            elif document_type == 'G유형':
                if selected_role == '팀원':
                    add_approver_if_not_exists(next_approver)
                    add_approver_if_not_exists(center_head)
                elif selected_role == '팀장':
                    add_approver_if_not_exists(center_head)
                if selected_center in ['Design 센터', '전장 R&D 센터']:
                    add_approver_if_not_exists('중앙기술연구소장')  # 센터장 뒤에 중앙기술연구소장 추가
                if agreement_team:
                    add_agreement_if_not_exists(agreement_team)

            elif document_type == '회원가입완료보고서':
                add_approver_if_not_exists(next_approver)

            else:
                add_approver_if_not_exists(next_approver)

    process_approval_line()

    # 결재라인 정렬
    approval_line = sorted(approval_line, key=lambda x: x[0])

    # 결과 문자열 생성
    approval_line_str = ''
    for i, action, name in approval_line:
        approval_line_str += f"{i}. {action}: {name}\n"

    return approval_line_str.strip()

# 메인 함수
def main():
    st.title("DRIMAES 결재 라인 생성기")

    st.markdown("""
    ### 결재 라인에 대한 설명
    - 결재 라인은 문서의 결재 과정을 나타내는 흐름도이며, 각 문서의 종류과 권한에 따라 결재자와 합의자가 결정됩니다.
    - 결재는 발신부서와 수신부서의 개념을 뜻하지만, 비즈박스 특성상 이를 구현할 수 없으므로 결재자와 합의자로 구분합니다.
    - 기본적인 흐름은 **발신부서 결재 완료** 후, **수신부서 합의 완료**의 흐름입니다.
    - 다만, 최상위 결재자인 **아이언맨**과 **백호**의 경우 **수신부서** (보통 GWP 센터)의 합의가 끝난 후 결재를 진행합니다.
    - 결재 라인이 심플한 센터와 전략실은 제외하였습니다.
    """)

    # 센터 선택
    selected_center = st.selectbox("센터 선택", sorted(list(team_dict.keys())))
    teams = team_dict.get(selected_center, ['팀 없음'])

    # 팀 선택
    selected_team = st.selectbox("팀 선택", teams)

    # 역할 선택 (디자인 센터일 경우 팀장 제외)
    if selected_center == 'Design 센터':
        available_roles = ['팀원']
    else:
        available_roles = default_roles
    selected_role = st.selectbox("역할 선택", available_roles)

    # 문서 선택
    selected_document = st.selectbox("문서 선택", get_all_documents())

    # 금액 입력 필드 조건부 표시 (거래처등록신청서 제외)
    if selected_document in documents_requiring_amount:
        amount_input = st.number_input("금액 입력 (원)", min_value=0, value=0, step=1000)
        formatted_amount = format_number_with_commas(amount_input)
        st.write(f"입력된 금액: {formatted_amount} 원")
    else:
        amount_input = 0

    # 버튼 클릭 시 결재 라인 생성
    if st.button("결재 라인 생성"):
        approval_line_str = generate_approval_line(
            selected_center, selected_team, selected_role, selected_document, amount_input
        )
        st.subheader("결재 라인:")
        st.text(approval_line_str)

if __name__ == "__main__":
    main()
