"""
Simple built-in translation system (no gettext / compilemessages needed,
so it works the same on any server or PaaS).

Usage in templates:   {% load i18n_tags %}  {% t "nav_dashboard" %}
Usage in Python:      translate("expense_added", "fr")
"""

DEFAULT_LANGUAGE = "ar"
DEFAULT_THEME = "light"
THEMES = ("light", "dark")

SUPPORTED_LANGUAGES = {
    "ar": {"name": "العربية", "dir": "rtl"},
    "en": {"name": "English", "dir": "ltr"},
    "es": {"name": "Español", "dir": "ltr"},
    "fr": {"name": "Français", "dir": "ltr"},
}

# key, Arabic, English, Spanish, French
_RAW = [
    # ---------- common / navigation ----------
    ("app_name", "نظام إدارة المصروفات", "Expense Management System", "Sistema de gestión de gastos", "Système de gestion des dépenses"),
    ("brand", "إدارة المصروفات", "Expense Manager", "Gestor de gastos", "Gestion des dépenses"),
    ("nav_dashboard", "لوحة التحكم", "Dashboard", "Panel", "Tableau de bord"),
    ("nav_expenses", "المصروفات", "Expenses", "Gastos", "Dépenses"),
    ("nav_categories", "التصنيفات", "Categories", "Categorías", "Catégories"),
    ("nav_budgets", "الميزانيات", "Budgets", "Presupuestos", "Budgets"),
    ("nav_add_expense", "إضافة مصروف", "Add expense", "Añadir gasto", "Ajouter une dépense"),
    ("nav_account", "الحساب", "Account", "Cuenta", "Compte"),
    ("logout", "تسجيل خروج", "Log out", "Cerrar sesión", "Déconnexion"),
    ("login", "تسجيل الدخول", "Log in", "Iniciar sesión", "Connexion"),
    ("sign_up", "إنشاء حساب", "Sign up", "Registrarse", "S'inscrire"),
    ("theme_to_dark", "الوضع الداكن", "Dark mode", "Modo oscuro", "Mode sombre"),
    ("theme_to_light", "الوضع الفاتح", "Light mode", "Modo claro", "Mode clair"),
    ("cur", "ج.م", "EGP", "EGP", "EGP"),
    ("cancel", "إلغاء", "Cancel", "Cancelar", "Annuler"),
    ("save", "حفظ", "Save", "Guardar", "Enregistrer"),
    ("add", "إضافة", "Add", "Añadir", "Ajouter"),
    ("update", "تحديث", "Update", "Actualizar", "Mettre à jour"),
    ("delete", "حذف", "Delete", "Eliminar", "Supprimer"),
    ("edit", "تعديل", "Edit", "Editar", "Modifier"),
    ("back", "رجوع", "Back", "Volver", "Retour"),
    ("none_short", "بدون", "None", "Ninguna", "Aucune"),
    ("language", "اللغة", "Language", "Idioma", "Langue"),

    # ---------- auth ----------
    ("login_title", "تسجيل الدخول", "Log in", "Iniciar sesión", "Connexion"),
    ("login_error", "اسم المستخدم أو كلمة المرور غير صحيحة.", "Incorrect username or password.", "Nombre de usuario o contraseña incorrectos.", "Nom d'utilisateur ou mot de passe incorrect."),
    ("username", "اسم المستخدم", "Username", "Nombre de usuario", "Nom d'utilisateur"),
    ("password", "كلمة المرور", "Password", "Contraseña", "Mot de passe"),
    ("login_button", "دخول", "Log in", "Entrar", "Se connecter"),
    ("new_user", "مستخدم جديد؟", "New here?", "¿Eres nuevo?", "Nouveau ?"),
    ("create_account", "إنشاء حساب", "Create account", "Crear cuenta", "Créer un compte"),
    ("register_title", "إنشاء حساب جديد", "Create a new account", "Crear una cuenta nueva", "Créer un nouveau compte"),
    ("register_button", "إنشاء الحساب", "Create account", "Crear cuenta", "Créer le compte"),
    ("have_account", "لديك حساب بالفعل؟", "Already have an account?", "¿Ya tienes una cuenta?", "Vous avez déjà un compte ?"),
    ("field_username", "اسم المستخدم", "Username", "Nombre de usuario", "Nom d'utilisateur"),
    ("field_email", "البريد الإلكتروني", "Email", "Correo electrónico", "E-mail"),
    ("field_password1", "كلمة المرور", "Password", "Contraseña", "Mot de passe"),
    ("field_password2", "تأكيد كلمة المرور", "Confirm password", "Confirmar contraseña", "Confirmer le mot de passe"),
    ("register_success", "تم إنشاء الحساب بنجاح، سجّل دخولك الآن.", "Account created successfully. Please log in.", "Cuenta creada correctamente. Inicia sesión.", "Compte créé avec succès. Connectez-vous."),

    # ---------- dashboard ----------
    ("total_all_time", "إجمالي المصروفات", "Total expenses", "Gastos totales", "Total des dépenses"),
    ("total_month", "مصروفات هذا الشهر", "This month's expenses", "Gastos de este mes", "Dépenses de ce mois"),
    ("op_count", "عدد العمليات", "Number of transactions", "Número de operaciones", "Nombre d'opérations"),
    ("budget", "الميزانية", "Budget", "Presupuesto", "Budget"),
    ("manage_budgets", "إدارة الميزانيات", "Manage budgets", "Gestionar presupuestos", "Gérer les budgets"),
    ("overall_budget_label", "الميزانية الكلية", "Overall budget", "Presupuesto total", "Budget global"),
    ("over_by", "تجاوزت بـ {amount}", "Over by {amount}", "Excedido en {amount}", "Dépassé de {amount}"),
    ("remaining", "متبقي {amount}", "{amount} left", "Restan {amount}", "Il reste {amount}"),
    ("category_stats", "إحصائيات حسب التصنيف", "Statistics by category", "Estadísticas por categoría", "Statistiques par catégorie"),
    ("th_category", "التصنيف", "Category", "Categoría", "Catégorie"),
    ("th_count", "عدد", "Count", "Cantidad", "Nombre"),
    ("th_total", "الإجمالي", "Total", "Total", "Total"),
    ("uncategorized", "بدون تصنيف", "Uncategorized", "Sin categoría", "Sans catégorie"),
    ("no_data", "لا توجد بيانات بعد.", "No data yet.", "Aún no hay datos.", "Pas encore de données."),
    ("last_6_months", "آخر 6 أشهر", "Last 6 months", "Últimos 6 meses", "6 derniers mois"),
    ("th_month", "الشهر", "Month", "Mes", "Mois"),
    ("recent_expenses", "آخر المصروفات", "Recent expenses", "Gastos recientes", "Dépenses récentes"),
    ("view_all", "عرض الكل", "View all", "Ver todo", "Tout voir"),
    ("th_date", "التاريخ", "Date", "Fecha", "Date"),
    ("th_description", "الوصف", "Description", "Descripción", "Description"),
    ("th_amount", "المبلغ", "Amount", "Importe", "Montant"),
    ("no_expenses_yet", "لم تقم بإضافة أي مصروفات بعد.", "You haven't added any expenses yet.", "Aún no has añadido ningún gasto.", "Vous n'avez encore ajouté aucune dépense."),
    ("add_first", "أضف أول مصروف", "Add your first expense", "Añade tu primer gasto", "Ajoutez votre première dépense"),

    # ---------- expense list / filter ----------
    ("filter_button", "فلترة", "Filter", "Filtrar", "Filtrer"),
    ("from_date", "من تاريخ", "From date", "Desde", "Du"),
    ("to_date", "إلى تاريخ", "To date", "Hasta", "Au"),
    ("search_desc", "بحث بالوصف", "Search description", "Buscar en la descripción", "Rechercher dans la description"),
    ("search_placeholder", "بحث في الوصف...", "Search description...", "Buscar en la descripción...", "Rechercher dans la description..."),
    ("all_categories", "كل التصنيفات", "All categories", "Todas las categorías", "Toutes les catégories"),
    ("results_count", "عدد النتائج: {n}", "Results: {n}", "Resultados: {n}", "Résultats : {n}"),
    ("no_matching", "لا توجد مصروفات مطابقة.", "No matching expenses.", "No hay gastos que coincidan.", "Aucune dépense correspondante."),

    # ---------- forms ----------
    ("add_expense_title", "إضافة مصروف", "Add expense", "Añadir gasto", "Ajouter une dépense"),
    ("edit_expense_title", "تعديل مصروف", "Edit expense", "Editar gasto", "Modifier la dépense"),
    ("field_amount", "المبلغ", "Amount", "Importe", "Montant"),
    ("field_category", "التصنيف", "Category", "Categoría", "Catégorie"),
    ("field_date", "التاريخ", "Date", "Fecha", "Date"),
    ("field_description", "الوصف", "Description", "Descripción", "Description"),
    ("field_name", "الاسم", "Name", "Nombre", "Nom"),
    ("field_color", "اللون", "Color", "Color", "Couleur"),

    # ---------- detail / delete ----------
    ("detail_title", "تفاصيل المصروف", "Expense details", "Detalles del gasto", "Détails de la dépense"),
    ("confirm_delete_title", "تأكيد الحذف", "Confirm deletion", "Confirmar eliminación", "Confirmer la suppression"),
    ("delete_expense_question", "هل أنت متأكد من حذف المصروف \"{name}\"؟", "Are you sure you want to delete the expense \"{name}\"?", "¿Seguro que quieres eliminar el gasto \"{name}\"?", "Voulez-vous vraiment supprimer la dépense « {name} » ?"),
    ("delete_category_question", "هل أنت متأكد من حذف تصنيف \"{name}\"؟ المصروفات المرتبطة به ستصبح بدون تصنيف.", "Are you sure you want to delete the category \"{name}\"? Its expenses will become uncategorized.", "¿Seguro que quieres eliminar la categoría \"{name}\"? Sus gastos quedarán sin categoría.", "Voulez-vous vraiment supprimer la catégorie « {name} » ? Ses dépenses deviendront sans catégorie."),

    # ---------- categories ----------
    ("add_category", "إضافة تصنيف جديد", "Add a new category", "Añadir una categoría nueva", "Ajouter une nouvelle catégorie"),
    ("current_categories", "التصنيفات الحالية", "Current categories", "Categorías actuales", "Catégories actuelles"),
    ("no_categories", "لا توجد تصنيفات بعد.", "No categories yet.", "Aún no hay categorías.", "Pas encore de catégories."),
    ("category_exists", "يوجد تصنيف بنفس الاسم بالفعل.", "A category with this name already exists.", "Ya existe una categoría con ese nombre.", "Une catégorie portant ce nom existe déjà."),

    # ---------- budgets ----------
    ("budgets_title", "الميزانيات", "Budgets", "Presupuestos", "Budgets"),
    ("overall_monthly_budget", "الميزانية الكلية للشهر", "Overall monthly budget", "Presupuesto mensual total", "Budget mensuel global"),
    ("overall_budget_amount", "الميزانية الكلية: {amount}", "Overall budget: {amount}", "Presupuesto total: {amount}", "Budget global : {amount}"),
    ("reserved_line", "محجوز لميزانيات التصنيفات: {amount}", "Reserved for category budgets: {amount}", "Reservado para presupuestos de categorías: {amount}", "Réservé aux budgets par catégorie : {amount}"),
    ("unbudgeted_line", "مصروف خارج ميزانيات التصنيفات: {amount}", "Spent outside category budgets: {amount}", "Gastado fuera de los presupuestos de categorías: {amount}", "Dépensé hors budgets par catégorie : {amount}"),
    ("overflow_line", "زيادة عن ميزانيات التصنيفات: {amount}", "Over category budgets: {amount}", "Exceso sobre presupuestos de categorías: {amount}", "Dépassement des budgets par catégorie : {amount}"),
    ("no_overall_budget", "لم يتم تحديد ميزانية كلية للشهر بعد.", "No overall monthly budget set yet.", "Aún no se ha definido un presupuesto mensual total.", "Aucun budget mensuel global défini pour l'instant."),
    ("edit_overall", "تعديل الميزانية الكلية", "Edit overall budget", "Editar presupuesto total", "Modifier le budget global"),
    ("set_overall", "حدد الميزانية الكلية", "Set overall budget", "Definir presupuesto total", "Définir le budget global"),
    ("example_placeholder", "مثلاً 5000", "e.g. 5000", "p. ej. 5000", "ex. 5000"),
    ("category_budgets", "ميزانيات التصنيفات", "Category budgets", "Presupuestos por categoría", "Budgets par catégorie"),
    ("spent_of", "{spent} من {amount}", "{spent} of {amount}", "{spent} de {amount}", "{spent} sur {amount}"),
    ("no_category_budgets", "لا توجد ميزانيات لتصنيفات محددة بعد.", "No category budgets yet.", "Aún no hay presupuestos por categoría.", "Aucun budget par catégorie pour l'instant."),
    ("add_budget_for_category", "إضافة ميزانية لتصنيف", "Add a budget for a category", "Añadir presupuesto a una categoría", "Ajouter un budget à une catégorie"),
    ("need_categories_first", "أضف تصنيفات أولاً لتتمكن من تحديد ميزانية لها:", "Add some categories first so you can set budgets for them:", "Añade primero algunas categorías para poder definir presupuestos:", "Ajoutez d'abord des catégories pour pouvoir définir des budgets :"),
    ("budget_overall_updated", "تم تحديث الميزانية الكلية.", "Overall budget updated.", "Presupuesto total actualizado.", "Budget global mis à jour."),
    ("budget_category_updated", "تم تحديث ميزانية {name}.", "Budget for {name} updated.", "Presupuesto de {name} actualizado.", "Budget de {name} mis à jour."),
    ("budget_invalid", "قيمة الميزانية غير صحيحة.", "Invalid budget amount.", "Importe de presupuesto no válido.", "Montant de budget invalide."),

    # ---------- flash messages ----------
    ("expense_added", "تمت إضافة المصروف بنجاح.", "Expense added successfully.", "Gasto añadido correctamente.", "Dépense ajoutée avec succès."),
    ("expense_updated", "تم تعديل المصروف بنجاح.", "Expense updated successfully.", "Gasto actualizado correctamente.", "Dépense modifiée avec succès."),
    ("expense_deleted", "تم حذف المصروف.", "Expense deleted.", "Gasto eliminado.", "Dépense supprimée."),
    ("category_added", "تمت إضافة التصنيف.", "Category added.", "Categoría añadida.", "Catégorie ajoutée."),
    ("category_deleted", "تم حذف التصنيف.", "Category deleted.", "Categoría eliminada.", "Catégorie supprimée."),

    # ---------- account ----------
    ("account_title", "الحساب", "Account", "Cuenta", "Compte"),
    ("account_info", "بيانات الحساب", "Account information", "Información de la cuenta", "Informations du compte"),
    ("prefs_title", "التفضيلات", "Preferences", "Preferencias", "Préférences"),
    ("theme_label", "المظهر", "Appearance", "Apariencia", "Apparence"),
    ("theme_light_option", "فاتح", "Light", "Claro", "Clair"),
    ("theme_dark_option", "داكن", "Dark", "Oscuro", "Sombre"),
    ("prefs_saved", "تم حفظ التفضيلات.", "Preferences saved.", "Preferencias guardadas.", "Préférences enregistrées."),
    ("logout_desc", "سجّل الخروج من هذا الجهاز.", "Sign out of this device.", "Cierra la sesión en este dispositivo.", "Déconnectez-vous de cet appareil."),
    ("danger_zone", "منطقة الخطر", "Danger zone", "Zona de peligro", "Zone de danger"),
    ("delete_account", "حذف الحساب", "Delete account", "Eliminar cuenta", "Supprimer le compte"),
    ("delete_account_warning", "سيتم حذف حسابك وكل مصروفاتك وتصنيفاتك وميزانياتك نهائيًا، ولا يمكن التراجع عن ذلك.", "Your account and all your expenses, categories and budgets will be permanently deleted. This cannot be undone.", "Tu cuenta y todos tus gastos, categorías y presupuestos se eliminarán de forma permanente. Esta acción no se puede deshacer.", "Votre compte ainsi que toutes vos dépenses, catégories et budgets seront définitivement supprimés. Cette action est irréversible."),
    ("confirm_with_password", "أدخل كلمة المرور للتأكيد", "Enter your password to confirm", "Introduce tu contraseña para confirmar", "Saisissez votre mot de passe pour confirmer"),
    ("delete_my_account", "نعم، احذف حسابي نهائيًا", "Yes, permanently delete my account", "Sí, eliminar mi cuenta definitivamente", "Oui, supprimer définitivement mon compte"),
    ("wrong_password", "كلمة المرور غير صحيحة.", "Incorrect password.", "Contraseña incorrecta.", "Mot de passe incorrect."),
    ("account_deleted", "تم حذف حسابك نهائيًا.", "Your account has been permanently deleted.", "Tu cuenta se ha eliminado de forma permanente.", "Votre compte a été supprimé définitivement."),
    ("last_admin", "لا يمكن حذف آخر حساب مسؤول (Admin).", "You can't delete the last admin account.", "No puedes eliminar la última cuenta de administrador.", "Impossible de supprimer le dernier compte administrateur."),
]

STRINGS = {
    key: {"ar": ar, "en": en, "es": es, "fr": fr}
    for key, ar, en, es, fr in _RAW
}


def translate(key, lang=DEFAULT_LANGUAGE, **kwargs):
    """Return the text for `key` in `lang` (falls back to English, then the key)."""
    entry = STRINGS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get("en") or key
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
