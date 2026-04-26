import json
import re


def prepare_text(report_data: dict) -> str:
    if isinstance(report_data, dict) and report_data.get("error"):
        err = report_data.get("error")
        err_type = report_data.get("error_type", "Error")
        return f"Ошибка анализа ({err_type}):\n{err}"

    def _try_parse_report(text: str) -> dict | None:
        try:
            return json.loads(text)
        except Exception:
            return None

    def _repair_common_json(text: str) -> str:
        s = text.strip()
        if not s:
            return s

        # Remove trailing commas before closing brackets/braces.
        s = re.sub(r",\s*([}\]])", r"\1", s)

        # Convert `"key": "v1", "v2", "v3"` into `"key": ["v1", "v2", "v3"]`.
        string_re = r'"(?:\\.|[^"\\])*"'
        pattern = re.compile(
            rf'("(?P<key>[^"]+)"\s*:\s*)(?P<first>{string_re})(?P<more>(?:\s*,\s*{string_re})+)(?=\s*,\s*"[^"]+"\s*:|\s*}})',
            flags=re.DOTALL,
        )
        s = pattern.sub(lambda m: f'{m.group(1)}[{m.group("first")}{m.group("more")}]', s)

        return s

    try:
        final_message = report_data["messages"][-1].content
        clean_json = final_message.strip().replace("```json", "").replace("```", "")

        report = _try_parse_report(clean_json)
        if report is None:
            repaired = _repair_common_json(clean_json)
            report = _try_parse_report(repaired)
        if report is None:
            return clean_json

        summary = report.get("summary", {})
        if isinstance(summary, (dict, list)):
            summary_text = json.dumps(summary, ensure_ascii=False, indent=4)
        else:
            summary_text = str(summary)

        title = report.get("title", "Отчёт по анализу данных").upper()
        return f"{title}\n{'-' * len(title)}\n\nАНАЛИЗ ДАННЫХ:\n{summary_text}"
    except Exception:
        raw_text = report_data["messages"][-1].content
        return f"ОШИБКА ФОРМАТИРОВАНИЯ (Сырые данные):\n\n{raw_text}"


__all__ = ["prepare_text"]
