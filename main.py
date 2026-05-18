import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from data_loader import DataLoader
from population_analyzer import PopulationAnalyzer
from inflation_analyzer import InflationAnalyzer  

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №3 - Анализ данных")
        self.root.geometry("1200x700")
        
        self.current_analyzer = None
        self.current_data = None
        
        self.setup_menu()
        self.setup_main_area()
    
    def setup_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Открыть файл...", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню Вариантов 
        variants_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Анализ данных", menu=variants_menu)
        variants_menu.add_command(label="Вариант 5: Численность населения", 
                                  command=self.run_population_analysis)
        variants_menu.add_command(label="Вариант 10: Инфляция", 
                                  command=self.run_inflation_analysis)
        
        # Меню Прогноз
        forecast_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Прогноз", menu=forecast_menu)
        forecast_menu.add_command(label="Прогнозировать на N периодов...", 
                                  command=self.show_forecast_dialog)
        
        # Меню Экспорт
        export_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Экспорт", menu=export_menu)
        export_menu.add_command(label="Сохранить график как PNG...", 
                                command=self.export_chart)
    
    def setup_main_area(self):
        """Основная область: таблица + график"""
        # Верхняя панель с информацией
        self.info_label = tk.Label(self.root, text="Выберите вариант анализа из меню", 
                                   font=('Arial', 12, 'bold'))
        self.info_label.pack(pady=5)
        
        # Рамка для таблицы
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(table_frame)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Рамка для графика
        chart_frame = tk.Frame(self.root)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def display_table(self, df: pd.DataFrame):
        """Отображение DataFrame в таблице"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        columns = list(df.columns)
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        for _, row in df.iterrows():
            self.tree.insert('', 'end', values=list(row))
    
    def open_file(self):
        """Открыть пользовательский файл с данными"""
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("JSON files", "*.json")]
        )
        if filepath:
            try:
                if filepath.endswith('.csv'):
                    self.current_data = pd.read_csv(filepath)
                elif filepath.endswith('.xlsx'):
                    self.current_data = pd.read_excel(filepath)
                else:
                    messagebox.showinfo("Информация", "Формат JSON требует ручной обработки")
                    return
                
                self.display_table(self.current_data)
                self.info_label.config(text=f"Загружен файл: {filepath}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
    
    def run_population_analysis(self):
        """Запуск анализа по варианту 5"""
        loader = DataLoader()
        data = loader.generate_sample_population()
        self.current_analyzer = PopulationAnalyzer(data)
        self.current_data = data
        self.display_table(data)
        self.current_analyzer.plot_data(self.figure, self.canvas)
        stats = self.current_analyzer.calculate_statistics()
        self.info_label.config(text=f"Вариант 5 - Численность населения | {stats}")
    
    def run_inflation_analysis(self):
        """Запуск анализа по варианту 10"""
        loader = DataLoader()
        data = loader.generate_sample_inflation()
        self.current_analyzer = InflationAnalyzer(data)
        self.current_data = data
        self.display_table(data)
        self.current_analyzer.plot_data(self.figure, self.canvas)
        stats = self.current_analyzer.calculate_statistics()
        self.info_label.config(text=f"Вариант 10 - Инфляция | {stats}")
    
    def show_forecast_dialog(self):
        """Диалог для ввода параметров прогноза"""
        if not self.current_analyzer:
            messagebox.showwarning("Предупреждение", "Сначала выберите вариант анализа")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Параметры прогноза")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="Количество прогнозируемых периодов (N):").pack(pady=5)
        n_entry = tk.Entry(dialog)
        n_entry.insert(0, "5")
        n_entry.pack(pady=5)
        
        tk.Label(dialog, text="Размер окна скользящей средней (n):").pack(pady=5)
        window_entry = tk.Entry(dialog)
        window_entry.insert(0, "3")
        window_entry.pack(pady=5)
        
        def run_forecast():
            try:
                n_periods = int(n_entry.get())
                window_size = int(window_entry.get())
                self.current_analyzer.plot_forecast(self.figure, self.canvas, n_periods, window_size)
                dialog.destroy()
                self.info_label.config(text=f"Прогноз на {n_periods} периодов (окно={window_size})")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите целые числа")
        
        tk.Button(dialog, text="Построить прогноз", command=run_forecast).pack(pady=20)
    
    def export_chart(self):
        """Экспорт графика в файл"""
        if not self.current_analyzer:
            messagebox.showwarning("Предупреждение", "Сначала выберите вариант анализа")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("SVG files", "*.svg"), ("PDF files", "*.pdf")]
        )
        if filepath:
            try:
                self.figure.savefig(filepath, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Успех", f"График сохранён как {filepath}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
