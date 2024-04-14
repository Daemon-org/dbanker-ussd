from django.db import models
import uuid

# Create your models here.

STATUS = (
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("failed", "Failed"),
)

TRANS_TYPE = (
    ("deposit", "Deposit"),
    ("withdraw", "Withdraw"),
    ("transfer", "Transfer"),
)


class UssdLog(models.Model):
    session_id = models.CharField(
        max_length=30, blank=True, null=True
    )  # Field name made lowercase.
    phone = models.CharField(
        max_length=30, blank=True, null=True
    )  # Field name made lowercase.
    message_type = models.IntegerField(
        blank=True, null=True
    )  # Field name made lowercase.
    body = models.CharField(
        max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    phone_number = models.CharField(
        max_length=18, blank=True, null=True
    )  # Field name made lowercase.
    stage = models.CharField(max_length=10, blank=True, null=True)


class UssdScreen(models.Model):
    session_id = models.CharField(
        max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    phone_number = models.CharField(
        blank=True, null=True, max_length=15
    )  # Field name made lowercase.
    level = models.IntegerField(blank=True, null=True)  # Field name made lowercase.


class UssdSession(models.Model):
    body = models.CharField(
        max_length=500, blank=True, null=True
    )  # Field name made lowercase.
    date_created = models.DateField(blank=True, null=True)  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(
        max_length=100, blank=True, null=True
    )  # Field name made lowercase.


# class UssdRequest(models.Model):
#     sessionId = models.CharField(max_length=150)
#     userId = models.CharField(max_length=150)
#     newSession = models.BooleanField(default=False)
#     msisdn = models.CharField(max_length=150)
#     userData = models.TextField(null=True, blank=True)
#     network = models.CharField(max_length=150)

#     def __str__(self) -> str:
#         return self.sessionId


# class UssdResponse(models.Model):
#     sessionId = models.CharField(max_length=150, null=True, blank=True)
#     userId = models.CharField(max_length=150, null=True, blank=True)
#     continueSession = models.BooleanField(default=False)
#     msisdn = models.CharField(max_length=150, null=True, blank=True)
#     message = models.TextField(null=True, blank=True)

#     def __str__(self) -> str:
#         return self.sessionId


# class UssdState(models.Model):
#     sessionId = models.CharField(max_length=150)
#     message = models.TextField()
#     newSession = models.BooleanField(default=False)
#     msisdn = models.CharField(max_length=150)
#     userData = models.TextField(null=True, blank=True)
#     network = models.CharField(max_length=150)
#     level = models.IntegerField()
#     part = models.IntegerField()
#     stage = models.CharField(max_length=100)

#     def __str__(self) -> str:
#         return self.sessionId


class Profile(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    pincode = models.CharField(max_length=150)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    isBanned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return self.phone_number


class Transaction(models.Model):
    transaction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    transaction_type = models.CharField(max_length=150, choices=TRANS_TYPE)
    receipient_number = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=150, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gte=0), name="transaction_amount_check"
            )
        ]

    def __str__(self) -> str:
        return self.status


# TODO: should be able to send transactional statements to users in the future
class Statements(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    transaction_type = models.CharField(max_length=150)
    receipient = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Statement"
        verbose_name_plural = "Statements"

        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gte=0), name="statement_amount_check"
            )
        ]

    def __str__(self) -> str:
        return self.status


# TODO: add a feature for reversal of transactions
