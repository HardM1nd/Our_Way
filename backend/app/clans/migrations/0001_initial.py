from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clans_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClanMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(max_length=50, default='member')),
                ('clan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='clans.clan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clan_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('clan', 'user')},
            },
        ),
        migrations.CreateModel(
            name='ClanQuest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
                ('points', models.PositiveIntegerField(default=20)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('clan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quests', to='clans.clan')),
            ],
        ),
    ]