import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from image_processing import apply_sepia_single, apply_sepia_parallel

class SepiaApp:
    """
    Klasa aplikacji GUI do przetwarzania obrazów na sepię.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Konwerter Obrazu na Sepię")
        self.root.geometry("800x500")
        self.root.configure(bg="#2E2E2E")  # Ciemnoszare tło
        self.image_path = None

        # Stylizacja czcionek
        self.title_font = ("Helvetica", 16, "bold")
        self.button_font = ("Helvetica", 12, "bold")
        self.label_font = ("Helvetica", 14, "bold")

        # Ramka podglądu obrazów
        self.preview_frame = tk.Frame(self.root, bg="#2E2E2E")  # Ciemnoszare tło
        self.preview_frame.place(relx=0.5, rely=0.4, anchor="center")

        # Etykieta i ramka oryginalnego obrazu
        self.original_label = tk.Label(
            self.preview_frame,
            text="Oryginalny Obraz",
            font=self.label_font,
            fg="#FFFFFF",
            bg="#2E2E2E"
        )
        self.original_label.grid(row=0, column=0, padx=10, pady=5)
        self.original_canvas = tk.Label(
            self.preview_frame,
            width=375,
            height=300,
            bg="#424242",
            relief="ridge",
            bd=2
        )
        self.original_canvas.grid(row=1, column=0, padx=10, pady=10)

        # Etykieta i ramka przetworzonego obrazu
        self.processed_label = tk.Label(
            self.preview_frame,
            text="Obraz Po Przetworzeniu",
            font=self.label_font,
            fg="#FFFFFF",
            bg="#2E2E2E"
        )
        self.processed_label.grid(row=0, column=1, padx=10, pady=5)
        self.processed_canvas = tk.Label(
            self.preview_frame,
            width=375,
            height=300,
            bg="#424242",
            relief="ridge",
            bd=2
        )
        self.processed_canvas.grid(row=1, column=1, padx=10, pady=10)

        # Ramka na przyciski
        self.button_frame = tk.Frame(self.root, bg="#2E2E2E")
        self.button_frame.place(relx=0.02, rely=0.05, anchor="nw")  # Umieszczona w lewym górnym rogu

        # Stylizacja przycisków
        button_style = {
            'font': self.button_font,
            'bg': "#BDBDBD",            # Jaśniejsze tło przycisku
            'fg': "#212121",            # Ciemny kolor tekstu
            'activebackground': "#9E9E9E",
            'activeforeground': "#212121",
            'relief': "raised",
            'bd': 2,
            'width': 30
        }

        # Przyciski ułożone pionowo
        self.load_button = tk.Button(
            self.button_frame,
            text="Wczytaj Obraz",
            command=self.load_image,
            **button_style
        )
        self.load_button.pack(fill='x', padx=10, pady=5)

        self.sepia_single_button = tk.Button(
            self.button_frame,
            text="Zastosuj Sepię (Jednowątkowo)",
            command=self.apply_sepia_single,
            **button_style
        )
        self.sepia_single_button.pack(fill='x', padx=10, pady=5)

        self.sepia_parallel_button = tk.Button(
            self.button_frame,
            text="Zastosuj Sepię (Wielowątkowo)",
            command=self.apply_sepia_parallel,
            **button_style
        )
        self.sepia_parallel_button.pack(fill='x', padx=10, pady=5)

        self.plot_bar_button = tk.Button(
            self.button_frame,
            text="Wykres Wydajności (Słupkowy)",
            command=self.show_performance_plot_bar,
            **button_style
        )
        self.plot_bar_button.pack(fill='x', padx=10, pady=5)

        self.plot_line_button = tk.Button(
            self.button_frame,
            text="Wykres Wydajności (Liniowy)",
            command=self.show_performance_plot_line,
            **button_style
        )
        self.plot_line_button.pack(fill='x', padx=10, pady=5)

        # Etykieta czasu przetwarzania
        self.time_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 12),
            fg="#FFFFFF",
            bg="#2E2E2E"
        )
        self.time_label.place(relx=0.5, rely=0.95, anchor="center")

    def load_image(self):
        """
        Metoda do wczytywania obrazu przez użytkownika.
        """
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Pliki graficzne", "*.jpg *.jpeg *.png")]
        )
        if self.image_path:
            img = Image.open(self.image_path)
            resized_img = self.resize_image(img, 375, 300)
            self.original_image = ImageTk.PhotoImage(resized_img)
            self.original_canvas.config(image=self.original_image)
            self.processed_canvas.config(image='')
            self.time_label.config(text="")

    def resize_image(self, image, max_width, max_height):
        """
        Zmień rozmiar obrazu, zachowując proporcje.

        Args:
            image (PIL.Image.Image): Obiekt obrazu PIL.
            max_width (int): Maksymalna szerokość.
            max_height (int): Maksymalna wysokość.

        Returns:
            PIL.Image.Image: Zmieniony rozmiar obrazu.
        """
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        return image

    def apply_sepia_single(self):
        """
        Zastosuj filtr sepii jednowątkowo i wyświetl wynik.
        """
        if not self.image_path:
            messagebox.showwarning(
                "Ostrzeżenie", "Proszę wczytać obraz przed przetwarzaniem."
            )
            return

        output_path = "sepia_single.jpg"
        processing_time = apply_sepia_single(self.image_path, output_path)
        self.display_processed_image(output_path, processing_time)

    def apply_sepia_parallel(self):
        """
        Zastosuj filtr sepii wielowątkowo i wyświetl wynik.
        """
        if not self.image_path:
            messagebox.showwarning(
                "Ostrzeżenie", "Proszę wczytać obraz przed przetwarzaniem."
            )
            return

        output_path = "sepia_parallel.jpg"
        processing_time = apply_sepia_parallel(self.image_path, output_path)
        self.display_processed_image(output_path, processing_time)

    def display_processed_image(self, image_path, processing_time):
        """
        Wyświetl przetworzony obraz i czas przetwarzania.

        Args:
            image_path (str): Ścieżka do przetworzonego obrazu.
            processing_time (float): Czas przetwarzania w sekundach.
        """
        img = Image.open(image_path)
        resized_img = self.resize_image(img, 375, 300)
        self.processed_image = ImageTk.PhotoImage(resized_img)
        self.processed_canvas.config(image=self.processed_image)
        self.time_label.config(
            text=f"Czas przetwarzania: {processing_time:.2f} s"
        )

    def show_performance_plot_bar(self):
        """
        Wyświetl wykres słupkowy porównujący czas przetwarzania dla różnej liczby procesów.
        """
        if not self.image_path:
            messagebox.showwarning(
                "Ostrzeżenie", "Proszę wczytać obraz przed generowaniem wykresu."
            )
            return

        worker_counts = [1, 2, 4, 6, 8, 16]
        processing_times = []

        for count in worker_counts:
            if count == 1:
                time_taken = apply_sepia_single(self.image_path, 'temp_sepia.jpg')
            else:
                time_taken = apply_sepia_parallel(
                    self.image_path, 'temp_sepia.jpg', num_workers=count
                )
            processing_times.append(time_taken)

        # Tworzenie wykresu słupkowego
        plt.figure(figsize=(10, 5))
        plt.bar(worker_counts, processing_times, color='blue')
        plt.title("Czas przetwarzania w zależności od liczby procesów")
        plt.xlabel("Liczba procesów")
        plt.ylabel("Czas przetwarzania (s)")
        plt.xticks(worker_counts)
        plt.grid(axis='y')
        plt.show()

    def show_performance_plot_line(self):
        """
        Wyświetl wykres liniowy porównujący czas przetwarzania dla różnej liczby procesów.
        """
        if not self.image_path:
            messagebox.showwarning(
                "Ostrzeżenie", "Proszę wczytać obraz przed generowaniem wykresu."
            )
            return

        worker_counts = [1, 2, 4, 6, 8, 16]
        processing_times = []

        for count in worker_counts:
            if count == 1:
                time_taken = apply_sepia_single(self.image_path, 'temp_sepia.jpg')
            else:
                time_taken = apply_sepia_parallel(
                    self.image_path, 'temp_sepia.jpg', num_workers=count
                )
            processing_times.append(time_taken)

        # Tworzenie wykresu liniowego
        plt.figure(figsize=(10, 5))
        plt.plot(worker_counts, processing_times, marker='o', linestyle='-', color='blue')
        plt.title("Czas przetwarzania w zależności od liczby procesów")
        plt.xlabel("Liczba procesów")
        plt.ylabel("Czas przetwarzania (s)")
        plt.xticks(worker_counts)
        plt.grid(axis='y')
        plt.show()
