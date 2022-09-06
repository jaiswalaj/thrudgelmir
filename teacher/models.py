from django.db import models

class Teacher(models.Model):
    teacher_name = models.CharField(max_length=50)

    def __str__(self):
        return self.teacher_name


class Cloudinfra(models.Model):
    INFRA_STATUS = (
        ('ACTIVE', 'ACTIVE'),
        ('SHUTOFF', 'SHUTOFF'),
    )

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    infra_name = models.CharField(max_length=50)
    minutes_to_live = models.IntegerField(default=10)
    infra_status = models.CharField(max_length=10, choices=INFRA_STATUS, default='SHUTOFF')
    last_started = models.DateTimeField(null=True)

    def __str__(self):
        return self.infra_name


class Router(models.Model):
    cloudinfra = models.ForeignKey(Cloudinfra, on_delete=models.CASCADE)
    router_name = models.CharField(max_length=50)

    def __str__(self):
        return self.router_name


class Network(models.Model):
    cloudinfra = models.ForeignKey(Cloudinfra, on_delete=models.CASCADE)
    router = models.ForeignKey(Router, on_delete=models.SET_NULL, blank=True, null=True)
    network_name = models.CharField(max_length=50)
    network_cidr = models.CharField(max_length=20)
    
    def __str__(self):
        return self.network_name


class Server(models.Model):
    SERVER_STATUS = (
        ('ACTIVE', 'ACTIVE'),
        ('SHUTOFF', 'SHUTOFF'),
    )

    cloudinfra = models.ForeignKey(Cloudinfra, on_delete=models.CASCADE)
    image = models.CharField(max_length=50)
    flavor = models.CharField(max_length=50)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    server_name = models.CharField(max_length=50)
    floating_ip = models.BooleanField(default=False)
    server_status = models.CharField(max_length=10, choices=SERVER_STATUS)

    def __str__(self):
        return self.server_name
