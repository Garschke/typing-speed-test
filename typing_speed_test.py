# typing_speed_test
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json


class TypingSpeedTest:
    """A GUI application for testing typing speed."""

    def __init__(self, root):
        """Initialize the application."""

        # Initialize variables
        self.test = 0
        self.text = ''
        self.msg_text = "<- Click the 'Select Text' button to load Text."
        self.entry_text = ' ' * 40 + 'Text input box (Type text in this area)'
        self.test_file = ''
        self.date = time.time()
        self.date_text = f'{time.strftime("%A, %d %B %Y")}'
        self.level = 0.0
        self.word_count = 0  # int
        self.character_count = 0  # int
        self.cpw = 0.0  # float
        self.unique_characters = 0   # int
        self.set_default()
        self.load_statistics()
        self.data = {}
        self.statistics_saved = False

# --------------------------- UI SETUP ------------------------------ #

        self.root = root    # root window
        self.root.title('Typing Speed Test')
        self.root.geometry('666x666')

        # Create a frame for the left border
        self.left_border = tk.Frame(self.root, width=10)
        self.left_border.grid(row=0, column=0, rowspan=14, sticky="ns")

        # Create a main frame for the content
        self.main_frame = tk.Frame(self.root)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        # Main content

        # Add content to the main frame
        self.text = self.load_text()  # Load text from file to display
        self.text_label = tk.Label(self.main_frame, text=self.text,
                                   width=60, height=18, wraplength=560,
                                   background='lightblue', foreground='black',
                                   justify='left',
                                   font=('American Typewriter', 14))
        self.text_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.select_button = tk.Button(self.main_frame,
                                       text='Select Text',
                                       command=self.select_text)
        self.select_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.msg_label = tk.Label(self.main_frame, text=self.msg_text)
        self.msg_label.grid(row=1, column=1, columnspan=3,
                            padx=5, pady=5, sticky="w")

        self.entry = tk.Entry(self.main_frame, width=60,
                              background='white', foreground='black',
                              font=('American Typewriter', 14),
                              state='normal')
        self.entry.insert(0, self.entry_text)
        self.entry.bind('<KeyRelease>', self.check_text)
        self.entry.grid(row=2, column=0, columnspan=4,
                        padx=5, pady=5, sticky="w")

        self.test_file_label = tk.Label(self.main_frame, text='Test File :   ')
        self.test_file_label.grid(row=3, column=0, columnspan=3,
                                  padx=5, pady=5, sticky="w")

        self.statistics_label = tk.Label(self.main_frame, text='STATISTICS')
        self.statistics_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.date_label = tk.Label(self.main_frame,
                                   text=('Date :' + ' ' * 16 + self.date_text))
        self.date_label.grid(row=4, column=2, columnspan=2,
                             padx=5, pady=5, sticky="w")

        self.words_label = tk.Label(self.main_frame,
                                    text=('Level :\n' +
                                          'Words :\n' +
                                          'Characters :\n' +
                                          'Characters / Word (cpw) :\n' +
                                          'Unique Characters :\n'),
                                    anchor="w",  # Align text to the left
                                    justify="left")  # Multi-line left-justifd
        self.words_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.words_data = tk.Label(self.main_frame,
                                   text=(f'{self.word_count}\n' +
                                         f'{self.word_count}\n' +
                                         f'{self.character_count}\n' +
                                         f'{self.cpw}\n' +
                                         f'{self.unique_characters}\n'),
                                   anchor="w",  # Align text to the left
                                   justify="left")  # Multi-line left-justified
        self.words_data.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.times_label = tk.Label(self.main_frame,
                                    text=('Start Time :\n' +
                                          'End Time :\n' +
                                          'Elapse Time :\n' +
                                          'Words / minute (wpm) :\n' +
                                          'Characters / minute (cpm) :\n' +
                                          'Typing Errors :\n'),
                                    anchor="w",  # Align text to the left
                                    justify="left")  # Multi-line left-justifd
        self.times_label.grid(row=5, column=2, padx=5, pady=5, sticky="w")

        self.times_data = tk.Label(self.main_frame,
                                   text=(f'{self.start_time_string}\n' +
                                         f'{self.end_time_string}\n' +
                                         f'{self.elapsed_string}\n' +
                                         f'{self.wpm}\n' +
                                         f'{self.cpm}\n'
                                         f'{self.typing_errors}\n'),
                                   anchor="w",  # Align text to the left
                                   justify="left")  # Multi-line left-justified
        self.times_data.grid(row=5, column=3, padx=5, pady=5, sticky="w")

        # Buttons to save and review statistics and to stop test
        self.stats_button = tk.Button(self.main_frame, text='Save Statistics',
                                      command=self.save_stats)
        self.stats_button.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.review_button = tk.Button(self.main_frame,
                                       text='Review Statistics',
                                       command=self.review_statistics)
        self.review_button.grid(row=7, column=1, padx=5, pady=5, sticky="e")

        self.stop_button = tk.Button(self.main_frame, text='Stop Test',
                                     command=self.stop)
        self.stop_button.grid(row=7, column=2, padx=5, pady=5, sticky="e")

    def load_text(self):
        """load initial display text from file"""
        file_path = os.path.join(os.path.dirname(__file__),
                                 'assets', 'Initial text.txt')
        with open(file_path, 'r') as file:
            text = file.read()
        return text

    def analyse_text(self):
        """ Analyse Word count, Character count, etc. """
        self.word_count = len(self.text.split())
        self.character_count = len(self.text)
        self.cpw = (self.character_count / self.word_count
                    if self.word_count > 0 else 0)
        self.unique_characters = len(set(self.text))
        numerator = self.cpw * (self.unique_characters**2)
        if self.character_count > 1000:
            denominator = 3 * 1000
        else:
            denominator = (3 * self.character_count)
        self.level = numerator / denominator
        # Update the statistics label
        self.refresh_text_stats()

    def analyse_typing(self):
        """ Analyse Typing, Word/Characters per minute etc. """
        text_typed = self.entry.get()
        if text_typed == '':
            print('no text entered')
        else:
            self.word_count = len(text_typed.split())
            self.character_count = len(text_typed)
            self.cpw = (self.character_count / self.word_count
                        if self.word_count > 0 else 0)
            self.unique_characters = len(set(text_typed))
            numerator = self.cpw * (self.unique_characters**2)
            if self.character_count > 1000:
                denominator = 3 * 1000
            else:
                denominator = (3 * self.character_count)
            self.level = numerator / denominator
            # Update the statistics label
            self.refresh_text_stats()
            # Calculate running stats
            self.elapsed_time = time.time() - self.start_time
            self.wpm = self.word_count / (self.elapsed_time / 60)
            self.cpm = self.character_count / (self.elapsed_time / 60)
            # Update the statistics label
            self.refresh_time_stats()

    def refresh_text_stats(self):
        """ Update the UI with Text Statistics """
        self.words_data.config(text=(f'{self.level:.1f}\n' +
                                     f'{self.word_count}\n' +
                                     f'{self.character_count}\n' +
                                     f'{self.cpw:.2f}\n' +
                                     f'{self.unique_characters}\n'))

    def refresh_time_stats(self):
        """ Update the UI with Time based Statistics """
        self.times_data.config(text=(f'{self.start_time_string}\n' +
                                     f'{self.end_time_string}\n' +
                                     f'{self.elapsed_time:.2f}\n' +
                                     f'{self.wpm:.2f}\n' +
                                     f'{self.cpm:.2f}\n' +
                                     f'{self.typing_errors}\n'))

    def check_text(self, event):
        """ Check if the text entered is correct, log error count"""
        characters_typed = len(self.entry.get())
        if self.start_time == 0.0:
            self.start()
        elif self.entry.get() == self.text[:characters_typed]:
            # change background color to white if text is correct
            self.entry.config(bg='white')
            if characters_typed == len(self.text):
                self.stop()
        else:
            # change background color to red if text is incorrect
            self.typing_errors = self.typing_errors + 1
            self.entry.config(bg='red')
        self.analyse_typing()

    def set_default(self):
        """ Set/Reset initial default values for Stats """
        self.start_time = 0.0
        self.end_time = 0.0
        self.elapsed_time = 0.0
        self.start_time_string = ''
        self.end_time_string = ''
        self.elapsed_string = ''
        self.wpm = 0.0  # float
        self.cpm = 0.0  # float
        self.typing_errors = 0

    def select_text(self):
        """ Select file and load text to UI display for typing test """
        file_path = os.path.join(os.path.dirname(__file__),
                                 'assets/test_text/')
        open_file = filedialog.askopenfile(initialdir=file_path,
                                           title='Select a file',
                                           filetypes=(('Text files', '*.txt'),
                                                      ('All files', '*.*')))
        if open_file:
            self.test_file = os.path.basename(open_file.name)
            self.test_file_label.config(text='Test File :   ' + self.test_file)
            self.text = open_file.read()
            self.text_label.config(text=self.text)  # test text to be display
            self.entry.config(state='normal')
            self.entry.delete(0, 'end')
            self.entry_text = ''
            self.msg_text = ('Type below the above text, ' +
                             'timer will begin when you start typing.')
            self.msg_label.config(text=self.msg_text)
            self.set_default()
            self.statistics_saved = False
            self.refresh_time_stats()
            self.analyse_text()
            self.entry.focus_set()

    def start(self):
        """ Set Start time vaiable and update user through UI"""
        self.start_time = time.time()
        self.start_time_string = time.strftime("%H:%M:%S",
                                               time.localtime(self.start_time))
        self.msg_label.config(text=('The timer has started for the test,' +
                                    'continue typing text below'))
        self.analyse_typing()
        self.entry.focus_set()

    def stop(self):
        """ Calculate elapse time update UI stats """
        if self.start_time == 0.0:
            if self.entry_text == '':
                self.msg_text = ("Test not yet started, begin typing below " +
                                 "the above text to start.")
            else:
                self.msg_text = ("Test not yet started, press 'Select Text'" +
                                 " button to load text.")
            self.msg_label.config(text=self.msg_text)
        else:
            self.end_time = time.time()
            self.elapsed_time = time.time() - self.start_time
            self.end_time_string = time.strftime("%H:%M:%S",
                                                 time.localtime(self.end_time))
            self.elapsed_string = time.strftime("%M:%S",
                                                time.localtime(self.elapsed_time))
            self.entry.config(state='disabled')
            self.msg_text = ("Test complete - check stats below - " +
                             "you can also 'Save Statistics'")
            self.msg_label.config(text=self.msg_text)
            self.analyse_typing()

    def save_stats(self):
        if ((self.statistics_saved is False) and
            (self.msg_text == ("Test complete - check stats below - " +
                               "you can also 'Save Statistics'")) and
            (len(self.entry.get()) > 0) and
            (self.entry.get() != 'Text input box (Type text in this area)') and
            (self.elapsed_time > 0)):
            self.save_statistics()
            return True
        else:
            print('save stats - False')
            return False

    def save_statistics(self):
        """ Save typing test Statistics to json file """
        if self.save_stats:
            self.test = self.test + 1
            test = self.test
            new_data = {
                test: {
                    "date_text": self.date_text,
                    "start_time": self.start_time,
                    "start_time_string": self.start_time_string,
                    "elapsed_time": self.elapsed_time,
                    "elapsed_string": self.elapsed_string,
                    "word_count": self.word_count,
                    "characters_count": self.character_count,
                    "unique_characters": self.unique_characters,
                    "typing_errors": self.typing_errors,
                    "test_file": self.test_file,
                }
            }
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)

                self.msg_text = ("Statistics saved, for next test press " +
                                 "'Select Text' button.")
                self.msg_label.config(text=self.msg_text)
                self.statistics_saved = True
        else:
            self.msg_text = ("<- press 'Select Text' button for next test, " +
                             "Statistics saved.")
            self.msg_label.config(text=self.msg_text)

    def load_statistics(self):
        """ Load Typing Statistics data and set test number """
        try:
            with open("data.json") as data_file:
                self.data = json.load(data_file)
                self.test = len(self.data)
        except FileNotFoundError:
            self.test = 0

    def review_statistics(self):
        """ Open the Statistics dialog """

# --------------------------- UI SETUP ------------------------------ #

        statistics = tk.Toplevel(self.root)
        statistics.title("Typing Speed Statistics & Overall Rating")
        statistics.geometry("1500x400")

        ttk.Label(statistics,
                  text="Test #").grid(row=0, column=0,
                                      padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Date").grid(row=0, column=1,
                                    padx=5, pady=5, sticky="w")
        ttk.Label(statistics,
                  text="Level").grid(row=0, column=3,
                                     padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Start Time").grid(row=0, column=4,
                                          padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Elapse Time").grid(row=0, column=5,
                                           padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Words").grid(row=0, column=6,
                                     padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Characters").grid(row=0, column=7,
                                          padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Unique Chrs").grid(row=0, column=8,
                                           padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="(cpw)").grid(row=0, column=9,
                                     padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="(wpm)").grid(row=0, column=10,
                                     padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="(cpm)").grid(row=0, column=11,
                                     padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Errors").grid(row=0, column=12,
                                      padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Error %").grid(row=0, column=13,
                                       padx=5, pady=5, sticky="e")
        ttk.Label(statistics,
                  text="Test File Name").grid(row=0, column=14,
                                              padx=5, pady=5, sticky="w")

# -------------------- Loop though Statistics ----------------------- #
        self.load_statistics()
        if len(self.data) == 0:
            messagebox.showinfo("Information", 'No Saved Statistics')

            msg = ttk.Button(statistics, text='NO SAVED STATISICAL DATA YET')
            msg.grid(row=2, column=0, columnspan=10,
                     padx=5, pady=5, sticky="e")

        else:
            for record in self.data:

                ttk.Label(statistics,
                          text=f'{record}').grid(row=record, column=0,
                                                 padx=5, pady=5, sticky="e")
                str_value = self.data[record]["date_text"]
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=1,
                                               padx=5, pady=5, sticky="e")
                # Level
                if (self.data[record]["characters_count"] > 1000):
                    char_cnt = 1000
                else:
                    char_cnt = self.data[record]["characters_count"]
                char_per_word = (int(self.data[record]["characters_count"]) /
                                 int(self.data[record]["word_count"]))
                level = ((char_per_word *
                          (self.data[record]["unique_characters"]**2))
                         / (3 * char_cnt))
                str_value = f'{level:.1f}'
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=3,
                                               padx=5, pady=5, sticky="e")
                str_value = self.data[record]["start_time_string"]
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=4,
                                               padx=5, pady=5, sticky="e")
                str_value = self.data[record]["elapsed_string"]
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=5,
                                               padx=5, pady=5, sticky="e")
                str_value = self.data[record]["word_count"]
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=6,
                                               padx=5, pady=5, sticky="e")
                str_value = self.data[record]["characters_count"]
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=7,
                                               padx=5, pady=5, sticky="e")
                str_value = self.data[record]["unique_characters"]
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=8,
                                               padx=5, pady=5, sticky="e")
                # (cpw)
                str_value = f'{(char_per_word):.2f}'
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=9,
                                               padx=5, pady=5, sticky="e")
                # (wpm)
                wpm = (self.data[record]["word_count"] /
                       (self.data[record]["elapsed_time"] / 60))
                str_value = f'{wpm:.2f}'
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=10,
                                               padx=5, pady=5, sticky="e")
                # (cpm)
                cpm = (self.data[record]["characters_count"] /
                       (self.data[record]["elapsed_time"] / 60))
                str_value = f'{cpm:.2f}'
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=11,
                                               padx=5, pady=5, sticky="e")
                str_value = self.data[record]["typing_errors"]
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=12,
                                               padx=5, pady=5, sticky="e")
                # Error %
                error_percent = (self.data[record]["typing_errors"] /
                                 (self.data[record]["typing_errors"] +
                                  self.data[record]["characters_count"]))
                str_value = f'{error_percent:.2%}'
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=13,
                                               padx=5, pady=5, sticky="e")
                str_value = self.data[record]["test_file"]
                ttk.Label(statistics,
                          text=str_value).grid(row=record, column=14,
                                               padx=5, pady=5, sticky="w")

# -------------------- Loop though Statistics ----------------------- #

        def on_close():
            statistics.destroy()

        statistics.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == '__main__':
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()    # start the GUI event loop
