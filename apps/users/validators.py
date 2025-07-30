
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    """
    Valida que la contraseña tenga:
    - Al menos 8 caracteres
    - Al menos una letra mayúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("La contraseña debe tener al menos 8 caracteres."),
                code='password_too_short',
            )

        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper',
            )

        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un número."),
                code='password_no_digit',
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{}|<>)."),
                code='password_no_special',
            )

    def __call__(self, value):
        """
        Makes the validator callable for DRF serializers.
        """
        self.validate(value)
    def get_help_text(self):
        return _(
            "Su contraseña debe contener:\n"
            "- Al menos 8 caracteres\n"
            "- Al menos una letra mayúscula\n"
            "- Al menos un número\n"
            "- Al menos un carácter especial (!@#$%^&*(),.?\":{}|<>)"
        )