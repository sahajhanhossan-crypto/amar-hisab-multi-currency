import sqlite3
import locale
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, DictProperty
from kivy.core.window import Window

Window.size = (360, 640)

TRANSLATIONS = {
    'en': {
        'app_title': 'Amar Hisab - Multi Currency',
        'income': 'Income',
        'expense': 'Expense',
        'balance': 'Remaining Balance',
        'add_transaction': 'Add Transaction',
        'amount': 'Amount',
        'category': 'Category',
        'select_currency': 'Select Currency',
        'save': 'Save',
        'history': 'History',
        'pin_prompt': 'Enter PIN to Unlock',
        'unlock': 'Unlock',
        'invalid_pin': 'Incorrect PIN!'
    }
}

def init_db():
    conn = sqlite3.connect('amar_hisab.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            category TEXT,
            currency TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

KV = '''
ScreenManager:
    PinScreen:
    MainScreen:

<PinScreen>:
    name: 'pin'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.18, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: app.lang_dict.get('pin_prompt', 'Enter PIN to Unlock')
            font_size: '20sp'
            bold: True
            color: 1, 1, 1, 1

        TextInput:
            id: pin_input
            password: True
            multiline: False
            input_type: 'number'
            halign: 'center'
            font_size: '24sp'
            size_hint_y: None
            height: '50dp'

        Label:
            id: error_label
            text: ''
            color: 1, 0.3, 0.3, 1

        Button:
            text: app.lang_dict.get('unlock', 'Unlock')
            size_hint_y: None
            height: '50dp'
            background_color: 0.2, 0.6, 1, 1
            on_press: root.verify_pin()

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        
        BoxLayout:
            size_hint_y: 0.1
            canvas.before:
                Color:
                    rgba: 0.15, 0.45, 0.85, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: app.lang_dict.get('app_title', 'Amar Hisab - Multi Currency')
                font_size: '18sp'
                bold: True
                color: 1, 1, 1, 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.25
            padding: 15
            spacing: 10
            Label:
                text: app.lang_dict.get('balance', 'Remaining Balance')
                font_size: '16sp'
            Label:
                text: str(app.total_balance) + " " + app.current_currency
                font_size: '32sp'
                bold: True
                color: 0.2, 0.8, 0.4, 1

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.65
            padding: 20
            spacing: 12

            TextInput:
                id: amount
                hint_text: app.lang_dict.get('amount', 'Amount')
                input_filter: 'float'
                multiline: False
                size_hint_y: None
                height: '45dp'

            TextInput:
                id: category
                hint_text: app.lang_dict.get('category', 'Category')
                multiline: False
                size_hint_y: None
                height: '45dp'

            BoxLayout:
                size_hint_y: None
                height: '45dp'
                spacing: 10
                Button:
                    text: app.lang_dict.get('income', 'Income')
                    background_color: 0.2, 0.8, 0.2, 1
                    on_press: root.add_record('Income')
                Button:
                    text: app.lang_dict.get('expense', 'Expense')
                    background_color: 0.9, 0.2, 0.2, 1
                    on_press: root.add_record('Expense')
'''

class PinScreen(Screen):
    def verify_pin(self):
        user_pin = self.ids.pin_input.text
        if user_pin == "1234": 
            self.manager.current = 'main'
        else:
            self.ids.error_label.text = App.get_running_app().lang_dict.get('invalid_pin', 'Incorrect PIN!')

class MainScreen(Screen):
    def add_record(self, trans_type):
        amount = self.ids.amount.text
        category = self.ids.category.text
        app = App.get_running_app()
        
        if amount and category:
            conn = sqlite3.connect('amar_hisab.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (type, amount, category, currency)
                VALUES (?, ?, ?, ?)
            ''', (trans_type, float(amount), category, app.current_currency))
            conn.commit()
            conn.close()
            
            self.ids.amount.text = ''
            self.ids.category.text = ''
            app.update_balance()

class AmarHisabApp(App):
    lang_dict = DictProperty({})
    total_balance = NumericProperty(0.0)
    current_currency = StringProperty('BDT')

    def build(self):
        self.detect_language()
        self.update_balance()
        return Builder.load_string(KV)

    def detect_language(self):
        try:
            loc = locale.getdefaultlocale()[0]
            lang_code = loc.split('_')[0] if loc else 'en'
        except:
            lang_code = 'en'

        self.lang_dict = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])

    def update_balance(self):
        conn = sqlite3.connect('amar_hisab.db')
        cursor = conn.cursor()
        cursor.execute("SELECT type, amount FROM transactions")
        rows = cursor.fetchall()
        conn.close()

        inc = sum(r[1] for r in rows if r[0] == 'Income')
        exp = sum(r[1] for r in rows if r[0] == 'Expense')
        self.total_balance = inc - exp

if __name__ == '__main__':
    AmarHisabApp().run()
