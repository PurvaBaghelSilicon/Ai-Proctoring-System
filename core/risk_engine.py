import time

class RiskEngine:
    def __init__(self):
        self.last_phone = None
        self.last_no_face = None
        self.last_multi_face = None
        self.last_look_away = None

        self.risk = 0                  # temporary risk (decays)
        self.permanent_risk = 0        # permanent penalties
        self.last_decay = time.time()

    def _elapsed(self, t, secs):
        return t is not None and (time.time() - t) >= secs

    def update(self, face_count, looking_away, phone_detected):
        now = time.time()
        delta = 0

        # ---------- NO FACE ----------
        if face_count == 0:
            if self.last_no_face is None:
                self.last_no_face = now
            elif self._elapsed(self.last_no_face, 2):
                delta += 5
                self.last_no_face = now
        else:
            self.last_no_face = None

        # ---------- MULTIPLE FACES ----------
        if face_count > 1:
            if self.last_multi_face is None:
                self.last_multi_face = now
            elif self._elapsed(self.last_multi_face, 2):
                delta += 10
                self.last_multi_face = now
        else:
            self.last_multi_face = None

        # ---------- LOOKING AWAY ----------
        if looking_away:
            if self.last_look_away is None:
                self.last_look_away = now
            elif now - self.last_look_away >= 3:
                delta += 6
                self.last_look_away = now
        else:
            self.last_look_away = None

        # ---------- PHONE ----------
        if phone_detected:
            if self.last_phone is None:
                self.last_phone = now
            elif now - self.last_phone >= 5:
                self.permanent_risk += 15
                self.last_phone = now
        else:
            self.last_phone = None

        # ---------- APPLY DELTA ----------
        self.risk += delta

        # ---------- DECAY ----------
        if now - self.last_decay >= 1:
            self.risk = max(0, self.risk - 1)
            self.last_decay = now

        total_risk = self.risk + self.permanent_risk
        return total_risk, delta

    # ✅ THIS METHOD WAS MISSING
    def add_external_penalty(self, points):
        self.permanent_risk += points
        return self.risk + self.permanent_risk
