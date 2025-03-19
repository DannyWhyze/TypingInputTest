# [project-name]/[project-name]/README.md

# Typing Test App

## Description

This project is a PyQt6-based interactive typing speed test application built on Object-Oriented Programming (OOP) principles. The application measures typing speed, accuracy, and calculates a score based on various factors such as speed, consistency, and error rate.

## Directory Structure

```
Typing-Test-App
├── main.py                     # Entry point of the application
├── highscores.json             # Stored highscores
├── README.md                   # Documentation
├── requirements.txt            # Dependencies
├── src
│   ├── controllers             # Controller components
│   ├── models                  # Data models and logic
│   │   ├── highscore_model.py  # Highscore management
│   │   ├── main_model.py       # Main logic
│   │   └── statisticsModel.py  # Statistics calculations
│   ├── ressources              # Text resources
│   │   └── wortschatzGrund1.txt # Word list file
│   ├── utils                   # Helper functions
│   └── views                   # UI components
│       ├── buttonsUI.py        # Button bar
│       ├── countdown.py        # Timer display
│       ├── highscores_window.py # Highscore window
│       ├── input_field.py      # Text input field
│       ├── main_window.py      # Main window
│       ├── menu_bar.py         # Menu bar
│       ├── results_window.py   # Results window
│       ├── statistics_widget.py # Statistics widget
│       ├── target_text_widget.py # Target text display
│       ├── textinfos.py        # Information display
│       └── tip_info.py         # Typing information
└── tests                       # Test cases
    ├── test_models.py          # Tests for models
    ├── test_statistics.py      # Tests for statistics functions
    
```
## Features

Flexible Time Settings: Choose between 1, 3, or 5-minute tests
Real-time Feedback: Color-coded marking of correct, partially correct, and incorrect inputs
Detailed Statistics: Analysis of keystrokes per minute, error rate, and typing accuracy
Highscore System: Save and compare your results
Bonus Points System: Earn additional points for sequences of error-free words, high speed, and consistent typing

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/DannyWhyze/TypingInputTest.git
   cd typing-test-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage

1. Start a Test: Select a test duration (1, 3, or 5 minutes) by clicking the corresponding buttons
2. Begin Typing: The timer starts automatically once you begin typing
4. Track Progress: The color-coded display shows correct (green), half-right (yellow), and incorrect (red) inputs
4. View Results: After time expires, detailed statistics and a score are displayed
5. Save Highscore: Enter your name to save your highscore
6. Restart: Start a new test or compare highscores with others

# Scoring System

## Base Points

+1 point for each correctly typed character

## Deductions

-1 point for each half-right word (incorrect capitalization)
-2 points for each wrong word
-1 point per backspace used

## Bonuses

+50 points for 10 error-free words in sequence
+100/+250/+500 points depending on keystrokes per minute
+200 points for consistent typing speed

# Testing

To run the tests, use the following command:

pytest test_statistics.py -v --color=yes

pytest test_statistics.py -v -s --color=yes

# Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

# Author

Danny Whyze
Organization: Bars2Bars

# License

This project is licensed under the [Your License] - see the LICENSE file for details.