class Config:
    GAMENAME = "Fruit Ninja WebCam"
    HEIGHT = 800
    WIDTH = 600
    FPS = 30

    SPAWN_INTERVAL = 500

    LEVEL = "easy"
    SETTINGS = {
        "easy": {
            "health": 3,
            "score_to_win": 100,
            "bomb_prob": 0.1
        },
        "medium": {
            "health": 2,
            "score_to_win": 150,
            "bomb_prob": 0.15
        },
        "hard": {
            "health": 1,
            "score_to_win": 200,
            "bomb_prob": 0.5
        }
    }

    @classmethod
    def get(cls, key):
        return cls.SETTINGS[cls.LEVEL][key]

    
