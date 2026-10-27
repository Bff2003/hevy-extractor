import json
import os

INPUT_FILE = "workouts_backup.json"
OUTPUT_FILE = "workouts_clean.json"

def clean_set(s):
    cleaned = {
        "index": s.get("index"),
        "type": s.get("indicator", "normal"),
        "weight_kg": s.get("weight_kg"),
        "reps": s.get("reps"),
    }
    if s.get("rpe") is not None:
        cleaned["rpe"] = s["rpe"]
    if s.get("completed_at"):
        cleaned["completed_at"] = s["completed_at"]
    return cleaned

def clean_exercise(ex):
    # Dá prioridade ao nome em português de Portugal se existir, senão usa o title em inglês
    name = ex.get("pt_title") or ex.get("title")

    cleaned = {
        "name": name,
        "muscle_group": ex.get("muscle_group"),
        "equipment": ex.get("equipment_category"),
        "rest_seconds": ex.get("rest_seconds"),
        "notes": ex.get("notes") or "",
        "sets": [clean_set(s) for s in ex.get("sets", [])]
    }

    if ex.get("other_muscles"):
        cleaned["secondary_muscles"] = ex["other_muscles"]

    return cleaned

def clean_workout(w):
    return {
        "id": w.get("id"),
        "name": w.get("name"),
        "nth_workout": w.get("nth_workout"),
        "created_at": w.get("created_at"),
        "start_time": w.get("start_time"),
        "end_time": w.get("end_time"),
        "estimated_volume_kg": w.get("estimated_volume_kg"),
        "description": w.get("description") or "",
        "exercises": [clean_exercise(ex) for ex in w.get("exercises", [])]
    }

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"[ERRO] O ficheiro '{INPUT_FILE}' não foi encontrado na pasta atual.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_workouts = data.get("workouts", [])
    cleaned_workouts = [clean_workout(w) for w in raw_workouts]

    output_payload = {"workouts": cleaned_workouts}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)

    original_size = os.path.getsize(INPUT_FILE) / 1024
    cleaned_size = os.path.getsize(OUTPUT_FILE) / 1024
    reduction = (1 - (cleaned_size / original_size)) * 100 if original_size > 0 else 0

    print(f"Limpeza concluída com sucesso!")
    print(f"Treinos processados: {len(cleaned_workouts)}")
    print(f"Tamanho original: {original_size:.1f} KB -> Limpo: {cleaned_size:.1f} KB (Redução de {reduction:.1f}%)")
    print(f"Ficheiro gerado: '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()