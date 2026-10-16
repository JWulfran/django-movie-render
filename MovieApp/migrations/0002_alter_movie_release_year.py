from django.db import migrations, models


def copy_release_year(apps, schema_editor):
    Movie = apps.get_model("MovieApp", "Movie")
    database = schema_editor.connection.alias

    for movie in Movie.objects.using(database).all().iterator():
        movie.release_year_number = movie.release_year.year
        movie.save(
            using=database,
            update_fields=["release_year_number"],
        )


class Migration(migrations.Migration):

    dependencies = [
        ("MovieApp", "0001_initial"),
    ]

    operations = [
        # 1. Create a temporary integer field.
        migrations.AddField(
            model_name="movie",
            name="release_year_number",
            field=models.PositiveIntegerField(null=True),
        ),

        # 2. Extract the year from each existing date.
        migrations.RunPython(copy_release_year),

        # 3. Remove the original date field.
        migrations.RemoveField(
            model_name="movie",
            name="release_year",
        ),

        # 4. Give the integer field its final name.
        migrations.RenameField(
            model_name="movie",
            old_name="release_year_number",
            new_name="release_year",
        ),

        # 5. Make the year required.
        migrations.AlterField(
            model_name="movie",
            name="release_year",
            field=models.PositiveIntegerField(),
        ),
    ]