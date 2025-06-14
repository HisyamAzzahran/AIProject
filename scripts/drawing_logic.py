import cv2
import numpy as np
import time
import easyocr

def draw_text_with_background(frame, text, position, font, font_scale, text_color, bg_color, thickness=1, alpha=0.6):
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = position
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y - text_height - baseline), (x + text_width, y + baseline), bg_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.putText(frame, text, position, font, font_scale, text_color, thickness)

def draw_progress_bar(frame, progress, position, size, color):
    x, y = position
    width, height = size
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + width, y + height), (50, 50, 50), -1)
    progress_width = int(min(progress, 1.0) * width)
    cv2.rectangle(overlay, (x, y), (x + progress_width, y + height), color, -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

class DrawingLogic:
    def __init__(self):
        self.canvas = None
        self.prev_x, self.prev_y = None, None
        self.color = (255, 255, 255)
        self.thickness = 5
        self.drawing_mode = False
        self.erasing_mode = False
        self.status_text = "Idle"
        self.idle_start_time = None
        self.has_processed = False
        self.detected_text = ""

        self.colors = [(255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
        self.color_names = ["White", "Red", "Green", "Blue"]
        self.selected_color_index = 0

        self.background = cv2.imread("backgrounds/grid.png")
        self.icons = {
            "Idle": "icons/idle.png",
            "Drawing": "icons/drawing.png",
            "Erasing": "icons/erasing.png",
            "Processing": "icons/process_icon.png"
        }

    def initialize_canvas(self, frame_shape):
        self.canvas = np.zeros(frame_shape, dtype=np.uint8)

    def draw(self, frame, index_finger):
        index_x, index_y = index_finger
        h, w, _ = frame.shape

        self.draw_color_palette(frame)

        if self.background is not None:
            background = cv2.resize(self.background, (w, h))
            frame[:] = cv2.addWeighted(frame, 0.7, background, 0.3, 0)

        self.draw_color_palette(frame)

        if self.drawing_mode:
            if self.prev_x is not None and self.prev_y is not None:
                for i in np.linspace(0, 1, num=10):
                    x = int(self.prev_x + i * (index_x - self.prev_x))
                    y = int(self.prev_y + i * (index_y - self.prev_y))
                    cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y), self.color, self.thickness)
            self.prev_x, self.prev_y = index_x, index_y
        elif self.erasing_mode:
            cv2.circle(self.canvas, (index_x, index_y), 30, (0, 0, 0), -1)
        else:
            self.prev_x, self.prev_y = None, None

        draw_text_with_background(frame, f"Status: {self.status_text}", (30, h - 30),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), (0, 0, 0), 2)

        if self.status_text == "Idle" and self.idle_start_time:
            elapsed = time.time() - self.idle_start_time
            progress = min(elapsed / 7, 1.0)
            draw_progress_bar(frame, progress, (w - 200, h - 30), (150, 20), (0, 255, 255))

        icon_path = self.icons.get(self.status_text)
        if icon_path:
            self.overlay_icon(frame, icon_path, (w - 100, 10))

    def overlay_icon(self, frame, path, position):
        x, y = position
        icon = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if icon is None or icon.shape[2] != 4:
            return
        icon = cv2.resize(icon, (50, 50))
        alpha = icon[:, :, 3] / 255.0
        overlay = icon[:, :, :3]
        for c in range(3):
            frame[y:y+50, x:x+50, c] = (1 - alpha) * frame[y:y+50, x:x+50, c] + alpha * overlay[:, :, c]

    def draw_color_palette(self, frame):
        for i, color in enumerate(self.colors):
            x1, y1 = i * 100, 0
            x2, y2 = (i + 1) * 100, 50
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
            if i == self.selected_color_index:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
            cv2.putText(frame, self.color_names[i], (x1 + 10, y2 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    def check_color_selection(self, landmarks):
        index_tip = landmarks[8]
        x = int(index_tip.x * self.canvas.shape[1])
        y = int(index_tip.y * self.canvas.shape[0])
        if y < 50:
            index = x // 100
            if 0 <= index < len(self.colors):
                self.selected_color_index = index
                self.color = self.colors[index]

    def toggle_modes(self, landmarks):
        tip = landmarks[8].y
        base = landmarks[6].y
        fist = all(landmarks[i].y > landmarks[i - 2].y for i in [8, 12, 16, 20])
        pointing = (tip < base) and all(landmarks[i].y > landmarks[i - 2].y for i in [12, 16, 20])

        if fist:
            self.drawing_mode = False
            self.erasing_mode = True
            self.status_text = "Erasing"
            self.idle_start_time = None
            self.has_processed = False
        elif pointing:
            self.drawing_mode = True
            self.erasing_mode = False
            self.status_text = "Drawing"
            self.idle_start_time = None
            self.has_processed = False
        else:
            self.drawing_mode = False
            self.erasing_mode = False
            if not self.idle_start_time:
                self.idle_start_time = time.time()
                self.check_color_selection(landmarks)
            self.status_text = "Idle"

    def process_canvas(self):
        if self.idle_start_time:
            elapsed = time.time() - self.idle_start_time
            if elapsed >= 7 and not self.has_processed:
                self.status_text = "Processing"
                self.has_processed = True
                processed = self.preprocess_for_ocr(self.canvas)
                reader = easyocr.Reader(['en'], gpu=False)
                results = reader.readtext(processed, detail=0)
                self.detected_text = " ".join(results)
                try:
                    value = eval(self.detected_text, {"__builtins__": {}}, {})
                    self.status_text = f"Result: {value}"
                except:
                    self.status_text = "Invalid Expression"
                self.clear_canvas()
                self.idle_start_time = None

    def preprocess_for_ocr(self, canvas):
        gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return cv2.resize(binary, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    def clear_canvas(self):
        self.canvas.fill(0)

    def get_result(self):
        return {
            "detected_text": self.detected_text,
            "status_text": self.status_text
        }
