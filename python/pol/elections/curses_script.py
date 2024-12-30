"""
    new_corrections = {}
    with open(PYTHON_PACKAGE_DIR / "elections/corrections.json", "r") as f:
        old_corrections = json.load(f)

    def add_to_corrections(geo_name, geo_id, ec_name, ec_province, corrections):
        new_entry = {"name": ec_name, "province": ec_province, "geo_name": geo_name}
        if geo_id in corrections:
            old_entry = corrections[geo_id]
            if isinstance(old_entry, list):
                old_entry.append(new_entry)
            else:
                corrections[geo_id] = [old_entry, new_entry]
        else:
            corrections[geo_id] = new_entry

    import curses
    def run_labeler(stdscr, ridings, unassigned_ridings):
        ur_index = 0
        geo_index = 0
        selected = ""

        PROVINCE_CODES = {
            "10": "Newfoundland and Labrador",
            "11": "Prince Edward Island",
            "12": "Nova Scotia",
            "13": "New Brunswick",
            "24": "Quebec",
            "35": "Ontario",
            "46": "Manitoba",
            "47": "Saskatchewan",
            "48": "Alberta",
            "59": "British Columbia",
            "60": "Yukon",
            "61": "Northwest Territories",
            "62": "Nunavut",
        }

        unassigned_ridings = [r for r in unassigned_ridings if r["ro_year"] != 2003]
        curses.curs_set(0)
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            ur = unassigned_ridings[ur_index]
            year_ridings = sorted(ridings[str(ur['ro_year'])], key=lambda r: r["name"])
            province_ridings = [r for r in year_ridings if PROVINCE_CODES[r["id"][4:6]] == ur["province"]]

            start_date = f"{ur['start_date']['year']}-{ur['start_date']['month']}-{ur['start_date']['day']}"
            end_date = f"{ur['end_date']['year']}-{ur['end_date']['month']}-{ur['end_date']['day']}"
            stdscr.addstr(
                0, 0,
                f"{ur['name']}, {ur['province']}  |  {start_date} - {end_date}  |  {ur['ro_year']}",
                curses.A_BOLD | curses.A_UNDERLINE
            )

            middle = (height // 2) - 1
            for y in range(2, height):
                list_index = max(min(geo_index + y - 1 - middle, len(province_ridings)), -1)
                if list_index == len(province_ridings):
                    break
                elif list_index < 0:
                    continue
                attr = curses.A_STANDOUT if list_index == geo_index else curses.A_NORMAL
                geo_riding = province_ridings[list_index]
                check = "✓" if (geo_riding["id"] in new_corrections and new_corrections[geo_riding["id"]]["name"] == ur["name"]) else " "
                stdscr.addstr(y, 0, f"{check} {geo_riding["name"]}", attr)

            ch = stdscr.getch()
            if ch == curses.KEY_RIGHT:
                ur_index = min(len(unassigned_ridings) - 1, ur_index + 1)
                geo_index = 0
            elif ch == curses.KEY_LEFT:
                ur_index = max(0, ur_index - 1)
                geo_index = 0
            elif ch == curses.KEY_UP:
                geo_index = max(0, geo_index - 1)
            elif ch == curses.KEY_DOWN:
                geo_index = min(len(province_ridings) - 1, geo_index + 1)
            elif ch == curses.KEY_PPAGE:
                geo_index = max(0, geo_index - 10)
            elif ch == curses.KEY_NPAGE:
                geo_index = min(len(province_ridings) - 1, geo_index + 10)
            elif ch == ord(" "):
                geo_riding = province_ridings[geo_index]
                for k, v in new_corrections.copy().items():
                    if v["name"] == ur["name"] and v["province"] == ur["province"] and k[:4] == str(ur["ro_year"]):
                        new_corrections.pop(k)

                add_to_corrections(
                    geo_riding["name"],
                    geo_riding["id"],
                    ur["name"],
                    ur["province"],
                    new_corrections,
                )
                ur_index = min(len(unassigned_ridings) - 1, ur_index + 1)
                geo_index = 0

    try:
        curses.wrapper(run_labeler, ridings, unassigned_ridings)
    except KeyboardInterrupt:
        pass

    print(f"New corrections: {len(new_corrections)}")
    for k, v in new_corrections.items():
        if isinstance(v, list):
            for entry in v:
                add_to_corrections(
                    entry["geo_name"],
                    k,
                    entry["name"],
                    entry["province"],
                    old_corrections,
                )
        else:
            add_to_corrections(
                v["geo_name"],
                k,
                v["name"],
                v["province"],
                old_corrections,
            )
    with open(PYTHON_PACKAGE_DIR / "elections/corrections.json", "w") as f:
        json.dump(old_corrections, f, indent=4, ensure_ascii=False, sort_keys=True)

    exit(0)
"""
