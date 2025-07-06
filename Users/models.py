from django.db import models
from uuid import uuid4
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import UserManager
# Create your models here.

class User(AbstractUser):
    
    '''
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    '''
    profile_image = CloudinaryField(_("Profile Image"),
                        resource_type = "image",
                        folder = "django-user-profile/avater/",
                        null = True,
                        blank = True)
    
    uid = models.UUIDField(_("Unique Identifier"),
                        default=uuid4,
                        primary_key=True,
                        unique=True,
                        editable=False)
    
    username = models.CharField(_("Nickname"),
                        unique=True,
                        max_length=20,
                        null=True,
                        blank=True)
    
    email = models.EmailField(_("Email"),
                        unique=True,
                        max_length=254)
    
    phone_number = models.CharField(_("Phone Number"),
                        max_length=10,
                        null=True,
                        blank=True)
    
    bio = models.TextField(_("Bio Data"),
                        max_length=100,
                        default=None,
                        null=True,
                        blank=True)
    
    date_of_birth = models.DateField(_("Date of Birth"),
                        auto_now=False,
                        auto_now_add=False,
                        null=True,
                        blank=True)
    
    is_verified = models.BooleanField(_("Verified"),
                        default=False)
    
    USERNAME_FIELD = ('email')
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self) -> str:
        return f"{self.email} ||| {self.uid}"

#------------------------------------------------------------------------------------------------
class OtpData(models.Model):
    email = models.EmailField(_("email"),
                        primary_key=True,
                        unique=True,
                        max_length=254)
    
    otp = models.CharField(_("one time password"),
                        max_length=10,
                        null=True,
                        blank=True)
    
    created_date= models.DateField(default=timezone.now, null= True)
    
    def __str__(self) -> str:
        return f'{self.email} ||| {self.otp}'