from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from datetime import date




CATEGORY_CHOICES = (
    ('tech','tech'),
    ('comics', 'comics'),
    ('games','games'),
    ('food','food'),
    ('music','music'),
)

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    picture = models.URLField()
    description = models.TextField()
    funding_goal = models.DecimalField(decimal_places=2, max_digits=8, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()
    amount_funded = models.DecimalField(decimal_places=2, max_digits=8, default=0.00)
    number_of_backers = models.IntegerField(default=0)
    category = models.CharField(max_length=6, choices=CATEGORY_CHOICES, default='tech')
    # status_updates =  models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} - {self.owner.username}'

    def update_total_funded(self):
        donations = self.donations.aggregate(Sum('donation_amount'))
        self.amount_funded = donations['donation_amount__sum']
        self.save()

    def update_total_backers(self):
        unique_backers = self.donations.values('user').distinct()
        self.number_of_backers = unique_backers.count()
        self.save()

    def met_goal(self):

        return self.amount_funded >= self.funding_goal


    def is_past_due(self):
        return date.today() > self.end_date

    def days_until_due(self):
        difference = self.end_date - self.start_date
        return difference.days

    @classmethod
    def successful_projects_exist(cls):
        successful_projects = Project.objects.filter(end_date__lte=date.today(), amount_funded__gte=models.F("funding_goal")).count()
        return successful_projects > 0

    @classmethod
    def get_successful_percentage(cls):
        successful_projects = Project.objects.filter(end_date__lte=date.today(), amount_funded__gte=models.F("funding_goal")).count()
        completed_projects = Project.objects.filter(end_date__lte=date.today()).count()
        percentage = int((successful_projects / completed_projects) * 100)
        return percentage

    @classmethod
    def successful_category_projects_exist(cls, cat):
        successful_projects = Project.objects.filter(category=cat, end_date__lte=date.today(), amount_funded__gte=models.F("funding_goal")).count()
        return successful_projects > 0

    @classmethod
    def get_successful_percentage_category(cls, cat):
        successful_projects = Project.objects.filter(category=cat, end_date__lte=date.today(), amount_funded__gte=models.F("funding_goal")).count()
        completed_projects = Project.objects.filter(category=cat, end_date__lte=date.today()).count()
        percentage = int((successful_projects / completed_projects) * 100)
        return percentage




class Reward(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    donation_value = models.DecimalField(decimal_places=2, max_digits=8, default=0.00)
    cap = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rewards')

    # make query list of all projects rewards, and sort by donation value
    # when donation is made iterate through list and make if/else statement that will apply reward to donation

    def __str__(self):
        return f'{self.project} - {self.name} - {self.donation_value}'

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    # reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='donations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    donation_amount = models.DecimalField(decimal_places=2, max_digits=5, default=0)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='donations', null=True)


    def __str__(self):
        return f'{self.project}, {self.donation_amount}'

    def get_reward(self, project_id):
        rewards = Reward.objects.filter(project=project_id).order_by('donation_value')
        for reward in rewards:
            if reward.donations.all().count() < reward.cap and self.donation_amount >= reward.donation_value:
                self.reward = reward

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')


