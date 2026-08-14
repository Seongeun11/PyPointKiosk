#src\my_package\repositories\excel_receipt_repository.py
import os
import json
from datetime import datetime, timedelta
from typing import Optional

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter  # Import 추가로 모듈 에러 해결

class ReceiptRepositoryModel:
    """
    영수증 일자별 JSON 저장 및 엑셀 보고서 변환 비즈니스 Model
    - 결제 내역을 영업일 기준 날짜별 파일(receipts_YYYY-MM-DD.json)로 나누어 저장 관리
    - 새벽 02:00 이전 결제건은 전일(어제) 영업일 매출로 저장됨
    """
    
    # 영업 마감 오프셋 (새벽 2시 영업 마감 기준)
    CLOSING_OFFSET_HOURS = 2

    def __init__(self, base_receipts_dir="resources/receipts", products_path="resources/products.json"):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.receipts_dir = os.path.join(self.base_dir, base_receipts_dir)
        self.products_path = os.path.join(self.base_dir, products_path)
        
        # 날짜별 영수증 폴더 생성
        os.makedirs(self.receipts_dir, exist_ok=True)

    def _get_business_date_str(self, dt: Optional[datetime] = None) -> str:
        """영업일 기준 YYYY-MM-DD 문자열 반환 (새벽 2시 미만은 전일 날짜)"""
        if dt is None:
            dt = datetime.now()
        business_dt = dt - timedelta(hours=self.CLOSING_OFFSET_HOURS)
        return business_dt.strftime("%Y-%m-%d")

    def _get_daily_file_path(self, date_str: Optional[str] = None) -> str:
        """지정한 날짜(YYYY-MM-DD) 또는 현재 영업일 날짜의 JSON 파일 경로 반환"""
        if not date_str:
            date_str = self._get_business_date_str()
        filename = f"receipts_{date_str}.json"
        return os.path.join(self.receipts_dir, filename)

    def _load_receipts_by_path(self, file_path: str) -> list:
        """특정 경로의 JSON 영수증 파일 로드"""
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Model Error] 영수증 파일 읽기 실패 ({file_path}): {e}")
            return []

    def add_receipt(self, pay_type: str, cart_items: list, purchase_amount: int, 
                    discount_type: str, discount_amount: int, final_amount: int,
                    currency: str = "KRW") -> dict:
        """결제 완료 시 영업일 기준 JSON 파일에 영수증 추가 (통화 단위 currency 명시 저장)"""
        now = datetime.now()
        business_date_str = self._get_business_date_str(now)
        daily_file_path = self._get_daily_file_path(business_date_str)

        receipts = self._load_receipts_by_path(daily_file_path)

        # 당일 결제 건수 기준 순번 (1 ~ 999)
        next_id = (len(receipts) % 999) + 1

        receipt_data = {
            "id": next_id,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "pay_type": pay_type,                     
            "discount_type": discount_type,           
            "currency": currency,                       # 통화 정보 기록 ('JPY' / 'KRW')
            "purchase_amount": purchase_amount,
            "discount_amount": discount_amount,
            "final_amount": final_amount,
            "items": cart_items                       
        }

        receipts.append(receipt_data)

        # 영업일자별 JSON 파일에 저장
        try:
            with open(daily_file_path, "w", encoding="utf-8") as f:
                json.dump(receipts, f, ensure_ascii=False, indent=2)
                print(f"[Model] 영수증 저장 완료 (통화: {currency}, 영업일: {business_date_str}): {daily_file_path}")
        except Exception as e:
            print(f"[Model Error] 영수증 저장 실패: {e}")

        return receipt_data

    def get_receipts_by_date(self, date_str: Optional[str] = None) -> list:
        """특정 영업일 날짜(YYYY-MM-DD)의 영수증 목록 조회"""
        file_path = self._get_daily_file_path(date_str)
        return self._load_receipts_by_path(file_path)

    def get_all_receipts(self) -> list:
        """모든 날짜의 영수증 목록을 병합하여 조회"""
        all_receipts = []
        if os.path.exists(self.receipts_dir):
            for filename in sorted(os.listdir(self.receipts_dir)):
                if filename.startswith("receipts_") and filename.endswith(".json"):
                    path = os.path.join(self.receipts_dir, filename)
                    all_receipts.extend(self._load_receipts_by_path(path))
        return all_receipts

    def export_to_excel(self, export_file_path: str, target_date: Optional[str] = None) -> bool:
        """
        [완벽 이미지 매칭 로직]
        - 이미지 양식(A~T열 레이아웃, 셀 병합, 헤더 구성)과 100% 동일한 일일 판매 보고서 생성
        - 엔화/현금/계좌 수량 집계 및 정확한 엑셀 수식 작성
        - 최하단에 엔화/원화 독립 매출 합계 행 추가
        """
        if not target_date:
            target_date = self._get_business_date_str()

        receipts = self.get_receipts_by_date(target_date)
        
        # 1. products.json Master ID 및 카테고리 정보 로드
        stats = {}
        if os.path.exists(self.products_path):
            try:
                with open(self.products_path, "r", encoding="utf-8") as f:
                    cat_data = json.load(f).get("categories", [])
                    for cat in cat_data:
                        c_name = cat.get("name", "미지정")
                        for p in cat.get("products", []):
                            prod_id = str(p.get("id"))
                            stats[prod_id] = {
                                "id": prod_id,
                                "name": p.get("name", ""),
                                "category": c_name,
                                "price": p.get("price", 0),
                                "disc_cash": 0, "disc_bank": 0, "disc_jpy": 0,
                                "norm_cash": 0, "norm_bank": 0, "norm_jpy": 0,
                                "acad_cash": 0, "acad_bank": 0,
                                "point_qty": 0, "total_qty": 0
                            }
            except Exception as e:
                print(f"[Model Error] 상품 목록 로드 실패: {e}")

        # 2. 영수증 내역 집계
        for r in receipts:
            p_type = r.get("pay_type")        # cash, bank, point 등
            d_type = r.get("discount_type")   # student, academy, none
            currency = r.get("currency", "KRW")
            items = r.get("items", [])

            for item in items:
                prod_id = str(item.get("id", item.get("name")))
                name = item.get("name", "미등록상품")
                qty = item.get("quantity", 0)
                item_currency = item.get("currency", currency)

                if prod_id not in stats:
                    stats[prod_id] = {
                        "id": prod_id,
                        "name": name,
                        "category": "기타", 
                        "price": item.get("price", 0),
                        "disc_cash": 0, "disc_bank": 0, "disc_jpy": 0,
                        "norm_cash": 0, "norm_bank": 0, "norm_jpy": 0,
                        "acad_cash": 0, "acad_bank": 0,
                        "point_qty": 0, "total_qty": 0
                    }

                st = stats[prod_id]
                st["total_qty"] += qty

                if p_type == "point":
                    st["point_qty"] += qty
                elif item_currency == "JPY": # 엔화 결제건
                    if d_type == "student":
                        st["disc_jpy"] += qty
                    else:
                        st["norm_jpy"] += qty
                elif d_type == "student": # 수련생 할인
                    if p_type == "cash": st["disc_cash"] += qty
                    elif p_type == "bank": st["disc_bank"] += qty
                elif d_type == "academy": # 아카데미 할인
                    if p_type == "cash": st["acad_cash"] += qty
                    elif p_type == "bank": st["acad_bank"] += qty
                else: # 일반
                    if p_type == "cash": st["norm_cash"] += qty
                    elif p_type == "bank": st["norm_bank"] += qty

        # 3. 엑셀 워크북 및 시트 초기화
        wb = openpyxl.Workbook()
        ws = wb.active

        if ws is None or not isinstance(ws, Worksheet):
            ws = wb.create_sheet(title="일일 판매 보고서")
        else:
            ws.title = "일일 판매 보고서"

        # 4. 서식 및 스타일 정의
        font_title = Font(name="맑은 고딕", size=14, bold=True)
        font_header = Font(name="맑은 고딕", size=9, bold=True)
        font_data = Font(name="맑은 고딕", size=9)
        font_sum = Font(name="맑은 고딕", size=10, bold=True) # 합계행 강조 폰트
        
        fill_green = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        fill_sub_title = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
        fill_sum_row = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # 합계행 연노랑 배경

        thin_border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )
        align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
        align_right = Alignment(horizontal='right', vertical='center')
        align_left = Alignment(horizontal='left', vertical='center')

        # --- 5. 타이틀 영역 (A1:N2 메인타이틀, O1:T2 날짜) ---
        ws.merge_cells("A1:N2")
        ws["A1"].value = "만물복귀 카페팀 일일 판매 보고서"
        ws["A1"].font = font_title
        ws["A1"].fill = fill_green
        ws["A1"].alignment = align_center

        ws.merge_cells("O1:T2")
        formatted_date = datetime.strptime(target_date, "%Y-%m-%d").strftime("%Y. %m. %d")
        ws["O1"].value = formatted_date
        ws["O1"].font = font_title
        ws["O1"].fill = fill_green
        ws["O1"].alignment = align_center

        for r in range(1, 3):
            for c in range(1, 21):
                ws.cell(row=r, column=c).border = thin_border

        # --- 6. 헤더 3행 & 4행 생성 ---
        ws.merge_cells("A3:A4") # 카테고리
        ws.merge_cells("B3:B4") # 품목
        ws.merge_cells("C3:F3") # 가격표
        ws.merge_cells("G3:I3") # 수련생할인가
        ws.merge_cells("J3:L3") # 일반가
        ws.merge_cells("M3:N3") # 아카데미할인가
        ws.merge_cells("O3:O4") # 엔화 합계
        ws.merge_cells("P3:P4") # 현금 합계
        ws.merge_cells("Q3:Q4") # 계좌 합계
        ws.merge_cells("R3:R4") # 총 합계
        ws.merge_cells("S3:S4") # 아카데미 포인트
        ws.merge_cells("T3:T4") # 총 판매량

        headers_row3 = [
            ("A3", "카테고리"), ("B3", "품목"), ("C3", "가격표"), 
            ("G3", "수련생할인가"), ("J3", "일반가"), ("M3", "아카데미할인가"), 
            ("O3", "엔화 합계"), ("P3", "현금 합계"), ("Q3", "계좌 합계"), 
            ("R3", "총 합계"), ("S3", "아카데미 포인트"), ("T3", "총 판매량")
        ]
        for cell_ref, text in headers_row3:
            ws[cell_ref].value = text
            ws[cell_ref].font = font_header
            ws[cell_ref].alignment = align_center
            ws[cell_ref].fill = fill_sub_title

        # 서브 헤더 (4행)
        sub_headers = {
            "C4": "할인", "D4": "원", "E4": "아카데미", "F4": "엔",
            "G4": "현금", "H4": "계좌", "I4": "엔화(현금)",
            "J4": "현금", "K4": "계좌", "L4": "엔화(현금)",
            "M4": "현금", "N4": "계좌"
        }
        for cell_ref, text in sub_headers.items():
            ws[cell_ref].value = text
            ws[cell_ref].font = font_header
            ws[cell_ref].alignment = align_center
            ws[cell_ref].fill = fill_sub_title

        for r in range(3, 5):
            for c in range(1, 21):
                ws.cell(row=r, column=c).border = thin_border

        # --- 7. 데이터 셀 채우기 (5행부터) ---
        start_data_row = 5
        row_idx = start_data_row

        for prod_id, data in stats.items():
            category = data.get("category", "기타")
            name = data["name"]
            price = data["price"]
            disc_price = int(price * 0.9)
            acad_price = int(price * 0.85)
            jpy_price = int(round(price / 10))

            # A~B열: 카테고리, 품목
            ws.cell(row=row_idx, column=1, value=category)
            ws.cell(row=row_idx, column=2, value=name)
            
            # C~F열: 가격표
            ws.cell(row=row_idx, column=3, value=disc_price)
            ws.cell(row=row_idx, column=4, value=price)
            ws.cell(row=row_idx, column=5, value=acad_price)
            ws.cell(row=row_idx, column=6, value=jpy_price)

            # G~N열: 수량 집계
            ws.cell(row=row_idx, column=7, value=data["disc_cash"] or None)
            ws.cell(row=row_idx, column=8, value=data["disc_bank"] or None)
            ws.cell(row=row_idx, column=9, value=data["disc_jpy"] or None)
            
            ws.cell(row=row_idx, column=10, value=data["norm_cash"] or None)
            ws.cell(row=row_idx, column=11, value=data["norm_bank"] or None)
            ws.cell(row=row_idx, column=12, value=data["norm_jpy"] or None)
            
            ws.cell(row=row_idx, column=13, value=data["acad_cash"] or None)
            ws.cell(row=row_idx, column=14, value=data["acad_bank"] or None)

            # O~R열: 수식 적용
            r = row_idx
            ws.cell(row=r, column=15, value=f"=(I{r}+L{r})*F{r}") 
            ws.cell(row=r, column=16, value=f"=(G{r}*{disc_price})+(J{r}*{price})+(M{r}*{acad_price})") 
            ws.cell(row=r, column=17, value=f"=(H{r}*{disc_price})+(K{r}*{price})+(N{r}*{acad_price})") 
            ws.cell(row=r, column=18, value=f"=P{r}+Q{r}") 

            # S~T열: 포인트 수량, 총 판매량
            ws.cell(row=r, column=19, value=data["point_qty"] or None)
            ws.cell(row=r, column=20, value=f"=SUM(G{r}:N{r})+S{r}")

            row_idx += 1

        end_data_row = row_idx - 1

        # --- 8. 데이터 영역 서식 지정 ---
        for r in range(start_data_row, row_idx):
            for c in range(1, 21):
                cell = ws.cell(row=r, column=c)
                cell.border = thin_border
                cell.font = font_data

                if c in [1, 2]:
                    cell.alignment = align_left
                elif c in [3, 4, 5]:
                    cell.alignment = align_right
                    cell.number_format = '"₩"#,##0'
                elif c == 6:
                    cell.alignment = align_right
                    cell.number_format = '"¥"#,##0'
                elif c in range(7, 15) or c in [19, 20]:
                    cell.alignment = align_center
                    cell.number_format = '#,##0'
                elif c == 15:
                    cell.alignment = align_right
                    cell.number_format = '"¥"#,##0'
                else: # P, Q, R열
                    cell.alignment = align_right
                    cell.number_format = '"₩"#,##0'

        # --- 9. 최하단 합계 행 추가 (엔화 & 원화 독립 합산) ---
        sum_row = row_idx
        ws.merge_cells(start_row=sum_row, start_column=1, end_row=sum_row, end_column=6)
        ws.cell(row=sum_row, column=1, value="합 계").alignment = align_center

        # G열 ~ T열 컬럼별 SUM 수식 적용
        for col_idx in range(7, 21):
            col_letter = get_column_letter(col_idx)
            # 엑셀 SUM 수식 작성
            ws.cell(row=sum_row, column=col_idx, value=f"=SUM({col_letter}{start_data_row}:{col_letter}{end_data_row})")

        # 합계 행 서식 및 스타일 지정
        for c in range(1, 21):
            cell = ws.cell(row=sum_row, column=c)
            cell.border = thin_border
            cell.font = font_sum
            cell.fill = fill_sum_row

            if c in range(7, 15) or c in [19, 20]: # 수량 항목 합계
                cell.alignment = align_center
                cell.number_format = '#,##0'
            elif c == 15: # 엔화 독립 합계
                cell.alignment = align_right
                cell.number_format = '"¥"#,##0'
            elif c in [16, 17, 18]: # 원화 독립 합계 (현금, 계좌, 총합)
                cell.alignment = align_right
                cell.number_format = '"₩"#,##0'

        wb.save(export_file_path)
        print(f"[Model] 엑셀 일일 판매 보고서 생성 완료: {export_file_path}")
        return True