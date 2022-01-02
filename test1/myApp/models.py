# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AsrNlpStage(models.Model):
    inputid = models.CharField(max_length=100)
    createtime = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    resultjson = models.JSONField(blank=True, null=True)
    endtime = models.CharField(max_length=100, blank=True, null=True)
    asr_nlp_stage_id = models.AutoField(db_column='asr_nlp_stage.id', primary_key=True)  # Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'asr_nlp_stage'
