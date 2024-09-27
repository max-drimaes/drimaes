# 특별 문서 유형 처리 ('협회가입신청서')
def process_special_approval_line():
    nonlocal order

    gwp_center_head = 'GWP 센터장'

    if not is_cri_member:
        # 중앙기술연구소 외부
        if selected_role == '팀원':
            add_approver_if_not_exists(get_next_approver())  # 팀장
            add_approver_if_not_exists(center_head)          # 센터장
            add_agreement_if_not_exists('해그리드')            # 전략실(해그리드)
            add_agreement_if_not_exists(gwp_center_head)     # GWP 센터장
            if amount >= 1000000:
                add_approver_if_not_exists('아이언맨')        # 아이언맨
        elif selected_role == '팀장':
            add_approver_if_not_exists(center_head)          # 센터장
            add_agreement_if_not_exists('해그리드')            # 전략실(해그리드)
            add_agreement_if_not_exists(gwp_center_head)     # GWP 센터장
            if amount >= 1000000:
                add_approver_if_not_exists('아이언맨')        # 아이언맨
    else:
        # 중앙기술연구소 소속
        if selected_role == '팀원':
            add_approver_if_not_exists(get_next_approver())  # 팀장
            add_approver_if_not_exists(center_head)          # 센터장
            if leadership != center_head:
                add_approver_if_not_exists(leadership)      # 중앙기술연구소장
            add_agreement_if_not_exists('해그리드')            # 전략실
            add_agreement_if_not_exists(gwp_center_head)     # GWP 센터장
            if amount >= 1000000:
                add_approver_if_not_exists('아이언맨')        # 아이언맨
        elif selected_role == '팀장':
            add_approver_if_not_exists(center_head)          # 센터장
            if leadership != center_head:
                add_approver_if_not_exists(leadership)      # 중앙기술연구소장
            add_agreement_if_not_exists('해그리드')            # 전략실
            add_agreement_if_not_exists(gwp_center_head)     # GWP 센터장
            if amount >= 1000000:
                add_approver_if_not_exists('아이언맨')        # 아이언맨
