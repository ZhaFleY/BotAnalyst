from backend.modules.analysis.application.report_text import prepare_text
from backend.shared.files.zip_utils import extract_zip


def extract_useful_data(df):
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "sample": df.head(10).to_dicts(),
        "describe": df.describe().to_dicts(),
    }


__all__ = ["extract_useful_data", "prepare_text", "extract_zip"]

