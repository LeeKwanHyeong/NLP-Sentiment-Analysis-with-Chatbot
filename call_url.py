def call_url():
    url_dict = {
        'CameraFi': 'https://play.google.com/store/apps/details?id=com.vaultmicro.camerafi.live&hl=ko&gl=US&showAllReviews=true',
        'V_app': 'https://play.google.com/store/apps/details?id=com.naver.vapp&hl=ko&gl=US&showAllReviews=true',
        'Mobizen': 'https://play.google.com/store/apps/details?id=com.rsupport.mobizen.live&hl=ko&gl=US&showAllReviews=true',
        'Bigolive': 'https://play.google.com/store/apps/details?id=sg.bigo.live&hl=ko&gl=US&showAllReviews=true',
        'Omlet': 'https://play.google.com/store/apps/details?id=mobisocial.arcade&hl=ko&gl=US&showAllReviews=true',
        'Sgether': 'https://play.google.com/store/apps/details?id=com.sgrsoft.streetgamer&hl=ko&gl=US&showAllReviews=true'}
    return url_dict


def select_url():
    url_list = [
        'https://play.google.com/store/apps/details?id=com.vaultmicro.camerafi.live&hl=ko&gl=US&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=com.naver.vapp&hl=ko&gl=US&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=com.rsupport.mobizen.live&hl=ko&gl=US&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=sg.bigo.live&hl=ko&gl=US&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=mobisocial.arcade&hl=ko&gl=US&showAllReviews=true',
        'https://play.google.com/store/apps/details?id=com.sgrsoft.streetgamer&hl=ko&gl=US&showAllReviews=true']

    check_num = int(input(
        "원하는 회사를 고르시오: \n" + "[0]:CameraFi\n" + "[1]:V_App\n" + "[2]:BigoLive\n" + "[3]:Mobizen\n" + "[4]:Omlet\n" + "[5]:Sgether\n"))

    name = check_num
    if (name == 0):
        CameraFi_live = url_list[0]
        checking_url = [CameraFi_live, 'CameraFi']
        checked = checking_url[0], checking_url[1]

    elif (name == 1):
        V_App = url_list[1]
        checking_url = [V_App, 'V_App']
        checked = checking_url[0], checking_url[1]

    elif (name == 2):
        Mobizen = url_list[2]
        checking_url = [Mobizen, 'Mobizen']
        checked = checking_url[0], checking_url[1]

    elif (name == 3):
        Bigolive = url_list[3]
        checking_url = [Bigolive, 'Bigolive']
        checked = checking_url[0], checking_url[1]

    elif (name == 4):
        Omlet = url_list[4]
        checking_url = [Omlet, 'Omlet']
        checked = checking_url[0], checking_url[1]
    elif (name == 5):
        Sgether = url_list[5]
        checking_url = [Sgether, 'Sgether']
        checked = checking_url[0], checking_url[1]
    return checked