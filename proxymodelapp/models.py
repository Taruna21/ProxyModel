

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

class UserAccountManager(BaseUserManager):
	def create_user(self , email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		
		user = self.model(
			email = self.normalize_email(email) ,
		)
		user.set_password(password)
		user.save(using = self._db)
		return user
	
	def create_superuser(self , email , password):
		user = self.create_user(
			email = self.normalize_email(email) ,
			password = password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user
	
class UserAccount(AbstractBaseUser):
	class Types(models.TextChoices):
		Dealer = "DEALER" , "dealer"
		NormalUser = "NORMALUSER" , "normaluser"
		
	type = models.CharField(max_length = 20 , choices = Types.choices ,
							# Default is user 
							default = Types.NormalUser)
	email = models.EmailField(max_length = 200 , unique = True)
	is_active = models.BooleanField(default = True)
	is_admin = models.BooleanField(default = False)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)
	

	is_dealer = models.BooleanField(default = False)
	is_normaluser = models.BooleanField(default = False)
	
	USERNAME_FIELD = "email"
	
	# defining the manager for the UserAccount model
	objects = UserAccountManager()
	
	def __str__(self):
		return str(self.email)
	
	def has_perm(self , perm, obj = None):
		return self.is_admin
	
	def has_module_perms(self , app_label):
		return True
	
	def save(self , *args , **kwargs):
		if not self.type or self.type == None :
			self.type = UserAccount.Types.NORMALUSER
		return super().save(*args , **kwargs)

class DealerManager(models.Manager):
	def create_user(self , email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		email = email.lower()
		user = self.model(
			email = email
		)
		user.set_password(password)
		user.save(using = self._db)
		return user
	
	def get_queryset(self , *args, **kwargs):
		queryset = super().get_queryset(*args , **kwargs)
		queryset = queryset.filter(type = UserAccount.Types.DEALER)
		return queryset	
		
class Dealer(UserAccount):
	class Meta :
		proxy = True
	objects = DealerManager()
	
	def save(self , *args , **kwargs):
		self.type = UserAccount.Types.DEALER
		self.is_dealer = True
		return super().save(*args , **kwargs)
	
class NormaluserManager(models.Manager):
	def create_user(self , email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		email = email.lower()
		user = self.model(
			email = email
		)
		user.set_password(password)
		user.save(using = self._db)
		return user
		
	def get_queryset(self , *args , **kwargs):
		queryset = super().get_queryset(*args , **kwargs)
		queryset = queryset.filter(type = UserAccount.Types.NORMALUSER)
		return queryset
	
class Normaluser(UserAccount):
	class Meta :
		proxy = True
	objects = NormaluserManager()
	
	def save(self , *args , **kwargs):
		self.type = UserAccount.Types.NORMALUSER
		self.is_normaluser = True
		return super().save(*args , **kwargs)
