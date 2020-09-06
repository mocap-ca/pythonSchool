import os
import sys
import json

import QuestionTemplate
import ResultTemplate
import WelcomeTemplate
from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial


class HangmanDialog(QtWidgets.QDialog):
    """ Sets up the dialog widget for the game, includes all the game logic.
        TODO: When game ends, ask to start over.
        TODO: When movie has been guessed, display "correct", and display a "next" button."""

    def __init__(self, parent=None):
        """ Initializes the dialog by creating the necessary UI framework, and setting the basic design/style.
        Creates a layout for the app, and adds a stacked widget to it.
        The stacked widget will contain 3 pages. All three pages are initialized.
        If there are no errors in loading the questions, starts the game.
        :param parent: provides ability to connect to external applications like Maya.
        :type parent: QWidget. """
        super(HangmanDialog, self).__init__(parent)

        self.setWindowTitle("Hangman Beta © Meg Mugur 2020")
        self.setStyleSheet("background-color: #D1D1D1")
        self.text_font = QtGui.QFont("Verdana", 10)

        self.game_stack_layout = QtWidgets.QVBoxLayout()
        self.create_game_stack_widget()
        self.game_stack_layout.addWidget(self.game_stack_widget)
        self.setLayout(self.game_stack_layout)

        self.database_error = False

        self.initialize_completed = False
        self.initialize_welcome_page()
        self.initialize_question_page()
        self.initialize_result_page()
        self.initialize_completed = True

        if not self.database_error:
            self.setup_welcome_page()
        else:
            self.setup_result_page()

    def create_game_stack_widget(self):
        """Creates a stack of widgets for the pages of the game: Welcome page, Question page, Result page."""
        self.game_stack_widget = QtWidgets.QStackedWidget()

        self.question_page_widget = QtWidgets.QWidget()
        self.welcome_page_widget = QtWidgets.QWidget()
        self.result_page_widget = QtWidgets.QWidget()

        self.game_stack_widget.addWidget(self.welcome_page_widget)
        self.game_stack_widget.addWidget(self.question_page_widget)
        self.game_stack_widget.addWidget(self.result_page_widget)

        self.stack_design()

    def stack_design(self):
        """Basic design settings of the stack."""
        self.setFixedWidth(800)
        self.setFixedHeight(600)

    def initialize_welcome_page(self):
        """ Creates an object of WelcomeClass. Sets uniform style. Makes signal-slot connection."""
        self.welcome_object = WelcomeTemplate.WelcomeClass()
        self.welcome_object.welcome_font = self.text_font
        self.welcome_object.setup_welcome_layout()
        self.welcome_object.enter_button.pressed.connect(self.setup_question_page)

    def setup_welcome_page(self):
        """Sets the current widget to welcome_page_widget, and sets its layout to the one from the welcome_object"""
        self.welcome_page_widget.setLayout(self.welcome_object.welcome_layout)
        self.game_stack_widget.setCurrentWidget(self.welcome_page_widget)

    def initialize_question_page(self):
        """Initializes the question page by creating an object of the QuestionClass type.
        Loads questions from the database into a list. In case of error, sets error flag to true and returns.
        If loading is successful, makes signal-slot connections for all buttons.
        Sends button name to the slot using Partial.
        :return : None"""

        self.index_of_clicked_button = -1
        self.ALLOWED_ATTEMPTS = 9                                           # hard-coding alert
        self.directory_path = "Database/MoviesDatabase.json"                # hard-coding alert
        self.correct_guess_count = 0
        self.question_index = 0
        self.image_path = ""
        self.questions_list = []

        if not os.path.isfile(self.directory_path) or not os.access(self.directory_path, os.R_OK) :
            self.database_error = True
            print("Error: Directory not found or not readable")
            return

        database_file = open(self.directory_path)
        try:                                                    # case: data loading successful.
            self.questions_dict = json.load(database_file)
            for movie_names in self.questions_dict:
                self.questions_list.append(movie_names)
        except ValueError as json_error:
            self.database_error = True
            print("Error: ", json_error)
            return
        if not self.questions_list:
            self.database_error = True
            print("Error: Movies list is empty")
            return

        self.question = self.questions_list[0]
        self.question_object = QuestionTemplate.QuestionClass(self.question)
        for index, button in enumerate(self.question_object.alphabet_button_list):
            self.question_object.alphabet_button_list[index].clicked.connect(
                partial(self.examine_guessed_alphabet, button))

    def setup_question_page(self):
        """Basic setting up of the Question page."""
        # While setting up signal-slot connection in welcome page initialization, no need to setup questions page.
        if self.initialize_completed == False:
            return

        self.question = self.questions_list[self.question_index]
        self.question_object.setup_question_layout(self.question)
        self.question_page_widget.setLayout(self.question_object.question_layout)
        self.game_stack_widget.setCurrentWidget(self.question_page_widget)
        self.setup_clue_image()

    def setup_clue_image(self):
        """ Loads the image into image_label on questions page."""
        self.image_path = "Images/" + self.question.replace(" ", "") + "/"\
                          + self.questions_dict[self.question][:-4].replace(" ", "") + "_"\
                          + str(self.ALLOWED_ATTEMPTS - self.question_object.health_loss)\
                          + self.questions_dict[self.question][-4:]
        self.question_object.image_label.setPixmap(self.image_path)

    def examine_guessed_alphabet(self, clicked_button):
        """Checks if the alphabet clicked on, exists in movie name.
        If it exists, fills out the corresponding boxes with that letter.
        If it exists, and the entire movie name has been filled, goes to next question.
        If it does not exist, reduces health.
        If it does not exist, and health is already zero, ends the game.
        :param clicked_button : the button which calls this method, when clicked on.
        :type clicked_button : QPushButton"""

        self.index_of_clicked_button = self.question_object.alphabet_button_list.index(clicked_button)
        self.clicked_button = clicked_button
        self.clicked_button.setEnabled(False)
        self.clicked_button.setStyleSheet("border : 0")
        if self.question_object.alphabet_list[self.index_of_clicked_button].upper() in self.question.upper():
            self.find_alphabet_position()
        elif self.question_object.health_loss < self.ALLOWED_ATTEMPTS:
            self.question_object.health_loss += 1
            self.setup_clue_image()
        else:
            self.result = "failure"
            self.setup_result_page()

    def find_alphabet_position(self):
        """Looks for the position of the selected alphabet in the movie name.
        Each time the alphabet is found, increments correct_guess_count.
        Once the entire movie name has been guessed correctly, goes to next question.
        If questions list is exhausted, proceeds to result page."""
	button = self.index_of_clicked_button
        for pos, char in enumerate(self.question):
            if self.question_object.alphabet_list[button].upper() != char.upper():
                continue
            self.question_object.answer_letters_list[pos].setText(
                self.question_object.alphabet_list[button].upper())
            self.correct_guess_count += 1
            if self.correct_guess_count != len(self.question) - self.question.count(" "):
                continue
            if self.question_index + 1 == len(self.questions_list):
                self.result = "success"
                self.setup_result_page()
                break
            self.setup_next_question_page()

    def initialize_next_question_page(self):
        """Initialization and basic setting up of the next Question page.
        Deletes the old question widget, creates a new one, adds to stack, and sets as current page."""
        self.question_page_widget.deleteLater()
        self.question_page_widget = QtWidgets.QWidget()
        self.game_stack_widget.addWidget(self.question_page_widget)
        self.question = self.questions_list[self.question_index]
        self.question_object = QuestionTemplate.QuestionClass(self.question)
        self.question_object.setup_question_layout(self.question)
        self.question_page_widget.setLayout(self.question_object.question_layout)
        self.game_stack_widget.setCurrentWidget(self.question_page_widget)

    def setup_next_question_page(self):
        """Resets some parameters for new question. Sets up a new question page."""
        self.question_index += 1
        del self.question_object
        self.index_of_clicked_button = -1
        self.correct_guess_count = 0
        self.initialize_next_question_page()
        for index, button in enumerate(self.question_object.alphabet_button_list):
            self.question_object.alphabet_button_list[index].clicked.connect(
                partial(self.examine_guessed_alphabet, button))
        self.setup_clue_image()

    def initialize_result_page(self):
        """Creates an object of the welcome page. Assigns values to the object's result string and text font."""
        self.result_object = ResultTemplate.ResultClass()
        self.result_object.result_font = self.text_font

    def setup_result_page(self):
        """Sets the result message, and displays the result page."""
        if self.database_error:
            self.result = "error"
        self.result_object.result = self.result
        self.result_object.setup_result_layout()
        self.result_page_widget.setLayout(self.result_object.result_layout)
        self.game_stack_widget.setCurrentWidget(self.result_page_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    game_dialog = HangmanDialog()
    game_dialog.exec_()

