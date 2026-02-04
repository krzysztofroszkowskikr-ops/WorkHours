"""
ProfileScreen - Zarządzanie profilami użytkowników
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import logging

logger = logging.getLogger(__name__)


class ProfileScreen(Screen):
    """
    Ekran zarządzania profilami
    
    Funkcje:
    - Wyświetlenie listy profilów
    - Tworzenie nowego profilu
    - Usuwanie profilu
    - Wybór aktywnego profilu
    """
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        
        # Nowy profil
        self.new_profile_name = None
        self.dialog = None
        
        # Załaduj UI
        self.load_ui()
    
    def load_ui(self):
        """Załaduj UI ekranu"""
        logger.info("Ładowanie Profile Screen...")
        
        # Scroll view
        scroll = MDScrollView()
        
        # Główny layout
        layout = MDBoxLayout(
            orientation='vertical',
            padding='16dp',
            spacing='12dp',
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))
        
        # Tytuł
        title = MDLabel(
            text="Zarządzanie profilami",
            size_hint_y=None,
            height='40dp',
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        # LISTA PROFILÓW
        from src.repository import ProfileRepository
        repo = ProfileRepository(self.app.app_context.database)
        profiles = repo.get_all() or []
        
        if profiles:
            for profile in profiles:
                profile_card = MDCard(
                    padding='12dp',
                    spacing='8dp',
                    orientation='vertical',
                    size_hint_y=None,
                    height='100dp'
                )
                
                profile_layout = MDBoxLayout(orientation='vertical', spacing='8dp')
                
                # Nazwa profilu
                name_layout = MDBoxLayout(size_hint_y=0.4)
                name_layout.add_widget(MDLabel(
                    text=f"👤 {profile.name}",
                    bold=True
                ))
                profile_layout.add_widget(name_layout)
                
                # Informacje
                info_layout = MDBoxLayout(size_hint_y=0.3)
                info_layout.add_widget(MDLabel(
                    text=f"ID: {profile.id}",
                    font_size='10sp'
                ))
                profile_layout.add_widget(info_layout)
                
                # Przyciski
                btn_layout = MDBoxLayout(spacing='8dp', size_hint_y=0.3)
                
                select_btn = MDRaisedButton(
                    text="Wybierz",
                    size_hint_x=0.5
                )
                select_btn.bind(on_release=lambda x, pid=profile.id, pname=profile.name: 
                    self.select_profile(pid, pname))
                btn_layout.add_widget(select_btn)
                
                delete_btn = MDRaisedButton(
                    text="Usuń",
                    size_hint_x=0.5
                )
                delete_btn.bind(on_release=lambda x, pid=profile.id, pname=profile.name: 
                    self.delete_profile(pid, pname))
                btn_layout.add_widget(delete_btn)
                
                profile_layout.add_widget(btn_layout)
                profile_card.add_widget(profile_layout)
                layout.add_widget(profile_card)
        else:
            layout.add_widget(MDLabel(
                text="Brak profilów",
                size_hint_y=None,
                height='40dp'
            ))
        
        # NOWY PROFIL
        new_profile_label = MDLabel(
            text="Nowy profil",
            size_hint_y=None,
            height='24dp',
            font_size='16sp',
            bold=True
        )
        layout.add_widget(new_profile_label)
        
        new_profile_card = MDCard(padding='8dp', spacing='8dp', size_hint_y=None, height='56dp')
        new_profile_layout = MDBoxLayout(spacing='8dp')
        
        self.new_profile_name = MDTextField(
            hint_text="Nazwa profilu",
            mode="rectangle",
            size_hint_x=0.7
        )
        new_profile_layout.add_widget(self.new_profile_name)
        
        create_btn = MDRaisedButton(text="➕ Utwórz", size_hint_x=0.3)
        create_btn.bind(on_release=self.create_profile)
        new_profile_layout.add_widget(create_btn)
        
        new_profile_card.add_widget(new_profile_layout)
        layout.add_widget(new_profile_card)
        
        # POWRÓT
        back_btn = MDRaisedButton(text="◀️ Wróć", size_hint_y=None, height='56dp')
        back_btn.bind(on_release=lambda x: self.app.switch_screen('settings'))
        layout.add_widget(back_btn)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
        
        logger.info("Profile Screen załadowany")
    
    def create_profile(self, instance):
        """Utwórz nowy profil"""
        try:
            name = self.new_profile_name.text.strip()
            if not name:
                logger.warning("Nazwa profilu jest pusta")
                return
            
            from src.models import Profile
            from src.repository import ProfileRepository
            
            # Waliduj
            is_valid, msg = self.app.app_context.validators.is_valid_profile_name(name)
            if not is_valid:
                logger.error(f"Błąd nazwy: {msg}")
                return
            
            # Utwórz
            profile = Profile(
                id=None,
                name=name,
                created_at=None,
                updated_at=None
            )
            
            repo = ProfileRepository(self.app.app_context.database)
            repo.create(profile)
            
            logger.info(f"Profil utworzony: {name}")
            
            # Przeładuj UI
            self.clear_widgets()
            self.load_ui()
            
        except Exception as e:
            logger.error(f"Błąd tworzenia profilu: {e}")
    
    def select_profile(self, profile_id, profile_name):
        """Wybierz profil"""
        try:
            self.app.app_context.set_current_profile_id(profile_id)
            logger.info(f"Profil wybrany: {profile_name}")
            
            # Powróć do dashboard
            self.app.switch_screen('dashboard')
            
        except Exception as e:
            logger.error(f"Błąd wyboru profilu: {e}")
    
    def delete_profile(self, profile_id, profile_name):
        """Usuń profil"""
        try:
            # Potwierdzenie
            dialog = MDDialog(
                title="Potwierdzenie",
                text=f"Czy chcesz usunąć profil '{profile_name}'?\nWszystkie wpisy zostaną usunięte.",
                buttons=[
                    MDFlatButton(
                        text="Anuluj",
                        on_release=lambda x: dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Usuń",
                        on_release=lambda x: self._do_delete_profile(profile_id, profile_name, dialog)
                    )
                ]
            )
            dialog.open()
            
        except Exception as e:
            logger.error(f"Błąd usuwania profilu: {e}")
    
    def _do_delete_profile(self, profile_id, profile_name, dialog):
        """Faktycznie usuń profil"""
        try:
            from src.repository import ProfileRepository
            
            repo = ProfileRepository(self.app.app_context.database)
            repo.delete(profile_id)
            
            dialog.dismiss()
            logger.info(f"Profil usunięty: {profile_name}")
            
            # Przeładuj UI
            self.clear_widgets()
            self.load_ui()
            
        except Exception as e:
            logger.error(f"Błąd przy usuwaniu: {e}")


__all__ = ['ProfileScreen']
