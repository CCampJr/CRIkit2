# Notes
* Unit testing and coverage skips the qt-related files in /ui
* Unit testing skips CRIKitUI.py because it's primarily pyqt

# TODO
* Refactor classes_ui to correctly initialize parent class and use no or fewer class attributes
* Create an abstract class for action that has calculate, _calc, and _transform
* Refactor PhaseError* and ScaleError to accept external methods rather than
explicitly being tied to ALS, for example