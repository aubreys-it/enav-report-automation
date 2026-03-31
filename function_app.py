import azure.functions as func
import logging
import tempfile

from scraper  import download_report
from uploader import upload_to_sharepoint

app = func.FunctionApp()

@app.timer_trigger(
    schedule         = "0 0 7 * * 1",  # Every Monday at 7:00 AM UTC
    arg_name         = "myTimer",
    run_on_startup   = False,
    use_monitor      = False
)
def hr_report_timer(myTimer: func.TimerRequest) -> None:
    logging.info("HR report automation started.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = download_report(tmp_dir)
        upload_to_sharepoint(file_path)

    logging.info("HR report automation completed.")