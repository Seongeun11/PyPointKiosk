#my_package\model\main_menu_model.py
class MainMenuModel:
    def __init__(self):
        pass 
    def on_print_message(self):
        # 서비스 시작 시 필요한 초기화 작업 수행
        print("MainMenuModel이 시작되었습니다.")
    
    def set_text(self,message:str):
        if message == "ja_jpy":
            self._text = "注文する"
        elif message == "ko_jpy":
            self._text = "주문하기 (엔화)"
        elif message == "ko_krw":
            self._text = "주문하기 (원화)"
        else:
            self._text = "주문하기"
        return self._text

    def get_text(self):
        
        return self._text