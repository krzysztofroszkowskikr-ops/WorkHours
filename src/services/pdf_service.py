"""
PDFService - Serwis generowania raportów PDF
"""

from typing import List, Dict, Optional
from datetime import datetime
import logging
from io import BytesIO

# ReportLab imports (zainstalować via pip)
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("ReportLab nie zainstalowany - PDF nie będzie dostępny")

logger = logging.getLogger(__name__)


class PDFService:
    """
    Serwis do generowania raportów PDF
    
    Generu je:
    - Miesięczne raporty pracy
    - Podsumowania godzin
    - Raporty wzajęcia
    """
    
    def __init__(self):
        """Inicjalizuj serwis PDF"""
        if not REPORTLAB_AVAILABLE:
            logger.warning("ReportLab nie jest dostępny - zainstaluj: pip install reportlab")
    
    def generate_monthly_report(
        self,
        profile_name: str,
        year: int,
        month: int,
        work_days: List[Dict],
        summary: Dict,
        output_path: Optional[str] = None
    ) -> Optional[BytesIO]:
        """
        Wygeneruj miesięczny raport
        
        Args:
            profile_name: Nazwa profilu
            year: Rok
            month: Miesiąc
            work_days: Lista dni pracy
            summary: Podsumowanie z polami:
                - total_work_hours_hm
                - work_days
                - average_daily_hours
                - sick_days
                - vacation_days
                - day_offs
            output_path: Ścieżka do zapisu pliku (jeśli None, zwróć BytesIO)
            
        Returns:
            BytesIO z PDF lub None jeśli ReportLab niedostępny
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("Nie można wygenerować PDF bez ReportLab")
            return None
        
        try:
            # Utwórz PDF
            if output_path:
                doc = SimpleDocTemplate(
                    output_path,
                    pagesize=A4,
                    rightMargin=0.75*inch,
                    leftMargin=0.75*inch,
                    topMargin=0.75*inch,
                    bottomMargin=0.75*inch
                )
            else:
                buffer = BytesIO()
                doc = SimpleDocTemplate(
                    buffer,
                    pagesize=A4,
                    rightMargin=0.75*inch,
                    leftMargin=0.75*inch,
                    topMargin=0.75*inch,
                    bottomMargin=0.75*inch
                )
            
            # Elementy dokumentu
            elements = []
            styles = getSampleStyleSheet()
            
            # Tytuł
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor("#1a1a1a"),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            month_name = [
                "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
                "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
            ][month - 1]
            
            title = Paragraph(
                f"RAPORT PRACY<br/>{profile_name}<br/>{month_name} {year}",
                title_style
            )
            elements.append(title)
            elements.append(Spacer(1, 0.3*inch))
            
            # Podsumowanie
            summary_data = [
                ["PODSUMOWANIE", ""],
                ["Całkowity czas pracy", summary.get('total_work_hours_hm', '0:00')],
                ["Dni pracujące", str(summary.get('work_days', 0))],
                ["Dni chorobowe", str(summary.get('sick_days', 0))],
                ["Urlopy", str(summary.get('vacation_days', 0))],
                ["Dni wolne", str(summary.get('day_offs', 0))],
                ["Średnia dziennie", f"{summary.get('average_daily_hours', 0)}h"],
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#4CAF50")),
                ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Szczegóły dni
            if work_days:
                details_heading = Paragraph("SZCZEGÓŁY PRACY", styles['Heading2'])
                elements.append(details_heading)
                elements.append(Spacer(1, 0.2*inch))
                
                # Tabela dni
                days_data = [["Data", "Start", "Koniec", "Przerwa", "Czas netto", "Typ"]]
                
                for day in work_days:
                    days_data.append([
                        day.get('date', ''),
                        day.get('start_time', '-'),
                        day.get('end_time', '-'),
                        f"{day.get('break_minutes', 0)}m",
                        day.get('net_hours_hm', '0:00'),
                        day.get('day_type', '')
                    ])
                
                days_table = Table(days_data, colWidths=[1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch, 1*inch])
                days_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2196F3")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]))
                
                elements.append(days_table)
            
            # Stopka
            elements.append(Spacer(1, 0.5*inch))
            footer = Paragraph(
                f"<font size=8>Wygenerowano: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</font>",
                styles['Normal']
            )
            elements.append(footer)
            
            # Zbuduj PDF
            doc.build(elements)
            
            if output_path:
                logger.info(f"Raport zapisany: {output_path}")
                return None
            else:
                buffer.seek(0)
                logger.info("Raport wygenerowany (buffer)")
                return buffer
        
        except Exception as e:
            logger.error(f"Błąd generowania PDF: {e}")
            return None
    
    def generate_summary_report(
        self,
        profile_name: str,
        summaries: List[Dict],
        output_path: Optional[str] = None
    ) -> Optional[BytesIO]:
        """
        Wygeneruj raport podsumowujący (kilka miesięcy)
        
        Args:
            profile_name: Nazwa profilu
            summaries: Lista podsumowań z polami:
                - year
                - month
                - total_work_hours_decimal
                - average_daily_hours
            output_path: Ścieżka do zapisu
            
        Returns:
            BytesIO z PDF lub None
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("Nie można wygenerować PDF bez ReportLab")
            return None
        
        try:
            if output_path:
                doc = SimpleDocTemplate(output_path, pagesize=A4)
            else:
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4)
            
            elements = []
            styles = getSampleStyleSheet()
            
            # Tytuł
            title = Paragraph(
                f"PODSUMOWANIE ROCZNE<br/>{profile_name}",
                styles['Title']
            )
            elements.append(title)
            elements.append(Spacer(1, 0.3*inch))
            
            # Tabela
            table_data = [["Miesiąc", "Godziny", "Średnia dziennie"]]
            
            for summary in summaries:
                month_name = [
                    "Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec",
                    "Lipiec", "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"
                ][summary.get('month', 1) - 1]
                
                table_data.append([
                    f"{month_name} {summary.get('year')}",
                    f"{summary.get('total_work_hours_decimal', 0)}h",
                    f"{summary.get('average_daily_hours', 0)}h"
                ])
            
            table = Table(table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4CAF50")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            elements.append(table)
            doc.build(elements)
            
            if output_path:
                logger.info(f"Raport roczny zapisany: {output_path}")
                return None
            else:
                buffer.seek(0)
                return buffer
        
        except Exception as e:
            logger.error(f"Błąd generowania raportu rocznego: {e}")
            return None


__all__ = ['PDFService']
