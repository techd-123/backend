from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class WeddingProfile(models.Model):
    RELIGION_CHOICES=[
        ('Hinduism', 'Hinduism'),
        ('Islam', 'Islam'),
        ('Christianity', 'Christianity'),
        ('Sikhism', 'Sikhism'),
        ('Buddhism', 'Buddhism'),
        ('Jainism', 'Jainism'),
        ('Zoroastrianism', 'Zoroastrianism'),
        ('Judaism', 'Judaism'),
        ('Baháʼí Faith', 'Baháʼí Faith'),
        ('Tribal Religions', 'Tribal Religions'),
        ('Animism', 'Animism'),
        ('Atheism', 'Atheism'),
        ('Agnosticism', 'Agnosticism'),
        ('Non-religious', 'Non-religious'),
        ('Other', 'Other')
    ]

    CASTE_CHOICES = [
        ('Brahmin', 'Brahmin'),
        ('Kshatriya', 'Kshatriya'),
        ('Vaishya', 'Vaishya'),
        ('Kayastha', 'Kayastha'),
        ('Chettiar', 'Chettiar'),
        ('Kamma', 'Kamma'),
        ('Kapu', 'Kapu'),
        ('Mudaliar', 'Mudaliar'),
        ('Iyer', 'Iyer'),
        ('Iyengar', 'Iyengar'),
        ('Saraswat', 'Saraswat'),
        ('Maithil', 'Maithil'),
        ('Gaur', 'Gaur'),
        ('Rajput', 'Rajput'),
        ('Maratha', 'Maratha'),
        ('Reddy', 'Reddy'),
        ('Nair', 'Nair'),
        ('Agarwal', 'Agarwal'),
        ('Jain', 'Jain'),
        ('Komati', 'Komati'),
        ('Yadav', 'Yadav'),
        ('Kurmi', 'Kurmi'),
        ('Jat', 'Jat'),
        ('Gujjar', 'Gujjar'),
        ('Ezhava', 'Ezhava'),
        ('Vokkaliga', 'Vokkaliga'),
        ('Thevar', 'Thevar'),
        ('Mukkulathor', 'Mukkulathor'),
        ('Nadar', 'Nadar'),
        ('Vishwakarma', 'Vishwakarma'),
        ('Teli', 'Teli'),
        ('Kumhar', 'Kumhar'),
        ('Gounder', 'Gounder'),
        ('Ahir', 'Ahir'),
        ('Mehtar', 'Mehtar'),
        ('Chamar', 'Chamar'),
        ('Mahar', 'Mahar'),
        ('Paraiyar', 'Paraiyar'),
        ('Mala', 'Mala'),
        ('Madiga', 'Madiga'),
        ('Jatav', 'Jatav'),
        ('Dholi', 'Dholi'),
        ('Dom', 'Dom'),
        ('Valmiki', 'Valmiki'),
        ('Arunthathiyar', 'Arunthathiyar'),
        ('Pasi', 'Pasi'),
        ('Gond', 'Gond'),
        ('Bhil', 'Bhil'),
        ('Santhal', 'Santhal'),
        ('Oraon', 'Oraon'),
        ('Munda', 'Munda'),
        ('Khasi', 'Khasi'),
        ('Naga', 'Naga'),
        ('Bodo', 'Bodo'),
        ('Toda', 'Toda'),
        ('Nicobarese', 'Nicobarese'),
        ('Other', 'Other')
    ]
    
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_weddings')
    partner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='partner_weddings')
    bride = models.CharField(max_length=100)
    groom = models.CharField(max_length=100)
    religion = models.CharField(max_length=100, choices=RELIGION_CHOICES)
    caste = models.CharField(max_length=100, choices=CASTE_CHOICES)
    wedding_date = models.DateField()
    engagement_date = models.DateField(null=True, blank=True)
    reception_date = models.DateField(null=True, blank=True)
    wedding_venue = models.CharField(max_length=255)
    engagement_venue = models.CharField(max_length=255, null=True, blank=True)
    reception_venue = models.CharField(max_length=255, null=True, blank=True)
    partner_can_edit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validate that engagement date is before wedding date if both exist
        if self.engagement_date and self.wedding_date:
            if self.engagement_date >= self.wedding_date:
                raise ValidationError("Engagement date must be before wedding date")
        
        # Validate that wedding date is in the future
        if self.wedding_date and self.wedding_date < timezone.now().date():
            raise ValidationError("Wedding date must be in the future")

    def save(self, *args, **kwargs):
        self.full_clean()  # Runs clean() and other validations
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bride} & {self.groom}'s Wedding"