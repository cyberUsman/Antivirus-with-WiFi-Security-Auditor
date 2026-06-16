import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "security_audit.db")

VIRUS_SIGNATURES = {
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Simulation.Threat.EmptyFile",
    "44d88612fe8a7f3ec78e5e7af35f292150937a060e2270923f5b08eb45d654f1": "Threat.Test.Pattern.A",
    "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03": "Threat.Test.Pattern.B"
}
