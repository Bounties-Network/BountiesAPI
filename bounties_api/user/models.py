import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from notifications.constants import default_email_options, notifications


class Language(models.Model):
    name = models.CharField(max_length=128, unique=True)
    normalized_name = models.CharField(max_length=128)
    native_name = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.normalized_name = self.name.lower().strip()
        super(Language, self).save(*args, **kwargs)


class Skill(models.Model):
    name = models.CharField(max_length=128, unique=True)
    normalized_name = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.normalized_name = self.name.lower().strip()
        super(Skill, self).save(*args, **kwargs)


class RankedSkill(models.Model):
    name = models.CharField(max_length=128)
    normalized_name = models.CharField(max_length=128)
    total_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'skill_ranks'


class Settings(models.Model):
    emails = JSONField(null=False, default=default_email_options)

    def readable_accepted_email_settings(self):
        merged_settings = {
            **self.emails['issuer'],
            **self.emails['both'],
            **self.emails['fulfiller']}
        return [setting for setting in merged_settings if merged_settings[setting]]

    def accepted_email_settings(self):
        merged_settings = {
            **self.emails['issuer'],
            **self.emails['both'],
            **self.emails['fulfiller']}
        return [notifications[setting]
                for setting in merged_settings if merged_settings[setting]]


class User(models.Model):
    # once a user's profiles has been touched manually, we should no longer
    # update their infomation based on data attached to bounties
    profile_touched_manually = models.BooleanField(default=False)

    public_address = models.TextField(max_length=500, blank=True, unique=True)
    nonce = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    name = models.CharField(max_length=128, blank=True)
    email = models.CharField(max_length=128, blank=True)
    wants_marketing_emails = models.BooleanField(default=False)
    organization = models.CharField(max_length=128, blank=True)
    languages = models.ManyToManyField('user.Language')
    skills = models.ManyToManyField('user.Skill')
    small_profile_image_url = models.CharField(max_length=256, blank=True)
    large_profile_image_url = models.CharField(max_length=256, blank=True)
    page_preview = models.CharField(max_length=256, blank=True)
    website = models.CharField(max_length=128, blank=True)
    twitter = models.CharField(max_length=128, blank=True)
    github = models.CharField(max_length=128, blank=True)
    linkedin = models.CharField(max_length=128, blank=True)
    dribble = models.CharField(max_length=128, blank=True)
    settings = models.ForeignKey(Settings, null=True)

    def save(self, *args, **kwargs):
        if not self.settings:
            self.settings = Settings.objects.create()
        super(User, self).save(*args, **kwargs)

    def save_and_clear_skills(self, skills):
        # this is really messy, but this is bc of psql django bugs
        self.skills.clear()
        if isinstance(skills, list):
            for skill in skills:
                if isinstance(skill, str):
                    try:
                        if skill != '':
                            matching_skill = Skill.objects.get(
                                name=skill.strip())
                            self.skills.add(matching_skill)
                    except ObjectDoesNotExist:
                        self.skills.create(name=skill.strip())

    def save_and_clear_languages(self, languages):
        # this is really messy, but this is bc of psql django bugs
        self.languages.clear()
        if isinstance(languages, list):
            for language in languages:
                if isinstance(language, str):
                    try:
                        matching_language = Language.objects.get(
                            normalized_name=language.strip().lower())
                        self.languages.add(matching_language)
                    except ObjectDoesNotExist:
                        pass
