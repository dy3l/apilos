import logging
import tempfile
import subprocess
from pathlib import Path

from celery import shared_task
from django.conf import settings
from django.core.files.storage import default_storage

from core.services import EmailService, EmailTemplateID
from upload.models import UploadedFile
from users.models import User

logger = logging.getLogger(__name__)


@shared_task()
def scan_uploaded_files(paths_to_scan, authenticated_user_id):
    # refresh the database on demand before the scan starts
    # subprocess.run(
    #     f'freshclam --config-file="{settings.CLAMAV_PATH}/clamav/freshclam.conf"',
    #     shell=True,
    #     check=True,
    # )

    for path, uploaded_file_id in paths_to_scan:
        with default_storage.open(path, "rb") as original_file_object:
            file_is_infected = False

            with tempfile.NamedTemporaryFile() as tf:
                tf.write(original_file_object.read())
                output = subprocess.run(
                    f'clamdscan {tf.name} --config-file="{settings.CLAMAV_PATH}/clamav/clamd.conf"',
                    capture_output=True,
                    shell=True,
                    check=False,
                    text=True,
                )

                logger.warning(f"{output.stdout=}")

                file_is_infected = (
                    "Infected files" in output.stdout
                    and "Infected files: 0" not in output.stdout
                )
            if file_is_infected:
                user = User.objects.get(id=authenticated_user_id)
                EmailService(
                    to_emails=[user.email],
                    email_template_id=EmailTemplateID.VIRUS_WARNING,
                ).send_transactional_email(
                    email_data={
                        "firstname": user.first_name,
                        "lastname": user.last_name,
                        "filename": path.name,
                    }
                )

                default_storage.delete(path)
                UploadedFile.objects.get(id=uploaded_file_id).delete()

                logger.warning(
                    "An infected file has been detected."
                    "The user has been warned by email "
                    "and the file has succesfully been removed. | File location : %s",
                    path,
                )
