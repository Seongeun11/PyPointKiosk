# src/my_package/model/receipt_repository_model.py

import os
import json
from datetime import datetime, timedelta
from typing import Optional

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

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
        """
        영업일 기준 YYYY-MM-DD 문자열 반환
        - 새벽 2시 미만(00:00 ~ 01:59)은 전일 날짜로 계산
        """
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
                    discount_type: str, discount_amount: int, final_amount: int) -> dict:
        """결제 완료 시 영업일 기준 JSON 파일(receipts_YYYY-MM-DD.json)에 영수증 추가"""
        now = datetime.now()
        business_date_str = self._get_business_date_str(now)
        daily_file_path = self._get_daily_file_path(business_date_str)

        receipts = self._load_receipts_by_path(daily_file_path)

        # 당일 결제 건수 기준 순번 (1 ~ 999)
        next_id = (len(receipts) % 999) + 1

        receipt_data = {
            "id": next_id,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"), # 실제 거래 일시는 그대로 보존
            "pay_type": pay_type,                     
            "discount_type": discount_type,           
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
                print(f"[Model] 영수증 저장 완료 (영업일: {business_date_str}): {daily_file_path} (총 {len(receipts)}건)")
        except Exception as e:
            print(f"[Model Error] 영수증 저장 실패: {e}")

        return receipt_data

    def get_receipts_by_date(self, date_str: Optional[str] = None) -> list:
        """특정 영업일 날짜(YYYY-MM-DD)의 영수증 목록 조회 (기본값: 현재 영업일)"""
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
        [개선된 로직]
        - target_date가 지정되지 않은 경우 현재 '영업일'을 기준으로 보고서 생성
        - A열에 카테고리명을 추가하여 카테고리별 노출/판매 정도 통계 작성 가능
        - 모든 열과 엑셀 계산 수식을 A열 추가에 맞춰 1열씩 이동하여 동기화
        """
        if not target_date:
            target_date = self._get_business_date_str()

        receipts = self.get_receipts_by_date(target_date)
        
        # 1. products.json으로부터 Master ID 및 카테고리 정보 로드
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
                                "disc_cash": 0, "disc_bank": 0,
                                "norm_cash": 0, "norm_bank": 0,
                                "acad_cash": 0, "acad_bank": 0,
                                "point_qty": 0, "total_qty": 0
                            }
            except Exception as e:
                print(f"[Model Error] 상품 목록 로드 실패: {e}")

        wb = openpyxl.Workbook()
        ws = wb.active

        if ws is None or not isinstance(ws, Worksheet):
            ws = wb.create_sheet(title="일일 판매 보고서")
        else:
            ws.title = "일일 판매 보고서"

        # 서식 및 스타일 정의
        font_title = Font(name="맑은 고딕", size=14, bold=True)
        font_header = Font(name="맑은 고딕", size=9, bold=True)
        
        fill_title = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
        fill_sub_title = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")

        thin_border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )
        align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
        align_right = Alignment(horizontal='right', vertical='center')

        # 엑셀 타이틀 헤더 (A열 추가로 인한 전체 열 영역: A~S열 총 19개)
        ws.merge_cells("A1:O2")
        ws["A1"].value = "만물복귀 카페팀 일일 판매 보고서"
        ws["A1"].font = font_title
        ws["A1"].fill = fill_title
        ws["A1"].alignment = align_center

        #사용설명서 넣기
        ws.merge_cells("T1")
        ws["T1"].value = "매일 02:00에 마감"
        ws["T1"].font = font_title
        ws["T1"].fill = fill_title
        ws["T1"].alignment = align_center

        #----
        ws.merge_cells("P1:S2")
        formatted_date = datetime.strptime(target_date, "%Y-%m-%d").strftime("%Y. %m. %d")
        ws["P1"].value = formatted_date
        ws["P1"].font = font_title
        ws["P1"].fill = fill_title
        ws["P1"].alignment = align_center

        # Row 3 메인 헤더 정의 (A3: 카테고리 추가)
        headers_row3 = [
            ("A3", "카테고리"), ("B3", "품목"), ("C3", "가격표"), ("G3", "수련생할인가"), 
            ("I3", "일반가"), ("K3", "아카데미할인가"), ("M3", "엔화"), ("N3", "엔화 합계"), 
            ("O3", "현금 합계"), ("P3", "계좌 합계"), ("Q3", "총 합계"), 
            ("R3", "아카데미 포인트"), ("S3", "총 판매량")
        ]
        
        ws.merge_cells("A3:A4")
        ws.merge_cells("B3:B4")
        ws.merge_cells("C3:F3")
        ws.merge_cells("G3:H3")
        ws.merge_cells("I3:J3")
        ws.merge_cells("K3:L3")
        ws.merge_cells("M3:M4")
        ws.merge_cells("N3:N4")
        ws.merge_cells("O3:O4")
        ws.merge_cells("P3:P4")
        ws.merge_cells("Q3:Q4")
        ws.merge_cells("R3:R4")
        ws.merge_cells("S3:S4")

        for cell_ref, text in headers_row3:
            ws[cell_ref].value = text
            ws[cell_ref].font = font_header
            ws[cell_ref].alignment = align_center
            ws[cell_ref].fill = fill_sub_title

        # Row 4 서브 헤더 정의 (각 1칸씩 우측으로 이동)
        sub_headers = {
            "C4": "할인", "D4": "원", "E4": "아카데미", "F4": "엔",
            "G4": "현금", "H4": "계좌", "I4": "현금", "J4": "계좌",
            "K4": "현금", "L4": "계좌"
        }
        for cell_ref, text in sub_headers.items():
            ws[cell_ref].value = text
            ws[cell_ref].font = font_header
            ws[cell_ref].alignment = align_center
            ws[cell_ref].fill = fill_sub_title

        # 2. 영수증 내역 집계 (ID 기준으로 분리)
        for r in receipts:
            p_type = r.get("pay_type")
            d_type = r.get("discount_type")
            items = r.get("items", [])

            for item in items:
                prod_id = str(item.get("id", item.get("name")))
                name = item.get("name", "미등록상품")
                qty = item.get("quantity", 0)

                if prod_id not in stats:
                    stats[prod_id] = {
                        "id": prod_id,
                        "name": name,
                        "category": "기타", 
                        "price": item.get("price", 0),
                        "disc_cash": 0, "disc_bank": 0,
                        "norm_cash": 0, "norm_bank": 0,
                        "acad_cash": 0, "acad_bank": 0,
                        "point_qty": 0, "total_qty": 0
                    }

                st = stats[prod_id]
                st["total_qty"] += qty

                if p_type == "point":
                    st["point_qty"] += qty
                elif d_type == "student":
                    if p_type == "cash": st["disc_cash"] += qty
                    elif p_type == "bank": st["disc_bank"] += qty
                elif d_type == "academy":
                    if p_type == "cash": st["acad_cash"] += qty
                    elif p_type == "bank": st["acad_bank"] += qty
                else:
                    if p_type == "cash": st["norm_cash"] += qty
                    elif p_type == "bank": st["norm_bank"] += qty

        # 3. 엑셀 셀 채우기 (A열: 카테고리, B열: 품목 ...)
        row_idx = 5
        for prod_id, data in stats.items():
            category = data.get("category", "기타")
            name = data["name"]
            price = data["price"]
            disc_price = int(price * 0.9)
            acad_price = int(price * 0.85)

            # Col 1: 카테고리
            ws.cell(row=row_idx, column=1, value=category)
            # Col 2: 품목
            ws.cell(row=row_idx, column=2, value=name)
            
            # Col 3~6: 가격표 (할인가, 원화, 아카데미가, 엔화)
            ws.cell(row=row_idx, column=3, value=f"₩{disc_price:,}")
            ws.cell(row=row_idx, column=4, value=f"₩{price:,}")
            ws.cell(row=row_idx, column=5, value=f"₩{acad_price:,}")
            ws.cell(row=row_idx, column=6, value=f"¥{int(price/10)}")

            # Col 7~12: 수량 집계 (할인 현금/계좌, 일반 현금/계좌, 아카데미 현금/계좌)
            ws.cell(row=row_idx, column=7, value=data["disc_cash"] or "")
            ws.cell(row=row_idx, column=8, value=data["disc_bank"] or "")
            ws.cell(row=row_idx, column=9, value=data["norm_cash"] or "")
            ws.cell(row=row_idx, column=10, value=data["norm_bank"] or "")
            ws.cell(row=row_idx, column=11, value=data["acad_cash"] or "")
            ws.cell(row=row_idx, column=12, value=data["acad_bank"] or "")
            ws.cell(row=row_idx, column=13, value="") # 엔화 결제 수량 칸

            # Col 14~19: 수식 계산 (1열씩 이동된 수식 적용)
            ws.cell(row=row_idx, column=14, value=f"=M{row_idx}*F{row_idx}")
            ws.cell(row=row_idx, column=15, value=f"=(G{row_idx}*{disc_price})+(I{row_idx}*{price})+(K{row_idx}*{acad_price})")
            ws.cell(row=row_idx, column=16, value=f"=(H{row_idx}*{disc_price})+(J{row_idx}*{price})+(L{row_idx}*{acad_price})")
            ws.cell(row=row_idx, column=17, value=f"=O{row_idx}+P{row_idx}")

            # R열(18): 포인트 수량
            ws.cell(row=row_idx, column=18, value=data["point_qty"] or "")
            # S열(19): 총 판매량 = SUM(G:M) + R
            ws.cell(row=row_idx, column=19, value=f"=SUM(G{row_idx}:M{row_idx})+R{row_idx}")

            row_idx += 1

        # 테두리 및 정렬 서식 적용 (1~19열 대상)
        for r in range(1, row_idx):
            for c in range(1, 20):
                cell = ws.cell(row=r, column=c)
                cell.border = thin_border
                if r >= 5:
                    if c in [1, 2]: # 카테고리, 품목
                        cell.alignment = Alignment(horizontal='left', vertical='center')
                    elif c in range(3, 7): # 가격표
                        cell.alignment = align_right
                    elif c <= 13 or c in [18, 19]: # 수량 관련 항목
                        cell.alignment = align_center
                    else: # 금액 계산 항목
                        cell.alignment = align_right

        wb.save(export_file_path)
        return True