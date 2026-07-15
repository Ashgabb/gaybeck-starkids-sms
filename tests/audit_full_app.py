import ast
import os
import re
import sqlite3
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

SMS_FILE = os.path.join(PROJECT_ROOT, 'sms.py')
DB_CANDIDATES = [
    os.path.join(PROJECT_ROOT, 'school_management.db'),
    os.path.join(PROJECT_ROOT, 'database', 'school_management.db'),
]


def load_source(path):
    with open(path, 'r', encoding='utf-8-sig') as f:
        return f.read()


def parse_command_callbacks(source):
    tree = ast.parse(source)
    class_methods = {}
    command_callbacks = []
    bind_callbacks = []
    target_class = 'SchoolManagementSystem'

    class CallbackVisitor(ast.NodeVisitor):
        def __init__(self):
            self.class_stack = []

        def visit_ClassDef(self, node):
            self.class_stack.append(node.name)
            methods = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
            class_methods[node.name] = methods
            self.generic_visit(node)
            self.class_stack.pop()

        def visit_Call(self, node):
            current_class = self.class_stack[-1] if self.class_stack else None

            if current_class == target_class:
                for kw in node.keywords:
                    if kw.arg == 'command' and isinstance(kw.value, ast.Attribute):
                        val = kw.value
                        if isinstance(val.value, ast.Name) and val.value.id == 'self':
                            command_callbacks.append((current_class, val.attr, node.lineno))

            if current_class == target_class and isinstance(node.func, ast.Attribute) and node.func.attr == 'bind':
                if len(node.args) >= 2 and isinstance(node.args[1], ast.Lambda):
                    lam = node.args[1]
                    body = lam.body
                    if isinstance(body, ast.Call) and isinstance(body.func, ast.Attribute):
                        if isinstance(body.func.value, ast.Name) and body.func.value.id == 'self':
                            bind_callbacks.append((current_class, body.func.attr, node.lineno))

            self.generic_visit(node)

    CallbackVisitor().visit(tree)
    return class_methods, command_callbacks, bind_callbacks


def find_role_sets(source):
    tree = ast.parse(source)
    login_roles = set()
    form_roles = set()
    change_dialog_roles = set()

    def literal_tuple_first_items(list_node):
        results = []
        for item in getattr(list_node, 'elts', []):
            if isinstance(item, ast.Tuple) and item.elts:
                first = item.elts[0]
                if isinstance(first, ast.Constant) and isinstance(first.value, str):
                    results.append(first.value)
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'roles' and isinstance(node.value, ast.List):
                    roles = set(literal_tuple_first_items(node.value))
                    if 5 <= len(roles) <= 8:
                        login_roles = roles
                    elif 'student' in roles and 'viewer' in roles and 'accountant' in roles:
                        change_dialog_roles = roles

    # Extract the user form role list from the exact create_user_form method block.
    form_block = re.search(r'def create_user_form\(self, parent\):(.+?)\n    def ', source, re.S)
    if form_block:
        form_match = re.search(r'role_cb\s*=\s*ttk\.Combobox\(fields_frame,\s*textvariable=self\.user_role_var,\s*values=\[([^\]]+)\]', form_block.group(1), re.S)
        form_roles = set(re.findall(r"'([a-z_]+)'", form_match.group(1) if form_match else ''))
    if not form_roles:
        form_match = re.search(r'role_cb\s*=\s*ttk\.Combobox\(fields_frame,\s*textvariable=self\.user_role_var,\s*values=\[([^\]]+)\]', source, re.S)
        form_roles = set(re.findall(r"'([a-z_]+)'", form_match.group(1) if form_match else ''))

    # If AST couldn't isolate the change-role list, fall back to the exact method block only.
    if not change_dialog_roles:
        change_match = re.search(r'def change_user_role\(self\):(.+?)def ', source, re.S)
        if change_match:
            block = change_match.group(1)
            role_list_match = re.search(r'roles\s*=\s*\[(.*?)\]\s*\n\s*\n\s*for role, description in roles:', block, re.S)
            if role_list_match:
                change_dialog_roles = set(re.findall(r"\('([a-z_]+)'\s*,", role_list_match.group(1)))

    return login_roles, form_roles, change_dialog_roles


def test_permission_logic():
    import sms

    class Dummy:
        pass

    d = Dummy()
    has_permission = sms.SchoolManagementSystem.has_permission

    d.current_user = {'role': 'admin', 'permissions': []}
    if not has_permission(d, 'nonexistent_permission'):
        return False, 'Admin should always pass permission checks'

    d.current_user = {'role': 'teacher', 'permissions': ['dashboard', 'students']}
    if not has_permission(d, 'dashboard'):
        return False, 'Teacher with explicit list permission should pass'
    if has_permission(d, 'fees'):
        return False, 'Teacher without fees permission should fail'

    d.current_user = {'role': 'staff', 'permissions': 'dashboard,attendance'}
    if not has_permission(d, 'attendance'):
        return False, 'Comma-separated string permissions should be supported'

    d.current_user = {'role': 'viewer', 'permissions': []}
    if has_permission(d, 'students'):
        return False, 'Viewer without permission should fail'

    return True, 'Permission logic checks passed'


def find_database():
    for path in DB_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def db_role_audit(known_roles):
    db_path = find_database()
    if not db_path:
        return True, 'Database not found; role-value audit skipped'

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT DISTINCT role FROM users')
        db_roles = {row[0] for row in cursor.fetchall() if row and row[0]}
    finally:
        conn.close()

    unknown = sorted(r for r in db_roles if r not in known_roles)
    if unknown:
        return False, f'Unknown DB role values found: {unknown}'

    return True, f'DB role values valid: {sorted(db_roles)}'


def main():
    print('=' * 78)
    print('FULL APP AUDIT - CALLBACKS, ROLES, AND PERMISSION LOGIC')
    print('=' * 78)

    source = load_source(SMS_FILE)
    class_methods, command_callbacks, bind_callbacks = parse_command_callbacks(source)

    missing_command_methods = []
    for cls, method, lineno in command_callbacks:
        if not cls:
            continue
        if method not in class_methods.get(cls, set()):
            missing_command_methods.append((cls, method, lineno, 'command='))

    missing_bind_methods = []
    for cls, method, lineno in bind_callbacks:
        if not cls:
            continue
        if method not in class_methods.get(cls, set()):
            missing_bind_methods.append((cls, method, lineno, 'bind lambda'))

    print(f'Callbacks found: {len(command_callbacks)} command bindings, {len(bind_callbacks)} bind lambdas')
    if missing_command_methods or missing_bind_methods:
        print('❌ Missing callback methods detected:')
        for cls, method, lineno, kind in missing_command_methods + missing_bind_methods:
            print(f'   - {kind}: {cls}.{method} at sms.py:{lineno}')
        callback_ok = False
    else:
        print('✅ All discovered callback targets resolve to class methods')
        callback_ok = True

    login_roles, form_roles, change_roles = find_role_sets(source)
    print(f'Login roles: {sorted(login_roles)}')
    print(f'User form roles: {sorted(form_roles)}')
    print(f'Change-role dialog roles: {sorted(change_roles)}')

    role_issues = []
    if login_roles - form_roles:
        role_issues.append(f'Roles in login but missing in user form: {sorted(login_roles - form_roles)}')
    if change_roles - form_roles:
        role_issues.append(f'Roles in change-role dialog but missing in user form: {sorted(change_roles - form_roles)}')

    if role_issues:
        print('❌ Role consistency issues:')
        for issue in role_issues:
            print(f'   - {issue}')
        roles_ok = False
    else:
        print('✅ Role options are internally consistent across login and user management')
        roles_ok = True

    perm_ok, perm_msg = test_permission_logic()
    print(('✅ ' if perm_ok else '❌ ') + perm_msg)

    known_roles = set.union(login_roles, form_roles, change_roles) if (login_roles or form_roles or change_roles) else set()
    db_ok, db_msg = db_role_audit(known_roles)
    print(('✅ ' if db_ok else '❌ ') + db_msg)

    overall_ok = callback_ok and roles_ok and perm_ok and db_ok

    print('\n' + '=' * 78)
    if overall_ok:
        print('AUDIT RESULT: PASS')
        return 0

    print('AUDIT RESULT: FAIL')
    return 1


if __name__ == '__main__':
    sys.exit(main())
