from krita import Krita
from PyQt5.QtWidgets import QDialog, QColorDialog
from .points_editor import PointsEditorDialog
from PyQt5.QtGui import QColor
import json


def open_points_editor(current_value=None):
    if current_value and isinstance(current_value, str):
        current_value = current_value.strip()
        if current_value and current_value.startswith("{") and current_value.endswith("}"):
            try:
                points_data = json.loads(current_value)
                if isinstance(points_data, dict) and "coordinates_positive" in points_data and "coordinates_negative" in points_data:
                    pos_pts = points_data.get("coordinates_positive", [])
                    neg_pts = points_data.get("coordinates_negative", [])
                    # validate pos_pts and neg_pts are lists of {x: float, y:float} pairs
                    if not (isinstance(pos_pts, list) and all(isinstance(pt, dict) and "x" in pt and "y" in pt for pt in pos_pts)):
                        print("Positive points not in expected format:" + str(pos_pts))
                        pos_pts = []
                    if not (isinstance(neg_pts, list) and all(isinstance(pt, dict) and "x" in pt and "y" in pt for pt in neg_pts)):
                        print("Negative points not in expected format:" + str(neg_pts))
                        neg_pts = []

                    if not pos_pts and not neg_pts:
                        current_value = None
                        print("No valid points found in JSON.:" + str(current_value))
                    else:
                        current_value = {
                            "coordinates_positive": pos_pts,
                            "coordinates_negative": neg_pts
                        }
                else:
                    print("JSON not in expected coordinates format:" + str(current_value))
                    current_value = None
            except json.JSONDecodeError:
                print("failed to parse possible JSON: "+ str(current_value))
                current_value = None
        else:
            current_value = None
    else:
        current_value = None

    dialog = PointsEditorDialog(Krita.instance().activeWindow().qwindow(), existing_points=current_value)
    if dialog.exec_() == QDialog.Accepted:
        return dialog.get_prompt_text()
    return None

def pick_random_seed():
    import random
    return random.randint(0, 4294967295)

def pick_color_as_int(current_value=None):
    current_color = QColor(128, 128, 128)  # default
    if current_value is not None:
        try:
            val = int(current_value)
            if 0 <= val <= 0xFFFFFF:
                r = (val >> 16) & 0xFF
                g = (val >> 8) & 0xFF
                b = val & 0xFF
                current_color = QColor(r, g, b)
        except (ValueError, TypeError):
            pass

    color = QColorDialog.getColor(current_color, None, _("Select Color"))
    if color.isValid():
        return (color.red() << 16) | (color.green() << 8) | color.blue()
    return None

def get_krita_foreground_color_as_int():
    try:
        krita = Krita.instance()
        view = krita.activeWindow().activeView()
        fg = view.foregroundColor()
        if fg.isValid():
            return (fg.red() << 16) | (fg.green() << 8) | fg.blue()
    except:
        pass
    return None
