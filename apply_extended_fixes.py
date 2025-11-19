"""
Extended fixes for remaining corrupted unicode
"""

# Read the file
with open('sms.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Specific line fixes
fixes_by_line = {
    7686: ('                                          "#27ae60", "Æ│")', '                                          "#27ae60", "📊")'),
    10861: ('        photo_clear_btn = self.create_enhanced_form_button(photo_buttons_frame, "ùæ∩╕Å Clear Photo",', '        photo_clear_btn = self.create_enhanced_form_button(photo_buttons_frame, "🧹 Clear Photo",'),
    10881: ('        clear_docs_btn = self.create_enhanced_form_button(docs_buttons_frame, "ùæ∩╕Å Clear All",', '        clear_docs_btn = self.create_enhanced_form_button(docs_buttons_frame, "🧹 Clear All",'),
    10930: ('        delete_btn = self.create_enhanced_form_button(button_row2, "ùæ∩╕Å Delete Selected",', '        delete_btn = self.create_enhanced_form_button(button_row2, "🧹 Delete Selected",'),
    12106: ('        save_btn = self.create_modern_button(right_buttons, "Æ╛ Save Changes",', '        save_btn = self.create_modern_button(right_buttons, "💾 Save Changes",'),
    12386: ('                                 "Æí Tip: Click on a student name to select, or hold Ctrl to select multiple students.")', '                                 "💡 Tip: Click on a student name to select, or hold Ctrl to select multiple students.")'),
    13938: ('                      f"Æí Alternative: Consider deactivating the user instead\\n"', '                      f"💡 Alternative: Consider deactivating the user instead\\n"'),
    13953: ('                                       f"ùæ∩╕Å User \'{username}\' has been permanently deleted.\\n\\n"', '                                       f"🧹 User \'{username}\' has been permanently deleted.\\n\\n"'),
    14208: ('        add_btn = self.create_modern_button(btns, "Æ╛ Add Payment", self.add_fee, \'primary\', width=15)', '        add_btn = self.create_modern_button(btns, "💾 Add Payment", self.add_fee, \'primary\', width=15)'),
    14214: ('        delete_btn = self.create_modern_button(btns, "ùæ∩╕Å Delete Payment", self.delete_fee, \'danger\', width=15)', '        delete_btn = self.create_modern_button(btns, "🧹 Delete Payment", self.delete_fee, \'danger\', width=15)'),
    19112: ('        notebook.add(finance_tab, text="Æ▒ Currency & Finance")', '        notebook.add(finance_tab, text="💳 Currency & Finance")'),
    19221: ('        currency_frame = tk.LabelFrame(content, text="Æ▒ Currency Settings",', '        currency_frame = tk.LabelFrame(content, text="💳 Currency Settings",'),
    21077: ('        tk.Label(rec_box, text=f"Æí Recommendation: {risk_score[\'recommendation\']}",', '        tk.Label(rec_box, text=f"💡 Recommendation: {risk_score[\'recommendation\']}",'),
}

# Apply fixes
for line_num in sorted(fixes_by_line.keys(), reverse=True):
    idx = line_num - 1  # Convert to 0-based index
    old, new = fixes_by_line[line_num]
    if idx < len(lines):
        if old.strip() in lines[idx]:
            lines[idx] = lines[idx].replace(old, new)
            print(f"✓ Fixed line {line_num}")
        else:
            print(f"⚠ Could not match line {line_num} exactly")

# Write back
with open('sms.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Extended fixes applied!")
