# Bittinikkari - engine.py
import os
import shutil
from datetime import datetime
import json
import re
import xml.etree.ElementTree as ET

# Käytetään sovittua config-tiedostoa
CONFIG_PATH = "config/config.json"

def load_settings():
    if not os.path.exists(CONFIG_PATH) or os.path.getsize(CONFIG_PATH) == 0:
        return create_default_settings() # Luodaan uudet jos tiedosto on tyhjä

    """Lataa asetukset tai luo oletustiedoston tarvittaessa."""
    # 1. Varmistetaan kansion olemassaolo
    config_dir = os.path.dirname(CONFIG_PATH)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"Luotu kansio: {config_dir}")

    # Oletusasetukset bittinikkarille
    default_settings = {
        "project_name": "bittinikkari",
        "current_project": "",
        "language": "fi",
        "backup_dir": "backups",
        "theme": "light"
    }

    # 2. Varmistetaan tiedoston olemassaolo
    if not os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(default_settings, f, indent=4)
            print(f"Luotu oletusasetukset: {CONFIG_PATH}")
            return default_settings
        except Exception as e:
            print(f"Virhe oletusasetusten luonnissa: {e}")
            return default_settings
            
    # 3. Luetaan olemassa oleva tiedosto
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Virhe asetusten luvussa: {e}")
        return default_settings

def save_settings(settings):
    """Tallentaa asetukset config.json tiedostoon."""
    try:
        # Korjattu: CONFIG_FILE -> CONFIG_PATH
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Virhe asetusten tallennuksessa: {e}")

def get_project_name():
    """Hakee projektin nimen asetuksista, oletuksena bittinikkari."""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("project_name", "bittinikkari")
    except:
        pass
    return "bittinikkari"

def process_full_project(project_path, settings):
    """
    Käy läpi kaikki .cbp-tiedostossa määritellyt tiedostot ja ajaa niille fix-logiikan.
    Palauttaa (muutosten_maara, lista_huomioista).
    """
    if not project_path or not os.path.exists(project_path):
        return 0, ["Projektitiedostoa ei löytynyt."]

    total_changes = 0
    all_issues = []
    project_dir = os.path.dirname(os.path.abspath(project_path))

    try:
        tree = ET.parse(project_path)
        root = tree.getroot()

        # Etsitään kaikki Unit-tagit, joissa on tiedostonimi
        for unit in root.findall(".//Unit"):
            rel_path = unit.get("filename")
            if not rel_path:
                continue

            # Muodostetaan täysi polku suhteessa .cbp-tiedostoon
            full_path = os.path.join(project_dir, rel_path)

            if os.path.exists(full_path):
                # Ajetaan aiemmin luotu run_fixing_logic jokaiselle tiedostolle
                changes, issues = run_fixing_logic(full_path, settings)
                total_changes += changes
                if issues:
                    all_issues.append(f"--- {rel_path} ---")
                    all_issues.extend(issues)
            else:
                all_issues.append(f"HUOMIO: Tiedostoa {rel_path} ei löydy levyltä.")

        return total_changes, all_issues

    except Exception as e:
        return 0, [f"Projektin käsittelyvirhe: {e}"]

def fix_indentation(content):
    lines = content.split('\n')
    fixed_lines = []
    for line in lines:
        # Muutetaan tabit 4 välilyönniksi ja poistetaan turha tyhjä lopusta
        line = line.replace('\t', '    ').rstrip()
        fixed_lines.append(line)
    return '\n'.join(fixed_lines)

def run_fixing_logic(file_path, settings):
    """Bittinikkarin ydintoiminto: Varmuuskopiot, Lisenssi ja C-muistinhallinta."""
    issues = []
    changes = 0
    project_name = get_project_name()

    if not file_path or not os.path.exists(file_path):
        return 0, ["Tiedostoa ei löytynyt."]

    # 1. VARMUUSKOPIO (Backup) - Tallennetaan configissa määriteltyyn paikkaan
    backup_dir = settings.get("backup_dir", "backups")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"{os.path.basename(file_path)}.{timestamp}.bak")
    shutil.copy2(file_path, backup_path)
    issues.append(f"Varmuuskopio luotu: {backup_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 2. GPL-LISENSSIN LISÄYS (Dynaaminen projektin nimi)
    gpl_header = f"/*\n * Lisenssi: GNU GPLv3\n * Projekti: {project_name}\n */\n"
    if "GPLv3" not in content:
        content = gpl_header + content
        changes += 1
        issues.append(f"GPLv3-lisenssi lisätty ({project_name}).")

    # 3. KEVYT MUISTINHALLINTA (C-kieli)
    if file_path.endswith((".c", ".h")):
        malloc_count = len(re.findall(r'\bmalloc\(', content))
        free_count = len(re.findall(r'\bfree\(', content))

        if malloc_count > free_count:
            issues.append(f"HUOM: {malloc_count} malloc vs {free_count} free. Muista vapauttaa muisti!")
        elif malloc_count < free_count:
            issues.append(f"HUOM: free-kutsuja ({free_count}) on enemmän kuin varauksia.")

    # 4. AUTOMAATTINEN SISENNYS
    old_content = content
    content = fix_indentation(content)
    if old_content != content:
        changes += 1
        issues.append("Sisennykset ja tyhjät välit siivottu.")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return changes, issues




